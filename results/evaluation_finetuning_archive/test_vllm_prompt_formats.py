#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test different HumanEval prompt formats with vLLM.

Goal:
- Compare model-family formats used by create_prompt()
- Use the same vLLM endpoint as generate_with_vllm_lora.py
- Recommend the best --model-family for Qwen3.5-9B / LoRA evaluation

This script does generation only.
It does not compile or execute the generated code.
"""

import argparse
import json
import sys
import time
from pathlib import Path

import requests


CURRENT_DIR = Path(__file__).resolve().parent
SANDBOX_DIR = CURRENT_DIR.parent

sys.path.insert(0, str(SANDBOX_DIR))
sys.path.insert(0, str(CURRENT_DIR))

try:
    from generate_with_openwebui import create_prompt
except Exception as e:
    print("ERROR: Could not import create_prompt from ../generate_with_openwebui.py")
    print(f"Reason: {e}")
    sys.exit(1)

try:
    from generate_with_vllm_lora import (
        robust_extract_fortran_code,
        looks_like_real_fortran_program,
    )
except Exception as e:
    print("ERROR: Could not import extraction helpers from generate_with_vllm_lora.py")
    print(f"Reason: {e}")
    sys.exit(1)


FORMATS = [
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
]


TEST_PROBLEM = {
    "task": "Write a Fortran90 program that reads two integers and prints their sum.",
    "signature": "int add(int a, int b)",
    "example": "Input: 2 3 | Output: 5",
    "tests": [
        {"input": "2 3", "output": 5},
        {"input": "10 20", "output": 30},
    ],
}


def call_vllm(prompt, model, base_url, temperature, top_p, max_tokens, timeout):
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

    r = requests.post(
        url,
        headers={"Content-Type": "application/json"},
        json=payload,
        timeout=timeout,
    )

    if r.status_code != 200:
        raise RuntimeError(f"vLLM HTTP {r.status_code}: {r.text[:1000]}")

    data = r.json()
    return data["choices"][0]["message"]["content"] or ""


def score_generation(raw_response, code):
    """
    Score /10.
    This is only a format quality score, not functional correctness.
    """
    score = 0
    low_raw = (raw_response or "").lower()
    low_code = (code or "").lower()

    checks = {}

    checks["has_code"] = bool(code and len(code.strip()) > 50)
    checks["real_program"] = looks_like_real_fortran_program(code)
    checks["has_program"] = "program" in low_code
    checks["has_implicit_none"] = "implicit none" in low_code
    checks["has_end_program"] = "end program" in low_code
    checks["no_think_tags"] = "<think>" not in low_raw and "</think>" not in low_raw
    checks["no_thinking_process"] = "thinking process" not in low_raw
    checks["no_markdown_in_code"] = "```" not in (code or "")
    checks["not_too_short"] = len(code or "") >= 100
    checks["not_too_verbose_raw"] = len(raw_response or "") <= 4000

    weights = {
        "has_code": 1,
        "real_program": 2,
        "has_program": 1,
        "has_implicit_none": 1,
        "has_end_program": 1,
        "no_think_tags": 1,
        "no_thinking_process": 1,
        "no_markdown_in_code": 1,
        "not_too_short": 1,
        "not_too_verbose_raw": 1,
    }

    for k, passed in checks.items():
        if passed:
            score += weights[k]

    return score, checks


def test_format(fmt, model, base_url, temperature, top_p, max_tokens, timeout, show_prompt=False):
    print("\n" + "=" * 80)
    print(f"Testing format: {fmt} | model: {model}")
    print("=" * 80)

    prompt = create_prompt(
        TEST_PROBLEM,
        model_family=fmt,
        model_name=model,
    )

    if show_prompt:
        print("\nPROMPT PREVIEW")
        print("-" * 80)
        print(prompt[:2500])
        print("-" * 80)

    start = time.time()

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

        elapsed = time.time() - start
        code = robust_extract_fortran_code(raw_response)
        score, checks = score_generation(raw_response, code)

        print(f"Generation time : {elapsed:.2f}s")
        print(f"Raw chars       : {len(raw_response)}")
        print(f"Code chars      : {len(code)}")
        print(f"Score           : {score}/11")

        print("\nChecks:")
        for k, v in checks.items():
            print(f"  {'✓' if v else '✗'} {k}")

        print("\nExtracted code preview:")
        print("-" * 80)
        print((code or "")[:1200])
        print("-" * 80)

        return {
            "format": fmt,
            "model": model,
            "score": score,
            "generation_time": elapsed,
            "raw_chars": len(raw_response),
            "code_chars": len(code),
            "checks": checks,
            "code_preview": (code or "")[:1500],
            "raw_preview": (raw_response or "")[:1500],
            "error": None,
        }

    except Exception as e:
        elapsed = time.time() - start
        print(f"ERROR after {elapsed:.2f}s: {e}")

        return {
            "format": fmt,
            "model": model,
            "score": 0,
            "generation_time": elapsed,
            "raw_chars": 0,
            "code_chars": 0,
            "checks": {},
            "code_preview": "",
            "raw_preview": "",
            "error": str(e),
        }


def main():
    parser = argparse.ArgumentParser(description="Test prompt formats with vLLM")
    parser.add_argument("--model", required=True, help="vLLM model name, e.g. qwen35-9b-base or ft_B")
    parser.add_argument("--base-url", default="http://internal-host:8087")
    parser.add_argument("--format", default=None, choices=FORMATS)
    parser.add_argument("--compare-all", action="store_true")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--top-p", type=float, default=1.0)
    parser.add_argument("--max-tokens", type=int, default=1024)
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--output", default=None)
    parser.add_argument("--show-prompt", action="store_true")

    args = parser.parse_args()

    if args.compare_all or args.format is None:
        formats = FORMATS
    else:
        formats = [args.format]

    print("\n" + "#" * 80)
    print("VLLM PROMPT FORMAT TEST")
    print("#" * 80)
    print(f"Model       : {args.model}")
    print(f"Base URL    : {args.base_url}")
    print(f"Formats     : {formats}")
    print(f"Temperature : {args.temperature}")
    print(f"Top-p       : {args.top_p}")
    print(f"Max tokens  : {args.max_tokens}")
    print("#" * 80)

    results = []

    for fmt in formats:
        res = test_format(
            fmt=fmt,
            model=args.model,
            base_url=args.base_url,
            temperature=args.temperature,
            top_p=args.top_p,
            max_tokens=args.max_tokens,
            timeout=args.timeout,
            show_prompt=args.show_prompt,
        )
        results.append(res)

    print("\n\n" + "=" * 80)
    print("SUMMARY - Best to Worst")
    print("=" * 80)

    results_sorted = sorted(
        results,
        key=lambda x: (x["score"], x["code_chars"], -x["generation_time"]),
        reverse=True,
    )

    print(f"{'Format':<20} {'Score':<8} {'Code chars':<12} {'Raw chars':<10} {'Time(s)':<10} {'Status'}")
    print("-" * 80)

    for r in results_sorted:
        status = "OK" if r["error"] is None else "ERROR"
        print(
            f"{r['format']:<20} "
            f"{r['score']:<8} "
            f"{r['code_chars']:<12} "
            f"{r['raw_chars']:<10} "
            f"{r['generation_time']:.1f}      "
            f"{status}"
        )

    best = results_sorted[0]["format"]

    print("\n" + "=" * 80)
    print(f"RECOMMENDATION FOR {args.model}: --model-family {best}")
    print("=" * 80)

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "model": args.model,
                    "base_url": args.base_url,
                    "best_format": best,
                    "results": results_sorted,
                },
                f,
                indent=2,
                ensure_ascii=False,
            )
        print(f"\nSaved results to: {args.output}")


if __name__ == "__main__":
    main()