#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any, Dict, List


def flatten(obj: Any, prefix: str = "") -> Dict[str, Any]:
    out = {}

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
    name = name.replace("_qwen27_humaneval_mistral_conc12_evaluation_summary.json", "")
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

    if name.startswith("ABC_filtered_accept_"):
        return "filtered_accept_subset"
    if name == "ABC_filtered_accept":
        return "filtered_accept_all"
    if name == "ABC_filtered_manual":
        return "filtered_manual"
    if name == "ABC_filtered_reject":
        return "filtered_reject"

    if name.startswith("ABC_source_"):
        return "source_subset"

    return "other"


def find_col(columns: List[str], patterns: List[str]):
    low = {c.lower(): c for c in columns}
    for pat in patterns:
        r = re.compile(pat)
        for lc, orig in low.items():
            if r.search(lc):
                return orig
    return None


def to_float(x):
    try:
        return float(x)
    except Exception:
        return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--results-dir", required=True)
    ap.add_argument("--output-dir", required=True)
    args = ap.parse_args()

    results_dir = Path(args.results_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    summary_files = sorted(results_dir.glob("*_evaluation_summary.json"))

    rows = []
    all_cols = set()

    for p in summary_files:
        obj = json.loads(p.read_text(encoding="utf-8"))
        flat = flatten(obj)

        run_name = simplify_name(p.name)
        row = {
            "file": p.name,
            "run_name": run_name,
            "family": family_from_name(run_name),
        }
        row.update(flat)

        rows.append(row)
        all_cols.update(row.keys())

    cols = ["run_name", "family", "file"] + sorted(c for c in all_cols if c not in {"run_name", "family", "file"})

    flat_csv = output_dir / "qwen27_summary_flat.csv"
    with flat_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    # Colonnes probables importantes
    metric_patterns = {
        "ok": [
            r"(^|[._-])ok($|[._-])",
            r"ok_count",
            r"num_ok",
            r"passed",
            r"success",
        ],
        "total": [
            r"total",
            r"num_tasks",
            r"n_tasks",
            r"tasks",
        ],
        "pass_at_1": [
            r"pass.?@?1",
            r"pass_at_1",
            r"pass1",
        ],
        "compile_rate": [
            r"compile.*rate",
            r"compilation.*rate",
        ],
        "execution_rate": [
            r"exec.*rate",
            r"execution.*rate",
        ],
        "correctness_rate": [
            r"correct.*rate",
            r"output.*correct",
        ],
    }

    detected = {name: find_col(cols, pats) for name, pats in metric_patterns.items()}

    selected_cols = ["run_name", "family"]
    for _, col in detected.items():
        if col and col not in selected_cols:
            selected_cols.append(col)

    # Ajouter quelques colonnes numériques intéressantes si non détectées
    for c in cols:
        lc = c.lower()
        if any(x in lc for x in ["ok", "pass", "compile", "exec", "correct", "rate", "total"]):
            if c not in selected_cols and len(selected_cols) < 18:
                selected_cols.append(c)

    selected_rows = []
    for r in rows:
        selected_rows.append({c: r.get(c, "") for c in selected_cols})

    # Tri par OK puis pass@1 si trouvé
    ok_col = detected.get("ok")
    pass_col = detected.get("pass_at_1")

    def sort_key(r):
        ok = to_float(r.get(ok_col)) if ok_col else None
        ps = to_float(r.get(pass_col)) if pass_col else None
        return (
            ok if ok is not None else -1,
            ps if ps is not None else -1,
        )

    selected_rows_sorted = sorted(selected_rows, key=sort_key, reverse=True)

    selected_csv = output_dir / "qwen27_summary_selected.csv"
    with selected_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=selected_cols)
        w.writeheader()
        for r in selected_rows_sorted:
            w.writerow(r)

    md = []
    md.append("# Qwen27 evaluation summary — epoch1 learning_rate_1")
    md.append("")
    md.append(f"Results dir: `{results_dir}`")
    md.append(f"Number of evaluation summaries: **{len(rows)}**")
    md.append("")
    md.append("## Detected metric columns")
    md.append("")
    for k, v in detected.items():
        md.append(f"- `{k}` → `{v}`")
    md.append("")
    md.append("## Ranking table")
    md.append("")
    md.append("| " + " | ".join(selected_cols) + " |")
    md.append("| " + " | ".join(["---"] * len(selected_cols)) + " |")
    for r in selected_rows_sorted:
        md.append("| " + " | ".join(str(r.get(c, "")) for c in selected_cols) + " |")

    (output_dir / "qwen27_summary_selected.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print("summary_files =", len(rows))
    print("flat_csv       =", flat_csv)
    print("selected_csv   =", selected_csv)
    print("selected_md    =", output_dir / "qwen27_summary_selected.md")
    print("detected_cols  =", detected)


if __name__ == "__main__":
    main()
