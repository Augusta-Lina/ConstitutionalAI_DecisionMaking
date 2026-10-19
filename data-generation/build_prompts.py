"""
Turn the synthetic decision prompts (a numbered Markdown list, one prompt per line, tag in brackets first)
into the files the pipeline reads: train.jsonl and test.jsonl, one prompt per line with its tag,
split 80/20 with a fixed seed so the same Markdown always gives the same split.

    uv run data-generation/build_prompts.py
"""

# Block 1: settings
# ---------------------
import argparse
import json
import random
import re
from collections import Counter
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--input", default="data-generation/synthetic-prompts.md")
parser.add_argument("--output", default="data-generation/prompts/synthetic")
parser.add_argument("--test_fraction", type=float, default=0.2)
parser.add_argument("--seed", type=int, default=0)
args = parser.parse_args()

# Block 2: read the numbered lines
# ---------------------
LINE = re.compile(r"^\d+\.\s+\[([\w-]+)\]\s+(.+?)\s*$")

rows = []
for line in Path(args.input).read_text().splitlines():
    m = LINE.match(line)
    if m:
        rows.append({"prompt": m.group(2), "tag": m.group(1)})

if not rows:
    raise SystemExit(f"No prompts found in {args.input}: expected lines like '12. [governance] text'")
print(f"{len(rows)} prompts read from {args.input}")
print("by tag:", dict(Counter(r["tag"] for r in rows)))

# Block 3: shuffle with a fixed seed, split, write train.jsonl and test.jsonl
# ---------------------
random.Random(args.seed).shuffle(rows)
n_test = round(len(rows) * args.test_fraction)
splits = {"test": rows[:n_test], "train": rows[n_test:]}

out_dir = Path(args.output)
out_dir.mkdir(parents=True, exist_ok=True)
for name, split_rows in splits.items():
    with open(out_dir / f"{name}.jsonl", "w") as f:
        for r in split_rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"{name}: {len(split_rows)} prompts -> {out_dir / (name + '.jsonl')} | by tag: {dict(Counter(r['tag'] for r in split_rows))}")
