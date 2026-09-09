#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import csv
import re
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(".")
COMPARE_DIR = Path("results/task_comparison_base_conc30_all_available")

BASE_DETAILS = Path("_base_reference/results/base_humaneval_mistral_conc30_evaluation_details.json")
BASE_SOLUTIONS = Path("_base_reference/results_qwen_lora/solutions/base_humaneval_mistral_conc30_solutions.json")
BENCHMARK = Path("../benchmark.json")

LOSSES_JSON = COMPARE_DIR / "base_ok_ft_fail_tasks.json"
OUT_DIR = Path("results/diagnosis_base_ok_ft_fail")
OUT_DIR.mkdir(parents=True, exist_ok=True)

CSV_OUT = OUT_DIR / "base_ok_ft_fail_diagnosis.csv"
JSON_OUT = OUT_DIR / "base_ok_ft_fail_diagnosis_full.json"
SUMMARY_OUT = OUT_DIR / "base_ok_ft_fail_diagnosis_summary.json"


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def safe_load(path, default=None):
    try:
        return load_json(path)
    except Exception:
        return default


def extract_items(obj):
    if isinstance(obj, list):
        return obj

    if isinstance(obj, dict):
        for key in ["details", "results", "items", "tasks", "evaluations"]:
            if isinstance(obj.get(key), list):
                return obj[key]

        if all(isinstance(v, dict) for v in obj.values()):
            return list(obj.values())

    return []


def task_id_of(item, fallback):
    if isinstance(item, dict):
        for key in ["task_id", "id", "task_index", "index", "problem_id"]:
            if key in item:
                return str(item[key])
        for key in ["name", "task_name"]:
            if key in item:
                return str(item[key])
    return str(fallback)


def status_of(item):
    if not isinstance(item, dict):
        return "unknown"

    for key in ["status", "result", "outcome", "verdict"]:
        v = item.get(key)
        if isinstance(v, str):
            return v

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
                v = sub.get(subkey)
                if isinstance(v, str):
                    return v

    return "unknown"


def build_map(details_file):
    data = load_json(details_file)
    items = extract_items(data)

    out = {}
    for i, item in enumerate(items):
        tid = task_id_of(item, i)
        out[tid] = item
    return out


def solution_map(solution_file):
    data = safe_load(solution_file, [])
    out = {}

    if not isinstance(data, list):
        return out

    for i, item in enumerate(data):
        if not isinstance(item, dict):
            continue

        tid = None
        for key in ["task_id", "id", "task_index", "index", "problem_id"]:
            if key in item:
                tid = str(item[key])
                break
        if tid is None:
            tid = str(i)

        out[tid] = item

    return out


def find_text(obj, keys):
    """
    Cherche récursivement un champ texte utile.
    """
    if isinstance(obj, dict):
        for k in keys:
            v = obj.get(k)
            if isinstance(v, str) and v.strip():
                return v
        for v in obj.values():
            found = find_text(v, keys)
            if found:
                return found
    elif isinstance(obj, list):
        for v in obj:
            found = find_text(v, keys)
            if found:
                return found
    return ""


def stringify_short(x, limit=1200):
    try:
        s = json.dumps(x, ensure_ascii=False)
    except Exception:
        s = str(x)
    s = s.replace("\n", "\\n")
    return s[:limit]


def extract_code(solution_item, detail_item):
    for source in [solution_item, detail_item]:
        if not isinstance(source, dict):
            continue

        for key in ["code", "extracted_code", "generated_code", "solution", "program"]:
            v = source.get(key)
            if isinstance(v, str) and v.strip():
                return v

        # parfois code dans nested
        nested = find_text(source, ["code", "extracted_code", "generated_code"])
        if nested:
            return nested

    return ""


def get_benchmark_prompt_map():
    bench = safe_load(BENCHMARK, [])
    out = {}

    if isinstance(bench, list):
        for i, item in enumerate(bench):
            out[str(i)] = item
            if isinstance(item, dict):
                for k in ["task_id", "id"]:
                    if k in item:
                        out[str(item[k])] = item

    return out


def detect_patterns(status, code, raw_detail):
    text_raw = stringify_short(raw_detail, 5000).lower()
    code_l = (code or "").lower()

    flags = []

    # Source-level patterns
    if re.search(r"\bread\s*\(\s*\*\s*,", code_l) or re.search(r"\bread\s*\(\s*5\s*,", code_l):
        flags.append("uses_stdin_read")

    if re.search(r'write\s*\([^)]*\)\s*["\']', code_l) or re.search(r'print\s*\*\s*,\s*["\']', code_l):
        flags.append("extra_text_in_output_possible")

    if "contains" in code_l:
        flags.append("uses_contains")

    if re.search(r"\breal\s*\*8\b", code_l) or re.search(r"\bcomplex\s*\*16\b", code_l):
        flags.append("legacy_real_complex")

    if re.search(r"::\s*\w+\s*\(\s*:\s*\)", code_l) and "allocatable" not in code_l:
        flags.append("deferred_shape_without_allocatable_possible")

    if "allocate(" in code_l and "allocatable" not in code_l:
        flags.append("allocate_without_allocatable_possible")

    if ".true." in code_l or ".false." in code_l:
        flags.append("fortran_logical_output_possible")

    # Error stderr / evaluator patterns
    if "end of file" in text_raw or "eof" in text_raw or "read past end" in text_raw:
        flags.append("runtime_eof_stdin")

    if "syntax error" in text_raw:
        flags.append("compile_syntax_error")

    if "no implicit type" in text_raw or "has no implicit type" in text_raw or "n'a pas de type implicit" in text_raw:
        flags.append("compile_implicit_decl")

    if "cannot have a deferred shape" in text_raw:
        flags.append("compile_deferred_shape")

    if "must be allocatable or a pointer" in text_raw or "allocate-object" in text_raw:
        flags.append("compile_allocatable_issue")

    if "unexpected" in text_raw and "contains" in text_raw:
        flags.append("compile_bad_contains_structure")

    if "type mismatch" in text_raw:
        flags.append("compile_type_mismatch")

    if "rank mismatch" in text_raw:
        flags.append("compile_rank_mismatch")

    if "expected" in text_raw and "end" in text_raw:
        flags.append("compile_expected_end")

    if "timeout" in text_raw:
        flags.append("runtime_timeout")

    if "segmentation fault" in text_raw or "sigsegv" in text_raw:
        flags.append("runtime_segfault")

    if status == "ineq":
        flags.append("output_mismatch")
        if "expected" in text_raw and ("stdout" in text_raw or "output" in text_raw):
            flags.append("output_mismatch_expected_vs_stdout")

    if status == "exception":
        flags.append("evaluator_exception")

    if not flags:
        flags.append("unclassified")

    return sorted(set(flags))


def primary_category(status, flags):
    flags = set(flags)

    if status == "compile_err":
        if "compile_deferred_shape" in flags or "compile_allocatable_issue" in flags:
            return "compile_array_allocation"
        if "compile_bad_contains_structure" in flags:
            return "compile_contains_structure"
        if "compile_implicit_decl" in flags:
            return "compile_implicit_decl"
        if "compile_syntax_error" in flags:
            return "compile_syntax"
        if "compile_type_mismatch" in flags:
            return "compile_type_mismatch"
        if "compile_rank_mismatch" in flags:
            return "compile_rank_mismatch"
        return "compile_other"

    if status == "runtime_err":
        if "runtime_eof_stdin" in flags or "uses_stdin_read" in flags:
            return "runtime_stdin_eof_or_io"
        if "runtime_timeout" in flags:
            return "runtime_timeout"
        if "runtime_segfault" in flags:
            return "runtime_segfault"
        return "runtime_other"

    if status == "ineq":
        if "extra_text_in_output_possible" in flags:
            return "ineq_extra_text_or_format"
        if "fortran_logical_output_possible" in flags:
            return "ineq_logical_format"
        return "ineq_wrong_value_or_format"

    if status == "exception":
        return "evaluator_exception"

    return "other"


def find_details_file(model_key):
    matches = list(Path(".").glob(f"**/{model_key}_evaluation_details.json"))
    matches = [p for p in matches if "_base_reference" not in str(p)]
    return sorted(matches)[0] if matches else None


def find_solution_file(model_key):
    matches = list(Path(".").glob(f"**/{model_key}_solutions.json"))
    matches = [p for p in matches if "_base_reference" not in str(p)]
    return sorted(matches)[0] if matches else None


def main():
    if not LOSSES_JSON.exists():
        raise SystemExit(f"Missing {LOSSES_JSON}")

    losses = load_json(LOSSES_JSON)
    base_details = build_map(BASE_DETAILS)
    base_solutions = solution_map(BASE_SOLUTIONS)
    bench_map = get_benchmark_prompt_map()

    rows = []
    full = []
    summary = {}

    for model_key, task_ids in losses.items():
        details_file = find_details_file(model_key)
        solution_file = find_solution_file(model_key)

        if not details_file:
            print("SKIP no details:", model_key)
            continue

        ft_details = build_map(details_file)
        ft_solutions = solution_map(solution_file) if solution_file else {}

        cat_counter = Counter()
        flag_counter = Counter()
        status_counter = Counter()

        for tid in task_ids:
            tid = str(tid)

            base_item = base_details.get(tid, {})
            ft_item = ft_details.get(tid, {})
            ft_status = status_of(ft_item)

            base_code = extract_code(base_solutions.get(tid, {}), base_item)
            ft_code = extract_code(ft_solutions.get(tid, {}), ft_item)

            flags = detect_patterns(ft_status, ft_code, ft_item)
            cat = primary_category(ft_status, flags)

            cat_counter[cat] += 1
            status_counter[ft_status] += 1
            for fl in flags:
                flag_counter[fl] += 1

            prompt_obj = bench_map.get(tid, {})
            prompt_short = stringify_short(prompt_obj, 1500)

            stderr_head = find_text(ft_item, [
                "stderr", "compile_stderr", "runtime_stderr",
                "error", "message", "traceback"
            ])[:1500]

            stdout_head = find_text(ft_item, [
                "stdout", "actual_output", "output", "got"
            ])[:700]

            expected_head = find_text(ft_item, [
                "expected", "expected_output", "target"
            ])[:700]

            row = {
                "model_key": model_key,
                "task_id": tid,
                "ft_status": ft_status,
                "primary_category": cat,
                "flags": "|".join(flags),
                "details_file": str(details_file),
                "solution_file": str(solution_file) if solution_file else "",
                "stderr_head": stderr_head.replace("\n", "\\n"),
                "stdout_head": stdout_head.replace("\n", "\\n"),
                "expected_head": expected_head.replace("\n", "\\n"),
                "prompt_head": prompt_short,
                "ft_code_head": (ft_code or "")[:1200].replace("\n", "\\n"),
            }
            rows.append(row)

            full.append({
                **row,
                "prompt": prompt_obj,
                "base_code": base_code,
                "ft_code": ft_code,
                "base_detail": base_item,
                "ft_detail": ft_item,
            })

        summary[model_key] = {
            "num_base_ok_ft_fail": len(task_ids),
            "ft_status_counts": dict(status_counter.most_common()),
            "primary_category_counts": dict(cat_counter.most_common()),
            "flag_counts": dict(flag_counter.most_common()),
            "details_file": str(details_file),
            "solution_file": str(solution_file) if solution_file else "",
        }

    fieldnames = [
        "model_key", "task_id", "ft_status", "primary_category", "flags",
        "details_file", "solution_file",
        "stderr_head", "stdout_head", "expected_head",
        "prompt_head", "ft_code_head"
    ]

    with open(CSV_OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    with open(JSON_OUT, "w", encoding="utf-8") as f:
        json.dump(full, f, indent=2, ensure_ascii=False)

    with open(SUMMARY_OUT, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print("=" * 100)
    print("BASE_OK_FT_FAIL DIAGNOSIS")
    print("=" * 100)

    for model, s in sorted(summary.items(), key=lambda kv: kv[1]["num_base_ok_ft_fail"], reverse=True):
        print()
        print(model)
        print("losses:", s["num_base_ok_ft_fail"])
        print("status:", s["ft_status_counts"])
        print("categories:", s["primary_category_counts"])
        print("top flags:", dict(list(s["flag_counts"].items())[:10]))

    print()
    print("Written:")
    print(" ", CSV_OUT)
    print(" ", JSON_OUT)
    print(" ", SUMMARY_OUT)


if __name__ == "__main__":
    main()
