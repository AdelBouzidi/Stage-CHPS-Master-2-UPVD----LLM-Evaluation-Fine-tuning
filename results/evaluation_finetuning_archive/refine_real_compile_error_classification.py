#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import csv
import re
from pathlib import Path
from collections import Counter, defaultdict

IN_JSON = Path("results/real_compile_diagnosis_base_ok_ft_fail/real_compile_cases.json")

OUT_DIR = Path("results/refined_real_compile_error_classification")
OUT_DIR.mkdir(parents=True, exist_ok=True)

OUT_CASES_JSON = OUT_DIR / "refined_cases.json"
OUT_CASES_CSV = OUT_DIR / "refined_cases.csv"
OUT_SUMMARY_JSON = OUT_DIR / "refined_summary_by_model.json"
OUT_SUMMARY_CSV = OUT_DIR / "refined_summary_by_model.csv"
OUT_GLOBAL_TXT = OUT_DIR / "refined_global_summary.txt"
OUT_EXAMPLES_MD = OUT_DIR / "refined_error_examples.md"


def load_json(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def short(s, n=1400):
    if s is None:
        return ""
    s = str(s)
    return s if len(s) <= n else s[:n] + "\n...[TRUNCATED]..."


def one_line(s, n=900):
    return short(s, n).replace("\n", "\\n")


def has(pattern, text):
    return re.search(pattern, text, flags=re.I | re.M) is not None


def classify_compile_or_eval(row):
    """
    Classification propre :
    - si compiled_ok=True : ce n'est pas une erreur de compilation.
      On classe selon ft_status : wrong_answer, runtime, exception.
    - si compiled_ok=False : on classe selon le vrai stderr gfortran.
    """

    compiled_ok = bool(row.get("compiled_ok"))
    ft_status = str(row.get("ft_status", "unknown"))
    stderr = row.get("compile_stderr", "") or ""
    code = row.get("ft_code", "") or ""

    t = stderr.lower()
    c = code.lower()

    labels = []

    # ------------------------------------------------------------------
    # 1) Cas où le code compile : l'erreur vient de l'exécution/output
    # ------------------------------------------------------------------
    if compiled_ok:
        if ft_status == "ineq":
            return "compiled_but_wrong_answer", ["compiled_ok", "wrong_answer_or_output_mismatch"]
        if ft_status == "runtime_err":
            return "compiled_but_runtime_error", ["compiled_ok", "runtime_error_after_compile"]
        if ft_status == "exception":
            return "compiled_but_evaluator_exception", ["compiled_ok", "evaluator_exception_after_compile"]
        return "compiled_ok_other_failure", ["compiled_ok", f"ft_status_{ft_status}"]

    # ------------------------------------------------------------------
    # 2) Erreurs de compilation réelles
    # ------------------------------------------------------------------

    # Code vide / pas de main
    if (
        "undefined reference to `main'" in t
        or "undefined reference to 'main'" in t
        or "unexpected end of file" in t and len(code.strip()) < 50
        or len(code.strip()) == 0
    ):
        return "empty_code_or_no_program", ["compile_failed", "empty_or_no_main"]

    # Erreur très spécifique : print(*,*) au lieu de print *, ...
    # gfortran donne souvent "Syntax error in PRINT statement".
    if "syntax error in print statement" in t:
        if "print(*,*)" in c or "print (*,*)" in c or re.search(r"\bprint\s*\(\s*\*\s*,\s*\*\s*\)", c):
            return "print_parentheses_syntax", ["compile_failed", "print_parentheses_syntax"]
        return "print_statement_syntax", ["compile_failed", "print_statement_syntax"]

    # C-like signatures réelles : int x, float[] arr, etc.
    if (
        "unexpected junk in formal argument list" in t
        or has(r"\b(subroutine|function)\s+\w+\s*\(\s*(int|float|double|char)\s+\w+", c)
        or has(r"\b(float|int|double)\s*\[\s*\]", c)
    ):
        return "c_like_procedure_signature", ["compile_failed", "c_like_procedure_signature"]

    # INTENT(IN) modifié
    if (
        "intent(in)" in t
        or "dummy argument" in t and "variable definition context" in t
    ):
        return "intent_in_modified", ["compile_failed", "intent_in_modified"]

    # character(len=*) local invalide
    if (
        "assumed character length" in t
        or "must be a dummy argument or a parameter" in t
        or has(r"character\s*\(\s*len\s*=\s*\*\s*\)\s*::", c)
    ):
        return "assumed_length_character_local", ["compile_failed", "assumed_length_character_local"]

    # Déclarations après instructions exécutables / déclarations dans if/do
    if (
        "unexpected data declaration statement" in t
        or "unexpected attribute declaration statement" in t
        or "data declaration statement" in t
    ):
        return "declaration_after_executable", ["compile_failed", "declaration_after_executable"]

    # Variables non déclarées
    if "has no implicit type" in t or "no implicit type" in t:
        # sous-cas pour real32/real64/int32/int64
        if any(x in t for x in ["real32", "real64", "int32", "int64"]):
            return "missing_iso_fortran_env_kind", ["compile_failed", "implicit_declaration", "missing_iso_fortran_env_kind"]
        return "undeclared_variable", ["compile_failed", "implicit_declaration"]

    # mauvais opérateur / expression invalide, ex: (a*b) mod p
    if (
        "unclassifiable statement" in t
        or "syntax error in expression" in t
        or "expected a right parenthesis" in t
        or has(r"\)\s*mod\s+\w+", c)
        or has(r"\bmod\s+\w+", c)
    ):
        return "invalid_operator_or_expression", ["compile_failed", "invalid_operator_or_expression"]

    # Type mismatch / mauvais intrinsics
    if "type mismatch" in t or "cannot convert" in t or "argument" in t and "type" in t and "mismatch" in t:
        return "type_mismatch_or_intrinsic_misuse", ["compile_failed", "type_mismatch_or_intrinsic_misuse"]

    # Rank mismatch
    if "rank mismatch" in t:
        return "rank_mismatch", ["compile_failed", "rank_mismatch"]

    # allocatable / shape / allocate
    if (
        "allocatable scalar" in t
        or "shape specification" in t
        or "allocate-object" in t
        or "must be allocatable" in t
        or "already allocated" in t
    ):
        return "allocatable_or_shape_error", ["compile_failed", "allocatable_or_shape_error"]

    # interface explicite assumed-shape
    if "explicit interface required" in t or "assumed-shape" in t:
        return "explicit_interface_required", ["compile_failed", "explicit_interface_required"]

    # contains / structure de programme
    if (
        "unexpected contains statement" in t
        or "two main programs" in t
        or "expecting end program statement" in t
        or "expecting end subroutine statement" in t
        or "expecting end function statement" in t
    ):
        return "bad_contains_or_program_structure", ["compile_failed", "bad_contains_or_program_structure"]

    # ligne trop longue
    if "line truncated" in t:
        return "line_truncation", ["compile_failed", "line_truncation"]

    # fallback syntax générale
    if "syntax error" in t:
        return "syntax_error_other", ["compile_failed", "syntax_error_other"]

    return "compile_other", ["compile_failed", "compile_other"]


def main():
    if not IN_JSON.exists():
        raise SystemExit(f"Missing input: {IN_JSON}")

    rows = load_json(IN_JSON)

    refined = []
    global_counter = Counter()
    global_label_counter = Counter()
    by_model = defaultdict(list)

    for r in rows:
        primary, labels = classify_compile_or_eval(r)

        rr = dict(r)
        rr["refined_primary"] = primary
        rr["refined_labels"] = labels

        refined.append(rr)
        global_counter[primary] += 1
        for lab in labels:
            global_label_counter[lab] += 1
        by_model[rr.get("model_key", "UNKNOWN")].append(rr)

    # ------------------------------------------------------------------
    # summary by model
    # ------------------------------------------------------------------
    summary = {}

    for model, items in by_model.items():
        prim = Counter(x["refined_primary"] for x in items)
        status = Counter(x.get("ft_status", "unknown") for x in items)
        labels = Counter()
        compiled_ok = sum(1 for x in items if x.get("compiled_ok") is True)
        compiled_failed = len(items) - compiled_ok

        for x in items:
            for lab in x["refined_labels"]:
                labels[lab] += 1

        summary[model] = {
            "num_cases": len(items),
            "compiled_ok": compiled_ok,
            "compiled_failed": compiled_failed,
            "ft_status_counts": dict(status.most_common()),
            "refined_primary_counts": dict(prim.most_common()),
            "refined_label_counts": dict(labels.most_common()),
        }

    # ------------------------------------------------------------------
    # write JSON
    # ------------------------------------------------------------------
    with open(OUT_CASES_JSON, "w", encoding="utf-8") as f:
        json.dump(refined, f, indent=2, ensure_ascii=False)

    with open(OUT_SUMMARY_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    # ------------------------------------------------------------------
    # write CSV cases
    # ------------------------------------------------------------------
    with open(OUT_CASES_CSV, "w", newline="", encoding="utf-8") as f:
        fields = [
            "model_key",
            "task_id",
            "base_status",
            "ft_status",
            "compiled_ok",
            "refined_primary",
            "refined_labels",
            "compile_primary_old",
            "compile_stderr_head",
            "source_file",
        ]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()

        for r in refined:
            w.writerow({
                "model_key": r.get("model_key", ""),
                "task_id": r.get("task_id", ""),
                "base_status": r.get("base_status", ""),
                "ft_status": r.get("ft_status", ""),
                "compiled_ok": r.get("compiled_ok", ""),
                "refined_primary": r.get("refined_primary", ""),
                "refined_labels": "|".join(r.get("refined_labels", [])),
                "compile_primary_old": r.get("compile_primary", ""),
                "compile_stderr_head": one_line(r.get("compile_stderr", ""), 1200),
                "source_file": r.get("source_file", ""),
            })

    # ------------------------------------------------------------------
    # write CSV summary
    # ------------------------------------------------------------------
    with open(OUT_SUMMARY_CSV, "w", newline="", encoding="utf-8") as f:
        fields = [
            "model_key",
            "num_cases",
            "compiled_ok",
            "compiled_failed",
            "top_ft_status",
            "top_refined_primary",
            "refined_primary_counts",
        ]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()

        for model, s in sorted(summary.items(), key=lambda kv: kv[1]["num_cases"], reverse=True):
            top_status = next(iter(s["ft_status_counts"].items()), ("", ""))
            top_primary = next(iter(s["refined_primary_counts"].items()), ("", ""))

            w.writerow({
                "model_key": model,
                "num_cases": s["num_cases"],
                "compiled_ok": s["compiled_ok"],
                "compiled_failed": s["compiled_failed"],
                "top_ft_status": f"{top_status[0]}:{top_status[1]}",
                "top_refined_primary": f"{top_primary[0]}:{top_primary[1]}",
                "refined_primary_counts": json.dumps(s["refined_primary_counts"], ensure_ascii=False),
            })

    # ------------------------------------------------------------------
    # global txt
    # ------------------------------------------------------------------
    lines = []
    lines.append("=" * 100)
    lines.append("REFINED REAL COMPILE / EVAL FAILURE CLASSIFICATION")
    lines.append("=" * 100)
    lines.append(f"total cases: {len(refined)}")
    lines.append("")
    lines.append("Refined primary counts:")
    for k, v in global_counter.most_common():
        lines.append(f"  {k:45s} {v}")
    lines.append("")
    lines.append("Refined label counts:")
    for k, v in global_label_counter.most_common():
        lines.append(f"  {k:45s} {v}")

    OUT_GLOBAL_TXT.write_text("\n".join(lines), encoding="utf-8")

    # ------------------------------------------------------------------
    # examples markdown
    # ------------------------------------------------------------------
    with open(OUT_EXAMPLES_MD, "w", encoding="utf-8") as f:
        f.write("# Refined error examples\n\n")

        for category, _ in global_counter.most_common():
            f.write(f"\n## {category}\n\n")
            examples = [r for r in refined if r["refined_primary"] == category][:5]

            for r in examples:
                f.write(f"### {r.get('model_key')} / task {r.get('task_id')}\n\n")
                f.write(f"- ft_status: `{r.get('ft_status')}`\n")
                f.write(f"- compiled_ok: `{r.get('compiled_ok')}`\n")
                f.write(f"- old compile_primary: `{r.get('compile_primary')}`\n\n")
                f.write("```text\n")
                f.write(short(r.get("compile_stderr", ""), 1600))
                f.write("\n```\n\n")

    print(OUT_GLOBAL_TXT.read_text(encoding="utf-8"))
    print()
    print("Written:")
    print(" ", OUT_CASES_JSON)
    print(" ", OUT_CASES_CSV)
    print(" ", OUT_SUMMARY_JSON)
    print(" ", OUT_SUMMARY_CSV)
    print(" ", OUT_GLOBAL_TXT)
    print(" ", OUT_EXAMPLES_MD)


if __name__ == "__main__":
    main()
