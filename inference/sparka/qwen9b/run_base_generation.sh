#!/usr/bin/env bash
set -euo pipefail

CONTAINER_NAME="adel_recover"

EVAL_DIR="/home/evaluator/workspace/Fortran-HumanEval_Adel/__sandbox_adel__/evaluation_finetuning"

HOST_BASE_URL="http://localhost:8087"
BASE_URL="http://localhost:8087"

BASE_MODEL_NAME="qwen35-9b-base"

BENCHMARK="../benchmark.json"

MODEL_FAMILY="mistral"
TEMPERATURE="0"
TOP_P="1"
MAX_TOKENS="2048"
CONCURRENCY="30"

OUTPUT_FILE="_base_reference/results_qwen_lora/solutions/base_humaneval_${MODEL_FAMILY}_conc${CONCURRENCY}_solutions.json"
LOG_FILE="_base_reference/logs/base_humaneval_${MODEL_FAMILY}_conc${CONCURRENCY}_generation.log"

FORCE_REGENERATE="${FORCE_REGENERATE:-0}"

echo "======================================================================"
echo "BASE MODEL HumanEval generation"
echo "======================================================================"
echo "Model       : ${BASE_MODEL_NAME}"
echo "Concurrency : ${CONCURRENCY}"
echo "Output      : ${OUTPUT_FILE}"
echo "Log         : ${LOG_FILE}"
echo "Force regen : ${FORCE_REGENERATE}"
echo "======================================================================"
echo ""

echo "[1/5] Basic checks..."

if ! docker ps --format '{{.Names}}' | grep -qx "${CONTAINER_NAME}"; then
  echo "ERROR: container ${CONTAINER_NAME} is not running."
  docker ps
  exit 1
fi

if ! curl -fsS "${HOST_BASE_URL}/health" >/dev/null 2>&1; then
  echo "ERROR: vLLM health endpoint is not reachable:"
  echo "  ${HOST_BASE_URL}/health"
  exit 1
fi

docker exec "${CONTAINER_NAME}" bash -lc "
  cd '${EVAL_DIR}'
  test -f generate_with_vllm_lora.py
  test -f '${BENCHMARK}'
"

echo "OK."
echo ""

echo "[2/5] Checking base model from host..."

MODELS_JSON="$(curl -fsS "${HOST_BASE_URL}/v1/models")"
echo "${MODELS_JSON}" | python3 -m json.tool

echo "${MODELS_JSON}" | python3 -c "
import json, sys
wanted = '${BASE_MODEL_NAME}'
data = json.load(sys.stdin)
ids = [x.get('id') for x in data.get('data', [])]
print('Available models:', ids)
if wanted not in ids:
    raise SystemExit(f'ERROR: {wanted} not found')
"

echo "OK: ${BASE_MODEL_NAME} is exposed from host."
echo ""

echo "[3/5] Checking existing output..."

OUTPUT_STATUS="$(docker exec "${CONTAINER_NAME}" bash -lc "
cd '${EVAL_DIR}'

if [ ! -f '${OUTPUT_FILE}' ]; then
  echo missing
  exit 0
fi

python3 -c \"
import json
p='${OUTPUT_FILE}'
try:
    data=json.load(open(p))
    total=len(data)
    none=sum(x is None for x in data)
    trailing=bool(total>0 and data[-1] is None)
    ok=sum(1 for x in data if x and x.get('extraction_status')=='ok')
    empty=sum(1 for x in data if x and not x.get('code'))
    if total==164 and none==0 and not trailing:
        print(f'complete_total_{total}_ok_{ok}_empty_{empty}')
    else:
        print(f'incomplete_total_{total}_none_{none}_trailing_{trailing}_ok_{ok}_empty_{empty}')
except Exception as e:
    print('invalid_json')
\"
" | tail -n 1)"

echo "Output status: ${OUTPUT_STATUS}"

if [ "${FORCE_REGENERATE}" != "1" ] && [[ "${OUTPUT_STATUS}" == complete_total_* ]]; then
  echo "Generation already complete. Skipping."
  exit 0
fi

echo ""

echo "[4/5] Preparing output/log folders..."

docker exec "${CONTAINER_NAME}" bash -lc "
cd '${EVAL_DIR}'

mkdir -p _base_reference/results_qwen_lora/solutions
mkdir -p _base_reference/logs

if [ '${FORCE_REGENERATE}' = '1' ] || [ '${OUTPUT_STATUS}' != 'missing' ]; then
  TS=\$(date +%Y%m%d_%H%M%S)

  if [ -f '${OUTPUT_FILE}' ]; then
    echo 'Backing up output: ${OUTPUT_FILE}.bak_'\${TS}
    mv '${OUTPUT_FILE}' '${OUTPUT_FILE}.bak_'\${TS}
  fi

  if [ -f '${LOG_FILE}' ]; then
    echo 'Backing up log: ${LOG_FILE}.bak_'\${TS}
    mv '${LOG_FILE}' '${LOG_FILE}.bak_'\${TS}
  fi
fi
"

echo ""

echo "[5/5] Launching base generation with concurrency=${CONCURRENCY}..."
echo "WARNING: concurrency=30 is high. This is only for testing."
echo ""

docker exec -i "${CONTAINER_NAME}" bash -lc "
set -euo pipefail

cd '${EVAL_DIR}'

python generate_with_vllm_lora.py \
  --benchmark '${BENCHMARK}' \
  --model '${BASE_MODEL_NAME}' \
  --base-url '${BASE_URL}' \
  --output '${OUTPUT_FILE}' \
  --model-family '${MODEL_FAMILY}' \
  --temperature '${TEMPERATURE}' \
  --top-p '${TOP_P}' \
  --max-tokens '${MAX_TOKENS}' \
  --concurrency '${CONCURRENCY}' \
  --save-every 1 \
  2>&1 | tee '${LOG_FILE}'
"

echo ""
echo "======================================================================"
echo "Final JSON check"
echo "======================================================================"

docker exec "${CONTAINER_NAME}" bash -lc "
cd '${EVAL_DIR}'

python3 -c \"
import json
p='${OUTPUT_FILE}'
data=json.load(open(p))
print('file:', p)
print('total:', len(data))
print('none:', sum(x is None for x in data))
print('ok:', sum(1 for x in data if x and x.get('extraction_status')=='ok'))
print('empty:', sum(1 for x in data if x and not x.get('code')))
print('errors:', sum(1 for x in data if x and x.get('error')))
\"
"

echo ""
echo "Done."
echo "Output: ${OUTPUT_FILE}"
echo "Log   : ${LOG_FILE}"
