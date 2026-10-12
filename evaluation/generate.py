"""
Evaluation: generate answers from the base model, the SFT model and the DPO
model on prompts from the test_sft split (never used in training), and write
them side by side in a Markdown report for reading.

    uv run evaluation/generate.py --output data/eval-report.md
"""

# Block 1: imports and settings
# ---------------------
import argparse

import torch
from datasets import load_dataset
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

parser = argparse.ArgumentParser()
parser.add_argument("--base", default="/workspace/models/Mistral-7B-v0.1")
parser.add_argument("--sft", default="/workspace/outputs/training/sft-mistral-7b-lora")
parser.add_argument("--dpo", default="/workspace/outputs/training/dpo-mistral-7b-lora")
parser.add_argument("--dataset", default="AugustaLina/cai-conversation-dev1791308628")
parser.add_argument("--num_prompts", type=int, default=10)
parser.add_argument("--max_new_tokens", type=int, default=256)
parser.add_argument("--output", default="data/eval-report.md")
args = parser.parse_args()

# Block 2: prompts, tokenizer, base model
# ---------------------
prompts = load_dataset(args.dataset, split="test_sft")["prompt"][: args.num_prompts]
print(f"{len(prompts)} prompts from test_sft")

tokenizer = AutoTokenizer.from_pretrained(args.sft)  # carries our chat template, saved by the SFT run

print("loading base model")
model = AutoModelForCausalLM.from_pretrained(
    args.base, dtype=torch.bfloat16, attn_implementation="sdpa", device_map="cuda"
)
model.eval()

# Block 3: generate one answer
# ---------------------
def answer(model, prompt):
    """Lay the prompt out with the chat template, let the model write, return only the new text."""
    text = tokenizer.apply_chat_template(
        [{"role": "user", "content": prompt}], tokenize=False, add_generation_prompt=True
    )
    inputs = tokenizer(text, return_tensors="pt").to(model.device)
    with torch.no_grad():
        out = model.generate(
            **inputs, max_new_tokens=args.max_new_tokens, do_sample=False, pad_token_id=tokenizer.eos_token_id
        )
    new_tokens = out[0][inputs["input_ids"].shape[1]:]
    return tokenizer.decode(new_tokens, skip_special_tokens=True).strip()

# Block 4: base, then SFT, then DPO; write the Markdown report
# ---------------------
results = {}

print("generating: base")
results["base"] = [answer(model, p) for p in prompts]

model = PeftModel.from_pretrained(model, args.sft, adapter_name="sft")
print("generating: sft")
results["sft"] = [answer(model, p) for p in prompts]

model.load_adapter(args.dpo, adapter_name="dpo")
model.set_adapter("dpo")
print("generating: dpo")
results["dpo"] = [answer(model, p) for p in prompts]

with open(args.output, "w") as f:
    f.write(f"# Base vs SFT vs DPO on {len(prompts)} test_sft prompts\n\n")
    for i, prompt in enumerate(prompts):
        f.write(f"## Prompt {i + 1}\n\n> " + prompt.replace("\n", "\n> ") + "\n\n")
        for name in ["base", "sft", "dpo"]:
            f.write(f"**{name}**\n\n{results[name][i]}\n\n")
print(f"Report written to {args.output}")
