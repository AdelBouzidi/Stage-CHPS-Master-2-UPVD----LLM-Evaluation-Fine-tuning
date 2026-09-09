#!/usr/bin/env python3
import json
import re
import csv
from pathlib import Path
from collections import Counter, defaultdict

BENCHMARK_PATH = Path("../benchmark.json")
RESULTS_DIR = Path("results")
SOLUTIONS_DIR = Path("results_qwen_lora/solutions")
OUT_DIR = Path("results/task_analysis")
OUT_DIR.mkdir(parents=True, exist_ok=True)

BASE_MODEL_KEY = "base_humaneval_mistral_conc3"

# Modèles à comparer si les fichiers existent
MODEL_KEYS = [
    "base_humaneval_mistral_conc3",
    "ft_A_humaneval_mistral_conc3",
    "ft_B_humaneval_mistral_conc3",
    "ft_C_humaneval_mistral_conc3",
    "ft_AB_antineighbor_humaneval_mistral_conc3",
    "ft_AC_antineighbor_humaneval_mistral_conc3",
    "ft_AB_shuffle_humaneval_mistral_conc3",
    "ft_AC_shuffle_humaneval_mistral_conc3",
    "ft_B_then_A_humaneval_mistral_conc3",
    "ft_C_then_A_humaneval_mistral_conc3",
]

SCIENTIFIC_KEYWORDS = [
    "matrix", "matrices", "vector", "vectors", "array", "arrays",
    "float", "double", "real", "number", "numbers", "numeric",
    "sum", "product", "mean", "average", "median", "variance",
    "distance", "euclidean", "geometry", "coordinate", "point", "points",
    "circle", "triangle", "rectangle", "polygon",
    "simulate", "simulation", "physics", "scientific", "compute",
    "linear", "equation", "polynomial", "integral", "derivative",
    "prime", "factor", "gcd", "lcm",
]

ALGORITHMIC_KEYWORDS = [
    "sort", "sorted", "reverse", "list", "string", "substring",
    "palindrome", "parentheses", "bracket", "sequence", "subsequence",
    "count", "filter", "remove", "replace", "split", "join",
    "unique", "duplicate", "index", "indices", "maximum", "minimum",
    "search", "find", "contains", "prefix", "suffix",
]

STRING_KEYWORDS = [
    "string", "character", "word", "words", "text", "substring",
    "palindrome", "parentheses", "bracket", "vowel", "consonant",
]

IO_KEYWORDS = [
    "read", "input", "stdin", "print", "output",
]

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_prompt(task):
    # Adapté aux formats possibles
    for k in ["prompt", "instruction", "description", "text"]:
        if k in task and task[k]:
            return str(task[k])
    return json.dumps(task, ensure_ascii=False)

def keyword_hits(text, keywords):
    low = text.lower()
    hits = []
    for kw in keywords:
        if re.search(r"\b" + re.escape(kw.lower()) + r"\b", low):
            hits.append(kw)
    return hits

def classify_task(prompt):
    sci = keyword_hits(prompt, SCIENTIFIC_KEYWORDS)
    algo = keyword_hits(prompt, ALGORITHMIC_KEYWORDS)
    strings = keyword_hits(prompt, STRING_KEYWORDS)
    io = keyword_hits(prompt, IO_KEYWORDS)

    # Classification heuristique simple
    if strings:
        main = "string/text"
    elif sci and algo:
        main = "mixed_scientific_algorithmic"
    elif sci:
        main = "scientific/numeric"
    elif algo:
        main = "algorithmic"
    else:
        main = "other/general"

    return {
        "main_category": main,
        "scientific_hits": sci,
        "algorithmic_hits": algo,
        "string_hits": strings,
        "io_hits": io,
        "is_scientific_like": bool(sci),
        "is_algorithmic_like": bool(algo),
        "is_string_like": bool(strings),
    }

def load_evaluation_details(model_key):
    path = RESULTS_DIR / f"{model_key}_evaluation_details.json"
    if not path.exists():
        return None
    data = load_json(path)
    return data

def load_solution_file(model_key):
    path = SOLUTIONS_DIR / f"{model_key}_solutions.json"
    if not path.exists():
        return None
    try:
        data = load_json(path)
    except Exception:
        return None
    if not isinstance(data, list):
        return None
    if any(x is None for x in data):
        # génération incomplète : on ignore
        return None
    return data

def status_by_task(details):
    d = {}
    for item in details:
        idx = item.get("index")
        d[idx] = {
            "status": item.get("status"),
            "score": int(item.get("score", 0)),
            "details": item.get("details"),
            "code_chars": item.get("code_chars"),
            "extraction_status": item.get("extraction_status"),
            "generation_error": item.get("generation_error"),
        }
    return d

def short(text, n=220):
    text = str(text).replace("\n", " ")
    return text[:n] + ("..." if len(text) > n else "")

def main():
    benchmark = load_json(BENCHMARK_PATH)
    n = len(benchmark)

    print("=" * 100)
    print("HumanEval task analysis")
    print("=" * 100)
    print("benchmark:", BENCHMARK_PATH)
    print("tasks:", n)

    # Charger les résultats existants
    model_details = {}
    model_status = {}
    model_solutions = {}

    for model in MODEL_KEYS:
        details = load_evaluation_details(model)
        sols = load_solution_file(model)

        if details is None:
            print(f"[SKIP] no evaluation details for {model}")
            continue

        if len(details) != n:
            print(f"[SKIP] details length mismatch for {model}: {len(details)} vs {n}")
            continue

        model_details[model] = details
        model_status[model] = status_by_task(details)
        model_solutions[model] = sols
        print(f"[OK] loaded {model}")

    if BASE_MODEL_KEY not in model_status:
        raise SystemExit(f"Base model details missing: {BASE_MODEL_KEY}")

    # Classifier les tâches
    task_rows = []
    category_counter = Counter()
    scientific_count = 0

    for i, task in enumerate(benchmark):
        prompt = get_prompt(task)
        cls = classify_task(prompt)
        category_counter[cls["main_category"]] += 1
        scientific_count += int(cls["is_scientific_like"])

        row = {
            "index": i,
            "task_id": task.get("task_id", i),
            "prompt": prompt,
            **cls,
        }
        task_rows.append(row)

    # Construire matrice par tâche
    per_task = []

    for i, task in enumerate(benchmark):
        row = dict(task_rows[i])
        base = model_status[BASE_MODEL_KEY][i]
        row["base_status"] = base["status"]
        row["base_score"] = base["score"]

        ft_ok_models = []
        ft_better_than_base = []
        base_better_than_ft = []

        for model in model_status:
            st = model_status[model][i]
            row[f"{model}__status"] = st["status"]
            row[f"{model}__score"] = st["score"]

            if model != BASE_MODEL_KEY:
                if st["score"] == 1:
                    ft_ok_models.append(model)
                if base["score"] == 0 and st["score"] == 1:
                    ft_better_than_base.append(model)
                if base["score"] == 1 and st["score"] == 0:
                    base_better_than_ft.append(model)

        row["ft_ok_models"] = ft_ok_models
        row["ft_better_than_base"] = ft_better_than_base
        row["base_better_than_ft"] = base_better_than_ft
        row["num_ft_better_than_base"] = len(ft_better_than_base)
        row["num_ft_ok"] = len(ft_ok_models)

        per_task.append(row)

    # Résumé par modèle
    model_summary = {}

    for model in model_status:
        ok = sum(model_status[model][i]["score"] for i in range(n))
        compile_err = sum(1 for i in range(n) if model_status[model][i]["status"] == "compile_err")
        runtime_err = sum(1 for i in range(n) if model_status[model][i]["status"] == "runtime_err")
        ineq = sum(1 for i in range(n) if model_status[model][i]["status"] == "ineq")
        exception = sum(1 for i in range(n) if model_status[model][i]["status"] == "exception")

        beats_base = []
        loses_to_base = []

        if model != BASE_MODEL_KEY:
            for i in range(n):
                b = model_status[BASE_MODEL_KEY][i]["score"]
                s = model_status[model][i]["score"]
                if b == 0 and s == 1:
                    beats_base.append(i)
                if b == 1 and s == 0:
                    loses_to_base.append(i)

        model_summary[model] = {
            "ok": ok,
            "total": n,
            "pass_at_1": ok / n if n else 0,
            "compile_err": compile_err,
            "runtime_err": runtime_err,
            "ineq": ineq,
            "exception": exception,
            "beats_base_count": len(beats_base),
            "beats_base_task_indices": beats_base,
            "loses_to_base_count": len(loses_to_base),
            "loses_to_base_task_indices": loses_to_base,
        }

    # Résumé catégories HumanEval
    category_summary = {}

    for cat in sorted(category_counter):
        indices = [r["index"] for r in task_rows if r["main_category"] == cat]
        category_summary[cat] = {
            "count": len(indices),
            "indices": indices,
            "model_ok": {}
        }
        for model in model_status:
            ok = sum(model_status[model][i]["score"] for i in indices)
            category_summary[cat]["model_ok"][model] = {
                "ok": ok,
                "total": len(indices),
                "rate": ok / len(indices) if indices else 0,
            }

    # Cas où au moins un FT bat le base
    ft_beats_base_tasks = [
        r for r in per_task
        if r["num_ft_better_than_base"] > 0
    ]

    base_beats_all_ft_tasks = [
        r for r in per_task
        if r["base_score"] == 1 and r["num_ft_ok"] == 0
    ]

    # Sauvegarde JSON global
    out_json = {
        "benchmark": str(BENCHMARK_PATH),
        "num_tasks": n,
        "loaded_models": list(model_status.keys()),
        "task_category_counts": dict(category_counter),
        "scientific_like_count": scientific_count,
        "scientific_like_rate": scientific_count / n if n else 0,
        "model_summary": model_summary,
        "category_summary": category_summary,
        "ft_beats_base_tasks": [
            {
                "index": r["index"],
                "task_id": r["task_id"],
                "main_category": r["main_category"],
                "prompt_short": short(r["prompt"]),
                "ft_better_than_base": r["ft_better_than_base"],
                "scientific_hits": r["scientific_hits"],
                "algorithmic_hits": r["algorithmic_hits"],
                "string_hits": r["string_hits"],
            }
            for r in ft_beats_base_tasks
        ],
        "base_beats_all_ft_tasks": [
            {
                "index": r["index"],
                "task_id": r["task_id"],
                "main_category": r["main_category"],
                "prompt_short": short(r["prompt"]),
                "scientific_hits": r["scientific_hits"],
                "algorithmic_hits": r["algorithmic_hits"],
                "string_hits": r["string_hits"],
            }
            for r in base_beats_all_ft_tasks
        ],
        "per_task": per_task,
    }

    out_path = OUT_DIR / "humaneval_task_difference_analysis.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out_json, f, indent=2, ensure_ascii=False)

    # CSV compact
    csv_path = OUT_DIR / "humaneval_task_difference_matrix.csv"
    fieldnames = [
        "index", "task_id", "main_category",
        "is_scientific_like", "is_algorithmic_like", "is_string_like",
        "base_status", "base_score",
        "num_ft_better_than_base", "num_ft_ok",
        "ft_better_than_base", "ft_ok_models",
        "prompt",
    ]
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in per_task:
            w.writerow({
                "index": r["index"],
                "task_id": r["task_id"],
                "main_category": r["main_category"],
                "is_scientific_like": r["is_scientific_like"],
                "is_algorithmic_like": r["is_algorithmic_like"],
                "is_string_like": r["is_string_like"],
                "base_status": r["base_status"],
                "base_score": r["base_score"],
                "num_ft_better_than_base": r["num_ft_better_than_base"],
                "num_ft_ok": r["num_ft_ok"],
                "ft_better_than_base": ";".join(r["ft_better_than_base"]),
                "ft_ok_models": ";".join(r["ft_ok_models"]),
                "prompt": r["prompt"].replace("\n", " "),
            })

    # Affichage résumé
    print("")
    print("=" * 100)
    print("TASK CATEGORY COUNTS")
    print("=" * 100)
    for k, v in category_counter.most_common():
        print(f"{k:35s}: {v}")

    print("")
    print("scientific_like:", scientific_count, "/", n, f"({scientific_count/n:.3f})")

    print("")
    print("=" * 100)
    print("MODEL SUMMARY")
    print("=" * 100)
    for model, s in sorted(model_summary.items(), key=lambda kv: kv[1]["pass_at_1"], reverse=True):
        print(
            f"{model:45s} ok={s['ok']:3d}/{n} "
            f"pass={s['pass_at_1']:.4f} "
            f"compile_err={s['compile_err']:3d} "
            f"runtime_err={s['runtime_err']:3d} "
            f"ineq={s['ineq']:3d} "
            f"beats_base={s['beats_base_count']:3d} "
            f"loses_to_base={s['loses_to_base_count']:3d}"
        )

    print("")
    print("=" * 100)
    print("TASKS WHERE AT LEAST ONE FT MODEL BEATS BASE")
    print("=" * 100)
    print("count:", len(ft_beats_base_tasks))
    for r in ft_beats_base_tasks[:30]:
        print("-" * 100)
        print("index:", r["index"], "task_id:", r["task_id"], "category:", r["main_category"])
        print("FT better:", ", ".join(r["ft_better_than_base"]))
        print("prompt:", short(r["prompt"], 350))

    print("")
    print("=" * 100)
    print("CATEGORY SUMMARY")
    print("=" * 100)
    for cat, cs in category_summary.items():
        print("-" * 100)
        print(cat, "count:", cs["count"])
        for model, m in sorted(cs["model_ok"].items(), key=lambda kv: kv[1]["rate"], reverse=True):
            print(f"  {model:45s} {m['ok']:3d}/{m['total']} rate={m['rate']:.4f}")

    print("")
    print("Saved:")
    print(" ", out_path)
    print(" ", csv_path)
    print("=" * 100)

if __name__ == "__main__":
    main()