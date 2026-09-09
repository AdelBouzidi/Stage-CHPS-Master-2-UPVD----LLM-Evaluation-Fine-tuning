#!/usr/bin/env bash
set -euo pipefail

CONTAINER_NAME="adel_recover"
EVAL_DIR="/home/evaluator/workspace/Fortran-HumanEval_Adel/__sandbox_adel__/evaluation_finetuning"

BASE_URL="http://localhost:8087"
HOST_BASE_URL="http://localhost:8087"

MODEL_NAME="qwen35-27b-base"
MODEL_KEY="base_qwen27"

MODEL_FAMILY="mistral"
TEMPERATURE="0"
TOP_P="1"
MAX_TOKENS="2048"
CONCURRENCY="${CONCURRENCY:-20}"

LAYOUT="qwen27/base"
BENCHMARK="../benchmark.json"

OUTPUT_FILE="${LAYOUT}/results_qwen_lora/solutions/${MODEL_KEY}_humaneval_${MODEL_FAMILY}_conc${CONCURRENCY}_solutions.json"
LOG_FILE="${LAYOUT}/logs/${MODEL_KEY}_humaneval_${MODEL_FAMILY}_conc${CONCURRENCY}_generation.log"

echo "======================================================================"
echo "Qwen27 base HumanEval generation"
echo "======================================================================"
echo "Model       : ${MODEL_NAME}"
echo "Base URL    : ${BASE_URL}"
echo "Layout      : ${LAYOUT}"
echo "Output      : ${OUTPUT_FILE}"
echo "Log         : ${LOG_FILE}"
echo "Concurrency : ${CONCURRENCY}"
echo "======================================================================"

echo
echo "[1/5] Host model check"
curl -fsS "${HOST_BASE_URL}/v1/models" | python3 -m json.tool

echo
echo "[2/5] Container model check"
docker exec "${CONTAINER_NAME}" bash -lc "
curl -fsS '${BASE_URL}/v1/models' | python3 -m json.tool
"

echo
echo "[3/5] Preparing output/log folders"
docker exec "${CONTAINER_NAME}" bash -lc "
set -euo pipefail
cd '${EVAL_DIR}'
mkdir -p '${LAYOUT}/results_qwen_lora/solutions'
mkdir -p '${LAYOUT}/results'
mkdir -p '${LAYOUT}/logs'
ls -ld '${LAYOUT}' '${LAYOUT}/results_qwen_lora/solutions' '${LAYOUT}/results' '${LAYOUT}/logs'
"

echo
echo "[4/5] Removing partial old output if exists"
docker exec "${CONTAINER_NAME}" bash -lc "
set -euo pipefail
cd '${EVAL_DIR}'
rm -f '${OUTPUT_FILE}'
rm -f '${LOG_FILE}'
"

echo
echo "[5/5] Launching generation"
docker exec -i "${CONTAINER_NAME}" bash -lc "
set -euo pipefail
cd '${EVAL_DIR}'

python generate_with_vllm_lora.py \
  --benchmark '${BENCHMARK}' \
  --model '${MODEL_NAME}' \
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

echo
echo "======================================================================"
echo "Generation finished."
echo "Output: ${OUTPUT_FILE}"
echo "Log   : ${LOG_FILE}"
echo "======================================================================"
