#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import csv
import re
import shutil
import subprocess
from pathlib import Path
from collections import Counter, defaultdict

IN_FILE = Path("results/deep_failure_analysis_base_ok_ft_fail/failure_cases_full.json")

OUT_DIR = Path("results/real_compile_diagnosis_base_ok_ft_fail")
WORK_DIR = OUT_DIR / "work"
OUT_DIR.mkdir(parents=True, exist_ok=True)
WORK_DIR.mkdir(parents=True, exist_ok=True)

OUT_JSON = OUT_DIR / "real_compile_cases.json"
OUT_CSV = OUT_DIR / "real_compile_cases.csv"
OUT_SUMMARY_JSON = OUT_DIR / "real_compile_summary_by_model.json"
OUT_SUMMARY_CSV = OUT_DIR / "real_compile_summary_by_model.csv"
OUT_GLOBAL_TXT = OUT_DIR / "real_compile_global_summary.txt"

GFORTRAN = shutil.which("gfortran") or "gfortran"

COMPILE_FLAGS = [
    "-std=f2008",
    "-Wall",
    "-Wextra",
    "-fcheck=all",
    "-fbacktrace",
]

TIMEOUT = 30


def load_json(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def safe_name(s):
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", str(s))


def short(s, n=1000):
    if s is None:
        return ""
    s = str(s)
    return s if len(s) <= n else s[:n] + "\n...[TRUNCATED]..."


def classify_gfortran(stderr, returncode):
    txt = (stderr or "").lower()
    labels = []

    if returncode == 0:
        labels.append("compile_ok")
        return labels, "compile_ok"

    labels.append("compile_failed")

    rules = [
        ("syntax_error", [
            "syntax error",
            "invalid character",
            "unclassifiable statement",
            "expected",
        ]),
        ("c_like_signature_or_invalid_decl", [
            "invalid character in name",
            "unexpected junk in formal argument list",
            "symbol 'int'",
            "symbol 'float'",
            "float[]",
            "int ",
        ]),
        ("implicit_declaration", [
            "has no implicit type",
            "no implicit type",
            "implicit type",
        ]),
        ("intent_in_modified", [
            "dummy argument",
            "intent(in)",
            "assignment to intent(in)",
            "variable definition context",
        ]),
        ("allocatable_shape_or_allocate", [
            "allocatable scalar",
            "shape specification",
            "allocate-object",
            "must be allocatable",
            "already allocated",
        ]),
        ("rank_mismatch", [
            "rank mismatch",
        ]),
        ("type_mismatch", [
            "type mismatch",
            "cannot convert",
        ]),
        ("interface_required", [
            "explicit interface required",
            "assumed-shape",
        ]),
        ("missing_kind_or_iso", [
            "real32",
            "real64",
            "int32",
            "int64",
            "has no implicit type",
        ]),
        ("invalid_operator_or_expression", [
            "unclassifiable statement",
            "syntax error in expression",
            "expected a right parenthesis",
            "operands of binary numeric operator",
        ]),
        ("empty_or_no_program", [
            "unexpected end of file",
            "undefined reference to `main'",
        ]),
        ("line_truncation", [
            "line truncated",
        ]),
    ]

    for label, terms in rules:
        if any(t in txt for t in terms):
            labels.append(label)

    # cas spécifique : programme vide
    if not txt.strip():
        labels.append("compile_failed_no_stderr")

    if len(labels) == 1:
        labels.append("compile_other")

    priority = [
        "c_like_signature_or_invalid_decl",
        "intent_in_modified",
        "implicit_declaration",
        "allocatable_shape_or_allocate",
        "interface_required",
        "rank_mismatch",
        "type_mismatch",
        "missing_kind_or_iso",
        "invalid_operator_or_expression",
        "syntax_error",
        "empty_or_no_program",
        "line_truncation",
        "compile_failed_no_stderr",
        "compile_other",
    ]

    primary = "compile_other"
    for p in priority:
        if p in labels:
            primary = p
            break

    return sorted(set(labels)), primary


def compile_code(model_key, task_id, code):
    model_dir = WORK_DIR / safe_name(model_key)
    model_dir.mkdir(parents=True, exist_ok=True)

    src = model_dir / f"task_{task_id}.f90"
    exe = model_dir / f"task_{task_id}.exe"
    stdout_file = model_dir / f"task_{task_id}.compile.stdout.txt"
    stderr_file = model_dir / f"task_{task_id}.compile.stderr.txt"

    src.write_text(code or "", encoding="utf-8")

    cmd = [GFORTRAN, *COMPILE_FLAGS, str(src), "-o", str(exe)]

    try:
        p = subprocess.run(
            cmd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=TIMEOUT,
        )
        stdout = p.stdout
        stderr = p.stderr
        returncode = p.returncode
        timeout = False
    except subprocess.TimeoutExpired as e:
        stdout = e.stdout or ""
        stderr = e.stderr or ""
        returncode = -999
        timeout = True

    stdout_file.write_text(stdout or "", encoding="utf-8")
    stderr_file.write_text(stderr or "", encoding="utf-8")

    labels, primary = classify_gfortran(stderr, returncode)

    return {
        "source_file": str(src),
        "exe_file": str(exe),
        "compile_cmd": " ".join(cmd),
        "compile_returncode": returncode,
        "compile_timeout": timeout,
        "compile_stdout": stdout,
        "compile_stderr": stderr,
        "compile_labels": labels,
        "compile_primary": primary,
        "compiled_ok": returncode == 0,
    }


def main():
    if not IN_FILE.exists():
        raise SystemExit(f"Missing input file: {IN_FILE}")

    print("=" * 100)
    print("REAL GFORTRAN COMPILE DIAGNOSIS FOR base_ok_ft_fail")
    print("=" * 100)
    print("Input:", IN_FILE)
    print("gfortran:", GFORTRAN)
    print("flags:", " ".join(COMPILE_FLAGS))
    print("output:", OUT_DIR)

    data = load_json(IN_FILE)

    rows = []
    summary = {}

    for i, case in enumerate(data, 1):
        model = case.get("model_key", "UNKNOWN")
        task_id = str(case.get("task_id", i))
        ft_status = case.get("ft_status", "")
        base_status = case.get("base_status", "")
        code = case.get("ft_code", "") or ""

        result = compile_code(model, task_id, code)

        row = {
            "model_key": model,
            "task_id": task_id,
            "base_status": base_status,
            "ft_status": ft_status,
            "prompt": case.get("prompt", ""),
            "ft_code": code,
            **result,
        }
        rows.append(row)

        if i % 50 == 0:
            print(f"processed {i}/{len(data)}")

    # summaries
    by_model = defaultdict(list)
    for r in rows:
        by_model[r["model_key"]].append(r)

    for model, items in by_model.items():
        status_counter = Counter(r["ft_status"] for r in items)
        compile_primary_counter = Counter(r["compile_primary"] for r in items)
        compile_label_counter = Counter()
        compiled_ok = 0

        for r in items:
            if r["compiled_ok"]:
                compiled_ok += 1
            for lab in r["compile_labels"]:
                compile_label_counter[lab] += 1

        summary[model] = {
            "num_cases": len(items),
            "compiled_ok": compiled_ok,
            "compiled_failed": len(items) - compiled_ok,
            "ft_status_counts": dict(status_counter.most_common()),
            "compile_primary_counts": dict(compile_primary_counter.most_common()),
            "compile_label_counts": dict(compile_label_counter.most_common()),
        }

    # write JSON
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)

    with open(OUT_SUMMARY_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    # write CSV
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        fields = [
            "model_key",
            "task_id",
            "base_status",
            "ft_status",
            "compiled_ok",
            "compile_returncode",
            "compile_primary",
            "compile_labels",
            "compile_stderr_head",
            "source_file",
        ]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({
                "model_key": r["model_key"],
                "task_id": r["task_id"],
                "base_status": r["base_status"],
                "ft_status": r["ft_status"],
                "compiled_ok": r["compiled_ok"],
                "compile_returncode": r["compile_returncode"],
                "compile_primary": r["compile_primary"],
                "compile_labels": "|".join(r["compile_labels"]),
                "compile_stderr_head": short(r["compile_stderr"], 1000).replace("\n", "\\n"),
                "source_file": r["source_file"],
            })

    with open(OUT_SUMMARY_CSV, "w", newline="", encoding="utf-8") as f:
        fields = [
            "model_key",
            "num_cases",
            "compiled_ok",
            "compiled_failed",
            "top_ft_status",
            "top_compile_primary",
        ]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for model, s in sorted(summary.items(), key=lambda kv: kv[1]["compiled_failed"], reverse=True):
            top_status = next(iter(s["ft_status_counts"].items()), ("", ""))
            top_primary = next(iter(s["compile_primary_counts"].items()), ("", ""))
            w.writerow({
                "model_key": model,
                "num_cases": s["num_cases"],
                "compiled_ok": s["compiled_ok"],
                "compiled_failed": s["compiled_failed"],
                "top_ft_status": f"{top_status[0]}:{top_status[1]}",
                "top_compile_primary": f"{top_primary[0]}:{top_primary[1]}",
            })

    # global summary text
    global_primary = Counter()
    global_labels = Counter()
    global_ft_status = Counter()
    global_ok = 0

    for r in rows:
        global_primary[r["compile_primary"]] += 1
        global_ft_status[r["ft_status"]] += 1
        if r["compiled_ok"]:
            global_ok += 1
        for lab in r["compile_labels"]:
            global_labels[lab] += 1

    lines = []
    lines.append("=" * 100)
    lines.append("GLOBAL REAL COMPILE SUMMARY")
    lines.append("=" * 100)
    lines.append(f"total cases       : {len(rows)}")
    lines.append(f"compiled_ok       : {global_ok}")
    lines.append(f"compiled_failed   : {len(rows) - global_ok}")
    lines.append("")
    lines.append("FT status counts:")
    for k, v in global_ft_status.most_common():
        lines.append(f"  {k:40s} {v}")
    lines.append("")
    lines.append("Compile primary counts:")
    for k, v in global_primary.most_common():
        lines.append(f"  {k:40s} {v}")
    lines.append("")
    lines.append("Compile label counts:")
    for k, v in global_labels.most_common():
        lines.append(f"  {k:40s} {v}")

    OUT_GLOBAL_TXT.write_text("\n".join(lines), encoding="utf-8")

    print()
    print("\n".join(lines))
    print()
    print("Written:")
    print(" ", OUT_JSON)
    print(" ", OUT_CSV)
    print(" ", OUT_SUMMARY_JSON)
    print(" ", OUT_SUMMARY_CSV)
    print(" ", OUT_GLOBAL_TXT)


if __name__ == "__main__":
    main()
