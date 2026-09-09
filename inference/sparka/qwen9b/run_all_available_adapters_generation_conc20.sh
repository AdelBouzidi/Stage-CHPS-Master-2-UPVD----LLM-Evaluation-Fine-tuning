#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# Generate HumanEval Fortran solutions for all available structured LoRA adapters
#
# Machine:
#   Sparka
#
# Adapters layout:
#   /path/to/sparka/workdir/vllm_qwen_lora/adapters/
#     epoch1/learning_rate_1/<adapter>
#     epoch1/learning_rate_2/<adapter>
#     epoch2/learning_rate_1/<adapter>
#     epoch2/learning_rate_2/<adapter>
#
# Evaluation output layout inside adel_recover:
#   evaluation_finetuning/
#     epoch1/learning_rate_1/results_qwen_lora/solutions/
#     epoch1/learning_rate_1/logs/
#     epoch1/learning_rate_2/results_qwen_lora/solutions/
#     epoch1/learning_rate_2/logs/
#     epoch2/learning_rate_1/results_qwen_lora/solutions/
#     epoch2/learning_rate_1/logs/
#     epoch2/learning_rate_2/results_qwen_lora/solutions/
#     epoch2/learning_rate_2/logs/
#
# Logic:
#   - scan structured adapter folders
#   - verify adapter_model.safetensors + adapter_config.json
#   - skip generation if output JSON is already complete
#   - load one adapter at a time into vLLM
#   - generate with --concurrency 20
#   - write outputs directly into the correct epoch/learning_rate folder
#
# Usage:
#   chmod +x run_all_available_adapters_generation_conc20.sh
#   ./run_all_available_adapters_generation_conc20.sh
#
# Optional:
#   FORCE_REGENERATE=1 ./run_all_available_adapters_generation_conc20.sh
###############################################################################

VLLM_PROJECT_DIR="/path/to/sparka/workdir/vllm_qwen_lora_server"
VLLM_PROJECT_NAME="qwen_lora_eval"

ADAPTERS_ROOT="/path/to/sparka/workdir/vllm_qwen_lora/adapters"

CONTAINER_NAME="adel_recover"
EVAL_DIR="/home/evaluator/workspace/Fortran-HumanEval_Adel/__sandbox_adel__/evaluation_finetuning"

HOST_BASE_URL="http://localhost:8087"
CONTAINER_BASE_URL="http://localhost:8087"

BENCHMARK="../benchmark.json"

MODEL_FAMILY="mistral"
TEMPERATURE="0"
TOP_P="1"
MAX_TOKENS="2048"
CONCURRENCY="20"

# Default behavior:
#   0 = skip already complete generations
#   1 = regenerate even if output exists and is complete
FORCE_REGENERATE="${FORCE_REGENERATE:-0}"

LAYOUTS=(
  "epoch1/learning_rate_1"
  "epoch1/learning_rate_2"
  "epoch2/learning_rate_1"
  "epoch2/learning_rate_2"
)

echo "======================================================================"
echo "RUN ALL STRUCTURED LORA ADAPTERS - HUMANEVAL GENERATION"
echo "======================================================================"
echo "VLLM_PROJECT_DIR   : ${VLLM_PROJECT_DIR}"
echo "ADAPTERS_ROOT      : ${ADAPTERS_ROOT}"
echo "CONTAINER_NAME     : ${CONTAINER_NAME}"
echo "EVAL_DIR           : ${EVAL_DIR}"
echo "HOST_BASE_URL      : ${HOST_BASE_URL}"
echo "CONTAINER_BASE_URL : ${CONTAINER_BASE_URL}"
echo "BENCHMARK          : ${BENCHMARK}"
echo "MODEL_FAMILY       : ${MODEL_FAMILY}"
echo "TEMPERATURE        : ${TEMPERATURE}"
echo "TOP_P              : ${TOP_P}"
echo "MAX_TOKENS         : ${MAX_TOKENS}"
echo "CONCURRENCY        : ${CONCURRENCY}"
echo "FORCE_REGENERATE   : ${FORCE_REGENERATE}"
echo "======================================================================"
echo ""

###############################################################################
# 0. Basic checks
###############################################################################

echo "[0/9] Basic checks..."

if [ ! -d "${VLLM_PROJECT_DIR}" ]; then
  echo "ERROR: vLLM project directory not found:"
  echo "  ${VLLM_PROJECT_DIR}"
  exit 1
fi

if [ ! -d "${ADAPTERS_ROOT}" ]; then
  echo "ERROR: adapters root not found:"
  echo "  ${ADAPTERS_ROOT}"
  exit 1
fi

cd "${VLLM_PROJECT_DIR}"

if [ ! -f "./set_lora_adapter.sh" ]; then
  echo "ERROR: set_lora_adapter.sh not found in:"
  echo "  ${VLLM_PROJECT_DIR}"
  exit 1
fi

chmod +x ./set_lora_adapter.sh

if ! docker ps --format '{{.Names}}' | grep -qx "${CONTAINER_NAME}"; then
  echo "ERROR: Docker container '${CONTAINER_NAME}' is not running."
  echo "Current containers:"
  docker ps
  exit 1
fi

docker exec "${CONTAINER_NAME}" bash -lc "
  cd '${EVAL_DIR}'
  test -f generate_with_vllm_lora.py
  test -f '${BENCHMARK}'
"

for layout in "${LAYOUTS[@]}"; do
  mkdir -p "${ADAPTERS_ROOT}/${layout}"
done

echo "OK."
echo ""

###############################################################################
# Helper functions
###############################################################################

model_name_from_adapter() {
  local adapter_basename="$1"

  if [[ "${adapter_basename}" == train_* ]]; then
    echo "ft_${adapter_basename#train_}"
  else
    echo "ft_${adapter_basename}"
  fi
}

check_output_status() {
  local output_file="$1"

  docker exec "${CONTAINER_NAME}" bash -lc "
    cd '${EVAL_DIR}'

    if [ ! -f '${output_file}' ]; then
      echo 'missing'
      exit 0
    fi

    python - << 'PY'
import json

p = '${output_file}'

try:
    data = json.load(open(p))
except Exception:
    print('invalid_json')
    raise SystemExit(0)

if not isinstance(data, list):
    print('not_list')
    raise SystemExit(0)

total = len(data)
none = sum(1 for x in data if x is None)
trailing_null = bool(total > 0 and data[-1] is None)
errors = sum(1 for x in data if x and x.get('error'))
empty = sum(1 for x in data if x and not x.get('code'))
ok = sum(1 for x in data if x and x.get('extraction_status') == 'ok')

if total == 164 and none == 0 and not trailing_null:
    print(f'complete_total_{total}_ok_{ok}_empty_{empty}_errors_{errors}')
else:
    print(f'incomplete_total_{total}_none_{none}_trailing_null_{trailing_null}_ok_{ok}_empty_{empty}_errors_{errors}')
PY
  " | tail -n 1
}

wait_for_vllm_health() {
  echo "Waiting for vLLM health endpoint..."

  for i in $(seq 1 120); do
    if curl -fsS "${HOST_BASE_URL}/health" >/dev/null 2>&1; then
      echo "vLLM is healthy."
      return 0
    fi

    echo "  waiting... ${i}/120"
    sleep 5
  done

  echo "ERROR: vLLM did not become healthy."
  docker logs --tail 200 vllm-qwen35-9b-lora || true
  return 1
}

check_model_exposed_host() {
  local model_name="$1"
  local models_json

  models_json="$(curl -fsS "${HOST_BASE_URL}/v1/models")"

  echo "${models_json}" | python3 -m json.tool

  MODEL_CHECK_JSON="${models_json}" MODEL_WANTED="${model_name}" python3 -c '
import json
import os
import sys

data = json.loads(os.environ["MODEL_CHECK_JSON"])
wanted = os.environ["MODEL_WANTED"]
ids = [x.get("id") for x in data.get("data", [])]

print("Available models:", ids)

sys.exit(0 if wanted in ids else 1)
'
}


check_model_exposed_container() {
  local model_name="$1"

  docker exec "${CONTAINER_NAME}" bash -lc "
    models_json=\$(curl -fsS '${CONTAINER_BASE_URL}/v1/models')

    echo \"\${models_json}\" | python3 -m json.tool

    MODEL_CHECK_JSON=\"\${models_json}\" MODEL_WANTED='${model_name}' python3 -c '
import json
import os
import sys

data = json.loads(os.environ[\"MODEL_CHECK_JSON\"])
wanted = os.environ[\"MODEL_WANTED\"]
ids = [x.get(\"id\") for x in data.get(\"data\", [])]

print(\"Available models:\", ids)

sys.exit(0 if wanted in ids else 1)
'
  "
}


backup_existing_file() {
  local file_path="$1"

  docker exec "${CONTAINER_NAME}" bash -lc "
    cd '${EVAL_DIR}'

    if [ -f '${file_path}' ]; then
      ts=\$(date +%Y%m%d_%H%M%S)
      echo 'Backing up ${file_path} -> ${file_path}.bak_'\${ts}
      mv '${file_path}' '${file_path}.bak_'\${ts}
    fi
  "
}

final_json_summary() {
  local output_file="$1"

  docker exec "${CONTAINER_NAME}" bash -lc "
    cd '${EVAL_DIR}'

    python - << 'PY'
import json

p = '${output_file}'

print('file:', p)

try:
    data = json.load(open(p))
except Exception as e:
    print('ERROR: invalid JSON:', e)
    raise SystemExit(1)

total = len(data)
none = sum(1 for x in data if x is None)
trailing_null = bool(total > 0 and data[-1] is None)
ok = sum(1 for x in data if x and x.get('extraction_status') == 'ok')
warn = sum(1 for x in data if x and x.get('extraction_status') != 'ok')
empty = sum(1 for x in data if x and not x.get('code'))
errors = sum(1 for x in data if x and x.get('error'))

print('total:', total)
print('none:', none)
print('trailing_null:', trailing_null)
print('ok_extractions:', ok)
print('warnings:', warn)
print('empty_code:', empty)
print('errors:', errors)

if total != 164 or none != 0 or trailing_null:
    raise SystemExit(2)
PY
  "
}

cleanup_alias() {
  local alias_name="$1"
  local alias_path="${ADAPTERS_ROOT}/${alias_name}"

  if [ -L "${alias_path}" ]; then
    rm -f "${alias_path}"
  fi
}

create_flat_alias_for_adapter() {
  local adapter_basename="$1"
  local adapter_rel_path="$2"

  local alias_path="${ADAPTERS_ROOT}/${adapter_basename}"

  if [ -e "${alias_path}" ] && [ ! -L "${alias_path}" ]; then
    echo "ERROR: flat adapter alias path already exists and is not a symlink:"
    echo "  ${alias_path}"
    echo "Move this directory into the structured layout first."
    return 1
  fi

  rm -f "${alias_path}"

  # Relative symlink, so it works inside Docker mount as /adapters/<alias>.
  ln -s "${adapter_rel_path}" "${alias_path}"

  echo "Created temporary adapter alias:"
  echo "  ${alias_path} -> ${adapter_rel_path}"
}

###############################################################################
# 1. Discover structured adapters
###############################################################################

echo "[1/9] Discovering structured adapters..."

ADAPTER_RECORDS=()
INVALID_RECORDS=()

for layout in "${LAYOUTS[@]}"; do
  layout_dir="${ADAPTERS_ROOT}/${layout}"

  echo "Scanning: ${layout_dir}"

  while IFS= read -r adapter_dir; do
    [ -n "${adapter_dir}" ] || continue

    adapter_basename="$(basename "${adapter_dir}")"
    adapter_rel_path="${layout}/${adapter_basename}"

    # Skip backup / non-experimental adapters
    if [[ "${adapter_basename}" == *"backup"* ]]; then
      echo "  SKIP backup adapter: ${layout}/${adapter_basename}"
      continue
    fi

    if [ -f "${adapter_dir}/adapter_model.safetensors" ] && [ -f "${adapter_dir}/adapter_config.json" ]; then
      ADAPTER_RECORDS+=("${layout}|${adapter_basename}|${adapter_rel_path}")
    else
      INVALID_RECORDS+=("${layout}|${adapter_basename}|${adapter_rel_path}")
    fi
  done < <(find "${layout_dir}" -mindepth 1 -maxdepth 1 -type d | sort)
done

echo ""
echo "Valid structured adapters     : ${#ADAPTER_RECORDS[@]}"
echo "Invalid/incomplete structured : ${#INVALID_RECORDS[@]}"
echo ""

if [ "${#ADAPTER_RECORDS[@]}" -gt 0 ]; then
  echo "Valid adapters:"
  for rec in "${ADAPTER_RECORDS[@]}"; do
    IFS="|" read -r layout adapter_basename adapter_rel_path <<< "${rec}"
    echo "  - ${layout}/${adapter_basename}"
  done
fi

if [ "${#INVALID_RECORDS[@]}" -gt 0 ]; then
  echo ""
  echo "Incomplete adapters skipped:"
  for rec in "${INVALID_RECORDS[@]}"; do
    IFS="|" read -r layout adapter_basename adapter_rel_path <<< "${rec}"
    echo "  - ${layout}/${adapter_basename}"
  done
fi

if [ "${#ADAPTER_RECORDS[@]}" -eq 0 ]; then
  echo "ERROR: no valid structured adapter found."
  echo "Expected examples:"
  echo "  ${ADAPTERS_ROOT}/epoch1/learning_rate_1/train_B"
  echo "  ${ADAPTERS_ROOT}/epoch2/learning_rate_2/train_A"
  exit 1
fi

echo ""

###############################################################################
# 2. Main loop
###############################################################################

SUCCESS_ADAPTERS=()
FAILED_ADAPTERS=()
SKIPPED_ADAPTERS=()

for rec in "${ADAPTER_RECORDS[@]}"; do
  IFS="|" read -r LAYOUT ADAPTER_BASENAME ADAPTER_REL_PATH <<< "${rec}"

  MODEL_NAME="$(model_name_from_adapter "${ADAPTER_BASENAME}")"

  OUTPUT_BASE="${LAYOUT}"
  OUTPUT_FILE="${OUTPUT_BASE}/results_qwen_lora/solutions/${MODEL_NAME}_humaneval_${MODEL_FAMILY}_conc${CONCURRENCY}_solutions.json"
  LOG_FILE="${OUTPUT_BASE}/logs/${MODEL_NAME}_humaneval_${MODEL_FAMILY}_conc${CONCURRENCY}_generation.log"

  ADAPTER_DIR="${ADAPTERS_ROOT}/${ADAPTER_REL_PATH}"

  echo ""
  echo "======================================================================"
  echo "ADAPTER GENERATION"
  echo "======================================================================"
  echo "Layout      : ${LAYOUT}"
  echo "Adapter     : ${ADAPTER_BASENAME}"
  echo "Adapter rel : ${ADAPTER_REL_PATH}"
  echo "vLLM model  : ${MODEL_NAME}"
  echo "Adapter dir : ${ADAPTER_DIR}"
  echo "Output file : ${OUTPUT_FILE}"
  echo "Log file    : ${LOG_FILE}"
  echo "======================================================================"
  echo ""

  echo "[2/9] Existing output status..."

  OUTPUT_STATUS="$(check_output_status "${OUTPUT_FILE}")"
  echo "Output status: ${OUTPUT_STATUS}"

  if [ "${FORCE_REGENERATE}" != "1" ] && [[ "${OUTPUT_STATUS}" == complete_total_* ]]; then
    echo "Generation already complete. Skipping ${LAYOUT}/${ADAPTER_BASENAME}."
    SKIPPED_ADAPTERS+=("${LAYOUT}/${ADAPTER_BASENAME}")
    continue
  fi

  echo ""

  echo "[3/9] Preparing temporary flat adapter alias..."

  cleanup_alias "${ADAPTER_BASENAME}"

  if ! create_flat_alias_for_adapter "${ADAPTER_BASENAME}" "${ADAPTER_REL_PATH}"; then
    FAILED_ADAPTERS+=("${LAYOUT}/${ADAPTER_BASENAME}:alias_failed")
    continue
  fi

  echo ""

  echo "[4/9] Switching vLLM adapter..."

  cd "${VLLM_PROJECT_DIR}"

  if ! ./set_lora_adapter.sh "${ADAPTER_BASENAME}"; then
    echo "ERROR: set_lora_adapter.sh failed for ${ADAPTER_BASENAME}"
    cleanup_alias "${ADAPTER_BASENAME}"
    FAILED_ADAPTERS+=("${LAYOUT}/${ADAPTER_BASENAME}:set_lora_failed")
    continue
  fi

  echo ""

  echo "[5/9] Restarting vLLM..."

  docker compose -p "${VLLM_PROJECT_NAME}" down
  docker compose -p "${VLLM_PROJECT_NAME}" up -d

  if ! wait_for_vllm_health; then
    cleanup_alias "${ADAPTER_BASENAME}"
    FAILED_ADAPTERS+=("${LAYOUT}/${ADAPTER_BASENAME}:vllm_not_healthy")
    continue
  fi

  echo ""

  echo "[6/9] Checking model exposed from host..."

  if ! check_model_exposed_host "${MODEL_NAME}"; then
    echo "ERROR: model ${MODEL_NAME} is not exposed from host."
    docker logs --tail 150 vllm-qwen35-9b-lora || true
    cleanup_alias "${ADAPTER_BASENAME}"
    FAILED_ADAPTERS+=("${LAYOUT}/${ADAPTER_BASENAME}:model_not_exposed_host")
    continue
  fi

  echo "OK: ${MODEL_NAME} exposed from host."
  echo ""

  echo "[7/9] Checking model exposed from adel_recover..."

  if ! check_model_exposed_container "${MODEL_NAME}"; then
    echo "ERROR: model ${MODEL_NAME} is not reachable from adel_recover."
    cleanup_alias "${ADAPTER_BASENAME}"
    FAILED_ADAPTERS+=("${LAYOUT}/${ADAPTER_BASENAME}:model_not_reachable_container")
    continue
  fi

  echo "OK: ${MODEL_NAME} reachable from adel_recover."
  echo ""

  echo "[8/9] Preparing output/log files..."

  docker exec "${CONTAINER_NAME}" bash -lc "
    cd '${EVAL_DIR}'
    mkdir -p '${OUTPUT_BASE}/results_qwen_lora/solutions'
    mkdir -p '${OUTPUT_BASE}/logs'
  "

  if [ "${FORCE_REGENERATE}" = "1" ]; then
    backup_existing_file "${OUTPUT_FILE}"
    backup_existing_file "${LOG_FILE}"
  else
    # If incomplete files exist, keep them as backups before regenerating.
    if [[ "${OUTPUT_STATUS}" != "missing" ]]; then
      backup_existing_file "${OUTPUT_FILE}"
      backup_existing_file "${LOG_FILE}"
    fi
  fi

  echo ""

  echo "[9/9] Launching generation with concurrency=${CONCURRENCY}..."

  if docker exec -i "${CONTAINER_NAME}" bash -lc "
    set -euo pipefail
    cd '${EVAL_DIR}'

    python generate_with_vllm_lora.py \
      --benchmark '${BENCHMARK}' \
      --model '${MODEL_NAME}' \
      --base-url '${CONTAINER_BASE_URL}' \
      --output '${OUTPUT_FILE}' \
      --model-family '${MODEL_FAMILY}' \
      --temperature '${TEMPERATURE}' \
      --top-p '${TOP_P}' \
      --max-tokens '${MAX_TOKENS}' \
      --concurrency '${CONCURRENCY}' \
      --save-every 1 \
      2>&1 | tee '${LOG_FILE}'
  "; then
    echo "Generation command completed for ${MODEL_NAME}."
  else
    echo "ERROR: generation failed for ${MODEL_NAME}."
    cleanup_alias "${ADAPTER_BASENAME}"
    FAILED_ADAPTERS+=("${LAYOUT}/${ADAPTER_BASENAME}:generation_failed")
    continue
  fi

  echo ""

  echo "[10/9] Final JSON summary..."

  if final_json_summary "${OUTPUT_FILE}"; then
    echo "OK: clean complete generation for ${MODEL_NAME}."
    SUCCESS_ADAPTERS+=("${LAYOUT}/${ADAPTER_BASENAME}")
  else
    echo "WARNING: generation finished but JSON is incomplete or problematic for ${MODEL_NAME}."
    cleanup_alias "${ADAPTER_BASENAME}"
    FAILED_ADAPTERS+=("${LAYOUT}/${ADAPTER_BASENAME}:bad_final_json")
    continue
  fi

  cleanup_alias "${ADAPTER_BASENAME}"

  echo ""
  echo "Finished adapter: ${LAYOUT}/${ADAPTER_BASENAME}"
  echo ""

done

###############################################################################
# Final summary
###############################################################################

echo ""
echo "======================================================================"
echo "FINAL SUMMARY"
echo "======================================================================"

echo "Successful adapters: ${#SUCCESS_ADAPTERS[@]}"
if [ "${#SUCCESS_ADAPTERS[@]}" -gt 0 ]; then
  printf '  - %s\n' "${SUCCESS_ADAPTERS[@]}"
fi

echo ""
echo "Skipped adapters: ${#SKIPPED_ADAPTERS[@]}"
if [ "${#SKIPPED_ADAPTERS[@]}" -gt 0 ]; then
  printf '  - %s\n' "${SKIPPED_ADAPTERS[@]}"
fi

echo ""
echo "Failed adapters: ${#FAILED_ADAPTERS[@]}"
if [ "${#FAILED_ADAPTERS[@]}" -gt 0 ]; then
  printf '  - %s\n' "${FAILED_ADAPTERS[@]}"
fi

echo "======================================================================"

if [ "${#FAILED_ADAPTERS[@]}" -gt 0 ]; then
  echo "Some adapters failed. Check logs above."
  exit 1
fi

echo "All requested adapter generations completed successfully."
