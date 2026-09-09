#!/bin/bash
#SBATCH --job-name=ft_eval
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=36
#SBATCH --time=12:00:00
#SBATCH --partition=grace

set -e
set -x

RUN_NAME=$1
CONFIG=$2

export WORKDIR=/path/to/calypso/workdir
export PROJECT=$WORKDIR/finetuning_domaines_eval
export IMG=/path/to/pytorch25.02.sif
export VENV=$WORKDIR/finetuning/axolotl_singularity_env
export TMPDIR=$WORKDIR/tmp
export PIP_CACHE_DIR=$WORKDIR/pip_cache

cd $PROJECT
mkdir -p logs outputs prepared results

echo "===== RUN INFO ====="
echo "RUN_NAME=$RUN_NAME"
echo "CONFIG=$CONFIG"
hostname
date
nvidia-smi

echo "===== CONFIG CHECK ====="
grep -E "base_model:|path:|dataset_prepared_path:|output_dir:|val_set_size:|num_epochs:|learning_rate:|evals_per_epoch:|shuffle_before_merging_datasets:|shuffle_merged_datasets:" $CONFIG

echo "===== CLEAN OLD RUN ====="
OUTDIR=$(grep "^output_dir:" $CONFIG | awk '{print $2}')
PREPDIR=$(grep "^dataset_prepared_path:" $CONFIG | awk '{print $2}')
rm -rf "$OUTDIR" "$PREPDIR"
rm -f logs/train_${RUN_NAME}.log logs/preprocess_${RUN_NAME}.log

echo "===== AXOLOTL PREPROCESS ====="
singularity exec --nv \
  --bind $WORKDIR:$WORKDIR \
  $IMG \
  bash -lc "
source $VENV/bin/activate
cd $PROJECT
axolotl preprocess $CONFIG 2>&1 | tee logs/preprocess_${RUN_NAME}.log
"

echo "===== AXOLOTL TRAIN ====="
singularity exec --nv \
  --bind $WORKDIR:$WORKDIR \
  $IMG \
  bash -lc "
source $VENV/bin/activate
cd $PROJECT
axolotl train $CONFIG 2>&1 | tee logs/train_${RUN_NAME}.log
"

echo "===== EXTRACT METRICS ====="
grep -E "'loss':|'eval_loss':|'train_loss':|Training completed|Model successfully saved" logs/train_${RUN_NAME}.log > results/metrics_${RUN_NAME}.txt || true

echo "===== DONE $RUN_NAME ====="
date
