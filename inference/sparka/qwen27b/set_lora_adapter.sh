#!/usr/bin/env bash
set -euo pipefail

ADAPTER_NAME="${1:-}"

if [ -z "$ADAPTER_NAME" ]; then
  echo "Usage:"
  echo "  ./set_lora_adapter.sh train_A"
  echo "  ./set_lora_adapter.sh train_B"
  echo "  ./set_lora_adapter.sh train_C"
  echo "  ./set_lora_adapter.sh train_AB_antineighbor"
  echo "  ./set_lora_adapter.sh train_AC_antineighbor"
  echo "  ./set_lora_adapter.sh train_AB_shuffle"
  echo "  ./set_lora_adapter.sh train_AC_shuffle"
  echo ""
  echo "Available adapters:"
  ls -1 /path/to/sparka/workdir/vllm_qwen_lora/adapters
  exit 1
fi

ADAPTER_DIR="/path/to/sparka/workdir/vllm_qwen_lora/adapters/${ADAPTER_NAME}"

if [ ! -d "$ADAPTER_DIR" ]; then
  echo "ERROR: adapter directory does not exist:"
  echo "  $ADAPTER_DIR"
  echo ""
  echo "Available adapters:"
  ls -1 /path/to/sparka/workdir/vllm_qwen_lora/adapters
  exit 1
fi

if [ ! -f "$ADAPTER_DIR/adapter_model.safetensors" ]; then
  echo "ERROR: adapter_model.safetensors not found in:"
  echo "  $ADAPTER_DIR"
  exit 1
fi

if [ ! -f "$ADAPTER_DIR/adapter_config.json" ]; then
  echo "ERROR: adapter_config.json not found in:"
  echo "  $ADAPTER_DIR"
  exit 1
fi

# Convert:
# train_A                -> ft_A
# train_B                -> ft_B
# train_AB_antineighbor  -> ft_AB_antineighbor
MODEL_SUFFIX="${ADAPTER_NAME#train_}"
VLLM_NAME="ft_${MODEL_SUFFIX}"

COMPOSE_FILE="docker-compose.yaml"
NEW_LINE="--lora-modules ${VLLM_NAME}=/adapters/${ADAPTER_NAME}"

echo "======================================================================"
echo "Configuring vLLM LoRA adapter"
echo "======================================================================"
echo "Requested adapter : ${ADAPTER_NAME}"
echo "Adapter directory : /adapters/${ADAPTER_NAME}"
echo "vLLM model name   : ${VLLM_NAME}"
echo "Compose file      : ${COMPOSE_FILE}"
echo "======================================================================"

if [ ! -f "$COMPOSE_FILE" ]; then
  echo "ERROR: ${COMPOSE_FILE} not found in current directory:"
  pwd
  exit 1
fi

CURRENT_LINE="$(grep -E -- '--lora-modules[[:space:]]+[^[:space:]]+=/adapters/[^[:space:]]+' "$COMPOSE_FILE" || true)"

if [ -z "$CURRENT_LINE" ]; then
  echo "ERROR: Could not find an existing --lora-modules line in ${COMPOSE_FILE}."
  echo "Please check the docker-compose.yaml manually."
  exit 1
fi

echo ""
echo "Current LoRA line:"
echo "  ${CURRENT_LINE# }"
echo ""
echo "Target LoRA line:"
echo "  ${NEW_LINE}"

# Case 1: already correct
if echo "$CURRENT_LINE" | grep -q -- "${NEW_LINE}"; then
  echo ""
  echo "Adapter is already correctly configured. Nothing to change."
  echo "======================================================================"
  exit 0
fi

# Case 2: replace old adapter with new adapter
cp "$COMPOSE_FILE" "${COMPOSE_FILE}.bak"

python3 - << PY
from pathlib import Path
import re

path = Path("${COMPOSE_FILE}")
text = path.read_text()

new_line = "${NEW_LINE}"

pattern = r"--lora-modules\s+\S+=/adapters/\S+"

if not re.search(pattern, text):
    raise SystemExit("ERROR: Could not find --lora-modules pattern to replace.")

text2 = re.sub(pattern, new_line, text, count=1)

path.write_text(text2)

print("docker-compose.yaml updated successfully.")
PY

echo ""
echo "Updated LoRA line:"
grep -E -- '--lora-modules[[:space:]]+[^[:space:]]+=/adapters/[^[:space:]]+' "$COMPOSE_FILE"

echo ""
echo "Backup saved as:"
echo "  ${COMPOSE_FILE}.bak"
echo "======================================================================"
