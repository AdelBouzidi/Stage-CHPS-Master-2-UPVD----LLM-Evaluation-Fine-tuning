from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

OUTDIR = Path("/path/to/project/results/06_figures/chapter_results")
OUTDIR.mkdir(parents=True, exist_ok=True)

type_a_new = np.array([
    [ 1.4, -3.5,  np.nan,  np.nan],
    [ 1.6, -6.7, -7.4,   -14.2 ],
    [ np.nan, np.nan, -9.8, -31.5]
], dtype=float)

benchmark_based = np.array([
    [ 0.2,  0.7,  np.nan,  np.nan],
    [ 0.5,  1.0,   1.2,   -13.6 ],
    [ np.nan, np.nan, np.nan, -23.0]
], dtype=float)

both = np.array([
    [ 1.0, -2.4,  np.nan,  np.nan],
    [ 0.5,  0.5,  -0.1,   -25.5 ],
    [ 1.8,  np.nan, -6.8, -48.0]
], dtype=float)

datasets = [
    ("TypeANew", type_a_new),
    ("BenchmarkBased", benchmark_based),
    ("Both", both),
]

xlabels = ["2e-05", "2e-04", "3e-04", "5e-04"]
ylabels = ["1", "2", "3"]

all_values = np.concatenate([
    type_a_new[~np.isnan(type_a_new)],
    benchmark_based[~np.isnan(benchmark_based)],
    both[~np.isnan(both)],
])

vmin = np.min(all_values)
vmax = np.max(all_values)

cmap = plt.cm.coolwarm.copy()
cmap.set_bad(color="#f2f2f2")

fig = plt.figure(figsize=(13.5, 4.8))
gs = GridSpec(1, 4, width_ratios=[1, 1, 1, 0.05], wspace=0.35, figure=fig)

axes = [fig.add_subplot(gs[0, i]) for i in range(3)]
cax = fig.add_subplot(gs[0, 3])

images = []

for idx, (title, data) in enumerate(datasets):
    ax = axes[idx]
    im = ax.imshow(data, cmap=cmap, vmin=vmin, vmax=vmax, aspect="auto")
    images.append(im)

    ax.set_title(title, fontsize=12)
    ax.set_xticks(range(len(xlabels)))
    ax.set_xticklabels(xlabels, rotation=35, ha="right")
    ax.set_yticks(range(len(ylabels)))

    if idx == 0:
        ax.set_yticklabels(ylabels)
        ax.set_ylabel("Nombre d'époques", fontsize=11)
    else:
        ax.set_yticklabels([])

    ax.set_xlabel("Learning rate", fontsize=11)

    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            val = data[i, j]
            if np.isnan(val):
                ax.text(j, i, "—", ha="center", va="center", fontsize=11, color="#444444")
            else:
                ax.text(j, i, f"{val:+.1f}", ha="center", va="center", fontsize=10, color="#222222")

cb = fig.colorbar(images[-1], cax=cax)
cb.set_label("Δ Pass@1 vs Qwen base (points)", fontsize=11)

fig.suptitle(
    "Sensibilité aux hyperparamètres de fine-tuning (baseline = 48,17 %)",
    fontsize=14,
    y=1.02
)

fig.tight_layout()

png_path = OUTDIR / "FIG07_TUTOR_LR_EPOCHS_HEATMAP.png"
pdf_path = OUTDIR / "FIG07_TUTOR_LR_EPOCHS_HEATMAP.pdf"

fig.savefig(png_path, dpi=300, bbox_inches="tight")
fig.savefig(pdf_path, bbox_inches="tight")
plt.close(fig)

print("Figure recréée :")
print(png_path)
print(pdf_path)
