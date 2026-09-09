#!/usr/bin/env bash
set -euo pipefail

layout="qwen27/epoch1/learning_rate_1"

SOLUTIONS_DIR="$layout/results_qwen_lora/solutions"
RESULTS_DIR="$layout/results"
LOGS_DIR="$layout/logs"
TMP_DIR="$layout/tmp_missing_eval_solutions"

mkdir -p "$TMP_DIR" "$RESULTS_DIR" "$LOGS_DIR"
rm -f "$TMP_DIR"/*

echo
echo "======================================================================"
echo "Selecting Qwen27 FT generations not yet evaluated"
echo "======================================================================"

python - << PY
import json
from pathlib import Path

solutions_dir = Path("$SOLUTIONS_DIR")
results_dir = Path("$RESULTS_DIR")
tmp_dir = Path("$TMP_DIR")
tmp_dir.mkdir(parents=True, exist_ok=True)

selected = 0
already_done = 0
incomplete = 0
invalid = 0

solution_files = sorted(solutions_dir.glob("ft_*_qwen27_humaneval_mistral_conc12_solutions.json"))

print(f"FOUND_SOLUTIONS={len(solution_files)}")

for sol in solution_files:
    model_key = sol.name.replace("_solutions.json", "")

    summary = results_dir / f"{model_key}_evaluation_summary.json"
    details = results_dir / f"{model_key}_evaluation_details.json"
    logs = results_dir / f"{model_key}_evaluation_logs.json"

    if summary.exists() and details.exists() and logs.exists():
        already_done += 1
        print(f"ALREADY_EVALUATED ignored {sol.name}")
        continue

    try:
        data = json.load(open(sol, encoding="utf-8"))
        total = len(data)
        none = sum(x is None for x in data)
        trailing = bool(total > 0 and data[-1] is None)

        ok_extract = sum(1 for x in data if x and x.get("extraction_status") == "ok")
        empty_code = sum(1 for x in data if x and not x.get("code"))
        errors = sum(1 for x in data if x and x.get("error"))

        if total == 164 and none == 0 and not trailing:
            target = tmp_dir / sol.name
            if target.exists() or target.is_symlink():
                target.unlink()
            target.symlink_to(sol.resolve())
            selected += 1
            print(f"TO_EVALUATE selected total={total} ok_extract={ok_extract} empty_code={empty_code} errors={errors} {sol.name}")
        else:
            incomplete += 1
            print(f"INCOMPLETE ignored total={total} none={none} trailing={trailing} {sol.name}")

    except Exception as e:
        invalid += 1
        print(f"INVALID ignored {sol.name} error={e}")

print()
print(f"SELECTED_TO_EVALUATE={selected}")
print(f"ALREADY_EVALUATED={already_done}")
print(f"INCOMPLETE={incomplete}")
print(f"INVALID={invalid}")
PY

COUNT=$(find "$TMP_DIR" -maxdepth 1 -type l -name "ft_*_qwen27_humaneval_mistral_conc12_solutions.json" | wc -l)

echo
echo "Models selected for evaluation: $COUNT"

if [ "$COUNT" -eq 0 ]; then
  echo "Nothing new to evaluate."
  exit 0
fi

echo
echo "======================================================================"
echo "Launching evaluation only for missing Qwen27 FT models"
echo "======================================================================"

python evaluate_all_qwen_lora_solutions.py \
  --benchmark ../benchmark.json \
  --solutions-dir "$TMP_DIR" \
  --results-dir "$RESULTS_DIR" \
  --execution-time-limit 10 \
  2>&1 | tee -a "$LOGS_DIR/evaluate_missing_only_$(date +%Y%m%d_%H%M%S).log"

echo
echo "======================================================================"
echo "Done. Number of Qwen27 FT summaries:"
echo "======================================================================"

find "$RESULTS_DIR" \
  -maxdepth 1 \
  -type f \
  -name "ft_*_qwen27_humaneval_mistral_conc12_evaluation_summary.json" \
  | wc -l
