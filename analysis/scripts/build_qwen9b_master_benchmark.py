import csv
import json
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime

SOURCE = Path("/path/to/project/__sandbox_adel__LAST/evaluation_finetuning")
DEST = Path("/path/to/project/results/02_qwen9b")

BASE_OK = 36
TOTAL = 164

rows = []

# ------------------------------------------------------------------
# Lecture de toutes les évaluations Qwen9B
# ------------------------------------------------------------------

for root in [SOURCE / "epoch1", SOURCE / "epoch2"]:
    for f in sorted(root.rglob("*_evaluation_summary.json")):
        try:
            d = json.loads(f.read_text())
        except Exception:
            continue

        metrics = d.get("metrics")
        model_key = d.get("model_key")

        if not isinstance(metrics, dict) or not model_key:
            continue

        m = re.match(r"^(.*)_humaneval_mistral_conc(\d+)$", model_key)
        if not m:
            continue

        experiment = m.group(1)
        concurrency = int(m.group(2))

        rel = f.relative_to(SOURCE)
        epoch = rel.parts[0]
        lr_label = rel.parts[1]

        rows.append({
            "epoch": epoch,
            "lr_label": lr_label,
            "experiment": experiment,
            "model_key": model_key,
            "concurrency": concurrency,
            "total": metrics.get("total"),
            "ok": metrics.get("ok"),
            "pass_at_1": metrics.get("pass_at_1"),
            "compile_err": metrics.get("compile_err"),
            "runtime_err": metrics.get("runtime_err"),
            "ineq": metrics.get("ineq"),
            "exception": metrics.get("exception"),
            "compilation_rate": metrics.get("compilation_rate"),
            "execution_success_rate": metrics.get("execution_success_rate"),
            "execution_limit": d.get("execution_time_limit"),
            "evaluated_at": d.get("evaluated_at", ""),
            "summary_path": str(rel),
        })

# ------------------------------------------------------------------
# Regroupement par fine-tuning
# ------------------------------------------------------------------

groups = defaultdict(list)

for r in rows:
    groups[(r["epoch"], r["lr_label"], r["experiment"])].append(r)

master = []

for key, vals in sorted(groups.items()):

    # Meilleur score HumanEval.
    # Si égalité : évaluation la plus récente.
    def selector(r):
        try:
            dt = datetime.fromisoformat(r["evaluated_at"])
        except Exception:
            dt = datetime.min

        return (
            r["ok"] if isinstance(r["ok"], int) else -1,
            dt,
        )

    selected = max(vals, key=selector)

    ordered = sorted(vals, key=lambda x: x["concurrency"])

    available_concurrencies = ";".join(
        str(x["concurrency"]) for x in ordered
    )

    available_scores = ";".join(
        f"conc{x['concurrency']}={x['ok']}"
        for x in ordered
    )

    delta = selected["ok"] - BASE_OK

    if delta > 0:
        relation = "above_base"
    elif delta == 0:
        relation = "equal_base"
    else:
        relation = "below_base"

    master.append({
        "epoch": selected["epoch"],
        "lr_label": selected["lr_label"],
        "experiment": selected["experiment"],

        "n_generations": len(vals),
        "available_concurrencies": available_concurrencies,
        "available_scores": available_scores,

        "selected_concurrency": selected["concurrency"],
        "selected_model_key": selected["model_key"],

        "total": selected["total"],
        "ok": selected["ok"],
        "pass_at_1": selected["pass_at_1"],

        "delta_vs_base_ok": delta,
        "relation_vs_base": relation,

        "compile_err": selected["compile_err"],
        "runtime_err": selected["runtime_err"],
        "ineq": selected["ineq"],
        "exception": selected["exception"],

        "compilation_rate": selected["compilation_rate"],
        "execution_success_rate": selected["execution_success_rate"],

        "execution_limit": selected["execution_limit"],
        "evaluated_at": selected["evaluated_at"],
        "summary_path": selected["summary_path"],
    })

# ------------------------------------------------------------------
# CSV maître
# ------------------------------------------------------------------

out = DEST / "QWEN9B_MASTER_BENCHMARK_PROVISIONAL.csv"

cols = [
    "epoch",
    "lr_label",
    "experiment",

    "n_generations",
    "available_concurrencies",
    "available_scores",

    "selected_concurrency",
    "selected_model_key",

    "total",
    "ok",
    "pass_at_1",

    "delta_vs_base_ok",
    "relation_vs_base",

    "compile_err",
    "runtime_err",
    "ineq",
    "exception",

    "compilation_rate",
    "execution_success_rate",

    "execution_limit",
    "evaluated_at",
    "summary_path",
]

with out.open("w", encoding="utf-8", newline="") as fp:
    writer = csv.DictWriter(fp, fieldnames=cols)
    writer.writeheader()
    writer.writerows(master)

# ------------------------------------------------------------------
# Synthèse
# ------------------------------------------------------------------

above = [r for r in master if r["delta_vs_base_ok"] > 0]
equal = [r for r in master if r["delta_vs_base_ok"] == 0]
below = [r for r in master if r["delta_vs_base_ok"] < 0]

print("=" * 85)
print("QWEN3.5-9B — TABLEAU MAÎTRE BENCHMARK PROVISOIRE")
print("=" * 85)

print(f"\nFine-tunings uniques : {len(master)}")
print(f"Baseline             : {BASE_OK}/{TOTAL}")
print()
print(f"Au-dessus baseline   : {len(above)}")
print(f"Égaux baseline       : {len(equal)}")
print(f"En-dessous baseline  : {len(below)}")

print("\n===== EXPÉRIENCES >= BASELINE =====")

for r in sorted(
    [x for x in master if x["delta_vs_base_ok"] >= 0],
    key=lambda x: (-x["ok"], x["experiment"])
):
    print(
        f"{r['ok']:>3}/164 "
        f"delta={r['delta_vs_base_ok']:+3d} | "
        f"{r['epoch']}/{r['lr_label']} | "
        f"{r['experiment']} | "
        f"selected=conc{r['selected_concurrency']} | "
        f"runs=[{r['available_scores']}]"
    )

print("\n===== TOP 15 =====")

for i, r in enumerate(
    sorted(master, key=lambda x: (-x["ok"], x["experiment"]))[:15],
    start=1
):
    print(
        f"{i:>2}. "
        f"{r['ok']:>3}/164 "
        f"({r['delta_vs_base_ok']:+3d}) | "
        f"{r['epoch']}/{r['lr_label']} | "
        f"{r['experiment']}"
    )

print("\n===== SÉLECTIONS OÙ PLUSIEURS GÉNÉRATIONS EXISTENT =====")

for r in master:
    if r["n_generations"] > 1:
        print(
            f"{r['epoch']}/{r['lr_label']} | "
            f"{r['experiment']:<28} | "
            f"{r['available_scores']:<30} "
            f"=> retenu conc{r['selected_concurrency']}"
        )

print("\nFichier maître :")
print(out)
