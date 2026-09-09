#!/usr/bin/env python3

from pathlib import Path
from collections import Counter, defaultdict
import csv
import difflib
import json
import re
import subprocess
import tempfile


SANDBOX = Path("/path/to/project/__sandbox_adel__LAST")
EVAL = SANDBOX / "evaluation_finetuning"

BASE = EVAL / "qwen27/base/results"
FT = EVAL / "qwen27/epoch1/learning_rate_1/results"

OUT = Path(
    "/path/to/project/results/"
    "04_task_analysis/qwen27_A_vs_base/exact_causes"
)
OUT.mkdir(parents=True, exist_ok=True)

TRANSITIONS = Path(
    "/path/to/project/results/"
    "04_task_analysis/qwen27_A_vs_base/"
    "QWEN27_BASE_VS_A_TASK_TRANSITIONS.csv"
)

BASE_DETAILS = BASE / (
    "base_qwen27_humaneval_mistral_conc12_"
    "evaluation_details.json"
)

BASE_LOGS = BASE / (
    "base_qwen27_humaneval_mistral_conc12_"
    "evaluation_logs.json"
)

A_DETAILS = FT / (
    "ft_A_qwen27_humaneval_mistral_conc12_"
    "evaluation_details.json"
)

A_LOGS = FT / (
    "ft_A_qwen27_humaneval_mistral_conc12_"
    "evaluation_logs.json"
)


# ============================================================
# BASIC HELPERS
# ============================================================

def load(p):
    with Path(p).open(encoding="utf-8", errors="replace") as f:
        return json.load(f)


def walk(obj, path=""):
    if isinstance(obj, dict):
        yield path, obj
        for k, v in obj.items():
            p = f"{path}.{k}" if path else str(k)
            yield from walk(v, p)

    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk(v, f"{path}[{i}]")


def get_tid(d):
    for k in [
        "task_id", "id", "task", "problem_id",
        "index", "task_idx", "problem_idx"
    ]:
        if k not in d:
            continue

        v = d[k]

        if isinstance(v, (str, int)):
            m = re.search(r"(\d+)$", str(v))
            if m:
                return int(m.group(1))

    return None


# ============================================================
# CODE EXTRACTION
# ============================================================

CODE_KEYS = [
    "code",
    "generated_code",
    "extracted_code",
    "solution",
    "fortran_code",
    "program",
    "response",
    "content",
    "completion",
    "answer",
]


def looks_like_fortran(s):
    if not isinstance(s, str):
        return False

    t = s.lower()

    score = sum([
        "program " in t,
        "implicit none" in t,
        "end program" in t,
        "subroutine " in t,
        "function " in t,
        "integer ::" in t,
        "real ::" in t,
        "read(" in t or "read *" in t,
        "print " in t or "write(" in t,
    ])

    return score >= 2


def strip_fences(s):
    s = s.strip()

    m = re.search(
        r"```(?:fortran|f90|fortran90)?\s*(.*?)```",
        s,
        flags=re.I | re.S
    )

    if m:
        return m.group(1).strip()

    return s


def build_task_objects(raw):
    out = defaultdict(list)

    for path, d in walk(raw):
        if not isinstance(d, dict):
            continue

        tid = get_tid(d)

        if tid is not None:
            out[tid].append((path, d))

    return out


def extract_code(task_objects):
    candidates = []

    for path, d in task_objects:
        for k in CODE_KEYS:
            v = d.get(k)

            if isinstance(v, str):
                vv = strip_fences(v)

                if looks_like_fortran(vv):
                    candidates.append(
                        (len(vv), f"{path}.{k}", vv)
                    )

        # inspect all string fields as fallback
        for k, v in d.items():
            if isinstance(v, str):
                vv = strip_fences(v)

                if looks_like_fortran(vv):
                    candidates.append(
                        (len(vv), f"{path}.{k}", vv)
                    )

    if not candidates:
        return "", ""

    candidates.sort(reverse=True)

    _, src, code = candidates[0]
    return code, src


# ============================================================
# COLLECT DIAGNOSTIC STRINGS
# ============================================================

DIAG_KEY_RE = re.compile(
    r"(error|stderr|stdout|message|exception|"
    r"compile|runtime|reason|trace|output|result)",
    re.I
)


def collect_diagnostics(task_objects):
    vals = []

    for path, d in task_objects:
        for k, v in d.items():
            if (
                isinstance(v, str)
                and v.strip()
                and DIAG_KEY_RE.search(k)
                and not looks_like_fortran(v)
            ):
                vals.append(
                    (f"{path}.{k}", v.strip())
                )

    # dedup
    seen = set()
    result = []

    for p, v in vals:
        if v not in seen:
            seen.add(v)
            result.append((p, v))

    return result


# ============================================================
# REAL RECOMPILATION
# ============================================================

def compile_code(code, task_id, model):
    if not code:
        return {
            "returncode": None,
            "stderr": "",
            "stdout": "",
            "timeout": False,
            "command": "",
        }

    work = OUT / "recompile" / model
    work.mkdir(parents=True, exist_ok=True)

    src = work / f"task_{task_id}.f90"
    exe = work / f"task_{task_id}.exe"

    src.write_text(code, encoding="utf-8")

    cmd = [
        "gfortran",
        "-std=f2008",
        "-Wall",
        "-Wextra",
        "-fcheck=all",
        "-fbacktrace",
        str(src),
        "-o",
        str(exe),
    ]

    try:
        p = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
        )

        return {
            "returncode": p.returncode,
            "stderr": p.stderr or "",
            "stdout": p.stdout or "",
            "timeout": False,
            "command": " ".join(cmd),
        }

    except subprocess.TimeoutExpired as e:
        return {
            "returncode": None,
            "stderr": (
                e.stderr.decode(errors="replace")
                if isinstance(e.stderr, bytes)
                else (e.stderr or "")
            ),
            "stdout": "",
            "timeout": True,
            "command": " ".join(cmd),
        }

    except FileNotFoundError:
        return {
            "returncode": None,
            "stderr": "gfortran_not_found",
            "stdout": "",
            "timeout": False,
            "command": " ".join(cmd),
        }


# ============================================================
# DETAILED ERROR TAXONOMY
# ============================================================

PATTERNS = [
    (
        "intent_in_modified",
        [
            r"intent\s*\(\s*in\s*\)",
            r"dummy argument.*intent",
            r"definition context.*intent",
            r"cannot appear in a variable definition context",
        ]
    ),

    (
        "undeclared_variable",
        [
            r"has no implicit type",
            r"symbol .* has no implicit type",
            r"undeclared",
            r"not declared",
        ]
    ),

    (
        "character_declaration",
        [
            r"character.*length",
            r"assumed character length",
            r"character\(len\s*=\s*\*\)",
            r"entity with assumed character length",
        ]
    ),

    (
        "rank_mismatch",
        [
            r"rank mismatch",
            r"incompatible ranks",
            r"rank-?mismatch",
        ]
    ),

    (
        "type_mismatch",
        [
            r"type mismatch",
            r"cannot convert",
            r"conversion from",
            r"different types",
        ]
    ),

    (
        "array_shape_interface",
        [
            r"explicit interface",
            r"assumed[- ]shape",
            r"shape mismatch",
            r"array.*shape",
            r"dimension mismatch",
        ]
    ),

    (
        "invalid_fortran_syntax",
        [
            r"syntax error",
            r"unclassifiable statement",
            r"unexpected .* statement",
            r"expecting .* statement",
            r"invalid form",
            r"invalid character",
            r"unexpected end of file",
        ]
    ),

    (
        "invalid_mod_operator",
        [
            r"\bmod\b.*syntax",
        ]
    ),

    (
        "duplicate_declaration",
        [
            r"already has basic type",
            r"already declared",
            r"duplicate",
        ]
    ),

    (
        "undefined_symbol_or_function",
        [
            r"undefined reference",
            r"function .* has no implicit type",
            r"procedure .* has no implicit type",
        ]
    ),

    (
        "allocation_problem",
        [
            r"allocatable",
            r"allocate-object",
            r"must be allocatable",
            r"already allocated",
        ]
    ),

    (
        "bounds_error",
        [
            r"above upper bound",
            r"below lower bound",
            r"out of bounds",
            r"array bound",
            r"index .* bound",
        ]
    ),

    (
        "io_format_error",
        [
            r"bad integer",
            r"bad real",
            r"formatted transfer",
            r"format error",
            r"input conversion",
            r"bad value during",
        ]
    ),

    (
        "unexpected_eof_input",
        [
            r"end of file",
            r"end-of-file",
        ]
    ),

    (
        "segmentation_fault",
        [
            r"segmentation fault",
            r"sigsegv",
        ]
    ),

    (
        "floating_point_error",
        [
            r"floating point",
            r"division by zero",
            r"divide by zero",
            r"overflow",
        ]
    ),

    (
        "timeout_or_infinite_loop",
        [
            r"timed out",
            r"timeout",
        ]
    ),
]


def classify_text(text, status):
    t = text or ""

    labels = []

    for label, regs in PATTERNS:
        if any(
            re.search(r, t, flags=re.I | re.S)
            for r in regs
        ):
            labels.append(label)

    if labels:
        return labels

    if status == "compile_err":
        return ["compile_error_other"]

    if status == "runtime_err":
        return ["runtime_error_other"]

    if status == "ineq":
        return ["wrong_output"]

    if status == "exception":
        return ["exception_other"]

    return ["none"]


# ============================================================
# LOAD TASK TRANSITIONS
# ============================================================

rows = list(
    csv.DictReader(
        TRANSITIONS.open(
            encoding="utf-8",
            errors="replace"
        )
    )
)

interesting = [
    r for r in rows
    if r["group"] in {"acquise", "regression"}
]

gain_ids = [
    int(r["task_id"])
    for r in interesting
    if r["group"] == "acquise"
]

regression_ids = [
    int(r["task_id"])
    for r in interesting
    if r["group"] == "regression"
]


# ============================================================
# LOAD JSONS
# ============================================================

base_details_raw = load(BASE_DETAILS)
a_details_raw = load(A_DETAILS)

base_logs_raw = load(BASE_LOGS) if BASE_LOGS.exists() else {}
a_logs_raw = load(A_LOGS) if A_LOGS.exists() else {}

base_details = build_task_objects(base_details_raw)
a_details = build_task_objects(a_details_raw)

base_logs = build_task_objects(base_logs_raw)
a_logs = build_task_objects(a_logs_raw)


# Also search all candidate solution JSONs
solution_files_base = list(BASE.glob("*solution*.json"))
solution_files_a = list(FT.glob("*ft_A*solution*.json"))

for p in solution_files_base:
    try:
        x = build_task_objects(load(p))
        for tid, objs in x.items():
            base_details[tid].extend(objs)
    except Exception:
        pass

for p in solution_files_a:
    try:
        x = build_task_objects(load(p))
        for tid, objs in x.items():
            a_details[tid].extend(objs)
    except Exception:
        pass


# ============================================================
# ANALYSE EACH GAIN / REGRESSION
# ============================================================

results = []

for r in interesting:
    tid = int(r["task_id"])

    base_status = r["base_status"]
    a_status = r["a_status_archived"]

    b_objs = (
        base_details.get(tid, []) +
        base_logs.get(tid, [])
    )

    a_objs = (
        a_details.get(tid, []) +
        a_logs.get(tid, [])
    )

    base_code, base_code_src = extract_code(b_objs)
    a_code, a_code_src = extract_code(a_objs)

    bdiag_existing = collect_diagnostics(b_objs)
    adiag_existing = collect_diagnostics(a_objs)

    # Recompile both codes so we have the same compiler diagnostics.
    bcomp = compile_code(base_code, tid, "base")
    acomp = compile_code(a_code, tid, "A")

    btext_parts = [
        v for _, v in bdiag_existing
    ]

    atext_parts = [
        v for _, v in adiag_existing
    ]

    if bcomp["stderr"]:
        btext_parts.append(bcomp["stderr"])

    if acomp["stderr"]:
        atext_parts.append(acomp["stderr"])

    base_text = "\n".join(btext_parts)
    a_text = "\n".join(atext_parts)

    base_labels = classify_text(
        base_text,
        base_status
    )

    a_labels = classify_text(
        a_text,
        a_status
    )

    # Save source + diff
    taskdir = OUT / "tasks" / f"task_{tid:03d}"
    taskdir.mkdir(parents=True, exist_ok=True)

    if base_code:
        (taskdir / "base.f90").write_text(
            base_code,
            encoding="utf-8"
        )

    if a_code:
        (taskdir / "A.f90").write_text(
            a_code,
            encoding="utf-8"
        )

    if base_code or a_code:
        diff = "".join(
            difflib.unified_diff(
                base_code.splitlines(True),
                a_code.splitlines(True),
                fromfile="base.f90",
                tofile="A.f90",
            )
        )

        (taskdir / "base_vs_A.diff").write_text(
            diff,
            encoding="utf-8"
        )

    (taskdir / "base_diagnostics.txt").write_text(
        base_text,
        encoding="utf-8"
    )

    (taskdir / "A_diagnostics.txt").write_text(
        a_text,
        encoding="utf-8"
    )

    results.append({
        "task_id": tid,
        "group": r["group"],
        "base_status": base_status,
        "A_status": a_status,

        "base_exact_causes":
            "|".join(base_labels),

        "A_exact_causes":
            "|".join(a_labels),

        "base_recompile_rc":
            bcomp["returncode"],

        "A_recompile_rc":
            acomp["returncode"],

        "base_code_found":
            bool(base_code),

        "A_code_found":
            bool(a_code),

        "base_code_source":
            base_code_src,

        "A_code_source":
            a_code_src,

        "task_dir":
            str(taskdir),
    })


# ============================================================
# SUMMARIES
# ============================================================

gain_causes = Counter()
regression_causes = Counter()

for r in results:
    if r["group"] == "acquise":
        for x in r["base_exact_causes"].split("|"):
            gain_causes[x] += 1

    elif r["group"] == "regression":
        for x in r["A_exact_causes"].split("|"):
            regression_causes[x] += 1


# ============================================================
# CSV
# ============================================================

csv_path = OUT / "QWEN27_A_GAINS_REGRESSIONS_EXACT_CAUSES.csv"

with csv_path.open(
    "w",
    newline="",
    encoding="utf-8"
) as f:
    w = csv.DictWriter(
        f,
        fieldnames=list(results[0].keys())
    )
    w.writeheader()
    w.writerows(results)


summary_csv = OUT / "QWEN27_A_EXACT_CAUSE_COUNTS.csv"

labels = sorted(
    set(gain_causes) |
    set(regression_causes)
)

with summary_csv.open(
    "w",
    newline="",
    encoding="utf-8"
) as f:
    w = csv.writer(f)

    w.writerow([
        "cause",
        "corrigee_par_A",
        "introduite_par_A",
    ])

    for label in labels:
        w.writerow([
            label,
            gain_causes[label],
            regression_causes[label],
        ])


# ============================================================
# JSON
# ============================================================

json_path = OUT / "QWEN27_A_EXACT_CAUSES.json"

json_path.write_text(
    json.dumps(
        {
            "gains_archived_run": len(gain_ids),
            "regressions_archived_run": len(regression_ids),

            "report_adjustment": {
                "additional_gain":
                    "1 compile_err -> OK",

                "exact_task_id":
                    None,

                "exact_compile_cause":
                    "non_localisee",
            },

            "corrected_causes": dict(
                gain_causes
            ),

            "introduced_causes": dict(
                regression_causes
            ),

            "tasks": results,
        },
        indent=2,
        ensure_ascii=False
    ),
    encoding="utf-8"
)


# ============================================================
# CHAT OUTPUT
# ============================================================

print("=" * 100)
print("QWEN27 A — CAUSES EXACTES DES GAINS ET RÉGRESSIONS")
print("=" * 100)

print()
print("Tâches analysées :", len(results))
print("Gains archivés   :", len(gain_ids))
print("Régressions      :", len(regression_ids))

print()
print("=" * 100)
print("ERREURS CORRIGÉES PAR A")
print("=" * 100)

for k, v in gain_causes.most_common():
    print(f"{k:40s} {v}")

print()
print(
    "+ 1 gain supplémentaire compile_err -> OK "
    "(rerun A=63, cause exacte non localisée)"
)

print()
print("=" * 100)
print("ERREURS INTRODUITES PAR A")
print("=" * 100)

for k, v in regression_causes.most_common():
    print(f"{k:40s} {v}")

print()
print("=" * 100)
print("DÉTAIL DES GAINS")
print("=" * 100)

for r in results:
    if r["group"] == "acquise":
        print(
            f"task {r['task_id']:3d} | "
            f"{r['base_status']:12s} -> OK | "
            f"{r['base_exact_causes']}"
        )

print()
print("=" * 100)
print("DÉTAIL DES RÉGRESSIONS")
print("=" * 100)

for r in results:
    if r["group"] == "regression":
        print(
            f"task {r['task_id']:3d} | "
            f"OK -> {r['A_status']:12s} | "
            f"{r['A_exact_causes']}"
        )

print()
print("=" * 100)
print("QUALITÉ DE L'EXTRACTION DU CODE")
print("=" * 100)

print(
    "Base code trouvé :",
    sum(r["base_code_found"] for r in results),
    "/",
    len(results)
)

print(
    "A code trouvé    :",
    sum(r["A_code_found"] for r in results),
    "/",
    len(results)
)

print()
print("=" * 100)
print("FICHIERS")
print("=" * 100)

print(csv_path)
print(summary_csv)
print(json_path)
print(OUT / "tasks")
