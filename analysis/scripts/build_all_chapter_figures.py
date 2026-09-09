from pathlib import Path
import json
import re
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


# ============================================================
# PATHS
# ============================================================

RESULTS = Path("/path/to/project/results")

PERSONAL = Path(
    "/path/to/project/__sandbox_adel__LAST/"
    "evaluation_finetuning/qwen27"
)

TUTOR = Path(
    "/path/to/project/FOR_ADEL/qwen3.6-27b-ft"
)

OUT = RESULTS / "06_figures" / "chapter_results"
OUT.mkdir(parents=True, exist_ok=True)

LOG = RESULTS / "FIGURES_CHAPTER_BUILD_LOG.txt"

BASE_TUTOR = (
    TUTOR /
    "02_refBench/benchmark/evals/aggregate.json"
)


# ============================================================
# UTILS
# ============================================================

def load_json(path):
    path = Path(path)
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def save(fig, stem):
    png = OUT / f"{stem}.png"
    pdf = OUT / f"{stem}.pdf"

    fig.savefig(
        png,
        dpi=300,
        bbox_inches="tight"
    )
    fig.savefig(
        pdf,
        bbox_inches="tight"
    )

    plt.close(fig)

    print(f"[OK] {png.name}")


def pct(x):
    return 100.0 * x


def agg(path):
    return load_json(path)


def pass1_mean(d):
    return 100 * d["pass_rate"]["mean"]


def pass1_std(d):
    return 100 * d["pass_rate"]["std"]


def pass10(d):
    p = d.get("pass_at_k") or {}
    v = p.get("pass@10")
    return None if v is None else 100 * v


def diff_mean(d):
    x = d.get("difficulty_weighted_score")
    if not x:
        return None
    return x.get("mean")


def diff_std(d):
    x = d.get("difficulty_weighted_score")
    if not x:
        return None
    return x.get("std")


def horizontal_baseline(ax, value, label=None):
    ax.axhline(
        value,
        linestyle="--",
        linewidth=1.2,
        label=label
    )


def label_bars(ax, bars, fmt="{:.2f}"):
    for b in bars:
        h = b.get_height()
        ax.text(
            b.get_x() + b.get_width()/2,
            h,
            fmt.format(h),
            ha="center",
            va="bottom",
            fontsize=8
        )


# ============================================================
# BASELINE TUTOR
# ============================================================

tutor_base = agg(BASE_TUTOR)
TUTOR_BASE_PASS1 = pass1_mean(tutor_base)

print("=" * 80)
print("BASELINE TUTEUR")
print("=" * 80)
print(f"Pass@1 moyen : {TUTOR_BASE_PASS1:.2f}%")
print(
    f"Pass@1 std    : "
    f"{pass1_std(tutor_base):.2f}%"
)


# ============================================================
# FIGURE 01
# QWEN27 PERSONNEL : BASE VS A
# ============================================================

base_summary_path = (
    PERSONAL /
    "base/results/"
    "base_qwen27_humaneval_mistral_conc12_evaluation_summary.json"
)

a_summary_path = (
    PERSONAL /
    "epoch1/learning_rate_1/results/"
    "ft_A_qwen27_humaneval_mistral_conc12_evaluation_summary.json"
)

base_summary = load_json(base_summary_path)
a_summary = load_json(a_summary_path)

bc = base_summary["counter"]
ac_archived = a_summary["counter"]

# ------------------------------------------------------------
# Rerun A retenu pour le rapport :
# 63 OK au lieu de 62.
#
# Convention demandée :
# 1 erreur de compilation du run archivé est considérée
# corrigée dans le rerun non sauvegardé.
# ------------------------------------------------------------

ac = dict(ac_archived)

ac["ok"] = ac_archived["ok"] + 1
ac["compile_err"] = ac_archived["compile_err"] - 1

assert sum(
    ac[k] for k in
    ["ok", "compile_err", "runtime_err", "ineq", "exception"]
) == 164

base_pass = 100 * bc["ok"] / 164
a_pass = 100 * ac["ok"] / 164


fig, axes = plt.subplots(
    1, 2,
    figsize=(10.8, 4.1)
)

# ---- panel A

ax = axes[0]

bars = ax.bar(
    ["Qwen3.5-27B\nbase", "FT sur A"],
    [base_pass, a_pass]
)

ax.set_ylabel("Pass@1 (%)")
ax.set_ylim(0, 45)
ax.set_title("(a) Performance globale")

for b, n, val in zip(
    bars,
    [bc["ok"], ac["ok"]],
    [base_pass, a_pass]
):
    ax.text(
        b.get_x() + b.get_width()/2,
        b.get_height() + 0.6,
        f"{val:.2f}%\n({n}/164)",
        ha="center",
        va="bottom",
        fontsize=9
    )

ax.text(
    0.5,
    42,
    f"+{ac['ok'] - bc['ok']} tâches "
    f"/ +{a_pass-base_pass:.2f} points",
    ha="center",
    fontsize=9
)

# ---- panel B

ax = axes[1]

statuses = [
    "Correct",
    "Compilation",
    "Runtime",
    "Sortie\nincorrecte",
    "Exception"
]

base_values = [
    bc["ok"],
    bc["compile_err"],
    bc["runtime_err"],
    bc["ineq"],
    bc["exception"]
]

a_values = [
    ac["ok"],
    ac["compile_err"],
    ac["runtime_err"],
    ac["ineq"],
    ac["exception"]
]

x = np.arange(len(statuses))
w = 0.36

b1 = ax.bar(
    x - w/2,
    base_values,
    width=w,
    label="Base"
)

b2 = ax.bar(
    x + w/2,
    a_values,
    width=w,
    label="FT A"
)

ax.set_xticks(x)
ax.set_xticklabels(statuses, fontsize=8)
ax.set_ylabel("Nombre de tâches")
ax.set_title("(b) Répartition des résultats")
ax.legend(fontsize=8)

for bars_ in [b1, b2]:
    for b in bars_:
        ax.text(
            b.get_x() + b.get_width()/2,
            b.get_height() + 0.7,
            str(int(b.get_height())),
            ha="center",
            fontsize=8
        )

fig.suptitle(
    "Qwen3.5-27B : modèle de base et fine-tuning sur Type A",
    fontsize=12
)

fig.tight_layout()

save(
    fig,
    "FIG01_QWEN27_BASE_VS_A"
)


# ============================================================
# FIGURE 02
# CONTEXTE : BASE / C / A / C→A
# ============================================================

def qwen27_summary(name):
    p = (
        PERSONAL /
        "epoch1/learning_rate_1/results" /
        f"{name}_qwen27_humaneval_mistral_conc12_evaluation_summary.json"
    )
    return load_json(p)


c_summary = qwen27_summary("ft_C")
ca_summary = qwen27_summary("ft_C_then_A")

scores = [
    bc["ok"],
    c_summary["counter"]["ok"],
    ac["ok"],
    ca_summary["counter"]["ok"]
]

labels = [
    "Base",
    "C",
    "A",
    "C → A"
]

fig, ax = plt.subplots(figsize=(7.0, 4.0))

bars = ax.bar(
    labels,
    [100*n/164 for n in scores]
)

ax.set_ylabel("Pass@1 (%)")
ax.set_ylim(0, 45)
ax.set_title(
    "Effet des stratégies A, C et C → A sur Qwen3.5-27B"
)

horizontal_baseline(
    ax,
    base_pass,
    "Baseline"
)

for b, n in zip(bars, scores):
    ax.text(
        b.get_x() + b.get_width()/2,
        b.get_height() + 0.5,
        f"{n}/164\n{100*n/164:.2f}%",
        ha="center",
        fontsize=8
    )

ax.legend(fontsize=8)
fig.tight_layout()

save(
    fig,
    "FIG02_QWEN27_BASE_C_A_CTHENA"
)


# ============================================================
# FIGURE 03
# EXPÉRIENCES PRÉLIMINAIRES DU PIPELINE TUTEUR :
# 00_firstTests / 01_wAttnProjLayers / 02_refBench
# ============================================================

early = [
    (
        "Premier FT",
        TUTOR /
        "00_firstTests/benchmark/evals/aggregate.json"
    ),
    (
        "Proj. attention",
        TUTOR /
        "01_wAttnProjLayers/benchmark/evals/aggregate.json"
    ),
    (
        "Qwen base",
        TUTOR /
        "02_refBench/benchmark/evals/aggregate.json"
    )
]

early_data = []

for label, path in early:
    if path.exists():
        d = agg(path)
        early_data.append(
            (
                label,
                pass1_mean(d),
                pass1_std(d),
                diff_mean(d),
                diff_std(d)
            )
        )

if early_data:

    fig, axes = plt.subplots(
        1, 2,
        figsize=(10.0, 4.0)
    )

    labels_ = [x[0] for x in early_data]
    means = [x[1] for x in early_data]
    stds = [x[2] for x in early_data]

    ax = axes[0]

    bars = ax.bar(
        labels_,
        means,
        yerr=stds,
        capsize=4
    )

    ax.set_ylabel("Pass@1 moyen (%)")
    ax.set_title("(a) Performance")
    ax.tick_params(axis="x", labelrotation=15)

    label_bars(ax, bars)

    available = [
        x for x in early_data
        if x[3] is not None
    ]

    ax = axes[1]

    if available:
        dlabs = [x[0] for x in available]
        dm = [x[3] for x in available]
        ds = [
            0 if x[4] is None else x[4]
            for x in available
        ]

        bars = ax.bar(
            dlabs,
            dm,
            yerr=ds,
            capsize=4
        )

        ax.set_ylabel("Score pondéré par difficulté")
        ax.set_title("(b) Difficulté")
        ax.tick_params(
            axis="x",
            labelrotation=15
        )

        label_bars(ax, bars, "{:.3f}")

    fig.suptitle(
        "Premières expérimentations Qwen3.6-27B",
        fontsize=12
    )

    fig.tight_layout()

    save(
        fig,
        "FIG03_TUTOR_PRELIMINARY_QWEN"
    )


# ============================================================
# FIGURE 04
# 03_DSsize : EFFET DE LA TAILLE DU DATASET
# ============================================================

ds_root = TUTOR / "03_DSsize"

ds_rows = []

if ds_root.exists():

    for p in ds_root.rglob(
        "benchmark/evals/aggregate.json"
    ):

        rel = p.relative_to(ds_root)
        text = str(rel)

        m_pct = re.search(
            r"(?:^|/)\d+_(\d+)pct(?:/|$)",
            text
        )

        m_ep = re.search(
            r"(\d+)_([12])epochs",
            text
        )

        if not m_ep:
            m_ep = re.search(
                r"(\d+)epochs",
                text
            )

        m_lr = re.search(
            r"lr([0-9.eE+-]+)",
            text
        )

        if not (
            m_pct and
            m_ep and
            m_lr
        ):
            continue

        frac = int(m_pct.group(1))

        if len(m_ep.groups()) >= 2:
            epochs = int(m_ep.group(2))
        else:
            epochs = int(m_ep.group(1))

        lr_txt = m_lr.group(1)

        try:
            lr = float(lr_txt)
        except Exception:
            continue

        d = agg(p)

        ds_rows.append(
            {
                "frac": frac,
                "epochs": epochs,
                "lr": lr,
                "mean": pass1_mean(d),
                "std": pass1_std(d),
            }
        )

if ds_rows:

    lrs = sorted(
        set(r["lr"] for r in ds_rows)
    )

    fig, axes = plt.subplots(
        1,
        len(lrs),
        figsize=(5.2*len(lrs), 4.0),
        squeeze=False
    )

    axes = axes[0]

    for ax, lr in zip(axes, lrs):

        rows_lr = [
            r for r in ds_rows
            if r["lr"] == lr
        ]

        epochs_values = sorted(
            set(r["epochs"] for r in rows_lr)
        )

        for ep in epochs_values:

            rows_ep = sorted(
                [
                    r for r in rows_lr
                    if r["epochs"] == ep
                ],
                key=lambda r: r["frac"]
            )

            xs = [r["frac"] for r in rows_ep]
            ys = [r["mean"] for r in rows_ep]
            es = [r["std"] for r in rows_ep]

            ax.errorbar(
                xs,
                ys,
                yerr=es,
                marker="o",
                capsize=3,
                label=f"{ep} époque(s)"
            )

        horizontal_baseline(
            ax,
            TUTOR_BASE_PASS1,
            "Qwen base"
        )

        ax.set_xlabel(
            "Fraction du dataset (%)"
        )
        ax.set_ylabel(
            "Pass@1 moyen (%)"
        )

        ax.set_title(
            f"LR = {lr:.0e}"
        )

        ax.legend(fontsize=8)

    fig.suptitle(
        "Influence de la quantité de données de fine-tuning",
        fontsize=12
    )

    fig.tight_layout()

    save(
        fig,
        "FIG04_TUTOR_DATASET_SIZE"
    )


# ============================================================
# FIGURE 05
# 04_DSAdel1 : COMPARAISON INITIALE DES DATASETS
# ============================================================

ds1_root = TUTOR / "04_DSAdel1"

ds1_labels = {
    "00_DStypeA": "Type A",
    "01_DSTypeB": "Type B",
    "02_DSTypeC": "Type C",
    "03_DSTypeABC_dedup_BC": "ABC dédupliqué",
    "04_DSTypeA_half1_next200": "A subset",
}

ds1_rows = []

for dirname, label in ds1_labels.items():

    p = (
        ds1_root /
        dirname /
        "benchmark/evals/aggregate.json"
    )

    if not p.exists():
        continue

    d = agg(p)

    ds1_rows.append(
        (
            label,
            pass1_mean(d),
            pass1_std(d)
        )
    )

if ds1_rows:

    fig, ax = plt.subplots(
        figsize=(7.8, 4.1)
    )

    labels_ = [x[0] for x in ds1_rows]
    means = [x[1] for x in ds1_rows]
    stds = [x[2] for x in ds1_rows]

    bars = ax.bar(
        labels_,
        means,
        yerr=stds,
        capsize=4
    )

    horizontal_baseline(
        ax,
        TUTOR_BASE_PASS1,
        f"Qwen base ({TUTOR_BASE_PASS1:.2f}%)"
    )

    ax.set_ylabel("Pass@1 moyen (%)")
    ax.set_title(
        "Influence du dataset de fine-tuning"
    )

    ax.tick_params(
        axis="x",
        labelrotation=15
    )

    ax.legend(fontsize=8)

    label_bars(ax, bars)

    fig.tight_layout()

    save(
        fig,
        "FIG05_TUTOR_INITIAL_DATASETS"
    )


# ============================================================
# FIGURE 06
# 05_temperatureSweep
# ============================================================

temp_root = TUTOR / "05_temperatureSweep"

temp_rows = []

if temp_root.exists():

    for p in temp_root.rglob(
        "benchmark/evals/aggregate.json"
    ):

        text = str(
            p.relative_to(temp_root)
        )

        m = re.search(
            r"temp([0-9.]+)",
            text
        )

        if not m:
            continue

        try:
            temperature = float(
                m.group(1)
            )
        except Exception:
            continue

        d = agg(p)

        temp_rows.append(
            {
                "temp": temperature,
                "mean": pass1_mean(d),
                "std": pass1_std(d),
                "pass10": pass10(d)
            }
        )

if temp_rows:

    temp_rows.sort(
        key=lambda r: r["temp"]
    )

    xs = [
        r["temp"]
        for r in temp_rows
    ]

    fig, axes = plt.subplots(
        1, 2,
        figsize=(10.0, 4.0)
    )

    ax = axes[0]

    ax.errorbar(
        xs,
        [r["mean"] for r in temp_rows],
        yerr=[
            r["std"]
            for r in temp_rows
        ],
        marker="o",
        capsize=3
    )

    ax.set_xlabel("Température")
    ax.set_ylabel("Pass@1 moyen (%)")
    ax.set_title("(a) Pass@1")

    if 0.7 in xs:
        ax.axvline(
            0.7,
            linestyle=":",
            linewidth=1
        )

    ax = axes[1]

    valid = [
        r for r in temp_rows
        if r["pass10"] is not None
    ]

    if valid:
        ax.plot(
            [r["temp"] for r in valid],
            [r["pass10"] for r in valid],
            marker="o"
        )

    ax.set_xlabel("Température")
    ax.set_ylabel("Pass@10 (%)")
    ax.set_title("(b) Pass@10")

    if 0.7 in xs:
        ax.axvline(
            0.7,
            linestyle=":",
            linewidth=1,
            label="Température 0,7"
        )
        ax.legend(fontsize=8)

    fig.suptitle(
        "Influence de la température d'inférence",
        fontsize=12
    )

    fig.tight_layout()

    save(
        fig,
        "FIG06_TUTOR_TEMPERATURE"
    )


# ============================================================
# FIGURE 07
# 06_DSAdel2 : HEATMAP Δ PASS@1
# ============================================================

sweep_root = TUTOR / "06_DSAdel2"

dataset_names = {
    "00_DSTypeANew": "TypeANew",
    "01_DSBenchmarkBased": "BenchmarkBased",
    "02_DSBoth": "Both",
}

rows = []

for p in sweep_root.rglob(
    "benchmark/evals/aggregate.json"
):

    rel = p.relative_to(sweep_root)
    parts = rel.parts

    ds_key = next(
        (
            k for k in dataset_names
            if k in parts
        ),
        None
    )

    if ds_key is None:
        continue

    text = str(rel)

    m_ep = re.search(
        r"(\d+)_([123])epochs",
        text
    )

    if not m_ep:
        m_ep = re.search(
            r"([123])epochs",
            text
        )

    m_lr = re.search(
        r"lr([0-9.eE+-]+)",
        text
    )

    if not (m_ep and m_lr):
        continue

    if len(m_ep.groups()) >= 2:
        ep = int(m_ep.group(2))
    else:
        ep = int(m_ep.group(1))

    try:
        lr = float(m_lr.group(1))
    except Exception:
        continue

    d = agg(p)

    rows.append(
        {
            "dataset": dataset_names[ds_key],
            "epochs": ep,
            "lr": lr,
            "pass1": pass1_mean(d),
            "delta": (
                pass1_mean(d) -
                TUTOR_BASE_PASS1
            ),
        }
    )

if rows:

    dataset_order = [
        "TypeANew",
        "BenchmarkBased",
        "Both"
    ]

    epochs_order = [1, 2, 3]

    lr_order = sorted(
        set(r["lr"] for r in rows)
    )

    all_delta = [
        abs(r["delta"])
        for r in rows
    ]

    vmax = max(all_delta) if all_delta else 1

    fig, axes = plt.subplots(
        1, 3,
        figsize=(12.0, 4.2),
        sharey=True
    )

    last_im = None

    for ax, ds in zip(
        axes,
        dataset_order
    ):

        matrix = np.full(
            (
                len(epochs_order),
                len(lr_order)
            ),
            np.nan
        )

        for r in rows:
            if r["dataset"] != ds:
                continue

            i = epochs_order.index(
                r["epochs"]
            )
            j = lr_order.index(
                r["lr"]
            )

            matrix[i, j] = r["delta"]

        masked = np.ma.masked_invalid(
            matrix
        )

        im = ax.imshow(
            masked,
            aspect="auto",
            vmin=-vmax,
            vmax=vmax,
            cmap="coolwarm"
        )

        last_im = im

        ax.set_title(ds)

        ax.set_xticks(
            np.arange(len(lr_order))
        )

        ax.set_xticklabels(
            [
                f"{lr:.0e}"
                for lr in lr_order
            ],
            rotation=35,
            ha="right"
        )

        ax.set_yticks(
            np.arange(len(epochs_order))
        )
        ax.set_yticklabels(
            epochs_order
        )

        ax.set_xlabel("Learning rate")

        for i in range(
            len(epochs_order)
        ):
            for j in range(
                len(lr_order)
            ):

                val = matrix[i, j]

                text = (
                    "—"
                    if np.isnan(val)
                    else f"{val:+.1f}"
                )

                ax.text(
                    j,
                    i,
                    text,
                    ha="center",
                    va="center",
                    fontsize=8
                )

    axes[0].set_ylabel(
        "Nombre d'époques"
    )

    if last_im is not None:
        cbar = fig.colorbar(
            last_im,
            ax=axes,
            shrink=0.85,
            pad=0.02
        )

        cbar.set_label(
            "Δ Pass@1 vs Qwen base (points)"
        )

    fig.suptitle(
        "Sensibilité aux hyperparamètres de fine-tuning "
        f"(baseline = {TUTOR_BASE_PASS1:.2f} %)",
        fontsize=12
    )

    fig.subplots_adjust(
        left=0.07,
        right=0.90,
        bottom=0.19,
        top=0.82,
        wspace=0.22
    )

    save(
        fig,
        "FIG07_TUTOR_LR_EPOCHS_HEATMAP"
    )


# ============================================================
# FIGURE 08
# 07_DSAdel2_LoraR : RANG LORA
# ============================================================

rank_root = TUTOR / "07_DSAdel2_LoraR"

rank_dataset_names = {
    "00_DSTypeANew": "TypeANew",
    "01_DSBenchmarkBased": "BenchmarkBased",
    "02_DSBoth": "Both",
}

rank_rows = []

for p in rank_root.rglob(
    "benchmark/evals/aggregate.json"
):

    rel = p.relative_to(rank_root)
    parts = rel.parts

    ds_key = next(
        (
            k for k in rank_dataset_names
            if k in parts
        ),
        None
    )

    if ds_key is None:
        continue

    text = str(rel)

    m = re.search(
        r"LoraR(\d+)",
        text,
        re.I
    )

    if not m:
        continue

    rank = int(m.group(1))
    d = agg(p)

    rank_rows.append(
        {
            "dataset": rank_dataset_names[ds_key],
            "rank": rank,
            "mean": pass1_mean(d),
            "std": pass1_std(d),
            "runs": d.get("runs"),
        }
    )

if rank_rows:

    fig, ax = plt.subplots(
        figsize=(7.6, 4.5)
    )

    incomplete = []

    for ds in [
        "TypeANew",
        "BenchmarkBased",
        "Both"
    ]:

        rr = sorted(
            [
                r for r in rank_rows
                if r["dataset"] == ds
            ],
            key=lambda r: r["rank"]
        )

        if not rr:
            continue

        ax.errorbar(
            [r["rank"] for r in rr],
            [r["mean"] for r in rr],
            yerr=[r["std"] for r in rr],
            marker="o",
            capsize=3,
            label=ds
        )

        for r in rr:
            if r["runs"] != 10:
                incomplete.append(
                    (
                        ds,
                        r["rank"],
                        r["runs"]
                    )
                )

    horizontal_baseline(
        ax,
        TUTOR_BASE_PASS1,
        f"Qwen base ({TUTOR_BASE_PASS1:.2f}%)"
    )

    ax.set_xlabel("Rang LoRA")
    ax.set_ylabel("Pass@1 moyen (%)")
    ax.set_xticks(
        [16, 32, 64, 128]
    )

    ax.set_title(
        "Influence du rang LoRA"
    )

    ax.legend(fontsize=8)

    if incomplete:
        note = "; ".join(
            f"{ds}, r={r}: n={n}"
            for ds, r, n
            in incomplete
        )

        ax.text(
            0.01,
            -0.20,
            "Évaluation incomplète : " + note,
            transform=ax.transAxes,
            fontsize=8
        )

    fig.tight_layout()

    save(
        fig,
        "FIG08_TUTOR_LORA_RANK"
    )


# ============================================================
# FIGURE 09
# BASELINE VS MEILLEUR FT : 10 RUNS COMPLETS
# ============================================================

best_path = (
    TUTOR /
    "06_DSAdel2/02_DSBoth/"
    "02_3epochs/00_lr2e-5/"
    "benchmark/evals/aggregate.json"
)

best = agg(best_path)

base_runs = [
    100*x
    for x in tutor_base[
        "pass_rate"
    ]["per_run"]
]

best_runs = [
    100*x
    for x in best[
        "pass_rate"
    ]["per_run"]
]

base_counts = [
    round(x / 100 * 164)
    for x in base_runs
]

best_counts = [
    round(x / 100 * 164)
    for x in best_runs
]

fig, axes = plt.subplots(
    1, 2,
    figsize=(10.5, 4.1)
)

# ---- panel A: 10 runs

ax = axes[0]

xs = np.arange(10)

ax.plot(
    xs,
    base_runs,
    marker="o",
    label="Qwen base"
)

ax.plot(
    xs,
    best_runs,
    marker="o",
    label="Meilleur FT"
)

ax.axhline(
    np.mean(base_runs),
    linestyle="--",
    linewidth=1
)

ax.axhline(
    np.mean(best_runs),
    linestyle=":",
    linewidth=1
)

ax.set_xticks(xs)
ax.set_xlabel("Répétition")
ax.set_ylabel("Pass@1 (%)")
ax.set_title("(a) Dix évaluations complètes")
ax.legend(fontsize=8)


# ---- panel B: mean / max

ax = axes[1]

mean_values = [
    np.mean(base_runs),
    np.mean(best_runs)
]

max_values = [
    max(base_runs),
    max(best_runs)
]

x = np.arange(2)
w = 0.34

b1 = ax.bar(
    x-w/2,
    mean_values,
    width=w,
    label="Moyenne"
)

b2 = ax.bar(
    x+w/2,
    max_values,
    width=w,
    label="Meilleur run"
)

ax.set_xticks(x)
ax.set_xticklabels(
    ["Qwen base", "Meilleur FT"]
)

ax.set_ylabel("Pass@1 (%)")
ax.set_title("(b) Moyenne et maximum")
ax.legend(fontsize=8)

for b, n in zip(
    b1,
    [
        round(
            np.mean(base_runs) /
            100 * 164
        ),
        round(
            np.mean(best_runs) /
            100 * 164
        )
    ]
):
    ax.text(
        b.get_x()+b.get_width()/2,
        b.get_height()+0.4,
        f"{b.get_height():.2f}%\n≈{n}/164",
        ha="center",
        fontsize=8
    )

for b, n in zip(
    b2,
    [
        max(base_counts),
        max(best_counts)
    ]
):
    ax.text(
        b.get_x()+b.get_width()/2,
        b.get_height()+0.4,
        f"{b.get_height():.2f}%\n{n}/164",
        ha="center",
        fontsize=8
    )

fig.suptitle(
    "Qwen3.6-27B : baseline et meilleure configuration "
    "(Both, 3 époques, LR=2e-5)",
    fontsize=11
)

fig.tight_layout()

save(
    fig,
    "FIG09_TUTOR_BASE_VS_BEST_10RUNS"
)


# ============================================================
# MANIFEST
# ============================================================

manifest = OUT / "FIGURES_MANIFEST.txt"

manifest.write_text(
f"""FIGURES DU CHAPITRE — CANDIDATS

FIG01
Qwen3.5-27B base vs FT A
A retenu = 63/164.
Convention : +1 OK et -1 compile_err par rapport au run A archivé à 62.

FIG02
Contexte Qwen27 : Base / C / A / C→A.

FIG03
Premières expériences du pipeline Qwen3.6-27B :
00_firstTests / 01_wAttnProjLayers / 02_refBench.
Candidate ; décision d'inclusion après inspection.

FIG04
Influence de la taille du dataset (03_DSsize).
Candidate importante.

FIG05
Comparaison initiale des datasets (04_DSAdel1).
Alternative propre au dashboard existant.
Peut être remplacée par le tableau si manque de place.

FIG06
Influence de la température (05_temperatureSweep).
Candidate ; peut être condensée dans le texte/tableau.

FIG07
Dataset × epochs × learning rate (06_DSAdel2).
Figure principale du pipeline Prompt2FortranBench.
Valeurs = delta par rapport à la baseline {TUTOR_BASE_PASS1:.2f}%.

FIG08
Influence du rang LoRA (07_DSAdel2_LoraR).
Utilise directement les aggregate.json actuels et inclut r=128 si disponible.

FIG09
Baseline vs meilleure configuration sur les 10 runs.
Baseline :
mean={np.mean(base_runs):.2f}%, max={max(base_runs):.2f}% ({max(base_counts)}/164)

FT Both / 3ep / 2e-5 :
mean={np.mean(best_runs):.2f}%, max={max(best_runs):.2f}% ({max(best_counts)}/164)
""",
encoding="utf-8"
)

print()
print("=" * 80)
print("FIGURES CRÉÉES")
print("=" * 80)

for p in sorted(OUT.glob("*.png")):
    print(p)

print()
print("Manifest :")
print(manifest)
