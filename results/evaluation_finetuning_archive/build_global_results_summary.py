#!/usr/bin/env python3

import json
from pathlib import Path
from datetime import datetime


RESULTS_DIR = Path("results")
SOLUTIONS_DIR = Path("results_qwen_lora/solutions")
OUTPUT_FILE = RESULTS_DIR / "global_qwen_lora_evaluation_summary.json"


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def model_key_from_solution(path: Path):
    name = path.name
    if name.endswith("_solutions.json"):
        return name[:-len("_solutions.json")]
    return path.stem


def model_key_from_summary(path: Path):
    name = path.name
    if name.endswith("_evaluation_summary.json"):
        return name[:-len("_evaluation_summary.json")]
    return path.stem


def inspect_generation_file(solution_path: Path):
    """
    Inspecte un fichier *_solutions.json.

    Une génération est considérée valide seulement si :
      - le fichier existe
      - le JSON est une liste
      - il ne contient aucun null
      - il ne finit pas par null
      - il contient 164 entrées pour HumanEval
    """
    info = {
        "solution_file": str(solution_path),
        "status": "missing",
        "complete_for_evaluation": False,
        "error": None,
        "num_solutions": None,
        "expected_solutions": 164,
        "length_ok": False,
        "trailing_null": None,
        "none_count": None,
        "ok_extractions": None,
        "warnings": None,
        "errors": None,
        "empty_code": None,
    }

    if not solution_path.exists():
        info["status"] = "missing"
        info["error"] = "solution file does not exist"
        return info

    try:
        data = load_json(solution_path)
    except Exception as e:
        info["status"] = "bad_json"
        info["error"] = str(e)
        return info

    if not isinstance(data, list):
        info["status"] = "not_list"
        info["error"] = "JSON root is not a list"
        return info

    num_solutions = len(data)
    trailing_null = bool(data and data[-1] is None)
    none_count = sum(1 for x in data if x is None)
    length_ok = num_solutions == 164

    ok_extractions = sum(
        1 for x in data
        if x and x.get("extraction_status") == "ok"
    )

    warnings = sum(
        1 for x in data
        if x and x.get("extraction_status") != "ok"
    )

    errors = sum(
        1 for x in data
        if x and x.get("error")
    )

    empty_code = sum(
        1 for x in data
        if x and not x.get("code")
    )

    info.update({
        "num_solutions": num_solutions,
        "length_ok": length_ok,
        "trailing_null": trailing_null,
        "none_count": none_count,
        "ok_extractions": ok_extractions,
        "warnings": warnings,
        "errors": errors,
        "empty_code": empty_code,
    })

    if not length_ok:
        info["status"] = "incomplete"
        info["error"] = f"expected 164 solutions, found {num_solutions}"
        return info

    if trailing_null:
        info["status"] = "incomplete"
        info["error"] = "JSON ends with null"
        return info

    if none_count > 0:
        info["status"] = "incomplete"
        info["error"] = f"JSON contains {none_count} null entries"
        return info

    info["status"] = "complete"
    info["complete_for_evaluation"] = True
    return info


def find_solution_for_summary(summary_data, generation_files):
    """
    Retrouve le fichier de génération correspondant à un summary.
    Priorité :
      1. champ solution_file dans le summary
      2. model_key dans generation_files
    """
    solution_file = summary_data.get("solution_file")
    if solution_file:
        p = Path(solution_file)
        if p.exists():
            return p

    model_key = summary_data.get("model_key")
    if model_key and model_key in generation_files:
        return Path(generation_files[model_key]["solution_file"])

    return None


def build_valid_evaluation_entry(model_key, summary_path, summary_data, generation_info):
    metrics = summary_data.get("metrics", {})
    counter = summary_data.get("counter", {})

    return {
        "status": "evaluated",
        "valid_for_ranking": True,
        "evaluation_summary_file": str(summary_path),
        "solution_file": summary_data.get("solution_file"),
        "benchmark_size": summary_data.get("benchmark_size"),
        "evaluated_at": summary_data.get("evaluated_at"),
        "execution_time_limit": summary_data.get("execution_time_limit"),

        "generation_status": generation_info.get("status"),
        "generation_complete": generation_info.get("complete_for_evaluation"),
        "num_solutions": generation_info.get("num_solutions"),
        "none_count": generation_info.get("none_count"),
        "trailing_null": generation_info.get("trailing_null"),
        "ok_extractions": generation_info.get("ok_extractions"),
        "generation_warnings": generation_info.get("warnings"),
        "generation_errors": generation_info.get("errors"),
        "empty_code": generation_info.get("empty_code"),

        "ok": metrics.get("ok"),
        "total": metrics.get("total"),
        "failed": metrics.get("failed"),
        "pass_at_1": metrics.get("pass_at_1"),
        "output_correctness_rate": metrics.get("output_correctness_rate"),
        "compilation_rate": metrics.get("compilation_rate"),
        "execution_success_rate": metrics.get("execution_success_rate"),

        "compile_err": metrics.get("compile_err"),
        "runtime_err": metrics.get("runtime_err"),
        "ineq": metrics.get("ineq"),
        "exception": metrics.get("exception"),

        "raw_counter": counter,
    }


def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    solution_files = sorted(SOLUTIONS_DIR.glob("*_solutions.json"))
    summary_files = sorted(RESULTS_DIR.glob("*_evaluation_summary.json"))

    generation_files = {}

    for p in solution_files:
        model_key = model_key_from_solution(p)
        generation_files[model_key] = inspect_generation_file(p)

    models = {}
    ignored_evaluations = {}

    for p in summary_files:
        try:
            summary_data = load_json(p)
        except Exception as e:
            key = model_key_from_summary(p)
            ignored_evaluations[key] = {
                "status": "ignored_bad_evaluation_json",
                "evaluation_summary_file": str(p),
                "reason": str(e),
            }
            continue

        model_key = summary_data.get("model_key", model_key_from_summary(p))
        solution_path = find_solution_for_summary(summary_data, generation_files)

        if solution_path is None:
            ignored_evaluations[model_key] = {
                "status": "ignored_missing_solution_file",
                "evaluation_summary_file": str(p),
                "solution_file": summary_data.get("solution_file"),
                "reason": "corresponding solution file not found",
            }
            continue

        generation_info = inspect_generation_file(solution_path)

        if not generation_info.get("complete_for_evaluation"):
            ignored_evaluations[model_key] = {
                "status": "ignored_incomplete_generation",
                "evaluation_summary_file": str(p),
                "solution_file": str(solution_path),
                "reason": generation_info.get("error"),
                "generation_status": generation_info.get("status"),
                "num_solutions": generation_info.get("num_solutions"),
                "trailing_null": generation_info.get("trailing_null"),
                "none_count": generation_info.get("none_count"),
                "ok_extractions": generation_info.get("ok_extractions"),
                "empty_code": generation_info.get("empty_code"),
            }
            continue

        models[model_key] = build_valid_evaluation_entry(
            model_key=model_key,
            summary_path=p,
            summary_data=summary_data,
            generation_info=generation_info,
        )

    # Ajouter les générations présentes mais pas encore évaluées
    for model_key, gen_info in generation_files.items():
        if model_key in models or model_key in ignored_evaluations:
            continue

        models[model_key] = {
            "status": "not_evaluated_yet",
            "valid_for_ranking": False,
            "solution_file": gen_info.get("solution_file"),
            "generation_status": gen_info.get("status"),
            "generation_complete": gen_info.get("complete_for_evaluation"),
            "num_solutions": gen_info.get("num_solutions"),
            "trailing_null": gen_info.get("trailing_null"),
            "none_count": gen_info.get("none_count"),
            "ok_extractions": gen_info.get("ok_extractions"),
            "warnings": gen_info.get("warnings"),
            "errors": gen_info.get("errors"),
            "empty_code": gen_info.get("empty_code"),
            "reason": gen_info.get("error"),
        }

    ranked = []

    for model_key, item in models.items():
        if item.get("status") != "evaluated":
            continue
        if not item.get("valid_for_ranking"):
            continue

        ranked.append({
            "model_key": model_key,
            "ok": item.get("ok"),
            "total": item.get("total"),
            "pass_at_1": item.get("pass_at_1"),
            "compilation_rate": item.get("compilation_rate"),
            "execution_success_rate": item.get("execution_success_rate"),
            "compile_err": item.get("compile_err"),
            "runtime_err": item.get("runtime_err"),
            "ineq": item.get("ineq"),
            "exception": item.get("exception"),
            "empty_code": item.get("empty_code"),
            "ok_extractions": item.get("ok_extractions"),
        })

    ranked = sorted(
        ranked,
        key=lambda x: (
            x["pass_at_1"] if x["pass_at_1"] is not None else -1,
            x["compilation_rate"] if x["compilation_rate"] is not None else -1,
            x["execution_success_rate"] if x["execution_success_rate"] is not None else -1,
        ),
        reverse=True,
    )

    complete_generations = [
        k for k, v in generation_files.items()
        if v.get("complete_for_evaluation")
    ]

    incomplete_generations = {
        k: v for k, v in generation_files.items()
        if not v.get("complete_for_evaluation")
    }

    global_summary = {
        "created_at": datetime.now().isoformat(),
        "results_dir": str(RESULTS_DIR),
        "solutions_dir": str(SOLUTIONS_DIR),

        "important_note": (
            "Only models whose generation file is complete "
            "(164 entries, no null, no trailing null) are included in ranking_by_pass_at_1."
        ),

        "counts": {
            "solution_files_found": len(solution_files),
            "evaluation_summary_files_found": len(summary_files),
            "complete_generations": len(complete_generations),
            "incomplete_generations": len(incomplete_generations),
            "valid_evaluated_models": len([
                x for x in models.values()
                if x.get("status") == "evaluated" and x.get("valid_for_ranking")
            ]),
            "not_evaluated_yet": len([
                x for x in models.values()
                if x.get("status") == "not_evaluated_yet"
            ]),
            "ignored_evaluations": len(ignored_evaluations),
        },

        "ranking_by_pass_at_1": ranked,
        "models": models,
        "generation_files": generation_files,
        "ignored_evaluations": ignored_evaluations,
        "incomplete_generations": incomplete_generations,
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(global_summary, f, indent=2, ensure_ascii=False)

    print("=" * 100)
    print("Global evaluation summary created")
    print("=" * 100)
    print("Output:", OUTPUT_FILE)
    print("")
    print("Counts:")
    for k, v in global_summary["counts"].items():
        print(f"  {k}: {v}")

    print("")
    print("Ranking by Pass@1, complete generations only:")
    for i, row in enumerate(ranked, 1):
        print(
            f"{i:02d}. {row['model_key']} | "
            f"ok={row['ok']}/{row['total']} | "
            f"Pass@1={row['pass_at_1']:.4f} | "
            f"Compilation={row['compilation_rate']:.4f} | "
            f"Execution={row['execution_success_rate']:.4f} | "
            f"empty_code={row['empty_code']}"
        )

    if incomplete_generations:
        print("")
        print("Incomplete generations excluded from ranking:")
        for k, v in incomplete_generations.items():
            print(
                f"  - {k}: status={v.get('status')}, "
                f"num={v.get('num_solutions')}, "
                f"none={v.get('none_count')}, "
                f"trailing_null={v.get('trailing_null')}, "
                f"reason={v.get('error')}"
            )

    if ignored_evaluations:
        print("")
        print("Ignored stale/invalid evaluations:")
        for k, v in ignored_evaluations.items():
            print(f"  - {k}: {v.get('reason')}")

    print("=" * 100)


if __name__ == "__main__":
    main()