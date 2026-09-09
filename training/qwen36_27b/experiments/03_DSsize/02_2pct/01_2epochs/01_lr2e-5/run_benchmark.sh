#!/bin/bash
#SBATCH --job-name=vllm-benchmark
#SBATCH --output=output.%j.out
#SBATCH --constraint=h100
#SBATCH --nodes=1
#SBATCH --ntasks=2
#SBATCH --gres=gpu:2
#SBATCH --cpus-per-task=24
#SBATCH --time=12:00:00
#SBATCH --hint=nomultithread
#SBATCH --account=olm@h100

set -uo pipefail   # not -e: we want to control exit codes ourselves below

# ----------------------------------------------------------------------------
# Environment
# ----------------------------------------------------------------------------

module purge
module load arch/h100
module load cuda/13.0.3
source /path/to/vllm_env/bin/activate
source /path/to/finetuning/env.sh

find_free_port() {
    local host="${1:-127.0.0.1}"
    python - "$host" <<'PY'
import socket, sys
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((sys.argv[1], 0))   # 0 => OS picks a free port
print(s.getsockname()[1])
s.close()
PY
}

# ----------------------------------------------------------------------------
# Config — edit these
# ----------------------------------------------------------------------------
MODEL_PATH="/path/to/models/Qwen3.6-27B"
LORA_ADAPTER_PATH="./outputs/"
TP_SIZE=$SLURM_NTASKS
HOST="127.0.0.1"
#PORT=8000
PORT=$(find_free_port "$HOST")
VLLM_LOG="vllm_server.${SLURM_JOB_ID}.log"
HEALTH_URL="http://${HOST}:${PORT}/health"
MAX_WAIT=900        # seconds to wait for the server to come up (big models take a while)
POLL_INTERVAL=5
BENCH_PATH="/path/to/work/AI/bench/02_prompt2fortranbench"

# ----------------------------------------------------------------------------
# 1. Launch the vLLM server in the background
# ----------------------------------------------------------------------------
echo "[$(date)] Starting vLLM server..."

export TIKTOKEN_ENCODINGS_BASE=/path/to/tiktoken_encodings

vllm serve "$MODEL_PATH" \
    --host "$HOST" \
    --port "$PORT" \
    --tensor-parallel-size "$TP_SIZE" \
    --trust-remote-code \
    --language-model-only \
    --reasoning-parser qwen3 \
    --served-model-name qwen3.6-27b \
    --max-model-len 49152 \
    --gdn-prefill-backend triton \
    --max_num_seqs 256 \
    --enable-lora \
    --lora-modules current_lora=$LORA_ADAPTER_PATH \
    --max-lora-rank 32 \
    > "$VLLM_LOG" 2>&1 &

VLLM_PID=$!
echo "[$(date)] vLLM server PID: $VLLM_PID (logging to $VLLM_LOG)"

# Make sure the server dies with this script no matter how it exits
# (normal completion, error, or the job being cancelled/timing out).
cleanup() {
    if kill -0 "$VLLM_PID" 2>/dev/null; then
        echo "[$(date)] Cleaning up: stopping vLLM server (PID $VLLM_PID)"
        kill "$VLLM_PID" 2>/dev/null
        wait "$VLLM_PID" 2>/dev/null
    fi
}
trap cleanup EXIT SIGTERM SIGINT

# ----------------------------------------------------------------------------
# 2. Wait until the server is actually ready to serve requests
# ----------------------------------------------------------------------------
echo "[$(date)] Waiting for vLLM server to become healthy at $HEALTH_URL ..."
elapsed=0
until curl -fs -o /dev/null "$HEALTH_URL"; do
    if ! kill -0 "$VLLM_PID" 2>/dev/null; then
        echo "[$(date)] vLLM server process died during startup. Check $VLLM_LOG"
        exit 1
    fi
    if (( elapsed >= MAX_WAIT )); then
        echo "[$(date)] Timed out after ${MAX_WAIT}s waiting for vLLM server."
        exit 1
    fi
    sleep "$POLL_INTERVAL"
    elapsed=$((elapsed + POLL_INTERVAL))
done
echo "[$(date)] vLLM server is up after ${elapsed}s."

# ----------------------------------------------------------------------------
# 3. Run the benchmark against the now-running server
# ----------------------------------------------------------------------------
source $BENCH_PATH/.venv/bin/activate
echo "[$(date)] Starting benchmark..."

python $BENCH_PATH/scripts/generation/generate.py \
    --phase 1 \
    --provider vllm \
    --model current_lora \
    --benchmark $BENCH_PATH/data/Fortran-HumanEval/benchmark.json \
    --output ./benchmark/generate/qwen3.6-27b.jsonl \
    --base-url "http://${HOST}:${PORT}/v1" \
    --concurrency 256 \
    --repeats 10 \
    --timeout 2400 \
    --max-tokens 32768

python $BENCH_PATH/scripts/evaluation/evaluate_phase1.py \
    --jobs 24 \
    --benchmark $BENCH_PATH/data/Fortran-HumanEval/benchmark.json \
    --difficulty $BENCH_PATH/data/fortran_difficulty.json \
    --responses-dir ./benchmark/generate \
    --output-dir ./benchmark/evals

python $BENCH_PATH/scripts/analysis/analyze_results.py \
    --results ./benchmark/evals/qwen3.6-27b.run*/results.json \
    --aggregate \
    --output ./benchmark/evals/aggregate.json

BENCH_STATUS=$?
echo "[$(date)] Benchmark finished with exit code $BENCH_STATUS"

# cleanup() runs automatically here via the trap, killing the vLLM server
exit $BENCH_STATUS
