#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter

ROOT = Path("/path/to/calypso/workdir/finetuning_domaines_eval")

FILES = [
    ("A", ROOT / "dataset/phase2_splits/train/train_A.json"),
    ("B", ROOT / "dataset/phase2_splits/train/train_B_dedup_output.json"),
    ("C", ROOT / "dataset/phase2_splits/train/train_C_dedup_output.json"),
]

OUT = ROOT / "dataset/phase2_splits/train/train_A_plus_B_plus_C_dedup_BC.json"

all_examples = []
stats = {}

for expected_type, path in FILES:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")

    data = json.load(open(path, "r", encoding="utf-8"))

    if not isinstance(data, list):
        raise ValueError(f"{path} is not a JSON list")

    print(f"{expected_type}: loaded {len(data)} examples from {path}")

    missing_instruction = 0
    missing_output = 0
    type_counter = Counter()

    for ex in data:
        if not isinstance(ex, dict):
            raise ValueError(f"Invalid example in {path}: not a dict")

        if "instruction" not in ex:
            missing_instruction += 1
        if "output" not in ex:
            missing_output += 1

        t = ex.get("type", ex.get("source_type", expected_type))
        type_counter[t] += 1

        # On ne modifie pas instruction/output.
        # On ajoute seulement un champ de traçabilité si absent.
        ex = dict(ex)
        ex.setdefault("abc_source_type", expected_type)

        all_examples.append(ex)

    stats[expected_type] = {
        "file": str(path),
        "count": len(data),
        "missing_instruction": missing_instruction,
        "missing_output": missing_output,
        "type_counter": dict(type_counter),
    }

# Vérifications globales
print("\nGlobal checks")
print("=" * 80)
print("Total examples:", len(all_examples))

source_counts = Counter(ex.get("abc_source_type", "UNKNOWN") for ex in all_examples)
print("abc_source_type counts:", dict(source_counts))

missing_instruction_total = sum(1 for ex in all_examples if "instruction" not in ex)
missing_output_total = sum(1 for ex in all_examples if "output" not in ex)

print("missing instruction:", missing_instruction_total)
print("missing output     :", missing_output_total)

if missing_instruction_total > 0 or missing_output_total > 0:
    raise ValueError("Some examples are missing instruction/output")

# Vérifier les doublons exacts par output dans B+C seulement
for label in ["B", "C"]:
    outputs = [
        ex.get("output", "")
        for ex in all_examples
        if ex.get("abc_source_type") == label
    ]
    unique_outputs = len(set(outputs))
    total = len(outputs)
    print(f"{label}: total={total}, unique_outputs={unique_outputs}, duplicates={total - unique_outputs}")

# Sauvegarde
OUT.parent.mkdir(parents=True, exist_ok=True)

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(all_examples, f, indent=2, ensure_ascii=False)

print("\nSaved:")
print(OUT)
print("Final total:", len(all_examples))
