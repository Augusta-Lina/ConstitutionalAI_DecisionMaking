# Block 1: imports and arguments
# ---------------------

"""Push a cleaned run folder (train.jsonl, test.jsonl) to the Hub with the four
split names the trainers expect: {split}_sft (first half) and {split}_prefs (second half)."""

from dataclasses import dataclass

from datasets import load_dataset
from dotenv import load_dotenv
from huggingface_hub import HfApi
from transformers import HfArgumentParser

load_dotenv()


@dataclass
class Args:
    folder: str = ""
    """Folder holding train.jsonl and test.jsonl"""
    repo_id: str = ""
    """Hub dataset name, e.g. cai-2026-10-20_synth_v3.1_clean (user prefix added if missing)"""


parser = HfArgumentParser((Args,))
args = parser.parse_args_into_dataclasses()[0]
api = HfApi()

# Block 2: load the two files and push each as two halves
# ---------------------
repo_id = args.repo_id
if "/" not in repo_id:  # find the current user, like generate_dataset.py
    repo_id = f"{api.whoami()['name']}/{repo_id}"

for split in ["train", "test"]:
    ds = load_dataset("json", data_files=f"{args.folder}/{split}.jsonl", split="train")
    half = len(ds) // 2
    ds.select(range(half)).push_to_hub(repo_id, split=f"{split}_sft")
    ds.select(range(half, len(ds))).push_to_hub(repo_id, split=f"{split}_prefs")
    print(f"{split}: {half} rows -> {split}_sft, {len(ds) - half} rows -> {split}_prefs")

print(f"Pushed to the Hub as {repo_id}")
