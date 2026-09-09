#!/usr/bin/env python3

from tqdm import tqdm
import signal
import subprocess
import os
import tempfile
import re
import platform
import json
import argparse
from pathlib import Path
from datetime import datetime


###############################################################################
# This script is intentionally very close to the old evaluate.py.
# It only adds:
#   - automatic discovery of *_solutions.json files
#   - skip incomplete JSON files ending with null
#   - skip already evaluated solution files
#   - save results/logs into evaluation_finetuning/results/
###############################################################################


# timeout exception
class TimeoutException(Exception):
    pass


# signal handler
def timeout_handler(signum, frame):
    raise TimeoutException()


# register the signal handler
signal.signal(signal.SIGALRM, timeout_handler)


def compile_fortran(fortran_code: str):
    """
    Function that compiles a fortran90 program using the gfortran compiler.
    In case of success, returns the executable and its path.
    """
    with tempfile.NamedTemporaryFile(suffix=".f90", delete=False, mode="w") as f:
        f.write(fortran_code)
        fortran_path = f.name

    exe_suffix = ".exe" if platform.system() == "Windows" else ""
    executable = fortran_path.replace(".f90", exe_suffix)

    compile_cmd = ["gfortran", "-o", executable, fortran_path]

    try:
        subprocess.run(
            compile_cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return executable, fortran_path
    except subprocess.CalledProcessError as e:
        return None, fortran_path, e.stderr.decode()


def parse_response(output: str) -> list[str]:
    stripped = output.strip()
    if not stripped:
        return []
    return [re.sub(r"\[s\]", r" ", st) for st in stripped.split()]


def parse_bool(s):
    """
    Function that parses booleans given as output by the fortran program.
    """
    s = s.strip().lower()
    if s in (".true.", "true", "t", "1"):
        return True
    if s in (".false.", "false", "f", "0"):
        return False
    raise ValueError(f"Not a boolean: {s}")


def equality(x, y, float_tol=1e-2):
    """
    Function that verifies equality between single elements of the program output
    and expected output.
    """
    if x == "" and y == []:
        return True

    try:
        if isinstance(y, bool):
            return parse_bool(x) == y
    except Exception:
        pass

    try:
        if abs(float(x) - float(y)) < float_tol:
            return True
    except Exception:
        pass

    return str(x) == str(y)


def run_program(executable, input_data="", expected_output=None):
    """
    Executes the executable program with input_data, parses its output and compares it
    with expected_output. Returns (score, (status, details)) where:
      - score: 1 if OK, 0 otherwise
      - status: 'ok', 'ineq', 'runtime_err' or 'exception'
      - details: in case of 'ok' or 'ineq', (raw_output, expected_output)
                 for 'runtime_err', the stderr message
                 for 'exception', the exception string
    """
    def normalize(x):
        if expected_output is None:
            return []
        return x if isinstance(x, list) else [x]

    try:
        proc = subprocess.run(
            [executable],
            input=input_data,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False
        )

        if proc.stderr:
            return 0, ("runtime_err", proc.stderr)

        if proc.stdout.strip() == str(expected_output).strip():
            return 1, ("ok", (proc.stdout.strip(), expected_output))

        raw = proc.stdout.strip()
        actual = parse_response(raw)
        exp = expected_output if expected_output is not None else []

        actual_list = normalize(actual)
        expected_list = normalize(exp)

        if len(actual_list) != len(expected_list):
            return 0, ("ineq", (raw, exp))

        for a, b in zip(actual_list, expected_list):
            try:
                if not equality(a, b):
                    return 0, ("ineq", (raw, exp))
            except Exception:
                return 0, ("ineq", (raw, exp))

        return 1, ("ok", (raw, exp))

    except Exception as e:
        return 0, ("exception", str(e))


def program_evaluation(fortran_code: str, test_cases: list):
    """
    Function that executes the correctness evaluation of a Fortran program
    through a battery of tests, compiling the code only once.
    """
    compile_result = compile_fortran(fortran_code)
    executable, source_file = compile_result[0], compile_result[1]

    if not executable:
        stderr_msg = compile_result[2] if len(compile_result) > 2 else "Unknown compile error"
        if os.path.exists(source_file):
            os.remove(source_file)
        return 0, ("compile_err", stderr_msg)

    try:
        for i, test_case in enumerate(test_cases):
            input_data = test_case["input"]
            expected_output = test_case["output"]

            result = run_program(executable, input_data, expected_output)

            if result[0] == 0:
                return result

        return 1, ("ok", "All tests passed")

    finally:
        if os.path.exists(executable):
            os.remove(executable)
        if os.path.exists(source_file):
            os.remove(source_file)


def evaluation(benchmark, inference, execution_time_limit=120):
    c = {
        "ineq": 0,
        "runtime_err": 0,
        "ok": 0,
        "exception": 0,
        "compile_err": 0,
        "ids": []
    }

    logs = {
        "ineq": [],
        "runtime_err": [],
        "ok": [],
        "exception": [],
        "compile_err": []
    }

    detailed_records = []

    for i in tqdm(range(len(inference)), desc="Evaluating"):
        bench = benchmark[i]

        item = inference[i]
        if item is None:
            result = (0, ("exception", "Missing/null solution entry"))
            code = ""
        else:
            code = item.get("code", "") or ""
            test_cases = bench["tests"]

            try:
                signal.alarm(execution_time_limit)
                result = program_evaluation(code, test_cases)
                signal.alarm(0)
            except TimeoutException:
                result = (0, ("runtime_err", "Timeout exceeded"))
                signal.alarm(0)

        if result[0] == 1:
            c["ok"] += 1
        else:
            status = result[1][0]
            if status not in c:
                c[status] = 0
                logs[status] = []
            c[status] += 1
            c["ids"].append(i)

        status = result[1][0]
        details = result[1][1]

        if status not in logs:
            logs[status] = []

        logs[status].append(details)

        detailed_records.append({
            "index": i,
            "task_id": item.get("task_id") if item else i,
            "status": status,
            "score": int(result[0]),
            "details": details,
            "code_chars": len(code),
            "extraction_status": item.get("extraction_status") if item else None,
            "generation_error": item.get("error") if item else "null_entry"
        })

    return c, logs, detailed_records


###############################################################################
# Added logic for the fine-tuned Qwen/vLLM solution files
###############################################################################


def has_trailing_null(data):
    """
    Returns True if the JSON list ends with at least one null.
    This means generation is probably still incomplete.
    """
    if not isinstance(data, list):
        return False

    if not data:
        return False

    return data[-1] is None


def safe_model_name_from_solution_path(path: Path):
    name = path.name

    if name.endswith("_solutions.json"):
        name = name[:-len("_solutions.json")]

    return name


def result_paths_for_solution(results_dir: Path, solution_path: Path):
    model_key = safe_model_name_from_solution_path(solution_path)

    summary_path = results_dir / f"{model_key}_evaluation_summary.json"
    logs_path = results_dir / f"{model_key}_evaluation_logs.json"
    details_path = results_dir / f"{model_key}_evaluation_details.json"

    return model_key, summary_path, logs_path, details_path


def compute_metrics(counter, total):
    ok = counter.get("ok", 0)
    compile_err = counter.get("compile_err", 0)
    runtime_err = counter.get("runtime_err", 0)
    ineq = counter.get("ineq", 0)
    exception = counter.get("exception", 0)

    return {
        "total": total,
        "ok": ok,
        "failed": total - ok,
        "pass_at_1": ok / total if total else 0.0,
        "output_correctness_rate": ok / total if total else 0.0,
        "compilation_rate": (total - compile_err) / total if total else 0.0,
        "execution_success_rate": (total - compile_err - runtime_err - exception) / total if total else 0.0,
        "compile_err": compile_err,
        "runtime_err": runtime_err,
        "ineq": ineq,
        "exception": exception
    }


def evaluate_one_solution_file(
    solution_path: Path,
    benchmark,
    results_dir: Path,
    execution_time_limit: int,
    force: bool = False
):
    model_key, summary_path, logs_path, details_path = result_paths_for_solution(
        results_dir,
        solution_path
    )

    if summary_path.exists() and logs_path.exists() and details_path.exists() and not force:
        print(f"[SKIP] Already evaluated: {solution_path.name}")
        print(f"       Existing summary: {summary_path}")
        return "skipped_existing"

    try:
        data = json.load(open(solution_path, "r", encoding="utf-8"))
    except Exception as e:
        print(f"[SKIP] Cannot read JSON: {solution_path}")
        print(f"       Error: {e}")
        return "skipped_bad_json"

    if not isinstance(data, list):
        print(f"[SKIP] Not a JSON list: {solution_path}")
        return "skipped_not_list"

    if has_trailing_null(data):
        print(f"[SKIP] Incomplete generation detected: {solution_path.name}")
        print("       Reason: JSON file ends with at least one null.")
        return "skipped_incomplete"

    if len(data) != len(benchmark):
        print(f"[SKIP] Length mismatch: {solution_path.name}")
        print(f"       solutions={len(data)} benchmark={len(benchmark)}")
        return "skipped_length_mismatch"

    print("=" * 100)
    print(f"Evaluating: {solution_path.name}")
    print(f"Model key : {model_key}")
    print(f"Problems  : {len(data)}")
    print("=" * 100)

    counter, logs, detailed_records = evaluation(
        benchmark,
        data,
        execution_time_limit=execution_time_limit
    )

    metrics = compute_metrics(counter, len(data))

    summary = {
        "model_key": model_key,
        "solution_file": str(solution_path),
        "benchmark_size": len(benchmark),
        "evaluated_at": datetime.now().isoformat(),
        "execution_time_limit": execution_time_limit,
        "counter": counter,
        "metrics": metrics
    }

    results_dir.mkdir(parents=True, exist_ok=True)

    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    with open(logs_path, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False, default=str)

    with open(details_path, "w", encoding="utf-8") as f:
        json.dump(detailed_records, f, indent=2, ensure_ascii=False, default=str)

    print("Summary:")
    print(json.dumps(summary["metrics"], indent=2))
    print("Saved:")
    print(f"  {summary_path}")
    print(f"  {logs_path}")
    print(f"  {details_path}")

    return "evaluated"


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate all Qwen/vLLM LoRA HumanEval solution JSON files."
    )

    parser.add_argument(
        "--benchmark",
        default="../benchmark.json",
        help="Path to benchmark.json"
    )

    parser.add_argument(
        "--solutions-dir",
        default="results_qwen_lora/solutions",
        help="Directory containing *_solutions.json files"
    )

    parser.add_argument(
        "--results-dir",
        default="results",
        help="Directory where evaluation results are saved"
    )

    parser.add_argument(
        "--execution-time-limit",
        type=int,
        default=120,
        help="Timeout per generated program, in seconds"
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-evaluate even if result files already exist"
    )

    args = parser.parse_args()

    benchmark_path = Path(args.benchmark)
    solutions_dir = Path(args.solutions_dir)
    results_dir = Path(args.results_dir)

    if not benchmark_path.exists():
        raise FileNotFoundError(f"Benchmark not found: {benchmark_path}")

    if not solutions_dir.exists():
        raise FileNotFoundError(f"Solutions directory not found: {solutions_dir}")

    results_dir.mkdir(parents=True, exist_ok=True)

    benchmark = json.load(open(benchmark_path, "r", encoding="utf-8"))

    solution_files = sorted(solutions_dir.glob("*_solutions.json"))

    print("=" * 100)
    print("Qwen/vLLM LoRA HumanEval evaluation")
    print("=" * 100)
    print(f"Benchmark     : {benchmark_path}")
    print(f"Solutions dir : {solutions_dir}")
    print(f"Results dir   : {results_dir}")
    print(f"Solution files: {len(solution_files)}")
    print(f"Timeout       : {args.execution_time_limit}s")
    print(f"Force         : {args.force}")
    print("=" * 100)

    if not solution_files:
        print("No *_solutions.json files found.")
        return

    run_summary = {
        "evaluated": [],
        "skipped_existing": [],
        "skipped_incomplete": [],
        "skipped_bad_json": [],
        "skipped_not_list": [],
        "skipped_length_mismatch": [],
        "other": []
    }

    for path in solution_files:
        status = evaluate_one_solution_file(
            solution_path=path,
            benchmark=benchmark,
            results_dir=results_dir,
            execution_time_limit=args.execution_time_limit,
            force=args.force
        )

        run_summary.setdefault(status, [])
        run_summary[status].append(path.name)

    run_summary_path = results_dir / "evaluation_run_summary.json"
    with open(run_summary_path, "w", encoding="utf-8") as f:
        json.dump(run_summary, f, indent=2, ensure_ascii=False)

    print("")
    print("=" * 100)
    print("GLOBAL RUN SUMMARY")
    print("=" * 100)

    for k, v in run_summary.items():
        print(f"{k}: {len(v)}")
        for name in v:
            print(f"  - {name}")

    print("")
    print(f"Saved global summary: {run_summary_path}")
    print("=" * 100)


if __name__ == "__main__":
    main()