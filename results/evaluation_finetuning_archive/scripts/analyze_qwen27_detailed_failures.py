#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from collections import Counter
from typing import Any, Dict, List, Optional


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def flatten(obj: Any, prefix: str = "") -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            key = f"{prefix}.{k}" if prefix else str(k)
            out.update(flatten(v, key))
    elif isinstance(obj, list):
        out[prefix + ".__len__"] = len(obj)
    else:
        out[prefix] = obj
    return out


def simplify_name(filename: str) -> str:
    name = filename
    name = name.replace("_qwen27_humaneval_mistral_conc12_evaluation_details.json", "")
    name = name.replace("_qwen27_humaneval_mistral_conc12_evaluation_summary.json", "")
    name = name.replace("_evaluation_details.json", "")
    name = name.replace("_evaluation_summary.json", "")
    name = name.replace("ft_", "")
    return name


def family_from_name(name: str) -> str:
    if name == "A":
        return "baseline_ft_A"
    if name == "AB_antineighbor":
        return "baseline_ft_AB"
    if name == "ABC_dedup_BC":
        return "abc_dedup_bc"
    if name == "ABC_filtered_accept":
        return "filtered_accept_all"
    if name.startswith("ABC_filtered_accept_"):
        return "filtered_accept_subset"
    if name == "ABC_filtered_manual":
        return "filtered_manual"
    if name == "ABC_filtered_reject":
        return "filtered_reject"
    if name.startswith("ABC_source_"):
        return "source_subset"
    return "other"


def extract_entries(obj: Any) -> List[Dict[str, Any]]:
    """
    Extract task-level evaluation entries.

    Expected common shapes:
    - list[dict]
    - dict task_id -> dict
    - dict containing a list[dict] under details/results/items/tasks/evaluations
    """
    candidates: List[List[Dict[str, Any]]] = []

    def add_candidate(lst: List[Dict[str, Any]]) -> None:
        if not lst:
            return
        text = json.dumps(lst[:5], ensure_ascii=False).lower()
        score = len(lst)
        for kw in ["task_id", "status", "score", "compile_err", "ineq", "ok", "stderr", "stdout", "expected"]:
            if kw in text:
                score += 100
        candidates.append((score, lst))  # type: ignore[arg-type]

    def rec(x: Any) -> None:
        if isinstance(x, list) and x and all(isinstance(e, dict) for e in x):
            add_candidate(x)
        elif isinstance(x, dict):
            if x and all(isinstance(v, dict) for v in x.values()):
                keyed = []
                for k, v in x.items():
                    y = dict(v)
                    y.setdefault("task_id", k)
                    keyed.append(y)
                add_candidate(keyed)

            for v in x.values():
                rec(v)

    rec(obj)

    if not candidates:
        return []

    candidates.sort(key=lambda z: z[0], reverse=True)  # type: ignore[index]
    return candidates[0][1]  # type: ignore[index]


def get_task_id(entry: Dict[str, Any], fallback_index: int) -> str:
    flat = flatten(entry)
    for k in [
        "task_id",
        "id",
        "problem_id",
        "humaneval_id",
        "metadata.task_id",
        "metadata.id",
        "sample.task_id",
        "sample.id",
    ]:
        if k in flat and flat[k] not in (None, ""):
            return str(flat[k])
    return str(fallback_index)


def get_status(entry: Dict[str, Any]) -> str:
    flat = flatten(entry)

    # Strong priority: exact/typical status fields
    for k in [
        "status",
        "result.status",
        "evaluation.status",
        "validation.status",
        "final_status",
        "result",
    ]:
        if k in flat and flat[k] not in (None, ""):
            return str(flat[k]).strip().lower()

    # Fallback: any key ending in status
    for k, v in flat.items():
        if str(k).lower().endswith("status") and v not in (None, ""):
            return str(v).strip().lower()

    # Fallback score only if no status exists
    for k in ["score", "passed", "ok", "correct", "is_correct"]:
        if k in flat:
            v = flat[k]
            if v is True or str(v).strip() == "1":
                return "ok"
            if v is False or str(v).strip() == "0":
                return "failed"

    return "unknown"


def is_ok_status(status: str) -> bool:
    return status in {"ok", "pass", "passed", "success", "accepted", "correct"}


def failure_category_from_status(status: str, entry: Dict[str, Any]) -> str:
    s = status.lower()

    if is_ok_status(s):
        return "ok"

    if s in {"compile_err", "compile_error", "compilation_error", "compilation_err"}:
        return "compile_error"

    if s in {"ineq", "wrong_output", "output_mismatch", "mismatch", "incorrect_output"}:
        return "wrong_output"

    if s in {"runtime_err", "runtime_error", "run_err", "execution_error"}:
        return "runtime_error"

    if s in {"timeout", "time_limit", "execution_time_limit", "timed_out"}:
        return "timeout"

    if s in {"exception", "generation_error", "parse_error", "invalid_json"}:
        return "generation_or_parse_error"

    # Text fallback
    text = json.dumps(entry, ensure_ascii=False).lower()

    if "compile_err" in text or "compile error" in text or "gfortran" in text:
        return "compile_error"
    if "timeout" in text or "time limit" in text:
        return "timeout"
    if "runtime" in text or "segmentation fault" in text or "floating point" in text:
        return "runtime_error"
    if "ineq" in text or "wrong_output" in text or "expected" in text and "actual" in text:
        return "wrong_output"

    return "unknown_failure"


def diagnostic_text(entry: Dict[str, Any], max_len: int = 350) -> str:
    flat = flatten(entry)
    parts = []

    for k, v in flat.items():
        lk = str(k).lower()
        if any(t in lk for t in ["status", "score", "stderr", "stdout", "expected", "actual", "error", "message", "diagnostic"]):
            if v not in (None, ""):
                sv = str(v).replace("\n", "\\n")
                parts.append(f"{k}={sv[:160]}")

    if not parts:
        text = json.dumps(entry, ensure_ascii=False).replace("\n", "\\n")
        return text[:max_len]

    text = " | ".join(parts)
    return text[:max_len]


def read_summary_ok(results_dir: Path) -> Dict[str, int]:
    out: Dict[str, int] = {}

    for p in sorted(results_dir.glob("*_evaluation_summary.json")):
        run = simplify_name(p.name)
        obj = load_json(p)
        flat = flatten(obj)

        ok_value = None
        for k in ["counter.ok", "metrics.ok", "ok", "counter.accepted"]:
            if k in flat:
                ok_value = flat[k]
                break

        if ok_value is None:
            raise SystemExit(f"Cannot find OK count in summary: {p}")

        out[run] = int(ok_value)

    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--results-dir", required=True)
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--reference-run", default="A")
    args = ap.parse_args()

    results_dir = Path(args.results_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    summary_ok = read_summary_ok(results_dir)

    detail_files = sorted(results_dir.glob("*_evaluation_details.json"))
    all_rows: List[Dict[str, Any]] = []
    parse_report: List[Dict[str, Any]] = []

    for p in detail_files:
        run = simplify_name(p.name)
        family = family_from_name(run)
        obj = load_json(p)
        entries = extract_entries(obj)

        parse_report.append({
            "run_name": run,
            "file": p.name,
            "entries_detected": len(entries),
        })

        for idx, e in enumerate(entries):
            tid = get_task_id(e, idx)
            status = get_status(e)
            ok = is_ok_status(status)
            failure_category = "ok" if ok else failure_category_from_status(status, e)

            all_rows.append({
                "run_name": run,
                "family": family,
                "task_id": tid,
                "status": status,
                "ok": int(ok),
                "failure_category": failure_category,
                "diagnostic": diagnostic_text(e),
                "detail_file": p.name,
            })

    # Validation against summaries
    detail_ok = Counter()
    detail_total = Counter()

    for r in all_rows:
        detail_total[r["run_name"]] += 1
        if r["ok"]:
            detail_ok[r["run_name"]] += 1

    mismatches = []
    for run, expected_ok in summary_ok.items():
        got_ok = detail_ok.get(run, 0)
        if got_ok != expected_ok:
            mismatches.append({
                "run_name": run,
                "summary_ok": expected_ok,
                "details_ok": got_ok,
                "details_total": detail_total.get(run, 0),
            })

    # Always write parse report before failing
    with (output_dir / "qwen27_details_parse_report.csv").open("w", newline="", encoding="utf-8") as f:
        cols = ["run_name", "file", "entries_detected"]
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(parse_report)

    if mismatches:
        mismatch_path = output_dir / "qwen27_details_summary_mismatches.json"
        mismatch_path.write_text(json.dumps(mismatches, indent=2, ensure_ascii=False), encoding="utf-8")
        print("ERROR: details OK counts do not match summary OK counts.")
        print("mismatch_path =", mismatch_path)
        print(json.dumps(mismatches, indent=2, ensure_ascii=False))
        raise SystemExit(2)

    runs = sorted({r["run_name"] for r in all_rows})
    tasks = sorted({r["task_id"] for r in all_rows}, key=lambda x: int(x) if str(x).isdigit() else str(x))

    by_run_task = {(r["run_name"], r["task_id"]): r for r in all_rows}

    # Outcomes
    outcomes_csv = output_dir / "qwen27_task_outcomes.csv"
    with outcomes_csv.open("w", newline="", encoding="utf-8") as f:
        cols = ["run_name", "family", "task_id", "status", "ok", "failure_category", "diagnostic", "detail_file"]
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(all_rows)

    # Matrix
    matrix_csv = output_dir / "qwen27_task_matrix.csv"
    with matrix_csv.open("w", newline="", encoding="utf-8") as f:
        cols = ["task_id"] + runs
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for tid in tasks:
            row = {"task_id": tid}
            for run in runs:
                item = by_run_task.get((run, tid))
                if not item:
                    row[run] = "missing"
                elif item["ok"]:
                    row[run] = "OK"
                else:
                    row[run] = item["failure_category"]
            w.writerow(row)

    # Failure categories
    failure_rows = []
    for run in runs:
        rows = [r for r in all_rows if r["run_name"] == run]
        c = Counter(r["failure_category"] for r in rows)
        ok_count = c.get("ok", 0)
        total = len(rows)
        failure_rows.append({
            "run_name": run,
            "family": family_from_name(run),
            "total_entries": total,
            "ok": ok_count,
            "failures": total - ok_count,
            "compile_error": c.get("compile_error", 0),
            "wrong_output": c.get("wrong_output", 0),
            "runtime_error": c.get("runtime_error", 0),
            "timeout": c.get("timeout", 0),
            "generation_or_parse_error": c.get("generation_or_parse_error", 0),
            "unknown_failure": c.get("unknown_failure", 0),
        })

    failure_rows.sort(key=lambda x: x["ok"], reverse=True)

    failure_csv = output_dir / "qwen27_failure_categories_by_model.csv"
    with failure_csv.open("w", newline="", encoding="utf-8") as f:
        cols = list(failure_rows[0].keys())
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(failure_rows)

    # Pairwise vs reference
    ref = args.reference_run
    ref_ok = {r["task_id"] for r in all_rows if r["run_name"] == ref and r["ok"]}

    pair_rows = []
    unique_rows = []
    ref_only_rows = []

    for run in runs:
        run_ok = {r["task_id"] for r in all_rows if r["run_name"] == run and r["ok"]}
        both_ok = ref_ok & run_ok
        run_only = run_ok - ref_ok
        ref_only = ref_ok - run_ok
        both_fail = set(tasks) - (ref_ok | run_ok)

        pair_rows.append({
            "run_name": run,
            "family": family_from_name(run),
            "ref_run": ref,
            "ref_ok": len(ref_ok),
            "run_ok": len(run_ok),
            "delta_vs_ref": len(run_ok) - len(ref_ok),
            "both_ok": len(both_ok),
            "run_only_unique_wins": len(run_only),
            "ref_only_losses": len(ref_only),
            "both_fail": len(both_fail),
        })

        for tid in sorted(run_only, key=lambda x: int(x) if str(x).isdigit() else str(x)):
            ref_item = by_run_task.get((ref, tid))
            unique_rows.append({
                "run_name": run,
                "task_id": tid,
                "run_status": "OK",
                "ref_failure_category": ref_item["failure_category"] if ref_item else "missing",
                "ref_status": ref_item["status"] if ref_item else "missing",
                "ref_diagnostic": ref_item["diagnostic"] if ref_item else "",
            })

        if run != ref:
            for tid in sorted(ref_only, key=lambda x: int(x) if str(x).isdigit() else str(x)):
                item = by_run_task.get((run, tid))
                ref_only_rows.append({
                    "run_name": run,
                    "task_id": tid,
                    "ref_status": "OK",
                    "run_failure_category": item["failure_category"] if item else "missing",
                    "run_status": item["status"] if item else "missing",
                    "run_diagnostic": item["diagnostic"] if item else "",
                })

    pair_rows.sort(key=lambda x: x["run_ok"], reverse=True)

    pair_csv = output_dir / "qwen27_pairwise_vs_A.csv"
    with pair_csv.open("w", newline="", encoding="utf-8") as f:
        cols = list(pair_rows[0].keys())
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(pair_rows)

    unique_csv = output_dir / "qwen27_unique_wins_vs_A.csv"
    with unique_csv.open("w", newline="", encoding="utf-8") as f:
        cols = ["run_name", "task_id", "run_status", "ref_failure_category", "ref_status", "ref_diagnostic"]
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(unique_rows)

    ref_only_csv = output_dir / "qwen27_A_only_losses_by_other_models.csv"
    with ref_only_csv.open("w", newline="", encoding="utf-8") as f:
        cols = ["run_name", "task_id", "ref_status", "run_failure_category", "run_status", "run_diagnostic"]
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(ref_only_rows)

    # Hard tasks
    hard_rows = []
    for tid in tasks:
        ok_runs = [run for run in runs if by_run_task.get((run, tid), {}).get("ok")]
        fail_cats = Counter(
            by_run_task.get((run, tid), {}).get("failure_category", "missing")
            for run in runs
            if not by_run_task.get((run, tid), {}).get("ok")
        )
        hard_rows.append({
            "task_id": tid,
            "success_count": len(ok_runs),
            "ok_runs": ",".join(ok_runs),
            "dominant_failure": fail_cats.most_common(1)[0][0] if fail_cats else "",
            "failure_distribution": json.dumps(dict(fail_cats), ensure_ascii=False),
        })

    hard_rows.sort(key=lambda x: x["success_count"])

    hard_csv = output_dir / "qwen27_hard_tasks.csv"
    with hard_csv.open("w", newline="", encoding="utf-8") as f:
        cols = ["task_id", "success_count", "ok_runs", "dominant_failure", "failure_distribution"]
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(hard_rows)

    # Markdown
    md = []
    md.append("# Qwen27 detailed failure analysis — corrected strict version")
    md.append("")
    md.append(f"Results dir: `{results_dir}`")
    md.append(f"Reference run: `{ref}`")
    md.append(f"Runs detected: **{len(runs)}**")
    md.append(f"Tasks detected: **{len(tasks)}**")
    md.append("")
    md.append("Validation: details OK counts match summary OK counts.")
    md.append("")

    md.append("## 1. Model ranking and failure categories")
    md.append("")
    cols = ["run_name", "family", "ok", "failures", "compile_error", "wrong_output", "runtime_error", "timeout", "unknown_failure"]
    md.append("| " + " | ".join(cols) + " |")
    md.append("| " + " | ".join(["---"] * len(cols)) + " |")
    for r in failure_rows:
        md.append("| " + " | ".join(str(r.get(c, "")) for c in cols) + " |")
    md.append("")

    md.append("## 2. Pairwise comparison vs FT-A")
    md.append("")
    cols = ["run_name", "run_ok", "delta_vs_ref", "both_ok", "run_only_unique_wins", "ref_only_losses", "both_fail"]
    md.append("| " + " | ".join(cols) + " |")
    md.append("| " + " | ".join(["---"] * len(cols)) + " |")
    for r in pair_rows:
        md.append("| " + " | ".join(str(r.get(c, "")) for c in cols) + " |")
    md.append("")

    md.append("## 3. Hardest tasks")
    md.append("")
    md.append("| task_id | success_count | dominant_failure | ok_runs |")
    md.append("| --- | --- | --- | --- |")
    for r in hard_rows[:30]:
        md.append(f"| {r['task_id']} | {r['success_count']} | {r['dominant_failure']} | {r['ok_runs']} |")

    md_path = output_dir / "qwen27_detailed_failure_analysis.md"
    md_path.write_text("\n".join(md) + "\n", encoding="utf-8")

    print("OK: details counts match summaries.")
    print("runs_detected =", len(runs))
    print("tasks_detected =", len(tasks))
    print("markdown =", md_path)
    print("failure_csv =", failure_csv)
    print("pairwise_csv =", pair_csv)
    print("unique_wins_csv =", unique_csv)
    print("hard_tasks_csv =", hard_csv)


if __name__ == "__main__":
    main()
