#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter
import re

RESULTS_DIR = Path("results")

def load_json(p):
    return json.load(open(p, "r", encoding="utf-8"))

def simplify_compile_error(msg):
    msg = str(msg)

    patterns = [
        ("undeclared_symbol", r"has no IMPLICIT type"),
        ("cannot_open_module", r"Cannot open module file"),
        ("unexpected_statement", r"Unexpected .* statement"),
        ("expected_end", r"Expecting END"),
        ("syntax_error", r"Syntax error"),
        ("type_mismatch", r"Type mismatch"),
        ("rank_mismatch", r"Rank mismatch"),
        ("invalid_character", r"Invalid character"),
        ("already_defined", r"already has basic type|already defined"),
        ("no_such_file", r"No such file"),
    ]

    for name, pat in patterns:
        if re.search(pat, msg, re.IGNORECASE):
            return name

    return "other_compile_error"

for summary_path in sorted(RESULTS_DIR.glob("*_evaluation_details.json")):
    model = summary_path.name.replace("_evaluation_details.json", "")
    details = load_json(summary_path)

    compile_errors = [x for x in details if x.get("status") == "compile_err"]
    counter = Counter()

    for x in compile_errors:
        counter[simplify_compile_error(x.get("details", ""))] += 1

    print("="*100)
    print(model)
    print("compile_err total:", len(compile_errors))
    for k, v in counter.most_common():
        print(f"  {k}: {v}")

    print("\nExamples:")
    for x in compile_errors[:3]:
        print("-"*80)
        print("index:", x.get("index"), "task_id:", x.get("task_id"))
        print(str(x.get("details", ""))[:1000])