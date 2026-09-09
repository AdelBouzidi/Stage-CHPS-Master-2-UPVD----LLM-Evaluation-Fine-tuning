from pathlib import Path
import csv
import matplotlib.pyplot as plt

ROOT = Path("/path/to/project/results")
FIG = ROOT / "06_figures"
TAB = ROOT / "tables"

FIG.mkdir(parents=True, exist_ok=True)
TAB.mkdir(parents=True, exist_ok=True)

# ============================================================
# TABLEAU 1 — synthèse campagnes personnelles
# ============================================================

rows = [
    {
        "model": "Qwen3.5-9B",
        "baseline": "36/164",
        "num_finetunings": 71,
        "above_baseline": 4,
        "equal_baseline": 1,
        "below_baseline": 66,
        "configuration_retenue": "source_fortran_lang",
        "score_retenu": "41/164",
    },
    {
        "model": "Qwen3.5-27B",
        "baseline": "56/164",
        "num_finetunings": 45,
        "above_baseline": 12,
        "equal_baseline": 1,
        "below_baseline": 32,
        "configuration_retenue": "A",
        "score_retenu": "63/164",
    },
]

csv_path = TAB / "TABLE1_PERSONAL_CAMPAIGNS_SUMMARY.csv"

with csv_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

tex_path = TAB / "TABLE1_PERSONAL_CAMPAIGNS_SUMMARY.tex"

tex_path.write_text(
r"""\begin{table}[ht]
\centering
\caption{Synthèse des campagnes de fine-tuning du pipeline expérimental principal.}
\label{tab:personal_ft_summary}
\begin{tabular}{lrrrrl}
\hline
Modèle & Base & FT & $>$ base & $\leq$ base & Configuration retenue \\
\hline
Qwen3.5-9B  & 36/164 & 71 & 4  & 67 & 41/164 \\
Qwen3.5-27B & 56/164 & 45 & 12 & 33 & A : 63/164 \\
\hline
\end{tabular}
\end{table}
""",
encoding="utf-8"
)

# ============================================================
# FIGURE 1 — Qwen27 base vs FT A
# ============================================================

labels = ["Qwen3.5-27B\nbase", "FT sur A"]

ok = [56, 63]
total = 164
pass1 = [100 * n / total for n in ok]

gain_tasks = ok[1] - ok[0]
gain_points = pass1[1] - pass1[0]

fig, ax = plt.subplots(figsize=(6.0, 4.0))

bars = ax.bar(labels, pass1)

ax.set_ylabel("Pass@1 (%)")
ax.set_ylim(0, 45)
ax.set_title("Performance sur HumanEval Fortran")

for bar, n, pct in zip(bars, ok, pass1):
    ax.text(
        bar.get_x() + bar.get_width()/2,
        bar.get_height() + 0.6,
        f"{pct:.2f}%\n({n}/164)",
        ha="center",
        va="bottom",
        fontsize=10
    )

ax.text(
    0.5,
    42.0,
    f"Gain : +{gain_tasks} tâches / +{gain_points:.2f} points",
    ha="center",
    va="center",
    fontsize=10
)

fig.tight_layout()

png = FIG / "FIG1_QWEN27_BASE_VS_A_PASS1.png"
pdf = FIG / "FIG1_QWEN27_BASE_VS_A_PASS1.pdf"

fig.savefig(png, dpi=300, bbox_inches="tight")
fig.savefig(pdf, bbox_inches="tight")

plt.close(fig)

print("TABLEAU :", csv_path)
print("LATEX   :", tex_path)
print("FIGURE  :", png)
print()
print("Valeurs utilisées :")
print(f"Base = {ok[0]}/164 = {pass1[0]:.2f}%")
print(f"A    = {ok[1]}/164 = {pass1[1]:.2f}%")
print(f"Gain = +{gain_tasks} tâches / +{gain_points:.2f} points")
