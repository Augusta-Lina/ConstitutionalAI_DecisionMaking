#!/usr/bin/env bash
# Run the whole pipeline for one constitution: generation -> SFT -> DPO -> evaluation.
# Every output goes to /workspace/runs/<run name>/ (persistent volume), nothing is overwritten.
# Usage, from the repo root on the pod, inside tmux so it survives disconnects:
#   bash scripts/run_pipeline.sh <run name> <constitution file> [max_samples] [prompt source]
#   e.g. bash scripts/run_pipeline.sh 2026-10-15_anthropic data-generation/constitution_anthropic.json 128

# Block 1: settings
# ---------------------
set -euo pipefail

RUN_NAME="${1:?usage: run_pipeline.sh <run name> <constitution file> [max_samples]}"
CONSTITUTION="${2:?usage: run_pipeline.sh <run name> <constitution file> [max_samples]}"
MAX_SAMPLES="${3:-128}"
PROMPT_SOURCE="${4:-hh-rlhf}"                  # "hh-rlhf", or a folder of unpacked TWA posts, e.g. /workspace/datasets/TWA
PRIVATE=$([ "${PROMPT_SOURCE}" = "hh-rlhf" ] && echo false || echo true)
MAX_WORKERS=16
HF_USER="AugustaLina"

RUN_DIR="/workspace/runs/${RUN_NAME}"
DATASET_NAME="cai-${RUN_NAME}"                 # Hub dataset: AugustaLina/cai-<run name>
DATASET_ID="${HF_USER}/${DATASET_NAME}"

export UV_CACHE_DIR=/root/.cache/uv HF_HOME=/root/.cache/huggingface

if [ -e "${RUN_DIR}" ]; then
  echo "Run folder ${RUN_DIR} already exists. Pick a new run name."; exit 1
fi
mkdir -p "${RUN_DIR}"/{dataset,sft,dpo,eval}
cp "${CONSTITUTION}" "${RUN_DIR}/constitution.json"

log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "${RUN_DIR}/pipeline.log"; }
log "Run ${RUN_NAME}: constitution=${CONSTITUTION}, max_samples=${MAX_SAMPLES}, dataset=${DATASET_ID}"

# Block 2: Stages 1-2, generation (needs the vLLM server)
# ---------------------
log "Starting vLLM server"
vllm serve /workspace/models/Mistral-7B-Instruct-v0.1 --served-model-name mistral --port 8000 \
  > "${RUN_DIR}/dataset/vllm.log" 2>&1 &
VLLM_PID=$!
until curl -s http://localhost:8000/v1/models > /dev/null; do
  if ! kill -0 "${VLLM_PID}" 2>/dev/null; then log "vLLM stopped unexpectedly, see dataset/vllm.log"; exit 1; fi
  sleep 15
done
log "vLLM ready"

uv run data-generation/generate_dataset.py \
  --constitution_path "${CONSTITUTION}" --max_samples "${MAX_SAMPLES}" --max_workers "${MAX_WORKERS}" \
  --output_dir "${RUN_DIR}/dataset" --repo_id "${DATASET_NAME}" --timestamp false --push_to_hub true \
  --prompt_source "${PROMPT_SOURCE}" --private "${PRIVATE}" \
  2>&1 | tee "${RUN_DIR}/dataset/generate.log"

for split in train test; do
  uv run data-generation/render_outputs.py --input "${RUN_DIR}/dataset/${DATASET_NAME}/${split}.jsonl"
done

log "Stopping vLLM"
kill "${VLLM_PID}"; wait "${VLLM_PID}" 2>/dev/null || true
sleep 10
log "Generation done: ${DATASET_ID}"

# Block 3: Stage 3, SFT
# ---------------------
# Per-run copy of the config with this run's dataset name; the copy is the record of what was trained.
sed "s|AugustaLina/cai-conversation-dev1791308628|${DATASET_ID}|" training/sft/config.yaml > "${RUN_DIR}/sft/config.yaml"

log "SFT starting"
uv run training/sft/sft.py --config "${RUN_DIR}/sft/config.yaml" --output_dir "${RUN_DIR}/sft" \
  2>&1 | tee "${RUN_DIR}/sft/train.log"
log "SFT done"

# Block 4: Stage 4, DPO (continues the SFT adapter from this run)
# ---------------------
sed "s|AugustaLina/cai-conversation-dev1791308628|${DATASET_ID}|" training/dpo/config.yaml > "${RUN_DIR}/dpo/config.yaml"

log "DPO starting"
uv run training/dpo/dpo.py --config "${RUN_DIR}/dpo/config.yaml" \
  --model_name_or_path "${RUN_DIR}/sft" --output_dir "${RUN_DIR}/dpo" \
  2>&1 | tee "${RUN_DIR}/dpo/train.log"
log "DPO done"

# Block 5: evaluation (base vs SFT vs DPO) and the one-page run summary
# ---------------------
log "Evaluation starting"
uv run evaluation/generate.py --sft "${RUN_DIR}/sft" --dpo "${RUN_DIR}/dpo" \
  --dataset "${DATASET_ID}" --output "${RUN_DIR}/eval/eval-report.md" \
  2>&1 | tee "${RUN_DIR}/eval/generate.log"

uv run python - "${RUN_DIR}" "${RUN_NAME}" "${DATASET_ID}" "${CONSTITUTION}" <<'EOF'
import json, sys
run_dir, run_name, dataset_id, constitution = sys.argv[1:5]
sft = json.load(open(f"{run_dir}/sft/all_results.json"))
dpo = json.load(open(f"{run_dir}/dpo/all_results.json"))
sft_base = json.load(open(f"{run_dir}/sft/eval_baseline_results.json"))
pct = lambda x: f"{100 * x:.0f}%"
lines = [
    f"# Run {run_name}", "",
    f"- Constitution: `{constitution}` (copy: `constitution.json`)",
    f"- Dataset: `{dataset_id}` (rows + Markdown reports in `dataset/`)",
    f"- Reports: `dataset/*/train.md`, `dataset/*/test.md`, `eval/eval-report.md`", "",
    "## SFT (held-out rows)", "", "| | Eval loss | Token accuracy |", "|---|---|---|",
    f"| Before training | {sft['eval_baseline_loss']:.3f} | {pct(sft_base['eval_mean_token_accuracy'])} |"
    if 'eval_baseline_loss' in sft else "| Before training | n/a | n/a |",
    f"| Final | {sft['eval_loss']:.3f} | {pct(sft['eval_mean_token_accuracy'])} |",
    f"| Train loss / time | {sft['train_loss']:.3f} | {sft['train_runtime'] / 60:.1f} min |", "",
    "## DPO (held-out pairs)", "", "| | Eval loss | Chosen preferred | Margin |", "|---|---|---|---|",
    f"| Before training | {dpo.get('eval_baseline_loss', float('nan')):.3f} | 0% | 0.00 |",
    f"| Final | {dpo['eval_loss']:.3f} | {pct(dpo['eval_rewards/accuracies'])} | {dpo['eval_rewards/margins']:.2f} |",
    f"| Train loss / time | {dpo['train_loss']:.3f} | {dpo['train_runtime'] / 60:.1f} min |", "",
    "Read `eval/eval-report.md` before trusting any of the numbers above.",
]
open(f"{run_dir}/run.md", "w").write("\n".join(lines) + "\n")
print(open(f"{run_dir}/run.md").read())
EOF

log "Run ${RUN_NAME} complete: ${RUN_DIR}"
