#!/usr/bin/env python3

from pathlib import Path
from collections import Counter, defaultdict
import csv
import json
import re


# ============================================================
# PATHS
# ============================================================

SANDBOX = Path(
    "/path/to/project/__sandbox_adel__LAST"
)

EVAL = SANDBOX / "evaluation_finetuning"

BASE_DIR = (
    EVAL /
    "qwen27/base/results"
)

A_DIR = (
    EVAL /
    "qwen27/epoch1/learning_rate_1/results"
)

BASE_SUMMARY = (
    BASE_DIR /
    "base_qwen27_humaneval_mistral_conc12_evaluation_summary.json"
)

BASE_DETAILS = (
    BASE_DIR /
    "base_qwen27_humaneval_mistral_conc12_evaluation_details.json"
)

BASE_LOGS = (
    BASE_DIR /
    "base_qwen27_humaneval_mistral_conc12_evaluation_logs.json"
)

A_SUMMARY = (
    A_DIR /
    "ft_A_qwen27_humaneval_mistral_conc12_evaluation_summary.json"
)

A_DETAILS = (
    A_DIR /
    "ft_A_qwen27_humaneval_mistral_conc12_evaluation_details.json"
)

A_LOGS = (
    A_DIR /
    "ft_A_qwen27_humaneval_mistral_conc12_evaluation_logs.json"
)

BENCHMARK = SANDBOX / "benchmark.json"

OUT = Path(
    "/path/to/project/results/"
    "04_task_analysis/qwen27_A_vs_base"
)

OUT.mkdir(parents=True, exist_ok=True)


# ============================================================
# CONVENTION DU RAPPORT
# ============================================================

# Run réellement archivé :
# A = 62 OK / 54 compile_err
#
# Rerun non sauvegardé retenu pour le rapport :
# A = 63 OK
#
# Convention :
# +1 OK
# -1 compile_err
#
# On ne modifie PAS les identifiants tâche par tâche,
# car l'identité de cette 63e tâche n'est pas connue.

REPORT_A_OK = 63


# ============================================================
# UTILS
# ============================================================

def load(path):
    with Path(path).open(
        encoding="utf-8",
        errors="replace"
    ) as f:
        return json.load(f)


def normalize_status(value):
    if value is None:
        return None

    s = str(value).strip().lower()

    if (
        s == "ok"
        or "success" in s
        or s == "pass"
        or s == "passed"
    ):
        return "ok"

    if (
        "compile" in s
        or "compilation" in s
    ):
        return "compile_err"

    if (
        "runtime" in s
        or "run_err" in s
    ):
        return "runtime_err"

    if (
        "ineq" in s
        or "incorrect" in s
        or "wrong" in s
        or "mismatch" in s
    ):
        return "ineq"

    if (
        "exception" in s
        or "error" == s
    ):
        return "exception"

    return None


def task_id_of(d):
    for key in [
        "task_id",
        "id",
        "problem_id",
        "task",
        "index",
    ]:
        if key in d:
            v = d[key]

            if isinstance(
                v,
                (str, int)
            ):
                s = str(v)

                m = re.search(
                    r"(\d+)$",
                    s
                )

                if m:
                    return int(
                        m.group(1)
                    )

    return None


def status_of(d):
    for key in [
        "status",
        "result",
        "outcome",
        "evaluation_status",
        "eval_status",
    ]:
        if key in d:
            st = normalize_status(
                d[key]
            )

            if st:
                return st

    for key in [
        "passed",
        "success",
        "ok",
    ]:
        if key in d and isinstance(
            d[key],
            bool
        ):
            return (
                "ok"
                if d[key]
                else None
            )

    return None


def walk(obj):
    if isinstance(obj, dict):
        yield obj

        for v in obj.values():
            yield from walk(v)

    elif isinstance(obj, list):
        for v in obj:
            yield from walk(v)


def index_details(obj):
    """
    Cherche récursivement les entrées correspondant
    aux tâches et retourne task_id -> dict.
    """

    candidates = defaultdict(list)

    for d in walk(obj):
        tid = task_id_of(d)
        st = status_of(d)

        if tid is not None and st:
            candidates[tid].append(d)

    out = {}

    for tid, values in candidates.items():

        # Prendre l'objet le plus riche.
        values.sort(
            key=lambda x: len(
                json.dumps(
                    x,
                    ensure_ascii=False
                )
            ),
            reverse=True
        )

        out[tid] = values[0]

    return out


def index_by_task_any(obj):
    """
    Pour les logs : pas nécessairement de status.
    """

    candidates = defaultdict(list)

    for d in walk(obj):
        tid = task_id_of(d)

        if tid is not None:
            candidates[tid].append(d)

    out = {}

    for tid, values in candidates.items():

        values.sort(
            key=lambda x: len(
                json.dumps(
                    x,
                    ensure_ascii=False
                )
            ),
            reverse=True
        )

        out[tid] = values[0]

    return out


TEXT_KEYS = [
    "stderr",
    "compile_stderr",
    "runtime_stderr",
    "error",
    "error_message",
    "message",
    "exception",
    "reason",
    "stdout",
]


def collect_text(*objs):
    texts = []

    for obj in objs:
        if not isinstance(obj, dict):
            continue

        for d in walk(obj):
            for key in TEXT_KEYS:
                v = d.get(key)

                if (
                    isinstance(v, str)
                    and v.strip()
                ):
                    texts.append(v.strip())

    # déduplication
    seen = set()
    cleaned = []

    for t in texts:
        if t not in seen:
            seen.add(t)
            cleaned.append(t)

    return "\n".join(cleaned)


# ============================================================
# CLASSIFICATION D'ERREUR
# basée uniquement sur messages effectivement présents
# ============================================================

CAUSE_PATTERNS = [
    (
        "variable_non_declaree",
        [
            r"has no implicit type",
            r"no implicit type",
            r"undeclared",
            r"not declared",
        ]
    ),
    (
        "modification_intent_in",
        [
            r"intent\s*\(\s*in\s*\)",
            r"dummy argument.*intent",
            r"definition context.*intent",
        ]
    ),
    (
        "chaine_character_invalide",
        [
            r"character.*length",
            r"assumed character length",
            r"character\(len=\*\)",
        ]
    ),
    (
        "interface_tableau",
        [
            r"explicit interface",
            r"assumed-shape",
            r"assumed shape",
        ]
    ),
    (
        "rank_mismatch",
        [
            r"rank mismatch",
            r"incompatible ranks",
        ]
    ),
    (
        "type_mismatch",
        [
            r"type mismatch",
            r"cannot convert",
            r"different types",
        ]
    ),
    (
        "syntaxe_fortran",
        [
            r"syntax error",
            r"unclassifiable statement",
            r"invalid form",
            r"unexpected.*statement",
            r"expected.*statement",
        ]
    ),
    (
        "symbole_introuvable",
        [
            r"undefined reference",
            r"no such function",
            r"has no implicit type",
        ]
    ),
    (
        "depassement_tableau",
        [
            r"index.*above upper bound",
            r"index.*below lower bound",
            r"out of bounds",
            r"bounds",
        ]
    ),
    (
        "lecture_entree_eof",
        [
            r"end of file",
            r"end-of-file",
            r"fortran runtime error.*eof",
        ]
    ),
    (
        "format_io",
        [
            r"bad integer",
            r"bad real",
            r"formatted transfer",
            r"format error",
            r"input conversion",
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
        "timeout_ou_boucle",
        [
            r"timeout",
            r"timed out",
        ]
    ),
    (
        "division_par_zero",
        [
            r"division by zero",
            r"divide by zero",
        ]
    ),
]


def classify_error(status, text):
    t = (text or "").lower()

    for label, patterns in CAUSE_PATTERNS:
        for p in patterns:
            if re.search(
                p,
                t,
                flags=re.I | re.S
            ):
                return label

    if status == "compile_err":
        return "compilation_non_detaillee"

    if status == "runtime_err":
        return "runtime_non_detaillee"

    if status == "ineq":
        return "sortie_incorrecte"

    if status == "exception":
        return "exception_non_detaillee"

    if status == "ok":
        return "aucune"

    return "inconnue"


def short_text(text, n=350):
    if not text:
        return ""

    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    if len(text) > n:
        return text[:n] + "..."

    return text


# ============================================================
# BENCHMARK
# ============================================================

def benchmark_prompts(obj):
    mapping = {}

    if isinstance(obj, list):
        iterable = enumerate(obj)

    elif isinstance(obj, dict):
        # plusieurs formats possibles
        if isinstance(
            obj.get("problems"),
            list
        ):
            iterable = enumerate(
                obj["problems"]
            )
        elif isinstance(
            obj.get("tasks"),
            list
        ):
            iterable = enumerate(
                obj["tasks"]
            )
        else:
            iterable = []

            for k, v in obj.items():
                if isinstance(v, dict):
                    iterable.append(
                        (k, v)
                    )
    else:
        iterable = []

    for fallback, d in iterable:
        if not isinstance(d, dict):
            continue

        tid = task_id_of(d)

        if tid is None:
            try:
                tid = int(fallback)
            except Exception:
                continue

        prompt = ""

        for key in [
            "prompt",
            "task",
            "description",
            "instruction",
        ]:
            v = d.get(key)

            if isinstance(v, str):
                prompt = v.strip()
                break

        mapping[tid] = prompt

    return mapping


# ============================================================
# LOAD
# ============================================================

base_summary = load(BASE_SUMMARY)
a_summary = load(A_SUMMARY)

base_details_raw = load(BASE_DETAILS)
a_details_raw = load(A_DETAILS)

base_logs_raw = (
    load(BASE_LOGS)
    if BASE_LOGS.exists()
    else {}
)

a_logs_raw = (
    load(A_LOGS)
    if A_LOGS.exists()
    else {}
)

benchmark_raw = load(BENCHMARK)

base_details = index_details(
    base_details_raw
)

a_details = index_details(
    a_details_raw
)

base_logs = index_by_task_any(
    base_logs_raw
)

a_logs = index_by_task_any(
    a_logs_raw
)

prompts = benchmark_prompts(
    benchmark_raw
)


# ============================================================
# CHECK
# ============================================================

print("=" * 100)
print("QWEN27 BASE VS A — ANALYSE TASK-LEVEL")
print("=" * 100)

print(
    "Tâches trouvées dans details base :",
    len(base_details)
)

print(
    "Tâches trouvées dans details A    :",
    len(a_details)
)

common = sorted(
    set(base_details) &
    set(a_details)
)

print(
    "Tâches communes                   :",
    len(common)
)

if len(common) != 164:
    print()
    print(
        "ATTENTION : 164 tâches n'ont pas été reconnues."
    )
    print(
        "Le script continue avec les tâches identifiées."
    )


# ============================================================
# TASK COMPARISON
# ============================================================

rows = []

transition_counts = Counter()

for tid in common:

    bd = base_details[tid]
    ad = a_details[tid]

    bs = status_of(bd)
    fs = status_of(ad)

    transition = f"{bs} -> {fs}"

    transition_counts[
        (bs, fs)
    ] += 1

    if bs != "ok" and fs == "ok":
        group = "acquise"

    elif bs == "ok" and fs != "ok":
        group = "regression"

    elif bs == "ok" and fs == "ok":
        group = "conservee"

    else:
        group = "echec_persistant"

    btext = collect_text(
        bd,
        base_logs.get(tid)
    )

    atext = collect_text(
        ad,
        a_logs.get(tid)
    )

    bcause = classify_error(
        bs,
        btext
    )

    acause = classify_error(
        fs,
        atext
    )

    rows.append({
        "task_id": tid,
        "group": group,
        "base_status": bs,
        "a_status_archived": fs,
        "transition": transition,
        "base_error_family": bcause,
        "a_error_family": acause,
        "prompt": prompts.get(
            tid,
            ""
        ),
        "base_error_excerpt": short_text(
            btext
        ),
        "a_error_excerpt": short_text(
            atext
        ),
    })


# ============================================================
# GROUP COUNTS
# ============================================================

group_counts = Counter(
    r["group"]
    for r in rows
)

gains = [
    r for r in rows
    if r["group"] == "acquise"
]

regressions = [
    r for r in rows
    if r["group"] == "regression"
]

persistent = [
    r for r in rows
    if r["group"] == "echec_persistant"
]

conserved = [
    r for r in rows
    if r["group"] == "conservee"
]


# ============================================================
# ERROR SUMMARIES
# ============================================================

corrected_statuses = Counter(
    r["base_status"]
    for r in gains
)

corrected_causes = Counter(
    r["base_error_family"]
    for r in gains
)

introduced_statuses = Counter(
    r["a_status_archived"]
    for r in regressions
)

introduced_causes = Counter(
    r["a_error_family"]
    for r in regressions
)

persistent_status_transitions = Counter(
    (
        r["base_status"],
        r["a_status_archived"]
    )
    for r in persistent
)

persistent_cause_transitions = Counter(
    (
        r["base_error_family"],
        r["a_error_family"]
    )
    for r in persistent
)


# ============================================================
# REPORT CONVENTION 63
# ============================================================

archived_counter = dict(
    a_summary["counter"]
)

report_counter = {
    k: archived_counter.get(k, 0)
    for k in [
        "ok",
        "compile_err",
        "runtime_err",
        "ineq",
        "exception",
    ]
}

delta_ok = (
    REPORT_A_OK -
    report_counter["ok"]
)

if delta_ok != 1:
    print()
    print(
        "ATTENTION : le run archivé n'est pas à 62 OK."
    )
    print(
        "Delta nécessaire pour atteindre 63 :",
        delta_ok
    )

report_counter["ok"] += delta_ok
report_counter["compile_err"] -= delta_ok


# ============================================================
# SAVE CSV TASK-LEVEL
# ============================================================

task_csv = (
    OUT /
    "QWEN27_BASE_VS_A_TASK_TRANSITIONS.csv"
)

with task_csv.open(
    "w",
    newline="",
    encoding="utf-8"
) as f:

    fields = list(
        rows[0].keys()
    )

    w = csv.DictWriter(
        f,
        fieldnames=fields
    )

    w.writeheader()
    w.writerows(rows)


# ============================================================
# SAVE TRANSITION MATRIX
# ============================================================

statuses = [
    "ok",
    "compile_err",
    "runtime_err",
    "ineq",
    "exception",
]

matrix_csv = (
    OUT /
    "QWEN27_BASE_VS_A_TRANSITION_MATRIX.csv"
)

with matrix_csv.open(
    "w",
    newline="",
    encoding="utf-8"
) as f:

    w = csv.writer(f)

    w.writerow(
        ["base \\ A"] +
        statuses
    )

    for bs in statuses:
        w.writerow(
            [bs] +
            [
                transition_counts[
                    (bs, fs)
                ]
                for fs in statuses
            ]
        )


# ============================================================
# SAVE ERROR FAMILY SUMMARY
# ============================================================

error_csv = (
    OUT /
    "QWEN27_BASE_VS_A_ERROR_FAMILIES.csv"
)

all_labels = sorted(
    set(corrected_causes) |
    set(introduced_causes)
)

with error_csv.open(
    "w",
    newline="",
    encoding="utf-8"
) as f:

    w = csv.writer(f)

    w.writerow([
        "error_family",
        "corrigee_base_fail_to_A_ok",
        "introduite_base_ok_to_A_fail",
    ])

    for label in all_labels:
        w.writerow([
            label,
            corrected_causes[label],
            introduced_causes[label],
        ])


# ============================================================
# SAVE JSON
# ============================================================

analysis = {
    "source": {
        "base_summary": str(BASE_SUMMARY),
        "base_details": str(BASE_DETAILS),
        "A_summary": str(A_SUMMARY),
        "A_details": str(A_DETAILS),
    },

    "archived_results": {
        "base": {
            k: base_summary[
                "counter"
            ].get(k)
            for k in [
                "ok",
                "compile_err",
                "runtime_err",
                "ineq",
                "exception",
            ]
        },

        "A": {
            k: archived_counter.get(k)
            for k in [
                "ok",
                "compile_err",
                "runtime_err",
                "ineq",
                "exception",
            ]
        },
    },

    "report_convention": {
        "A": report_counter,

        "note": (
            "Le rerun A=63 n'est pas sauvegardé. "
            "Pour les agrégats du rapport : "
            "+1 OK, -1 compile_err. "
            "Les IDs task-level restent ceux "
            "du run A archivé."
        )
    },

    "task_level_archived_run": {
        "counts": dict(
            group_counts
        ),

        "transition_counts": {
            f"{a}->{b}": n
            for (a, b), n
            in transition_counts.items()
        },

        "corrected_statuses": dict(
            corrected_statuses
        ),

        "corrected_error_families": dict(
            corrected_causes
        ),

        "introduced_statuses": dict(
            introduced_statuses
        ),

        "introduced_error_families": dict(
            introduced_causes
        ),

        "persistent_status_transitions": {
            f"{a}->{b}": n
            for (a, b), n
            in persistent_status_transitions.items()
        },

        "persistent_error_family_transitions": {
            f"{a}->{b}": n
            for (a, b), n
            in persistent_cause_transitions.items()
        },
    }
}

json_path = (
    OUT /
    "QWEN27_BASE_VS_A_ANALYSIS.json"
)

json_path.write_text(
    json.dumps(
        analysis,
        indent=2,
        ensure_ascii=False
    ),
    encoding="utf-8"
)


# ============================================================
# MARKDOWN REPORT
# ============================================================

md = []

md.append(
    "# Qwen3.5-27B — base vs fine-tuning Type A"
)

md.append("")

md.append(
    "## Résultats globaux"
)

md.append("")

md.append(
    f"- Base : "
    f"{base_summary['counter']['ok']}/164 tâches correctes"
)

md.append(
    f"- A archivé : "
    f"{archived_counter['ok']}/164"
)

md.append(
    f"- A retenu pour le rapport : "
    f"{report_counter['ok']}/164"
)

md.append(
    f"- Erreurs de compilation A retenues : "
    f"{report_counter['compile_err']}"
)

md.append("")

md.append(
    "La correction 62→63 est appliquée uniquement "
    "aux statistiques agrégées : +1 OK et "
    "-1 compile_err."
)

md.append("")

md.append(
    "## Transitions tâche par tâche "
    "(run A archivé)"
)

md.append("")

for label in [
    "acquise",
    "regression",
    "conservee",
    "echec_persistant",
]:
    md.append(
        f"- {label}: "
        f"{group_counts[label]}"
    )

md.append("")

md.append(
    "## Erreurs corrigées par le fine-tuning"
)

md.append("")

for k, v in corrected_statuses.most_common():
    md.append(
        f"- {k} → OK : {v}"
    )

md.append("")

md.append(
    "### Familles détaillées corrigées"
)

md.append("")

for k, v in corrected_causes.most_common():
    md.append(
        f"- {k}: {v}"
    )

md.append("")

md.append(
    "## Régressions introduites"
)

md.append("")

for k, v in introduced_statuses.most_common():
    md.append(
        f"- OK → {k}: {v}"
    )

md.append("")

md.append(
    "### Familles détaillées introduites"
)

md.append("")

for k, v in introduced_causes.most_common():
    md.append(
        f"- {k}: {v}"
    )

md.append("")

md.append(
    "## Échecs persistants"
)

md.append("")

for (a, b), v in (
    persistent_status_transitions
    .most_common()
):
    md.append(
        f"- {a} → {b}: {v}"
    )

md.append("")

md.append(
    "## Exemples de tâches acquises"
)

md.append("")

for r in gains[:10]:
    md.append(
        f"### Tâche {r['task_id']}"
    )

    if r["prompt"]:
        md.append(
            r["prompt"]
        )

    md.append(
        f"- Base : "
        f"{r['base_status']} "
        f"({r['base_error_family']})"
    )

    md.append(
        "- Après A : OK"
    )

    if r["base_error_excerpt"]:
        md.append(
            f"- Message : "
            f"`{r['base_error_excerpt']}`"
        )

    md.append("")

md.append(
    "## Exemples de régressions"
)

md.append("")

for r in regressions[:10]:
    md.append(
        f"### Tâche {r['task_id']}"
    )

    if r["prompt"]:
        md.append(
            r["prompt"]
        )

    md.append(
        "- Base : OK"
    )

    md.append(
        f"- Après A : "
        f"{r['a_status_archived']} "
        f"({r['a_error_family']})"
    )

    if r["a_error_excerpt"]:
        md.append(
            f"- Message : "
            f"`{r['a_error_excerpt']}`"
        )

    md.append("")


md_path = (
    OUT /
    "QWEN27_BASE_VS_A_REPORT.md"
)

md_path.write_text(
    "\n".join(md),
    encoding="utf-8"
)


# ============================================================
# CHAT SUMMARY
# ============================================================

print()
print("=" * 100)
print("RÉSULTATS GLOBAUX")
print("=" * 100)

print(
    "BASE :",
    base_summary["counter"]["ok"],
    "OK /",
    base_summary["counter"]["compile_err"],
    "compile /",
    base_summary["counter"]["runtime_err"],
    "runtime /",
    base_summary["counter"]["ineq"],
    "ineq"
)

print(
    "A ARCHIVÉ :",
    archived_counter["ok"],
    "OK /",
    archived_counter["compile_err"],
    "compile /",
    archived_counter["runtime_err"],
    "runtime /",
    archived_counter["ineq"],
    "ineq"
)

print(
    "A RAPPORT :",
    report_counter["ok"],
    "OK /",
    report_counter["compile_err"],
    "compile /",
    report_counter["runtime_err"],
    "runtime /",
    report_counter["ineq"],
    "ineq"
)


print()
print("=" * 100)
print("TRANSITIONS — RUN ARCHIVÉ")
print("=" * 100)

print(
    "Acquises (base fail → A OK) :",
    group_counts["acquise"]
)

print(
    "Régressions (base OK → A fail) :",
    group_counts["regression"]
)

print(
    "Conservées (OK → OK) :",
    group_counts["conservee"]
)

print(
    "Échecs persistants :",
    group_counts["echec_persistant"]
)


print()
print("=" * 100)
print("ERREURS CORRIGÉES — STATUT INITIAL")
print("=" * 100)

for k, v in corrected_statuses.most_common():
    print(
        f"{k:20s} -> OK : {v}"
    )


print()
print("=" * 100)
print("FAMILLES D'ERREURS CORRIGÉES")
print("=" * 100)

for k, v in corrected_causes.most_common():
    print(
        f"{k:35s} {v}"
    )


print()
print("=" * 100)
print("RÉGRESSIONS INTRODUITES")
print("=" * 100)

for k, v in introduced_statuses.most_common():
    print(
        f"OK -> {k:20s} : {v}"
    )


print()
print("=" * 100)
print("FAMILLES D'ERREURS INTRODUITES")
print("=" * 100)

for k, v in introduced_causes.most_common():
    print(
        f"{k:35s} {v}"
    )


print()
print("=" * 100)
print("PRINCIPAUX ÉCHECS PERSISTANTS")
print("=" * 100)

for (a, b), v in (
    persistent_status_transitions
    .most_common(15)
):
    print(
        f"{a:15s} -> {b:15s} : {v}"
    )


print()
print("=" * 100)
print("IDS — TÂCHES ACQUISES")
print("=" * 100)

print(
    [r["task_id"] for r in gains]
)


print()
print("=" * 100)
print("IDS — RÉGRESSIONS")
print("=" * 100)

print(
    [r["task_id"] for r in regressions]
)


print()
print("=" * 100)
print("FICHIERS SAUVEGARDÉS")
print("=" * 100)

for p in [
    task_csv,
    matrix_csv,
    error_csv,
    json_path,
    md_path,
]:
    print(p)

