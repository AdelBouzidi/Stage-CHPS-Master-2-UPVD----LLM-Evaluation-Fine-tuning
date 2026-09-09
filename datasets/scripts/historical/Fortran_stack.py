from datasets import load_dataset
import json
import os

HF_TOKEN = os.environ.get("HF_TOKEN")

dataset = load_dataset(
    "bigcode/the-stack",
    data_dir="data/fortran",
    split="train",
    streaming=True,
    token=HF_TOKEN,
)

results = []
max_samples = 1000
scanned = 0

for sample in dataset:
    scanned += 1
    code = sample.get("content", "")

    # Filtres simples
    if len(code) < 50 or len(code) > 5000:
        continue

    code_lower = code.lower()
    if "program" not in code_lower and "subroutine" not in code_lower and "function" not in code_lower and "module" not in code_lower:
        continue

    results.append({
        "id": scanned,
        "code": code,
        "path": sample.get("path"),
        "repo": sample.get("repo_name"),
        "size": sample.get("size"),
        "ext": sample.get("ext"),
    })

    if len(results) >= max_samples:
        break

    if scanned % 500 == 0:
        print(f"Scanned {scanned}, kept {len(results)}")

with open("fortran_candidates.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"Done. Scanned {scanned}, saved {len(results)} samples.")