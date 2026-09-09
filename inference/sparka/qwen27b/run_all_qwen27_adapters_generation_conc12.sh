#!/usr/bin/env bash
set -euo pipefail

CONTAINER_NAME="adel_recover"
EVAL_DIR="/home/evaluator/workspace/Fortran-HumanEval_Adel/__sandbox_adel__/evaluation_finetuning"

SERVER_DIR="/path/to/sparka/workdir/vllm_qwen27_lora_server"
ADAPTERS_ROOT="/path/to/sparka/workdir/vllm_qwen27_lora/adapters/epoch1/learning_rate_1"

BASE_URL="http://localhost:8087"
HOST_BASE_URL="http://localhost:8087"

MODEL_FAMILY="mistral"
TEMPERATURE="0"
TOP_P="1"
MAX_TOKENS="2048"
CONCURRENCY="${CONCURRENCY:-12}"
FORCE="${FORCE:-0}"

LAYOUT="qwen27/epoch1/learning_rate_1"
BENCHMARK="../benchmark.json"

PROJECT_NAME="qwen27_lora_eval"

echo "======================================================================"
echo "Qwen27 LoRA HumanEval generation - all adapters"
echo "======================================================================"
echo "Adapters root : ${ADAPTERS_ROOT}"
echo "Base URL      : ${BASE_URL}"
echo "Layout        : ${LAYOUT}"
echo "Concurrency   : ${CONCURRENCY}"
echo "Force         : ${FORCE}"
echo "======================================================================"

cd "${SERVER_DIR}"

echo
echo "[1/6] Check adapters"
if [ ! -d "${ADAPTERS_ROOT}" ]; then
  echo "ERROR: adapters root not found: ${ADAPTERS_ROOT}"
  exit 1
fi

mapfile -t ADAPTER_DIRS < <(
  find "${ADAPTERS_ROOT}" -mindepth 1 -maxdepth 1 -type d | sort
)

if [ "${#ADAPTER_DIRS[@]}" -eq 0 ]; then
  echo "ERROR: no adapters found in ${ADAPTERS_ROOT}"
  exit 1
fi

echo "Found adapters: ${#ADAPTER_DIRS[@]}"
for d in "${ADAPTER_DIRS[@]}"; do
  name="$(basename "$d")"
  if [ ! -f "$d/adapter_model.safetensors" ] || [ ! -f "$d/adapter_config.json" ]; then
    echo "ERROR: incomplete adapter: $name"
    exit 1
  fi
  echo "  OK $name"
done

echo
echo "[2/6] Prepare output folders in evaluator container"
docker exec "${CONTAINER_NAME}" bash -lc "
set -euo pipefail
cd '${EVAL_DIR}'
mkdir -p '${LAYOUT}/results_qwen_lora/solutions'
mkdir -p '${LAYOUT}/results'
mkdir -p '${LAYOUT}/logs'
ls -ld '${LAYOUT}' '${LAYOUT}/results_qwen_lora/solutions' '${LAYOUT}/results' '${LAYOUT}/logs'
"

echo
echo "[3/6] Start loop over adapters"

for ADAPTER_PATH in "${ADAPTER_DIRS[@]}"; do
  RUN_NAME="$(basename "${ADAPTER_PATH}")"

  # train_A -> ft_A_qwen27
  # train_ABC_dedup_BC -> ft_ABC_dedup_BC_qwen27
  CLEAN_NAME="${RUN_NAME#train_}"
  MODEL_NAME="ft_${CLEAN_NAME}_qwen27"
  MODEL_KEY="ft_${CLEAN_NAME}_qwen27"

  OUTPUT_FILE="${LAYOUT}/results_qwen_lora/solutions/${MODEL_KEY}_humaneval_${MODEL_FAMILY}_conc${CONCURRENCY}_solutions.json"
  LOG_FILE="${LAYOUT}/logs/${MODEL_KEY}_humaneval_${MODEL_FAMILY}_conc${CONCURRENCY}_generation.log"

  echo
  echo "======================================================================"
  echo "Adapter    : ${RUN_NAME}"
  echo "Model name : ${MODEL_NAME}"
  echo "Adapter dir: ${ADAPTER_PATH}"
  echo "Output     : ${OUTPUT_FILE}"
  echo "Log        : ${LOG_FILE}"
  echo "======================================================================"

  echo "[3.1] Check existing output"
  if [ "${FORCE}" != "1" ]; then
    COMPLETE="$(docker exec "${CONTAINER_NAME}" bash -lc "
cd '${EVAL_DIR}'
python3 - << 'PY'
import json
from pathlib import Path
p = Path('${OUTPUT_FILE}')
if not p.exists():
    print('NO')
else:
    try:
        data = json.load(open(p, encoding='utf-8'))
        ok = (
            isinstance(data, list)
            and len(data) == 164
            and all(x is not None for x in data)
            and not (data and data[-1] is None)
        )
        print('YES' if ok else 'NO')
    except Exception:
        print('NO')
PY
")"

    COMPLETE_LAST="$(printf "%s\n" "${COMPLETE}" | tail -n 1)"
    if [ "${COMPLETE_LAST}" = "YES" ]; then
      echo "SKIP: complete output already exists. Use FORCE=1 to regenerate."
      continue
    fi
  fi

  echo "[3.2] Stop current vLLM service"
  docker compose -p "${PROJECT_NAME}" down || true

  echo "[3.3] Patch docker-compose.yaml for current adapter"
  python3 - << PY
from pathlib import Path

compose = Path("docker-compose.yaml")
s = compose.read_text()

adapter_host = "${ADAPTER_PATH}"
adapter_in_container = adapter_host.replace(
    "/path/to/sparka/workdir/vllm_qwen27_lora/adapters",
    "/adapters"
)

model_name = "${MODEL_NAME}"

lines = s.splitlines()
out = []
inserted_lora = False

for line in lines:
    stripped = line.strip()

    # Replace served model name.
    if stripped.startswith("--served-model-name"):
        indent = line[:len(line) - len(line.lstrip())]
        out.append(f"{indent}--served-model-name qwen35-27b-base")
        continue

    # Remove old lora-modules lines, active or commented.
    if "--lora-modules" in line:
        continue

    out.append(line)

    # Add lora module immediately after --enable-lora.
    if stripped == "--enable-lora":
        indent = line[:len(line) - len(line.lstrip())]
        out.append(f"{indent}--lora-modules {model_name}={adapter_in_container}")
        inserted_lora = True

if not inserted_lora:
    raise SystemExit("ERROR: could not find --enable-lora in docker-compose.yaml")

compose.write_text("\\n".join(out) + "\\n")
print("Patched docker-compose.yaml")
print("LoRA:", f"{model_name}={adapter_in_container}")
PY

  echo "[3.4] Start vLLM with adapter"
  docker compose -p "${PROJECT_NAME}" up -d

  echo "[3.5] Wait for vLLM health"
  for i in $(seq 1 120); do
    if curl -fsS "${HOST_BASE_URL}/health" >/dev/null 2>&1; then
      echo "vLLM health OK"
      break
    fi
    if [ "$i" -eq 120 ]; then
      echo "ERROR: vLLM did not become healthy"
      docker logs --tail 200 vllm-qwen35-27b-base || true
      exit 1
    fi
    sleep 5
  done

  echo "[3.6] Check exposed models"
  curl -fsS "${HOST_BASE_URL}/v1/models" | python3 -m json.tool

  echo "[3.7] Check model from evaluator container"
  docker exec "${CONTAINER_NAME}" bash -lc "
curl -fsS '${BASE_URL}/v1/models' | python3 -m json.tool
"

  echo "[3.8] Remove partial old output/log if FORCE=1 or incomplete"
  docker exec "${CONTAINER_NAME}" bash -lc "
set -euo pipefail
cd '${EVAL_DIR}'
rm -f '${OUTPUT_FILE}'
rm -f '${LOG_FILE}'
"

  echo "[3.9] Launch generation"
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

  echo "[3.10] Verify generated file"
  docker exec "${CONTAINER_NAME}" bash -lc "
cd '${EVAL_DIR}'
python3 - << 'PY'
import json
from pathlib import Path

p = Path('${OUTPUT_FILE}')
print('file:', p)
if not p.exists():
    print('ERROR: missing output')
    raise SystemExit(1)

data = json.load(open(p, encoding='utf-8'))
print('total:', len(data))
print('none:', sum(x is None for x in data))
print('trailing_null:', bool(data and data[-1] is None))
print('ok_extractions:', sum(1 for x in data if x and x.get('extraction_status') == 'ok'))
print('empty_code:', sum(1 for x in data if x and not x.get('code')))
print('errors:', sum(1 for x in data if x and x.get('error')))

if len(data) != 164 or any(x is None for x in data) or (data and data[-1] is None):
    print('ERROR: incomplete generation')
    raise SystemExit(1)

print('OK: complete generation')
PY
"

done

echo
echo "======================================================================"
echo "All Qwen27 adapter generations finished."
echo "Layout: ${LAYOUT}"
echo "======================================================================"
