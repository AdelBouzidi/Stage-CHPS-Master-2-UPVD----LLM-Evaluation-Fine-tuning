#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import csv
import subprocess
from pathlib import Path
from collections import Counter

ROOT = Path(".")
BENCHMARK = Path("../benchmark.json")

BASE_SUMMARY = Path("_base_reference/results/base_humaneval_mistral_conc30_evaluation_summary.json")
BASE_DETAILS = Path("_base_reference/results/base_humaneval_mistral_conc30_evaluation_details.json")

OUT_COMPARE_DIR = Path("results/task_comparison_base_conc30_all_available")
OUT_COMPARE_DIR.mkdir(parents=True, exist_ok=True)

LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

EVALUATOR = Path("evaluate_all_qwen_lora_solutions.py")

LAYOUTS = [
    Path("epoch1/learning_rate_1"),
    Path("epoch1/learning_rate_2"),
    Path("epoch2/learning_rate_1"),
    Path("epoch2/learning_rate_2"),
]

EXECUTION_TIME_LIMIT = 120


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def solution_is_complete(path):
    try:
        data = load_json(path)
    except Exception:
        return False, "invalid_json"

    if not isinstance(data, list):
        return False, "not_list"

    total = len(data)
    none = sum(x is None for x in data)
    trailing_null = bool(total > 0 and data[-1] is None)
    ok = sum(1 for x in data if x and x.get("extraction_status") == "ok")
    empty = sum(1 for x in data if x and not x.get("code"))
    errors = sum(1 for x in data if x and x.get("error"))

    if total == 164 and none == 0 and not trailing_null:
        return True, f"complete_total={total}_ok={ok}_empty={empty}_errors={errors}"

    return False, f"incomplete_total={total}_none={none}_trailing_null={trailing_null}_ok={ok}_empty={empty}_errors={errors}"


def solution_key(path):
    return path.name.replace("_solutions.json", "")


def expected_details_path(results_dir, sol_path):
    key = solution_key(sol_path)
    return results_dir / f"{key}_evaluation_details.json"


def expected_summary_path(results_dir, sol_path):
    key = solution_key(sol_path)
    return results_dir / f"{key}_evaluation_summary.json"


def run_eval_for_layout(layout):
    solutions_dir = layout / "results_qwen_lora" / "solutions"
    results_dir = layout / "results"
    logs_dir = layout / "logs"

    results_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    if not solutions_dir.exists():
        print(f"SKIP layout without solutions dir: {layout}")
        return

    solution_files = sorted(solutions_dir.glob("*_solutions.json"))
    if not solution_files:
        print(f"SKIP layout without solutions: {layout}")
        return

    complete_not_evaluated = []

    for sol in solution_files:
        complete, status = solution_is_complete(sol)
        details = expected_details_path(results_dir, sol)

        if complete and not details.exists():
            complete_not_evaluated.append(sol)

        print(f"[GEN] {sol} | {status} | evaluated={details.exists()}")

    if not complete_not_evaluated:
        print(f"OK: nothing new to evaluate in {layout}")
        return

    print("=" * 100)
    print(f"EVALUATING LAYOUT: {layout}")
    print(f"Complete but not evaluated: {len(complete_not_evaluated)}")
    for sol in complete_not_evaluated:
        print("  -", sol.name)
    print("=" * 100)

    log_file = logs_dir / "evaluate_all_qwen_lora_solutions_auto.log"

    cmd = [
        "python",
        str(EVALUATOR),
        "--benchmark", str(BENCHMARK),
        "--solutions-dir", str(solutions_dir),
        "--results-dir", str(results_dir),
        "--execution-time-limit", str(EXECUTION_TIME_LIMIT),
    ]

    with open(log_file, "a", encoding="utf-8") as log:
        log.write("\n" + "=" * 100 + "\n")
        log.write("COMMAND: " + " ".join(cmd) + "\n")
        log.write("=" * 100 + "\n")
        log.flush()

        subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, check=False)

    print(f"Evaluation log: {log_file}")


def extract_items(obj):
    if isinstance(obj, list):
        return obj

    if isinstance(obj, dict):
        for key in ["details", "results", "items", "tasks", "evaluations"]:
            if isinstance(obj.get(key), list):
                return obj[key]

        if all(isinstance(v, dict) for v in obj.values()):
            return list(obj.values())

    raise ValueError("Unsupported evaluation details format")


def get_task_id(item, fallback):
    if isinstance(item, dict):
        for key in ["task_id", "id", "task_index", "index", "problem_id"]:
            if key in item:
                return str(item[key])
        for key in ["name", "task_name"]:
            if key in item:
                return str(item[key])
    return str(fallback)


def get_status(item):
    if not isinstance(item, dict):
        return "unknown"

    for key in ["status", "result", "outcome", "verdict"]:
        value = item.get(key)
        if isinstance(value, str):
            return value

    if item.get("error_type"):
        return str(item["error_type"])

    if "passed" in item:
        return "ok" if item["passed"] else "failed"

    if "ok" in item:
        return "ok" if item["ok"] else "failed"

    for key in ["evaluation", "eval", "execution"]:
        sub = item.get(key)
        if isinstance(sub, dict):
            for subkey in ["status", "result", "outcome", "verdict"]:
                value = sub.get(subkey)
                if isinstance(value, str):
                    return value

    return "unknown"


def is_ok(status):
    return str(status).lower() == "ok"


def build_task_map(details_file):
    obj = load_json(details_file)
    items = extract_items(obj)

    out = {}
    for i, item in enumerate(items):
        task_id = get_task_id(item, i)
        out[task_id] = {
            "task_id": task_id,
            "status": get_status(item),
            "raw": item,
        }

    return out


def model_key_from_details(path):
    return path.name.replace("_evaluation_details.json", "")


def get_metrics(summary_file):
    if not summary_file.exists():
        return {}

    d = load_json(summary_file)
    return d.get("metrics", d)


def compare_all_vs_base():
    if not BASE_DETAILS.exists():
        raise SystemExit(f"Missing base details file: {BASE_DETAILS}")

    base = build_task_map(BASE_DETAILS)
    base_metrics = get_metrics(BASE_SUMMARY)

    print("=" * 100)
    print("BASE REFERENCE")
    print("=" * 100)
    print("Base details:", BASE_DETAILS)
    print("Base summary:", BASE_SUMMARY)
    print("Base OK:", base_metrics.get("ok"))
    print("Base pass_at_1:", base_metrics.get("pass_at_1"))
    print("Base tasks:", len(base))

    detail_files = []
    for root in ["epoch1", "epoch2", "results"]:
        detail_files.extend(Path(root).glob("**/*_evaluation_details.json"))

    detail_files = sorted(set(detail_files))

    rows_summary = []
    rows_task = []
    wins = {}
    losses = {}
    transitions_all = {}

    for details_file in detail_files:
        model_key = model_key_from_details(details_file)

        if model_key.startswith("base_"):
            continue

        try:
            ft = build_task_map(details_file)
        except Exception as e:
            print("SKIP unreadable details:", details_file, e)
            continue

        common = sorted(
            set(base) & set(ft),
            key=lambda x: int(x) if str(x).isdigit() else str(x)
        )

        if not common:
            print("SKIP no common tasks:", details_file)
            continue

        c = Counter()
        transitions = Counter()
        base_fail_ft_ok = []
        base_ok_ft_fail = []

        for task_id in common:
            base_status = base[task_id]["status"]
            ft_status = ft[task_id]["status"]

            base_ok = is_ok(base_status)
            ft_ok = is_ok(ft_status)

            if base_ok and ft_ok:
                category = "base_ok_ft_ok"
            elif (not base_ok) and ft_ok:
                category = "base_fail_ft_ok"
                base_fail_ft_ok.append(task_id)
            elif base_ok and (not ft_ok):
                category = "base_ok_ft_fail"
                base_ok_ft_fail.append(task_id)
            else:
                category = "base_fail_ft_fail"

            c[category] += 1
            transitions[(base_status, ft_status)] += 1

            rows_task.append({
                "model_key": model_key,
                "details_file": str(details_file),
                "task_id": task_id,
                "base_status": base_status,
                "ft_status": ft_status,
                "category": category,
            })

        ft_ok_count = sum(1 for tid in common if is_ok(ft[tid]["status"]))
        base_ok_count = sum(1 for tid in common if is_ok(base[tid]["status"]))

        summary_file = details_file.with_name(details_file.name.replace("_evaluation_details.json", "_evaluation_summary.json"))
        metrics = get_metrics(summary_file)

        rows_summary.append({
            "model_key": model_key,
            "details_file": str(details_file),
            "summary_file": str(summary_file),
            "common_tasks": len(common),
            "base_ok": base_ok_count,
            "ft_ok": ft_ok_count,
            "delta_ok": ft_ok_count - base_ok_count,
            "base_fail_ft_ok": c["base_fail_ft_ok"],
            "base_ok_ft_fail": c["base_ok_ft_fail"],
            "base_ok_ft_ok": c["base_ok_ft_ok"],
            "base_fail_ft_fail": c["base_fail_ft_fail"],
            "compile_err": metrics.get("compile_err"),
            "runtime_err": metrics.get("runtime_err"),
            "ineq": metrics.get("ineq"),
            "exception": metrics.get("exception"),
            "compilation_rate": metrics.get("compilation_rate"),
            "execution_success_rate": metrics.get("execution_success_rate"),
            "pass_at_1": metrics.get("pass_at_1"),
        })

        wins[model_key] = base_fail_ft_ok
        losses[model_key] = base_ok_ft_fail
        transitions_all[model_key] = {
            f"{a} -> {b}": n
            for (a, b), n in transitions.most_common()
        }

    rows_summary.sort(key=lambda r: (int(r["delta_ok"]), int(r["ft_ok"])), reverse=True)

    summary_csv = OUT_COMPARE_DIR / "summary_vs_base_conc30_all_available.csv"
    with open(summary_csv, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "model_key",
            "details_file",
            "summary_file",
            "common_tasks",
            "base_ok",
            "ft_ok",
            "delta_ok",
            "base_fail_ft_ok",
            "base_ok_ft_fail",
            "base_ok_ft_ok",
            "base_fail_ft_fail",
            "compile_err",
            "runtime_err",
            "ineq",
            "exception",
            "compilation_rate",
            "execution_success_rate",
            "pass_at_1",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows_summary)

    task_csv = OUT_COMPARE_DIR / "task_by_task_vs_base_conc30_all_available.csv"
    with open(task_csv, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "model_key",
            "details_file",
            "task_id",
            "base_status",
            "ft_status",
            "category",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows_task)

    with open(OUT_COMPARE_DIR / "base_fail_ft_ok_tasks.json", "w", encoding="utf-8") as f:
        json.dump(wins, f, indent=2, ensure_ascii=False)

    with open(OUT_COMPARE_DIR / "base_ok_ft_fail_tasks.json", "w", encoding="utf-8") as f:
        json.dump(losses, f, indent=2, ensure_ascii=False)

    with open(OUT_COMPARE_DIR / "status_transitions.json", "w", encoding="utf-8") as f:
        json.dump(transitions_all, f, indent=2, ensure_ascii=False)

    print()
    print("=" * 100)
    print("SUMMARY VS BASE CONC30 - ALL AVAILABLE")
    print("=" * 100)

    for r in rows_summary:
        print(
            f"{r['model_key']:75s} "
            f"ft_ok={int(r['ft_ok']):3d} "
            f"base_ok={int(r['base_ok']):3d} "
            f"delta={int(r['delta_ok']):+4d} "
            f"wins={int(r['base_fail_ft_ok']):3d} "
            f"losses={int(r['base_ok_ft_fail']):3d} "
            f"compile={r['compile_err']} runtime={r['runtime_err']} ineq={r['ineq']}"
        )

    print()
    print("Written:")
    print(" ", summary_csv)
    print(" ", task_csv)
    print(" ", OUT_COMPARE_DIR / "base_fail_ft_ok_tasks.json")
    print(" ", OUT_COMPARE_DIR / "base_ok_ft_fail_tasks.json")
    print(" ", OUT_COMPARE_DIR / "status_transitions.json")


def main():
    print("=" * 100)
    print("STEP 1 - Evaluate complete generations not evaluated yet")
    print("=" * 100)

    if not EVALUATOR.exists():
        raise SystemExit(f"Missing evaluator script: {EVALUATOR}")

    if not BENCHMARK.exists():
        raise SystemExit(f"Missing benchmark: {BENCHMARK}")

    for layout in LAYOUTS:
        run_eval_for_layout(layout)

    print()
    print("=" * 100)
    print("STEP 2 - Compare all evaluated models against base conc30")
    print("=" * 100)

    compare_all_vs_base()


if __name__ == "__main__":
    main()
