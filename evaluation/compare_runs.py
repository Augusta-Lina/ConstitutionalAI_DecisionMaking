# Comparison of finished models on the same prompts: Mistral-7B-Instruct, pilot SFT and DPO, medium-scale SFT and DPO.
# Prompts are the first 10 of the medium-scale run's test_sft split, which neither run trained on.
# Usage (on the pod, from the repo folder):   uv run evaluation/compare_runs.py

# Block 1: imports and settings
# ---------------------
import argparse
import json

import torch
from datasets import load_dataset
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

parser = argparse.ArgumentParser()
parser.add_argument("--instruct", default="/workspace/models/Mistral-7B-Instruct-v0.1")
parser.add_argument("--base", default="/workspace/models/Mistral-7B-v0.1")
parser.add_argument("--pilot_sft", default="/workspace/runs/2026-10-20_synth_v3.1_clean/sft")
parser.add_argument("--pilot_dpo", default="/workspace/runs/2026-10-20_synth_v3.1_clean/dpo")
parser.add_argument("--medium_sft", default="/workspace/runs/2026-10-21_synth1000_v3.1_clean_all/sft")
parser.add_argument("--medium_dpo", default="/workspace/runs/2026-10-21_synth1000_v3.1_clean_all/dpo")
parser.add_argument("--dataset", default="AugustaLina/cai-2026-10-21_synth1000_v3.1_clean_all")
parser.add_argument("--num_prompts", type=int, default=10)
parser.add_argument("--max_new_tokens", type=int, default=512)
parser.add_argument("--output", default="/workspace/runs/comparison-2026-10-21.md")
args = parser.parse_args()


# Block 2: prompts and the generation function
# ---------------------
# Same prompts, same greedy decoding (no sampling) and same length limit for every model,
# so differences between answers come from the models, not from chance.
prompts = load_dataset(args.dataset, split="test_sft")["prompt"][: args.num_prompts]
print(f"{len(prompts)} prompts from test_sft")


def answer(model, tokenizer, prompt):
    """Lay the prompt out with this model's chat template, let it write, return only the new text."""
    text = tokenizer.apply_chat_template(
        [{"role": "user", "content": prompt}], tokenize=False, add_generation_prompt=True
    )
    inputs = tokenizer(text, return_tensors="pt", add_special_tokens=False).to(model.device)
    with torch.no_grad():
        out = model.generate(
            **inputs, max_new_tokens=args.max_new_tokens, do_sample=False, pad_token_id=tokenizer.eos_token_id
        )
    new_tokens = out[0][inputs["input_ids"].shape[1]:]
    return tokenizer.decode(new_tokens, skip_special_tokens=True).strip()


def load(path):
    return AutoModelForCausalLM.from_pretrained(path, dtype=torch.bfloat16, attn_implementation="sdpa", device_map="cuda")


results = {}  # model name -> list of answers, one per prompt


# Block 3: Mistral-7B-Instruct on its own, with its own chat template
# ---------------------
print("loading instruct")
tok = AutoTokenizer.from_pretrained(args.instruct)
model = load(args.instruct)
model.eval()
print("generating: instruct")
results["instruct"] = [answer(model, tok, p) for p in prompts]
del model
torch.cuda.empty_cache()  # free the GPU before loading the base model


# Block 4: the four adapters on one copy of the base model
# ---------------------
# Each adapter carries our chat template in its folder, saved by its training run.
# The base model is loaded once; adapters are swapped in and out with set_adapter.
print("loading base")
base = load(args.base)
adapters = {
    "pilot_sft": args.pilot_sft,
    "pilot_dpo": args.pilot_dpo,
    "medium_sft": args.medium_sft,
    "medium_dpo": args.medium_dpo,
}
model = None
for name, path in adapters.items():
    if model is None:
        model = PeftModel.from_pretrained(base, path, adapter_name=name)
    else:
        model.load_adapter(path, adapter_name=name)
    model.set_adapter(name)
    model.eval()
    tok = AutoTokenizer.from_pretrained(path)
    print(f"generating: {name}")
    results[name] = [answer(model, tok, p) for p in prompts]


# Block 5: write the report (Markdown to read, JSON to keep)
# ---------------------
labels = {
    "instruct": "Mistral-7B-Instruct",
    "pilot_sft": "Pilot SFT (82 rows)",
    "pilot_dpo": "Pilot DPO (82 rows)",
    "medium_sft": "Medium-scale SFT (787 rows)",
    "medium_dpo": "Medium-scale DPO (787 rows)",
}
lines = [f"# Five models on {len(prompts)} test_sft prompts (max {args.max_new_tokens} new tokens, greedy)\n"]
for i, prompt in enumerate(prompts):
    lines.append(f"## Prompt {i + 1}\n\n> {prompt}\n")
    for name, label in labels.items():
        lines.append(f"**{label}**\n\n{results[name][i]}\n")
with open(args.output, "w") as f:
    f.write("\n".join(lines))
with open(args.output.replace(".md", ".json"), "w") as f:
    json.dump({"prompts": prompts, "answers": results}, f, indent=2)
print(f"Report written to {args.output}")
