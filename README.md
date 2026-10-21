# Constitutional AI replication

A small-scale replication of Hugging Face's Constitutional AI pipeline
(https://huggingface.co/blog/constitutional_ai), built to run on a single rented GPU e.g. RunPod instead of a cluster, while staying compatible with the original scripts.

The replication was made on RunPod, using a single A40 GPU with a persistent Global volume mounted at `/workspace`.

## Folder Structure

```
cai-replication/
├── README.md                 ← this file
├── SPEC.md                   ← what was changed from the original scripts, and why
├── scripts/                  ← setup and one-off tasks
│   ├── download_model.py     ← download Mistral-7B-Instruct-v0.1 to /workspace/models
│   ├── setup_pod.sh          ← pod setup: uv, caches, uv sync, vLLM
│   └── serve_model.sh        ← start the vLLM server on port 8000
├── data-generation/          ← Stages 1–2
│   ├── constitution_anthropic.json ← the original constitution, unchanged
│   ├── generate_dataset.py   ← critique–revision generation + dataset construction
│   └── render_outputs.py     ← JSONL → readable Markdown report
├── training/
│   ├── sft/                  ← Stage 3: config.yaml, chat_template.jinja, sft.py
│   └── dpo/                  ← Stage 4: config.yaml, dpo.py
└── evaluation/
    └── generate.py           ← base vs SFT vs DPO answers on test_sft prompts → Markdown

```

## 1. Setup

Requires [uv](https://docs.astral.sh/uv/). On your own machine, after cloning: `uv sync`.

On a RunPod pod (fresh container each session):

```bash
cd /root
git clone https://github.com/Augusta-Lina/cai-replication.git
cd cai-replication
source scripts/setup_pod.sh
```

## 2. Scripts

### 2.1 Download the model

Downloads Mistral-7B-Instruct-v0.1 (about 14 GB) to `/workspace/models/`. Run on the GPU pod,
where `/workspace` is the persistent volume:

```bash
uv run scripts/download_model.py
```

### 2.2. Pod Setup

Installs uv, points its cache at the container disk (the `/workspace` volume does not allow setting file permissions), and runs `uv sync`. Must be run with `source`, not `bash`, so the environment settings persist in your terminal.

```bash
source scripts/setup_pod.sh
```

## 3. Running the pipeline (Stages 1–2)

Three terminals on the pod. All commands from the repo folder `/root/cai-replication`.

**Terminal A: model server.** Replaces llm-swarm + TGI. Leave it running.

```bash
bash scripts/serve_model.sh
```

Ready when it prints `Application startup complete`. Loading from `/workspace` takes 3–15 minutes depending on the host.

**Terminal B: generation.** First a tiny test, then the real run.

```bash
export UV_CACHE_DIR=/root/.cache/uv HF_HOME=/root/.cache/huggingface
uv run data-generation/generate_dataset.py --max_samples 2
uv run data-generation/generate_dataset.py --max_samples 128 --max_workers 16 --push_to_hub
```

Each run saves `train.jsonl` and `test.jsonl` to `/workspace/outputs/<repo_id>/`, where `<repo_id>` is `cai-conversation-dev` plus a timestamp. With `--push_to_hub` the same name is used for the Hub dataset, with splits `train_sft`, `train_prefs`, `test_sft`, `test_prefs`. Pushing needs a Hugging Face **Write** token in `.env` on the pod (`HF_TOKEN=hf_...`); `.env` is git-ignored.

Useful options: `--max_workers 1` for strictly sequential requests, `--constitution_path` to use a different constitution, `--no_timestamp` to reuse a dataset name.

**Prompt sources** (`--prompt_source`):

| Value | Prompts | Split |
|---|---|---|
| `hh-rlhf` (default, the baseline) | first human turn of `Anthropic/hh-rlhf` harmless-base, as in HF's pipeline | the dataset's own |
| a folder holding `train.jsonl` and `test.jsonl` | our own prompts: `synthetic-prompts-1000.md` (1,000 decision prompts, 700 AI safety, 300 lay) turned into the two files by `build_prompts.py --input data-generation/synthetic-prompts-1000.md --output <folder> --test_fraction 0.1` | 90/10, seed 0 → 900 / 100 |


**Readable report.** Turns a JSONL file into Markdown, one section per prompt (prompt, first answer, principle, critique, revision). Works on the pod or on your own machine after `scp`-ing the file.

```bash
uv run data-generation/render_outputs.py --input /workspace/outputs/<repo_id>/train.jsonl
uv run data-generation/render_outputs.py --input <file> --rows 0 3 7 --max_chars 600
```

## 4. Results

First toy run (2026-10-06): 128 prompts per split, 768 model calls, under 3 minutes on one GPU with 16 concurrent requests. Dataset: https://huggingface.co/datasets/AugustaLina/cai-conversation-dev1791308628

See `SPEC.md` for every difference from the original scripts.

## 5. Training and evaluation (Stages 3–4)

LoRA on one GPU instead of HF's full fine-tune on 8×H100. Each stage is a YAML config plus a script. From the repo folder on the pod:

```bash
uv run training/sft/sft.py --config training/sft/config.yaml      # Stage 3, ~10 min for Mistral-7B
uv run training/dpo/dpo.py --config training/dpo/config.yaml      # Stage 4, ~13 min; starts from the SFT adapter
uv run evaluation/generate.py --output data/eval-report.md        # base vs SFT vs DPO on 10 test_sft prompts
```

Both trainers evaluate the untrained model first (`eval_baseline`), then after every epoch, and keep the best epoch. Read the eval report before trusting the metrics: at 128 rows the DPO metrics improved while its answers collapsed into boilerplate.
