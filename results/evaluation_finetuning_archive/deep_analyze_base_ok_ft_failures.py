#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import csv
import re
import difflib
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(".")
BENCHMARK = Path("../benchmark.json")

BASE_DETAILS = Path("_base_reference/results/base_humaneval_mistral_conc30_evaluation_details.json")
BASE_LOGS = Path("_base_reference/results/base_humaneval_mistral_conc30_evaluation_logs.json")
BASE_SOLUTIONS = Path("_base_reference/results_qwen_lora/solutions/base_humaneval_mistral_conc30_solutions.json")

COMPARE_DIR = Path("results/task_comparison_base_conc30_all_available")
LOSSES_JSON = COMPARE_DIR / "base_ok_ft_fail_tasks.json"

OUT_DIR = Path("results/deep_failure_analysis_base_ok_ft_fail")
OUT_DIR.mkdir(parents=True, exist_ok=True)
PER_MODEL_DIR = OUT_DIR / "per_model"
PER_MODEL_DIR.mkdir(parents=True, exist_ok=True)

OUT_CASES_CSV = OUT_DIR / "failure_cases.csv"
OUT_CASES_JSON = OUT_DIR / "failure_cases_full.json"
OUT_SUMMARY_CSV = OUT_DIR / "summary_by_model.csv"
OUT_SUMMARY_JSON = OUT_DIR / "summary_by_model.json"


# ======================================================================================
# Generic JSON helpers
# ======================================================================================

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def safe_load_json(path, default=None):
    try:
        return load_json(path)
    except Exception:
        return default

def short(s, n=2000):
    if s is None:
        return ""
    s = str(s)
    return s if len(s) <= n else s[:n] + "\n...[TRUNCATED]..."

def flatten_text(obj, limit=10000):
    try:
        s = json.dumps(obj, ensure_ascii=False, indent=2)
    except Exception:
        s = str(obj)
    return s[:limit]


# ======================================================================================
# Format adapters
# ======================================================================================

def extract_items(obj):
    if isinstance(obj, list):
        return obj

    if isinstance(obj, dict):
        for key in ["details", "results", "items", "tasks", "evaluations"]:
            if isinstance(obj.get(key), list):
                return obj[key]

        # Sometimes dict is task_id -> detail.
        if obj and all(isinstance(v, dict) for v in obj.values()):
            return list(obj.values())

    return []

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

    # Fallback: infer from known fields.
    text = flatten_text(item, 5000).lower()
    if "compile_err" in text or "compilation" in text and "error" in text:
        return "compile_err"
    if "runtime_err" in text or "runtime error" in text:
        return "runtime_err"
    if "ineq" in text or "mismatch" in text or "wrong answer" in text:
        return "ineq"

    return "unknown"

def build_map_from_details(path):
    obj = safe_load_json(path, [])
    items = extract_items(obj)
    out = {}
    for i, item in enumerate(items):
        tid = get_task_id(item, i)
        out[str(tid)] = item
    return out

def build_map_from_solutions(path):
    obj = safe_load_json(path, [])
    out = {}
    if not isinstance(obj, list):
        return out

    for i, item in enumerate(obj):
        if not isinstance(item, dict):
            continue
        tid = get_task_id(item, i)
        out[str(tid)] = item

    return out

def build_benchmark_map(path):
    obj = safe_load_json(path, [])
    out = {}
    if isinstance(obj, list):
        for i, item in enumerate(obj):
            out[str(i)] = item
            if isinstance(item, dict):
                for k in ["task_id", "id", "name"]:
                    if k in item:
                        out[str(item[k])] = item
    elif isinstance(obj, dict):
        for k, v in obj.items():
            out[str(k)] = v
    return out


# ======================================================================================
# Field extraction
# ======================================================================================

def find_text_rec(obj, preferred_keys):
    if isinstance(obj, dict):
        for k in preferred_keys:
            v = obj.get(k)
            if isinstance(v, str) and v.strip():
                return v

        for v in obj.values():
            found = find_text_rec(v, preferred_keys)
            if found:
                return found

    elif isinstance(obj, list):
        for v in obj:
            found = find_text_rec(v, preferred_keys)
            if found:
                return found

    return ""

def extract_code(solution_item, detail_item):
    for source in [solution_item, detail_item]:
        if not isinstance(source, dict):
            continue

        for key in [
            "code",
            "extracted_code",
            "generated_code",
            "program",
            "solution",
            "completion",
            "response",
        ]:
            v = source.get(key)
            if isinstance(v, str) and v.strip():
                return v

        nested = find_text_rec(source, ["code", "extracted_code", "generated_code"])
        if nested:
            return nested

    return ""

def extract_stderr(detail_item):
    return find_text_rec(detail_item, [
        "stderr",
        "compile_stderr",
        "compiler_output",
        "hidden_compiler_output",
        "runtime_stderr",
        "runtime_error",
        "hidden_runtime_error",
        "error",
        "traceback",
        "message",
    ])

def extract_stdout(detail_item):
    return find_text_rec(detail_item, [
        "stdout",
        "actual_output",
        "actual",
        "got",
        "program_output",
        "run_stdout",
    ])

def extract_expected(detail_item):
    return find_text_rec(detail_item, [
        "expected",
        "expected_output",
        "target_output",
        "reference_output",
    ])

def extract_prompt(benchmark_item):
    if not isinstance(benchmark_item, dict):
        return str(benchmark_item)

    for key in ["prompt", "instruction", "task", "description", "text"]:
        v = benchmark_item.get(key)
        if isinstance(v, str) and v.strip():
            return v

    return flatten_text(benchmark_item, 3000)


# ======================================================================================
# Static code analysis
# ======================================================================================

def static_features(code):
    c = code or ""
    low = c.lower()

    lines = c.splitlines()
    nonempty_lines = [x for x in lines if x.strip()]

    features = {}

    features["num_lines"] = len(lines)
    features["num_nonempty_lines"] = len(nonempty_lines)
    features["has_program"] = bool(re.search(r"^\s*program\s+\w+", low, re.M))
    features["has_contains"] = "contains" in low
    features["num_subroutines"] = len(re.findall(r"^\s*subroutine\s+\w+", low, re.M))
    features["num_functions"] = len(re.findall(r"^\s*(?:\w+\s+)?function\s+\w+", low, re.M))
    features["uses_module"] = bool(re.search(r"^\s*use\s+\w+", low, re.M))
    features["uses_iso_fortran_env"] = "iso_fortran_env" in low
    features["uses_implicit_none"] = "implicit none" in low
    features["uses_read_stdin"] = bool(re.search(r"\bread\s*\(\s*\*\s*,", low) or re.search(r"\bread\s*\(\s*,", low))
    features["uses_print_star"] = bool(re.search(r"\bprint\s*\*", low))
    features["uses_write_star"] = bool(re.search(r"\bwrite\s*\(\s*\*\s*,", low))
    features["has_labels_in_output"] = bool(
        re.search(r"(print\s*\*|write\s*\([^)]*\))\s*,?\s*['\"][^'\"]*[a-zA-Z][^'\"]*['\"]", low)
    )
    features["has_timestamp"] = "timestamp" in low or "date_and_time" in low
    features["has_debug_words"] = any(w in low for w in [
        "normal end", "demo", "demonstration", "test:", "initialized values",
        "finalization", "result ", "error in", "called from"
    ])
    features["uses_hardcoded_arrays"] = bool(re.search(r"=\s*\[", c) or re.search(r"=\s*\(/\s*", c))
    features["uses_hardcoded_scalars"] = bool(re.search(r"^\s*\w+\s*=\s*[-+0-9.'\"]", c, re.M))
    features["uses_allocatable"] = "allocatable" in low
    features["uses_allocate"] = "allocate(" in low
    features["possible_allocate_without_allocatable"] = features["uses_allocate"] and not features["uses_allocatable"]
    features["uses_assumed_shape"] = bool(re.search(r"::\s*\w+\s*\(\s*:\s*\)", low))
    features["uses_assumed_size"] = bool(re.search(r"::\s*\w+\s*\(\s*\*\s*\)", low))
    features["uses_index_0_loop"] = bool(re.search(r"\bdo\s+\w+\s*=\s*0\s*,", low))
    features["uses_array_index_0_literal"] = bool(re.search(r"\w+\s*\(\s*0\s*\)", low))
    features["uses_c_like_signature"] = bool(re.search(r"\b(subroutine|function)\s+\w+\s*\(\s*(int|float|double|char)\s+\w+", low))
    features["modifies_intent_in_possible"] = False

    # Very rough detection: find intent(in) variable names and assignments to them.
    intent_in_vars = set()
    for m in re.finditer(r"::\s*([a-zA-Z_][a-zA-Z0-9_,\s]*)", c):
        before = c[max(0, m.start()-120):m.start()].lower()
        if "intent(in)" in before and "intent(inout)" not in before:
            vars_part = m.group(1)
            for v in re.split(r"[,\s]+", vars_part):
                v = v.strip().lower()
                if v and re.match(r"^[a-zA-Z_]\w*$", v):
                    intent_in_vars.add(v)

    for v in intent_in_vars:
        if re.search(r"^\s*" + re.escape(v) + r"\s*=", low, re.M):
            features["modifies_intent_in_possible"] = True
            break

    return features

def feature_diff(base_features, ft_features):
    diffs = {}
    for k in sorted(set(base_features) | set(ft_features)):
        b = base_features.get(k)
        f = ft_features.get(k)
        if b != f:
            diffs[k] = {"base": b, "ft": f}
    return diffs


# ======================================================================================
# Error classification
# ======================================================================================

ERROR_RULES = [
    ("compile_c_like_signature", ["c-like", "c like"], []),
    ("compile_unexpected_end_or_missing_end", ["unexpected end of file", "expected end", "end program"], []),
    ("compile_syntax_error", ["syntax error"], []),
    ("compile_implicit_declaration", ["has no implicit type", "no implicit type", "symbol", "implicit"], []),
    ("compile_rank_mismatch", ["rank mismatch"], []),
    ("compile_allocatable_shape", ["allocatable scalar", "shape specification", "allocate-object", "must be allocatable"], []),
    ("compile_explicit_interface_required", ["explicit interface required", "assumed-shape"], []),
    ("compile_type_mismatch", ["type mismatch"], []),
    ("compile_kind_or_iso_missing", ["real32", "real64", "int32", "int64", "iso_fortran_env"], []),
    ("runtime_array_bounds", ["below lower bound", "above upper bound", "out of bounds", "index"], []),
    ("runtime_eof_or_stdin", ["end of file", "eof", "read past end"], []),
    ("runtime_division_or_nan", ["floating", "divide", "nan", "inf"], []),
    ("runtime_timeout", ["timeout"], []),
    ("runtime_segfault", ["segmentation fault", "sigsegv"], []),
    ("ineq_output_format", ["expected", "actual", "mismatch", "different"], []),
]

def classify_error(status, stderr, stdout, expected, ft_code, ft_features):
    text = " ".join([
        str(status or ""),
        str(stderr or ""),
        str(stdout or ""),
        str(expected or ""),
    ]).lower()

    labels = []

    if status:
        labels.append(f"status_{status}")

    for label, terms, _ in ERROR_RULES:
        if any(t in text for t in terms):
            labels.append(label)

    # Static-code-based labels.
    if ft_features.get("uses_c_like_signature"):
        labels.append("static_c_like_signature")
    if ft_features.get("uses_index_0_loop") or ft_features.get("uses_array_index_0_literal"):
        labels.append("static_possible_zero_indexing")
    if ft_features.get("possible_allocate_without_allocatable"):
        labels.append("static_allocate_without_allocatable")
    if ft_features.get("has_labels_in_output"):
        labels.append("static_output_labels")
    if ft_features.get("has_timestamp"):
        labels.append("static_timestamp_or_date")
    if ft_features.get("uses_read_stdin"):
        labels.append("static_stdin_read")
    if ft_features.get("uses_assumed_shape") and not ft_features.get("has_contains"):
        labels.append("static_assumed_shape_needs_interface")
    if ft_features.get("modifies_intent_in_possible"):
        labels.append("static_modifies_intent_in_possible")

    if not labels:
        labels.append("unclassified")

    # Primary cause heuristic.
    priority = [
        "compile_c_like_signature",
        "static_c_like_signature",
        "compile_explicit_interface_required",
        "static_assumed_shape_needs_interface",
        "compile_allocatable_shape",
        "static_allocate_without_allocatable",
        "compile_rank_mismatch",
        "compile_implicit_declaration",
        "compile_syntax_error",
        "compile_unexpected_end_or_missing_end",
        "runtime_array_bounds",
        "static_possible_zero_indexing",
        "runtime_eof_or_stdin",
        "static_stdin_read",
        "ineq_output_format",
        "static_output_labels",
        "static_timestamp_or_date",
        f"status_{status}",
    ]

    primary = "unclassified"
    for p in priority:
        if p in labels:
            primary = p
            break

    return sorted(set(labels)), primary


# ======================================================================================
# File discovery
# ======================================================================================

def find_details_file(model_key):
    matches = [p for p in Path(".").glob(f"**/{model_key}_evaluation_details.json") if "_base_reference" not in str(p)]
    return sorted(matches)[0] if matches else None

def find_logs_file(model_key):
    matches = [p for p in Path(".").glob(f"**/{model_key}_evaluation_logs.json") if "_base_reference" not in str(p)]
    return sorted(matches)[0] if matches else None

def find_solution_file(model_key):
    matches = [p for p in Path(".").glob(f"**/{model_key}_solutions.json") if "_base_reference" not in str(p)]
    return sorted(matches)[0] if matches else None


# ======================================================================================
# Markdown report
# ======================================================================================

def code_block(lang, text):
    return f"```{lang}\n{text}\n```\n"

def write_case_markdown(model_dir, case):
    task_id = case["task_id"]
    p = model_dir / f"task_{task_id}.md"

    diff_text = "\n".join(case["code_diff_unified"][:300])

    content = []
    content.append(f"# Failure case: {case['model_key']} / task {task_id}\n")
    content.append(f"- Base status: `{case['base_status']}`\n")
    content.append(f"- FT status: `{case['ft_status']}`\n")
    content.append(f"- Primary cause: `{case['primary_cause']}`\n")
    content.append(f"- Labels: `{', '.join(case['error_labels'])}`\n")
    content.append("\n## Prompt\n")
    content.append(code_block("text", short(case["prompt"], 4000)))

    content.append("\n## FT stderr / error\n")
    content.append(code_block("text", short(case["ft_stderr"], 4000)))

    content.append("\n## FT stdout\n")
    content.append(code_block("text", short(case["ft_stdout"], 2000)))

    content.append("\n## Expected output\n")
    content.append(code_block("text", short(case["expected"], 2000)))

    content.append("\n## Static feature differences base -> FT\n")
    content.append(code_block("json", json.dumps(case["feature_diff"], indent=2, ensure_ascii=False)))

    content.append("\n## Base generated code\n")
    content.append(code_block("fortran", short(case["base_code"], 8000)))

    content.append("\n## FT generated code\n")
    content.append(code_block("fortran", short(case["ft_code"], 8000)))

    content.append("\n## Unified diff base vs FT\n")
    content.append(code_block("diff", short(diff_text, 8000)))

    p.write_text("\n".join(content), encoding="utf-8")


# ======================================================================================
# Main
# ======================================================================================

def main():
    if not LOSSES_JSON.exists():
        raise SystemExit(f"Missing losses file: {LOSSES_JSON}. Run evaluate_and_compare_all_available_vs_base.py first.")

    losses = load_json(LOSSES_JSON)

    base_details = build_map_from_details(BASE_DETAILS)
    base_solutions = build_map_from_solutions(BASE_SOLUTIONS)
    benchmark = build_benchmark_map(BENCHMARK)

    cases = []
    summary = {}

    for model_key, task_ids in sorted(losses.items()):
        details_file = find_details_file(model_key)
        logs_file = find_logs_file(model_key)
        solution_file = find_solution_file(model_key)

        if not details_file:
            print("SKIP no details file:", model_key)
            continue

        ft_details = build_map_from_details(details_file)
        ft_solutions = build_map_from_solutions(solution_file) if solution_file else {}

        model_dir = PER_MODEL_DIR / model_key
        model_dir.mkdir(parents=True, exist_ok=True)

        status_counter = Counter()
        primary_counter = Counter()
        label_counter = Counter()
        static_counter = Counter()

        for task_id in task_ids:
            task_id = str(task_id)

            base_detail = base_details.get(task_id, {})
            ft_detail = ft_details.get(task_id, {})

            base_solution = base_solutions.get(task_id, {})
            ft_solution = ft_solutions.get(task_id, {})

            benchmark_item = benchmark.get(task_id, {})

            base_status = get_status(base_detail)
            ft_status = get_status(ft_detail)

            base_code = extract_code(base_solution, base_detail)
            ft_code = extract_code(ft_solution, ft_detail)

            prompt = extract_prompt(benchmark_item)

            ft_stderr = extract_stderr(ft_detail)
            ft_stdout = extract_stdout(ft_detail)
            expected = extract_expected(ft_detail)

            base_features = static_features(base_code)
            ft_features = static_features(ft_code)
            fdiff = feature_diff(base_features, ft_features)

            labels, primary = classify_error(
                ft_status, ft_stderr, ft_stdout, expected, ft_code, ft_features
            )

            diff = list(difflib.unified_diff(
                base_code.splitlines(),
                ft_code.splitlines(),
                fromfile="base_code",
                tofile="ft_code",
                lineterm=""
            ))

            case = {
                "model_key": model_key,
                "task_id": task_id,
                "details_file": str(details_file),
                "logs_file": str(logs_file) if logs_file else "",
                "solution_file": str(solution_file) if solution_file else "",
                "base_status": base_status,
                "ft_status": ft_status,
                "primary_cause": primary,
                "error_labels": labels,
                "prompt": prompt,
                "ft_stderr": ft_stderr,
                "ft_stdout": ft_stdout,
                "expected": expected,
                "base_code": base_code,
                "ft_code": ft_code,
                "base_features": base_features,
                "ft_features": ft_features,
                "feature_diff": fdiff,
                "code_diff_unified": diff,
            }

            cases.append(case)

            status_counter[ft_status] += 1
            primary_counter[primary] += 1
            for label in labels:
                label_counter[label] += 1
            for k, v in ft_features.items():
                if isinstance(v, bool) and v:
                    static_counter[k] += 1

            write_case_markdown(model_dir, case)

        summary[model_key] = {
            "num_base_ok_ft_fail": len(task_ids),
            "details_file": str(details_file),
            "solution_file": str(solution_file) if solution_file else "",
            "ft_status_counts": dict(status_counter.most_common()),
            "primary_cause_counts": dict(primary_counter.most_common()),
            "error_label_counts": dict(label_counter.most_common()),
            "static_feature_true_counts": dict(static_counter.most_common()),
        }

    # CSV cases
    with open(OUT_CASES_CSV, "w", newline="", encoding="utf-8") as f:
        fields = [
            "model_key",
            "task_id",
            "base_status",
            "ft_status",
            "primary_cause",
            "error_labels",
            "details_file",
            "solution_file",
            "ft_stderr_head",
            "ft_stdout_head",
            "expected_head",
            "prompt_head",
            "base_num_lines",
            "ft_num_lines",
            "ft_has_contains",
            "ft_uses_read_stdin",
            "ft_has_labels_in_output",
            "ft_has_timestamp",
            "ft_uses_index_0_loop",
            "ft_uses_c_like_signature",
            "ft_possible_allocate_without_allocatable",
            "ft_uses_assumed_shape",
            "ft_uses_assumed_size",
        ]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for c in cases:
            ff = c["ft_features"]
            w.writerow({
                "model_key": c["model_key"],
                "task_id": c["task_id"],
                "base_status": c["base_status"],
                "ft_status": c["ft_status"],
                "primary_cause": c["primary_cause"],
                "error_labels": "|".join(c["error_labels"]),
                "details_file": c["details_file"],
                "solution_file": c["solution_file"],
                "ft_stderr_head": short(c["ft_stderr"], 600).replace("\n", "\\n"),
                "ft_stdout_head": short(c["ft_stdout"], 400).replace("\n", "\\n"),
                "expected_head": short(c["expected"], 400).replace("\n", "\\n"),
                "prompt_head": short(c["prompt"], 500).replace("\n", "\\n"),
                "base_num_lines": c["base_features"].get("num_lines"),
                "ft_num_lines": ff.get("num_lines"),
                "ft_has_contains": ff.get("has_contains"),
                "ft_uses_read_stdin": ff.get("uses_read_stdin"),
                "ft_has_labels_in_output": ff.get("has_labels_in_output"),
                "ft_has_timestamp": ff.get("has_timestamp"),
                "ft_uses_index_0_loop": ff.get("uses_index_0_loop"),
                "ft_uses_c_like_signature": ff.get("uses_c_like_signature"),
                "ft_possible_allocate_without_allocatable": ff.get("possible_allocate_without_allocatable"),
                "ft_uses_assumed_shape": ff.get("uses_assumed_shape"),
                "ft_uses_assumed_size": ff.get("uses_assumed_size"),
            })

    # JSON full
    with open(OUT_CASES_JSON, "w", encoding="utf-8") as f:
        json.dump(cases, f, indent=2, ensure_ascii=False)

    with open(OUT_SUMMARY_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    # CSV summary
    with open(OUT_SUMMARY_CSV, "w", newline="", encoding="utf-8") as f:
        fields = [
            "model_key",
            "num_base_ok_ft_fail",
            "top_status",
            "top_primary_cause",
            "details_file",
            "solution_file",
        ]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for model, s in sorted(summary.items(), key=lambda kv: kv[1]["num_base_ok_ft_fail"], reverse=True):
            top_status = next(iter(s["ft_status_counts"].items()), ("", ""))
            top_primary = next(iter(s["primary_cause_counts"].items()), ("", ""))
            w.writerow({
                "model_key": model,
                "num_base_ok_ft_fail": s["num_base_ok_ft_fail"],
                "top_status": f"{top_status[0]}:{top_status[1]}",
                "top_primary_cause": f"{top_primary[0]}:{top_primary[1]}",
                "details_file": s["details_file"],
                "solution_file": s["solution_file"],
            })

    print("=" * 100)
    print("DEEP FAILURE ANALYSIS: BASE OK / FT FAIL")
    print("=" * 100)

    for model, s in sorted(summary.items(), key=lambda kv: kv[1]["num_base_ok_ft_fail"], reverse=True):
        print()
        print(model)
        print("  losses:", s["num_base_ok_ft_fail"])
        print("  ft statuses:", s["ft_status_counts"])
        print("  primary causes:", s["primary_cause_counts"])
        print("  top labels:", dict(list(s["error_label_counts"].items())[:10]))

    print()
    print("Written:")
    print(" ", OUT_SUMMARY_CSV)
    print(" ", OUT_SUMMARY_JSON)
    print(" ", OUT_CASES_CSV)
    print(" ", OUT_CASES_JSON)
    print(" ", PER_MODEL_DIR)


if __name__ == "__main__":
    main()
