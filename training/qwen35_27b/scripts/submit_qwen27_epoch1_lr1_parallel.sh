#!/usr/bin/env bash
set -euo pipefail

NEW_ROOT="/path/to/calypso/workdir/finetuning_qwen_27_b"
MANIFEST="$NEW_ROOT/qwen27_epoch1_lr1_runs.tsv"
SBATCH_SCRIPT="batch/train_eval_generic_qwen27.sbatch"
SUBMITTED="$NEW_ROOT/submitted_jobs_qwen27_epoch1_lr1.txt"

echo "======================================================================"
echo "SUBMIT QWEN3.5-27B — epoch1 / learning_rate_1"
echo "======================================================================"
echo "NEW_ROOT : $NEW_ROOT"
echo "MANIFEST : $MANIFEST"
echo "SBATCH   : $SBATCH_SCRIPT"
echo "======================================================================"

if [ ! -d "$NEW_ROOT" ]; then
  echo "ERROR: NEW_ROOT does not exist. Run prepare script first."
  exit 1
fi

if [ ! -f "$MANIFEST" ]; then
  echo "ERROR: manifest missing: $MANIFEST"
  exit 1
fi

cd "$NEW_ROOT"

if [ ! -f "$SBATCH_SCRIPT" ]; then
  echo "ERROR: sbatch script missing: $SBATCH_SCRIPT"
  exit 1
fi

echo
echo "[1/3] Dry validation"

python3 - << 'PY'
from pathlib import Path
import csv
import yaml

root = Path("/path/to/calypso/workdir/finetuning_qwen_27_b")
manifest = root / "qwen27_epoch1_lr1_runs.tsv"

rows = list(csv.DictReader(open(manifest, encoding="utf-8"), delimiter="\t"))

for row in rows:
    run = row["run_name"]
    cfg = root / row["config_path"]

    if not cfg.exists():
        raise SystemExit(f"Missing config for {run}: {cfg}")

    y = yaml.safe_load(open(cfg))

    data_paths = []
    ds = y.get("datasets") or y.get("dataset") or []
    if isinstance(ds, list):
        for item in ds:
            if isinstance(item, dict) and "path" in item:
                data_paths.append(Path(str(item["path"])))

    for p in data_paths:
        if not p.exists():
            raise SystemExit(f"Missing dataset for {run}: {p}")

    print(f"OK {run:35s} {cfg}")

print()
print("Total runs:", len(rows))
PY

echo
echo "[2/3] Submitting jobs"

: > "$SUBMITTED"

declare -A JOBIDS

submit_one() {
  local run="$1"
  local cfg="$2"
  local dep_run="$3"

  local short="${run#train_}"
  local job_name="q27_${short}"
  local dependency_arg=""

  if [ -n "$dep_run" ]; then
    dep_job="${JOBIDS[$dep_run]:-}"
    if [ -z "$dep_job" ]; then
      echo "ERROR: dependency job not submitted yet: $run depends on $dep_run"
      exit 1
    fi
    dependency_arg="--dependency=afterok:${dep_job}"
  fi

  echo "----------------------------------------------------------------------" | tee -a "$SUBMITTED"
  echo "RUN=$run" | tee -a "$SUBMITTED"
  echo "CFG=$cfg" | tee -a "$SUBMITTED"
  echo "DEP=${dep_run:-none}" | tee -a "$SUBMITTED"

  if [ -n "$dependency_arg" ]; then
    jid=$(sbatch --parsable "$dependency_arg" --job-name="$job_name" "$SBATCH_SCRIPT" "$run" "$cfg")
  else
    jid=$(sbatch --parsable --job-name="$job_name" "$SBATCH_SCRIPT" "$run" "$cfg")
  fi

  JOBIDS["$run"]="$jid"

  echo "JOBID=$jid" | tee -a "$SUBMITTED"
}

# Submit independent jobs first, skip dependent ones temporarily.
while IFS=$'\t' read -r run cfg dep; do
  if [ "$run" = "run_name" ]; then
    continue
  fi
  if [ -n "$dep" ]; then
    continue
  fi
  submit_one "$run" "$cfg" ""
done < "$MANIFEST"

# Submit dependent jobs after their parents are known.
while IFS=$'\t' read -r run cfg dep; do
  if [ "$run" = "run_name" ]; then
    continue
  fi
  if [ -z "$dep" ]; then
    continue
  fi
  submit_one "$run" "$cfg" "$dep"
done < "$MANIFEST"

echo
echo "[3/3] Summary"
echo "Submitted jobs:"
cat "$SUBMITTED"

echo
echo "Follow:"
echo "  squeue -u "$USER""
echo
echo "Logs:"
echo "  cd $NEW_ROOT"
echo "  ls logs"
echo "  tail -f logs/q27_A_*.out"
echo
echo "Errors:"
echo "  grep -iE \"error|exception|traceback|failed|oom|out of memory|killed|timeout\" logs/*.out logs/*.err"
echo "======================================================================"
