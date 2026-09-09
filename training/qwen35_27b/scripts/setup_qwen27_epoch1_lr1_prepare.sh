#!/usr/bin/env bash
set -euo pipefail

ROOT="/path/to/calypso/workdir/finetuning_domaines_eval"
SRC_EPOCH1_LR1="${ROOT}/A_tailles_checking/learning1/epoch1"

NEW_ROOT="/path/to/calypso/workdir/finetuning_qwen_27_b"

SRC_MODEL="/path/to/shared/models/Qwen/Qwen3.5-27B"
DST_MODEL="/path/to/calypso/workdir/models/Qwen3.5-27B"

echo "======================================================================"
echo "PREPARE QWEN3.5-27B — epoch1 / learning_rate_1"
echo "======================================================================"
echo "ROOT          : $ROOT"
echo "SRC_EPOCH1_LR1: $SRC_EPOCH1_LR1"
echo "NEW_ROOT      : $NEW_ROOT"
echo "SRC_MODEL     : $SRC_MODEL"
echo "DST_MODEL     : $DST_MODEL"
echo "======================================================================"

cd "$ROOT"

echo
echo "[1/8] Safety checks"

if [ ! -d "$SRC_EPOCH1_LR1" ]; then
  echo "ERROR: source epoch1/lr1 project not found:"
  echo "  $SRC_EPOCH1_LR1"
  exit 1
fi

if [ -d "$NEW_ROOT" ]; then
  echo "ERROR: target project already exists:"
  echo "  $NEW_ROOT"
  echo
  echo "If you want to recreate it, remove it manually:"
  echo "  rm -rf $NEW_ROOT"
  exit 1
fi

if [ ! -d "$SRC_MODEL" ] && [ ! -d "$DST_MODEL" ]; then
  echo "ERROR: Qwen3.5-27B model not found."
  echo "Expected:"
  echo "  $SRC_MODEL"
  echo "or:"
  echo "  $DST_MODEL"
  exit 1
fi

echo "OK."

echo
echo "[2/8] Copy Qwen3.5-27B model if needed"

mkdir -p "$(dirname "$DST_MODEL")"

if [ -d "$DST_MODEL" ]; then
  echo "Model already exists:"
  echo "  $DST_MODEL"
else
  echo "Copying model..."
  rsync -a --info=progress2 "$SRC_MODEL/" "$DST_MODEL/"
fi

du -sh "$DST_MODEL" || true

echo
echo "[3/8] Create clean project"

mkdir -p "$NEW_ROOT"

for d in batch configs data dataset scripts notes logs outputs prepared results; do
  mkdir -p "$NEW_ROOT/$d"
done

# Main source for epoch1/lr1 campaign: it already contains A halves + by_source + main configs.
rsync -a "$SRC_EPOCH1_LR1/batch/"   "$NEW_ROOT/batch/"
rsync -a "$SRC_EPOCH1_LR1/configs/" "$NEW_ROOT/configs/"
rsync -a "$SRC_EPOCH1_LR1/data/"    "$NEW_ROOT/data/"
rsync -a "$SRC_EPOCH1_LR1/dataset/" "$NEW_ROOT/dataset/" 2>/dev/null || true
rsync -a "$SRC_EPOCH1_LR1/scripts/" "$NEW_ROOT/scripts/" 2>/dev/null || true
rsync -a "$SRC_EPOCH1_LR1/notes/"   "$NEW_ROOT/notes/" 2>/dev/null || true

# Add filtered GPT-120B datasets/configs created in the main project.
cp -a "$ROOT"/data/train_ABC_filtered_*_chat.jsonl "$NEW_ROOT/data/" 2>/dev/null || true
cp -a "$ROOT"/configs/qwen35-9b-ft-ABC_filtered_*.yaml "$NEW_ROOT/configs/" 2>/dev/null || true

if [ -d "$ROOT/filtered_observed_errors_gpt120b_v2_train_ABC_full" ]; then
  rsync -a "$ROOT/filtered_observed_errors_gpt120b_v2_train_ABC_full" "$NEW_ROOT/"
fi

echo "Created:"
echo "  $NEW_ROOT"

echo
echo "[4/8] Create missing filtered configs if needed"

python3 - << 'PY'
from pathlib import Path
import re

ROOT = Path("/path/to/calypso/workdir/finetuning_qwen_27_b")
BASE = ROOT / "configs/qwen35-9b-ft-ABC_dedup_BC.yaml"

filtered = {
    "ABC_filtered_accept": "train_ABC_filtered_accept_chat.jsonl",
    "ABC_filtered_manual": "train_ABC_filtered_manual_chat.jsonl",
    "ABC_filtered_reject": "train_ABC_filtered_reject_chat.jsonl",
}

def replace_or_add(text, key, value):
    pat = rf"(?m)^{re.escape(key)}:\s*.*$"
    line = f"{key}: {value}"
    if re.search(pat, text):
        return re.sub(pat, line, text, count=1)
    return text.rstrip() + "\n" + line + "\n"

def replace_first_dataset_path(text, value):
    pat = r"(?m)^(\s*-\s*path:\s*).*$"
    repl = f"  - path: {value}"
    if re.search(pat, text):
        return re.sub(pat, repl, text, count=1)
    raise RuntimeError("dataset '- path:' line not found")

if not BASE.exists():
    raise SystemExit(f"Missing base config: {BASE}")

base_text = BASE.read_text()

for run, data_file in filtered.items():
    out_cfg = ROOT / "configs" / f"qwen35-9b-ft-{run}.yaml"
    data_path = ROOT / "data" / data_file

    if out_cfg.exists():
        print("filtered config already exists:", out_cfg)
        continue

    if not data_path.exists():
        print("filtered data missing, skip:", data_path)
        continue

    text = base_text
    text = replace_first_dataset_path(text, data_path)
    text = replace_or_add(text, "dataset_prepared_path", ROOT / "prepared" / f"train_{run}")
    text = replace_or_add(text, "output_dir", ROOT / "outputs" / f"train_{run}")
    text = replace_or_add(text, "num_epochs", "1")
    text = replace_or_add(text, "learning_rate", "1e-4")
    text = replace_or_add(text, "val_set_size", "0.1")
    text = replace_or_add(text, "evals_per_epoch", "4")

    out_cfg.write_text(text)
    print("created filtered config:", out_cfg)
PY

echo
echo "[5/8] Create run manifest"

cat > "$NEW_ROOT/qwen27_epoch1_lr1_runs.tsv" << 'EOF'
run_nameconfig_pathdependency
train_AB_shuffle_epoch2_lr1.tar.gz configs/qwen35-9b-ft-A.yaml 
train_Bconfigs/qwen35-9b-ft-B.yaml
train_Cconfigs/qwen35-9b-ft-C.yaml
train_AB_antineighborconfigs/qwen35-9b-ft-AB_antineighbor.yaml
train_AC_antineighborconfigs/qwen35-9b-ft-AC_antineighbor.yaml
train_AB_shuffle_epoch2_lr1.tar.gz configs/qwen35-9b-ft-AB_shuffle.yaml 
train_AC_shuffleconfigs/qwen35-9b-ft-AC_shuffle.yaml
train_ABC_dedup_BCconfigs/qwen35-9b-ft-ABC_dedup_BC.yaml
train_ABC_Strongconfigs/qwen35-9b-ft-ABC_Strong.yaml
train_ABC_source_stack_v1configs/by_source/qwen35-9b-ft-ABC_source_stack_v1.yaml
train_ABC_source_stack_v2configs/by_source/qwen35-9b-ft-ABC_source_stack_v2.yaml
train_ABC_source_numericalhubconfigs/by_source/qwen35-9b-ft-ABC_source_numericalhub.yaml
train_ABC_source_burkardtconfigs/by_source/qwen35-9b-ft-ABC_source_burkardt.yaml
train_ABC_source_fortran_langconfigs/by_source/qwen35-9b-ft-ABC_source_fortran_lang.yaml
train_ABC_source_numerical_methodsconfigs/by_source/qwen35-9b-ft-ABC_source_numerical_methods.yaml
train_A_half1configs/A_tailles/qwen35-9b-ft-A_half1_learning1_epoch1.yaml
train_A_half2configs/A_tailles/qwen35-9b-ft-A_half2_learning1_epoch1.yaml
train_ABC_filtered_acceptconfigs/qwen35-9b-ft-ABC_filtered_accept.yaml
train_ABC_filtered_manualconfigs/qwen35-9b-ft-ABC_filtered_manual.yaml
train_ABC_filtered_rejectconfigs/qwen35-9b-ft-ABC_filtered_reject.yaml
train_B_then_Aconfigs/qwen35-9b-ft-B_then_A.yamltrain_B
train_C_then_Aconfigs/qwen35-9b-ft-C_then_A.yamltrain_C
EOF

cat "$NEW_ROOT/qwen27_epoch1_lr1_runs.tsv"

echo
echo "[6/8] Rewrite configs for isolated Qwen27 campaign"

python3 - << 'PY'
from pathlib import Path
import re
import csv

OLD_ROOT = Path("/path/to/calypso/workdir/finetuning_domaines_eval")
SRC_EPOCH1_LR1 = OLD_ROOT / "A_tailles_checking/learning1/epoch1"
NEW_ROOT = Path("/path/to/calypso/workdir/finetuning_qwen_27_b")
DST_MODEL = Path("/path/to/calypso/workdir/models/Qwen3.5-27B")
MANIFEST = NEW_ROOT / "qwen27_epoch1_lr1_runs.tsv"

def replace_or_add(text, key, value):
    value = str(value)
    pat = rf"(?m)^{re.escape(key)}:\s*.*$"
    line = f"{key}: {value}"
    if re.search(pat, text):
        return re.sub(pat, line, text, count=1)
    return text.rstrip() + "\n" + line + "\n"

rows = list(csv.DictReader(open(MANIFEST, encoding="utf-8"), delimiter="\t"))

for row in rows:
    run = row["run_name"]
    cfg_rel = row["config_path"]
    cfg_path = NEW_ROOT / cfg_rel

    if not cfg_path.exists():
        raise SystemExit(f"Missing config for {run}: {cfg_path}")

    text = cfg_path.read_text()

    # Redirect every known old root to the new isolated project.
    text = text.replace(str(SRC_EPOCH1_LR1), str(NEW_ROOT))
    text = text.replace(str(OLD_ROOT), str(NEW_ROOT))

    text = replace_or_add(text, "base_model", DST_MODEL)
    text = replace_or_add(text, "num_epochs", "1")
    text = replace_or_add(text, "learning_rate", "1e-4")
    text = replace_or_add(text, "dataset_prepared_path", NEW_ROOT / "prepared" / run)
    text = replace_or_add(text, "output_dir", NEW_ROOT / "outputs" / run)

    if run == "train_B_then_A":
        text = replace_or_add(text, "lora_model_dir", NEW_ROOT / "outputs" / "train_B")

    if run == "train_C_then_A":
        text = replace_or_add(text, "lora_model_dir", NEW_ROOT / "outputs" / "train_C")

    cfg_path.write_text(text)

    print("=" * 80)
    print("RUN:", run)
    print("CFG:", cfg_path)
    for key in [
        "base_model",
        "dataset_prepared_path",
        "output_dir",
        "lora_model_dir",
        "num_epochs",
        "learning_rate",
        "val_set_size",
        "evals_per_epoch",
    ]:
        m = re.search(rf"(?m)^{key}:\s*(.*)$", text)
        if m:
            print(f"{key}: {m.group(1)}")
PY

echo
echo "[7/8] Create Qwen27 Slurm batch"

cat > "$NEW_ROOT/batch/train_eval_generic_qwen27.sbatch" << 'SBATCH'
#!/usr/bin/env bash
#SBATCH --partition=grace
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=36
#SBATCH --time=24:00:00
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err

set -euo pipefail

RUN_NAME="${1:?RUN_NAME required}"
CONFIG="${2:?CONFIG required}"

PROJECT="/path/to/calypso/workdir/finetuning_qwen_27_b"

cd "$PROJECT"

echo "======================================================================"
echo "Qwen27 fine-tuning"
echo "======================================================================"
echo "Date     : $(date)"
echo "Host     : $(hostname)"
echo "RUN_NAME : $RUN_NAME"
echo "CONFIG   : $CONFIG"
echo "PROJECT  : $PROJECT"
echo "CUDA     : ${CUDA_VISIBLE_DEVICES:-none}"
echo "======================================================================"

nvidia-smi || true

SIF="/path/to/pytorch25.02.sif"
VENV="/path/to/calypso/workdir/finetuning/axolotl_singularity_env"

if [ ! -f "$SIF" ]; then
  echo "ERROR: Singularity image not found: $SIF"
  exit 1
fi

if [ ! -d "$VENV" ]; then
  echo "ERROR: Axolotl venv not found: $VENV"
  exit 1
fi

OUT_DIR="$(python3 - << PY
import yaml
cfg = yaml.safe_load(open("$CONFIG"))
print(cfg.get("output_dir", ""))
PY
)"

PREP_DIR="$(python3 - << PY
import yaml
cfg = yaml.safe_load(open("$CONFIG"))
print(cfg.get("dataset_prepared_path", ""))
PY
)"

echo "Output dir   : $OUT_DIR"
echo "Prepared dir : $PREP_DIR"

rm -rf "$OUT_DIR" "$PREP_DIR"

mkdir -p logs outputs prepared results

singularity exec --nv "$SIF" bash -lc "
  set -euo pipefail
  source '$VENV/bin/activate'
  cd '$PROJECT'

  echo 'Axolotl version:'
  axolotl --version || true

  echo
  echo 'Preprocess...'
  axolotl preprocess '$CONFIG' 2>&1 | tee 'logs/preprocess_${RUN_NAME}.log'

  echo
  echo 'Train...'
  axolotl train '$CONFIG' 2>&1 | tee 'logs/train_${RUN_NAME}.log'
"

METRICS="results/metrics_${RUN_NAME}.txt"
{
  echo "RUN_NAME=$RUN_NAME"
  echo "CONFIG=$CONFIG"
  echo "DATE=$(date)"
  echo
  echo "=== eval_loss ==="
  grep -h "eval_loss" "logs/train_${RUN_NAME}.log" || true
  echo
  echo "=== train_loss ==="
  grep -h "train_loss" "logs/train_${RUN_NAME}.log" || true
  echo
  echo "=== possible errors ==="
  grep -iE "error|exception|traceback|failed|oom|out of memory|killed|timeout" "logs/train_${RUN_NAME}.log" || true
} > "$METRICS"

echo "Metrics saved to $METRICS"
echo "Done: $(date)"
SBATCH

chmod +x "$NEW_ROOT/batch/train_eval_generic_qwen27.sbatch"

echo
echo "[8/8] Final validation"

python3 - << 'PY'
from pathlib import Path
import csv
import yaml
import re

NEW_ROOT = Path("/path/to/calypso/workdir/finetuning_qwen_27_b")
DST_MODEL = "/path/to/calypso/workdir/models/Qwen3.5-27B"
MANIFEST = NEW_ROOT / "qwen27_epoch1_lr1_runs.tsv"

rows = list(csv.DictReader(open(MANIFEST, encoding="utf-8"), delimiter="\t"))

errors = []

for row in rows:
    run = row["run_name"]
    cfg_rel = row["config_path"]
    cfg = NEW_ROOT / cfg_rel

    if not cfg.exists():
        errors.append(f"missing config: {run} {cfg}")
        continue

    text = cfg.read_text()
    y = yaml.safe_load(open(cfg))

    if y.get("base_model") != DST_MODEL:
        errors.append(f"bad base_model: {run} -> {y.get('base_model')}")

    if str(NEW_ROOT) not in str(y.get("output_dir", "")):
        errors.append(f"bad output_dir: {run}")

    if str(NEW_ROOT) not in str(y.get("dataset_prepared_path", "")):
        errors.append(f"bad prepared path: {run}")

    if str(y.get("num_epochs")) != "1":
        errors.append(f"bad num_epochs: {run} -> {y.get('num_epochs')}")

    if str(y.get("learning_rate")) not in {"0.0001", "1e-4", "1e-04"}:
        errors.append(f"bad learning_rate: {run} -> {y.get('learning_rate')}")

    if "/finetuning_domaines_eval/" in text:
        errors.append(f"old root remains in config: {run}")

if errors:
    print("VALIDATION ERRORS:")
    for e in errors:
        print(" -", e)
    raise SystemExit(1)

print("Validation OK.")
print("Runs:", len(rows))
PY

echo
echo "======================================================================"
echo "PREPARATION DONE"
echo "New project:"
echo "  $NEW_ROOT"
echo
echo "Next step:"
echo "  cd $NEW_ROOT"
echo "  bash submit_qwen27_epoch1_lr1_parallel.sh"
echo "======================================================================"
