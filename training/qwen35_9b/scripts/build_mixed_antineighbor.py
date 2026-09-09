import json, hashlib, argparse, random
from pathlib import Path
from collections import defaultdict, deque

def h(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()

def load(path):
    return json.load(open(path, encoding="utf-8"))

def save(data, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    json.dump(data, open(path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

p = argparse.ArgumentParser()
p.add_argument("--inputs", nargs="+", required=True)
p.add_argument("--output", required=True)
p.add_argument("--min-gap", type=int, default=64)
p.add_argument("--seed", type=int, default=42)
args = p.parse_args()

random.seed(args.seed)

data = []
for f in args.inputs:
    data.extend(load(f))

groups = defaultdict(list)
for x in data:
    groups[h(x["output"])].append(x)

for g in groups.values():
    random.shuffle(g)

result = []
recent = deque(maxlen=args.min_gap)

while groups:
    candidates = [(k, len(v)) for k, v in groups.items() if k not in recent]
    if not candidates:
        candidates = [(k, len(v)) for k, v in groups.items()]

    k, _ = max(candidates, key=lambda x: x[1])
    item = groups[k].pop()
    result.append(item)
    recent.append(k)

    if not groups[k]:
        del groups[k]

# Vérification
last = {}
violations = 0
min_seen_gap = 10**9

for i, x in enumerate(result):
    key = h(x["output"])
    if key in last:
        gap = i - last[key]
        min_seen_gap = min(min_seen_gap, gap)
        if gap < args.min_gap:
            violations += 1
    last[key] = i

print("total:", len(result))
print("unique outputs:", len(set(h(x['output']) for x in result)))
print("min_gap_requested:", args.min_gap)
print("min_gap_observed:", None if min_seen_gap == 10**9 else min_seen_gap)
print("violations:", violations)

save(result, args.output)
print("saved:", args.output)
