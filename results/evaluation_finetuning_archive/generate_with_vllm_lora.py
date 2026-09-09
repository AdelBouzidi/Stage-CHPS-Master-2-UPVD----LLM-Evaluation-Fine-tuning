#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generate Fortran HumanEval solutions using vLLM OpenAI-compatible API.

This script ONLY performs generation.

Pipeline:
benchmark.json
  -> vLLM /v1/chat/completions
  -> extract Fortran code
  -> solutions.json

Evaluation is done later by a separate script using evaluate.py.
"""

import argparse
import json
import os
import re
import sys
import time
import threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from tqdm import tqdm


# ---------------------------------------------------------------------
# Import old prompt function from parent sandbox directory
# ---------------------------------------------------------------------

CURRENT_DIR = Path(__file__).resolve().parent
SANDBOX_DIR = CURRENT_DIR.parent

sys.path.insert(0, str(SANDBOX_DIR))

try:
    from generate_with_openwebui import create_prompt
except Exception as e:
    print("ERROR: Could not import create_prompt from generate_with_openwebui.py")
    print(f"Reason: {e}")
    print(f"Expected file: {SANDBOX_DIR / 'generate_with_openwebui.py'}")
    sys.exit(1)


# ---------------------------------------------------------------------
# Robust Fortran extraction
# ---------------------------------------------------------------------

def clean_extracted_fortran(code: str) -> str:
    if not code:
        return ""

    code = code.strip()

    code = re.sub(r"^```(?:fortran|f90)?", "", code.strip(), flags=re.IGNORECASE)
    code = re.sub(r"```$", "", code.strip())

    bad_prefixes = [
        "here is the code:",
        "solution:",
        "program:",
        "fortran code:",
    ]

    changed = True
    while changed:
        changed = False
        stripped = code.lstrip()
        lower = stripped.lower()
        for p in bad_prefixes:
            if lower.startswith(p):
                code = stripped[len(p):].lstrip()
                changed = True

    return code.strip()


def looks_like_real_fortran_program(code: str) -> bool:
    """
    Strict validation to avoid false positives like:
    'program structure (`program name` ... `end program name`)'
    """
    if not code:
        return False

    code = code.strip()

    has_program_start = re.search(
        r"(?im)^\s*program\s+[a-zA-Z_][a-zA-Z0-9_]*\b",
        code,
    )

    has_end_program = re.search(
        r"(?im)^\s*end\s+program(?:\s+[a-zA-Z_][a-zA-Z0-9_]*)?\b",
        code,
    )

    has_implicit_none = re.search(
        r"(?im)^\s*implicit\s+none\b",
        code,
    )

    bad_markers = [
        "thinking process",
        "analyze the request",
        "determine program",
        "drafting the code",
        "program structure",
        "no explanations",
        "markdown",
        "code block",
    ]

    low = code.lower()
    if any(marker in low for marker in bad_markers):
        return False

    return bool(
        has_program_start
        and has_end_program
        and has_implicit_none
        and len(code) >= 80
    )


def robust_extract_fortran_code(raw_response: str) -> str:
    """
    Extract only a real Fortran program.

    Strategy:
    1. Remove everything before </think>, if present.
    2. Prefer valid fenced Fortran code blocks.
    3. Otherwise find valid line-based program ... end program blocks.
    4. Do NOT fallback to the old extractor, because it produced false positives.
    """
    if not raw_response:
        return ""

    candidates = []

    full_text = raw_response.strip()

    texts_to_scan = [full_text]

    if "</think>" in full_text:
        after_think = full_text.split("</think>")[-1].strip()
        texts_to_scan.insert(0, after_think)

    for text in texts_to_scan:
        fenced_patterns = [
            r"```fortran\s*(.*?)```",
            r"```f90\s*(.*?)```",
            r"```\s*(.*?)```",
        ]

        for pattern in fenced_patterns:
            matches = re.findall(pattern, text, flags=re.IGNORECASE | re.DOTALL)
            for m in matches:
                code = clean_extracted_fortran(m)
                if looks_like_real_fortran_program(code):
                    candidates.append(code)

        program_pattern = (
            r"(?im)^\s*program\s+[a-zA-Z_][a-zA-Z0-9_]*\b"
            r".*?"
            r"^\s*end\s+program(?:\s+[a-zA-Z_][a-zA-Z0-9_]*)?\b"
        )

        matches = re.findall(
            program_pattern,
            text,
            flags=re.IGNORECASE | re.DOTALL | re.MULTILINE,
        )

        for m in matches:
            code = clean_extracted_fortran(m)
            if looks_like_real_fortran_program(code):
                candidates.append(code)

    if candidates:
        return candidates[-1].strip()

    return ""


# ---------------------------------------------------------------------
# HTTP call to vLLM
# ---------------------------------------------------------------------

_thread_local = threading.local()


def get_session() -> requests.Session:
    if not hasattr(_thread_local, "session"):
        _thread_local.session = requests.Session()
    return _thread_local.session


def call_vllm(
    prompt: str,
    model: str,
    base_url: str,
    temperature: float,
    top_p: float,
    max_tokens: int,
    timeout: int,
) -> str:
    url = base_url.rstrip("/") + "/v1/chat/completions"

    strict_prompt = (
        prompt
        + "\n\nIMPORTANT OUTPUT RULES:\n"
        + "Return only a complete Fortran 90 program.\n"
        + "The first non-empty line must start with: program <name>\n"
        + "The output must contain implicit none.\n"
        + "The output must end with: end program <name>\n"
        + "Do not include explanations.\n"
        + "Do not include reasoning.\n"
        + "Do not include Thinking Process.\n"
        + "Do not include markdown fences.\n"
        + "Do not include ```fortran.\n"
        + "Do not include <think> or </think>.\n"
    )

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a Fortran 90 code generator. "
                    "You must output only raw Fortran 90 source code. "
                    "No explanations. No reasoning. No markdown. "
                    "The output must be directly compilable with gfortran."
                ),
            },
            {
                "role": "user",
                "content": strict_prompt,
            },
        ],
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens,
        "stream": False,
    }

    session = get_session()

    response = session.post(
        url,
        headers={"Content-Type": "application/json"},
        json=payload,
        timeout=timeout,
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"vLLM HTTP {response.status_code}: {response.text[:1000]}"
        )

    data = response.json()

    try:
        return data["choices"][0]["message"]["content"] or ""
    except Exception:
        raise RuntimeError(f"Unexpected vLLM response format: {data}")


# ---------------------------------------------------------------------
# JSON helpers
# ---------------------------------------------------------------------

def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json_atomic(path: str, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    os.replace(tmp_path, path)


# ---------------------------------------------------------------------
# Generation logic
# ---------------------------------------------------------------------

def generate_one_problem(
    index: int,
    problem: dict,
    model: str,
    base_url: str,
    model_family: str,
    temperature: float,
    top_p: float,
    max_tokens: int,
    timeout: int,
) -> dict:
    task_id = problem.get("task_id", index)

    start = time.time()

    prompt = create_prompt(
        problem,
        model_family=model_family,
        model_name=model,
    )

    raw_response = ""
    code = ""
    error = None
    extraction_status = "unknown"

    try:
        raw_response = call_vllm(
            prompt=prompt,
            model=model,
            base_url=base_url,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            timeout=timeout,
        )

        code = robust_extract_fortran_code(raw_response)

        if looks_like_real_fortran_program(code):
            extraction_status = "ok"
        else:
            extraction_status = "warning"

    except Exception as e:
        error = str(e)
        code = ""
        extraction_status = "failed"

    elapsed = time.time() - start

    return {
        "index": index,
        "task_id": task_id,
        "model": model,
        "code": code,
        "raw_response": raw_response,
        "generation_time": elapsed,
        "prompt_chars": len(prompt),
        "response_chars": len(raw_response),
        "code_chars": len(code),
        "extraction_status": extraction_status,
        "error": error,
    }


def generate_solutions_vllm(
    benchmark_file: str,
    output_file: str,
    model: str,
    base_url: str,
    model_family: str,
    temperature: float,
    top_p: float,
    max_tokens: int,
    timeout: int,
    concurrency: int,
    save_every: int,
):
    benchmark = load_json(benchmark_file)
    total = len(benchmark)

    Path(output_file).parent.mkdir(parents=True, exist_ok=True)

    results = [None] * total
    completed = 0
    failed = 0
    warnings = 0

    print("=" * 70)
    print("vLLM Fortran HumanEval generation")
    print("=" * 70)
    print(f"Benchmark     : {benchmark_file}")
    print(f"Output        : {output_file}")
    print(f"Model         : {model}")
    print(f"Base URL      : {base_url}")
    print(f"Model family  : {model_family}")
    print(f"Problems      : {total}")
    print(f"Concurrency   : {concurrency}")
    print(f"Temperature   : {temperature}")
    print(f"Top-p         : {top_p}")
    print(f"Max tokens    : {max_tokens}")
    print(f"Timeout       : {timeout}s")
    print("=" * 70)
    print("")

    global_start = time.time()

    if concurrency <= 1:
        for i, problem in enumerate(tqdm(benchmark, desc=f"Generating {model}")):
            result = generate_one_problem(
                index=i,
                problem=problem,
                model=model,
                base_url=base_url,
                model_family=model_family,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens,
                timeout=timeout,
            )

            results[i] = result
            completed += 1

            if result["error"]:
                failed += 1
            elif result["extraction_status"] != "ok":
                warnings += 1

            print(
                f"[{completed}/{total}] "
                f"idx={i} task_id={result['task_id']} "
                f"time={result['generation_time']:.2f}s "
                f"response_chars={result['response_chars']} "
                f"code_chars={result['code_chars']} "
                f"extract={result['extraction_status']} "
                f"error={'yes' if result['error'] else 'no'}"
            )

            if completed % save_every == 0 or completed == total:
                save_json_atomic(output_file, results)

    else:
        with ThreadPoolExecutor(max_workers=concurrency) as executor:
            futures = {
                executor.submit(
                    generate_one_problem,
                    i,
                    problem,
                    model,
                    base_url,
                    model_family,
                    temperature,
                    top_p,
                    max_tokens,
                    timeout,
                ): i
                for i, problem in enumerate(benchmark)
            }

            with tqdm(total=total, desc=f"Generating {model}") as pbar:
                for future in as_completed(futures):
                    i = futures[future]

                    try:
                        result = future.result()
                    except Exception as e:
                        result = {
                            "index": i,
                            "task_id": benchmark[i].get("task_id", i),
                            "model": model,
                            "code": "",
                            "raw_response": "",
                            "generation_time": 0.0,
                            "prompt_chars": 0,
                            "response_chars": 0,
                            "code_chars": 0,
                            "extraction_status": "failed",
                            "error": f"future_error: {e}",
                        }

                    results[i] = result
                    completed += 1

                    if result["error"]:
                        failed += 1
                    elif result["extraction_status"] != "ok":
                        warnings += 1

                    elapsed = time.time() - global_start
                    avg = elapsed / completed
                    eta = avg * (total - completed)

                    print(
                        f"[{completed}/{total}] "
                        f"idx={i} task_id={result['task_id']} "
                        f"time={result['generation_time']:.2f}s "
                        f"response_chars={result['response_chars']} "
                        f"code_chars={result['code_chars']} "
                        f"extract={result['extraction_status']} "
                        f"failed={failed} warnings={warnings} "
                        f"ETA={eta/60:.1f}min"
                    )

                    if completed % save_every == 0 or completed == total:
                        save_json_atomic(output_file, results)

                    pbar.update(1)

    total_time = time.time() - global_start

    for i, item in enumerate(results):
        if item is None:
            results[i] = {
                "index": i,
                "task_id": benchmark[i].get("task_id", i),
                "model": model,
                "code": "",
                "raw_response": "",
                "generation_time": 0.0,
                "prompt_chars": 0,
                "response_chars": 0,
                "code_chars": 0,
                "extraction_status": "missing",
                "error": "missing_result",
            }

    save_json_atomic(output_file, results)

    print("")
    print("=" * 70)
    print("Generation complete")
    print("=" * 70)
    print(f"Model        : {model}")
    print(f"Problems     : {total}")
    print(f"Completed    : {completed}/{total}")
    print(f"Failed       : {failed}")
    print(f"Warnings     : {warnings}")
    print(f"Total time   : {total_time:.2f}s")
    print(f"Avg/problem  : {total_time / total:.2f}s")
    print(f"Output file  : {output_file}")
    print("=" * 70)

    return results


# ---------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate Fortran HumanEval solutions using vLLM + Qwen LoRA"
    )

    parser.add_argument("--benchmark", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--base-url", default="http://internal-host:8087")

    parser.add_argument(
        "--model-family",
        default="qwen",
        choices=[
            "mistral",
            "qwen",
            "deepseek",
            "codellama",
            "gpt",
            "llama3",
            "gemma",
            "phi",
            "generic-instruct",
            "base",
        ],
    )

    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--top-p", type=float, default=1.0)
    parser.add_argument("--max-tokens", type=int, default=2048)
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--concurrency", type=int, default=1)
    parser.add_argument("--save-every", type=int, default=1)

    args = parser.parse_args()

    generate_solutions_vllm(
        benchmark_file=args.benchmark,
        output_file=args.output,
        model=args.model,
        base_url=args.base_url,
        model_family=args.model_family,
        temperature=args.temperature,
        top_p=args.top_p,
        max_tokens=args.max_tokens,
        timeout=args.timeout,
        concurrency=args.concurrency,
        save_every=args.save_every,
    )