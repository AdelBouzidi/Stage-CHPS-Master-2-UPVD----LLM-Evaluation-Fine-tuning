#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rebuild_type_a_humaneval_like_v3.py

V3 du pipeline de reconstruction Type A pour Fortran HumanEval-like.

Objectif scientifique
---------------------
Reconstruire un Type A propre, HumanEval-like, dédupliqué, non hardcodé,
sans sorties parasites, validé par compilation + exécution + tests fonctionnels.

Ce script n'est PAS une modification de l'ancien script hardcoded rebuild.
Il applique une nouvelle logique :
  - analyse statique du code Type A existant ;
  - décision keep_rebuild / split / isolate / delete ;
  - reconstruction par LLM en JSON strict ;
  - retry ciblé multi-causes, avec validation locale parallélisable :
      invalid_json, schema, static_policy, compile, runtime, wrong_output,
      stdout_label, hardcoding, bad_array_input, intent_in_modified, etc.
  - validation gfortran stricte ;
  - tests stdin/stdout ;
  - déduplication des outputs reconstruits ;
  - anti-fuite HumanEval optionnelle ;
  - routing clean / targeted / manual / isolated / deleted.

Exemples
--------
Analyse seule :
  python3 rebuild_type_a_humaneval_like_v3.py \
    --input train_A.json \
    --output-dir rebuilt_A_v2_analysis \
    --analysis-only

Petit test LLM :
  python3 rebuild_type_a_humaneval_like_v3.py \
    --input train_A.json \
    --output-dir rebuilt_A_v2_test20 \
    --model gpt-oss-120b \
    --base-url http://localhost:8086 \
    --benchmark ../benchmark.json \
    --max-items 20 \
    --checkpoint-every 5 \
    --max-total-retries 5 \
    --validation-workers 4

Run complet :
  python3 rebuild_type_a_humaneval_like_v3.py \
    --input train_A.json \
    --output-dir rebuilt_A_v2 \
    --model gpt-oss-120b \
    --base-url http://localhost:8086 \
    --benchmark ../benchmark.json \
    --checkpoint-every 10 \
    --sleep 0.5 \
    --max-total-retries 5

Notes
-----
Ce script ne garantit pas de dépasser la base. Il implémente la stratégie
la plus rationnelle selon les diagnostics observés.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import subprocess
import tempfile
import time
import threading
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import requests
    from requests.adapters import HTTPAdapter
except ImportError:
    requests = None


# =============================================================================
# Constantes de stratégie
# =============================================================================

TARGETED_FAMILIES = {
    "integer_digits",
    "array",
    "string",
    "bool",
    "tuple",
    "modulo",
    "factorization",
    "floating",
}

DECISIONS = {"keep_rebuild", "split", "isolate", "delete"}
CODE_FORMS = {"program", "function", "subroutine", "module"}

DEFAULT_ENDPOINTS = [
    "/v1/chat/completions",
]

EXTERNAL_MODULE_WHITELIST = {
    "iso_fortran_env",
    "ieee_arithmetic",
    "ieee_exceptions",
    "ieee_features",
}

# Règles fortes envoyées au LLM à la reconstruction et au retry.
FORTRAN_EXTENDED_RULES = """
CRITICAL FORTRAN AND HUMANEVAL-LIKE RULES:
1. Return valid JSON only. No markdown, no explanation outside JSON.
2. Preserve the original scientific or algorithmic intent. Do not invent an unrelated task.
3. Do NOT copy HumanEval tasks, task names, function names, examples, constants, or tests.
4. For keep_rebuild/split, produce a complete Fortran 90 free-form program.
5. Use strict stdin/stdout:
   - no hardcoded input values;
   - no prompts;
   - no labels such as "Result:", "Output:", "Answer:", "Enter:";
   - stdout must contain only the expected result.
6. Use implicit none and declare all variables, including loop indices.
7. Never modify an argument declared intent(in). Use a local copy, e.g. temp = n.
8. For arrays provided on one line, use:
      read(*,*) n
      allocate(a(n))
      read(*,*) (a(i), i = 1, n)
   Do not read array elements line by line unless explicitly required.
9. For local strings in a program, use character(len=256) :: s.
   character(len=*) is only for dummy arguments.
10. For modulo, use mod(a,b), never "a mod b".
11. For integer ranges, do not write sum(1:i). Use a formula or sum(arr(1:i)).
12. Avoid C-like signatures. No "int n", "float[] arr", "&&", "||".
13. No external files, no open(file=...), no MPI/OpenMP/OpenACC/coarray.
14. No random/time/nondeterministic behavior.
15. No declarations after executable statements.
16. Allocatable arrays must be declared allocatable before allocate().
17. Generate 5 tests when possible:
    - 3 normal tests;
    - 1 limit test;
    - 1 edge case.
18. If the output is an array, print values only, e.g. print *, (arr(i), i=1,n)
19. If the output is a tuple/multiple values, print values on one line without labels.
"""

TYPE_A_INSTRUCTION_RULES = """
CRITICAL TYPE A INSTRUCTION CONSTRUCTION RULES:
1. The rewritten_instruction must be a generation task, not a debugging task.
2. It must start with a clear computational verb such as:
   Write, Compute, Generate, Given, Determine, Count, Evaluate, Simulate, Transform.
3. It must explicitly describe:
   - the input quantities;
   - the output quantity;
   - the scientific or algorithmic operation;
   - the source method or convention when identifiable.
4. Do not write vague instructions such as:
   "perform a scientific calculation",
   "process the data",
   "compute the result",
   "analyze the array",
   unless the exact computation is also stated.
5. If the source code uses a specific method, preserve it in the instruction:
   examples: recurrence, mixed-radix encoding, constrained tuple enumeration,
   packed triangular indexing, stencil update, weighted tensor contraction,
   interpolation rule, pivot convention, stride convention.
6. Do not replace the source method by another algorithmically equivalent method.
7. Do not mention:
   bug, fix, error, corrected code, original code, source code, reconstruction.
8. The instruction must be self-contained and understandable without seeing the original code.
9. The instruction must be consistent with stdin_contract, stdout_contract, tests, and fortran_code.
10. If the task has a special convention or edge case, state it explicitly.
"""


# =============================================================================
# I/O utilitaires
# =============================================================================

def load_json_or_jsonl(path: str) -> Any:
    p = Path(path)
    text = p.read_text(encoding="utf-8").strip()
    if not text:
        return []
    if text.startswith("["):
        return json.loads(text)
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def save_json(path: str | Path, data: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, p)


def get_record_id(rec: Dict[str, Any], idx: int) -> str:
    for k in ("id", "origin_id", "merged_id", "task_id", "original_id", "source_id"):
        if k in rec and rec[k] is not None:
            return str(rec[k])
    return f"idx_{idx}"


def get_instruction(rec: Dict[str, Any]) -> str:
    for k in ("instruction", "prompt", "input", "question", "task", "description"):
        v = rec.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()

    msgs = rec.get("messages")
    if isinstance(msgs, list):
        parts = []
        for m in msgs:
            if isinstance(m, dict) and m.get("role") in ("user", "system"):
                c = m.get("content")
                if isinstance(c, str) and c.strip():
                    parts.append(c.strip())
        return "\n".join(parts).strip()

    return ""


def get_code(rec: Dict[str, Any]) -> str:
    for k in ("output", "completion", "answer", "code", "generated_code", "source_code", "fortran_code"):
        v = rec.get(k)
        if isinstance(v, str) and v.strip():
            return clean_code_fences(v)

    msgs = rec.get("messages")
    if isinstance(msgs, list):
        for m in reversed(msgs):
            if isinstance(m, dict) and m.get("role") == "assistant":
                c = m.get("content")
                if isinstance(c, str) and c.strip():
                    return clean_code_fences(c)

    return ""


def clean_code_fences(text: str) -> str:
    t = (text or "").strip()
    m = re.search(r"```(?:fortran|f90|f95|f03|f08|text)?\s*(.*?)```", t, re.I | re.S)
    if m:
        return m.group(1).strip()
    t = re.sub(r"^```(?:fortran|f90|f95|f03|f08|text)?\s*", "", t, flags=re.I)
    t = re.sub(r"\s*```$", "", t)
    return t.strip()


def remove_fortran_comment(line: str) -> str:
    # Simple heuristic. It may remove ! inside strings, acceptable for risk detection.
    if "!" in line:
        return line.split("!", 1)[0]
    return line


def normalize_code_for_hash(code: str) -> str:
    c = clean_code_fences(code).lower()
    lines = []
    for line in c.splitlines():
        stripped = remove_fortran_comment(line).strip()
        if not stripped:
            continue
        stripped = re.sub(r"\s+", " ", stripped)
        lines.append(stripped)
    return "\n".join(lines)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()


def code_line_count(code: str) -> int:
    return len([l for l in (code or "").splitlines() if l.strip()])


# =============================================================================
# Détection de risques
# =============================================================================

@dataclass
class RiskReport:
    flags: List[str] = field(default_factory=list)
    counts: Dict[str, Any] = field(default_factory=dict)
    line_count: int = 0
    exact_hash: str = ""
    normalized_hash: str = ""

    def add(self, flag: str, count: Any = 1) -> None:
        if flag not in self.flags:
            self.flags.append(flag)
        self.counts[flag] = count


def detect_output_label_in_code(code: str) -> bool:
    """
    Détecte les sorties explicatives parasites, sans rejeter automatiquement
    les sorties string légitimes comme 'YES' ou 'NO'.
    """
    label_words = (
        "result", "output", "answer", "value", "computed",
        "enter", "input", "please", "the result", "final"
    )
    for raw in (code or "").splitlines():
        clean = remove_fortran_comment(raw).strip().lower()
        if not re.match(r"^(print\s*\*|write\s*\([^)]*\))", clean):
            continue

        # Chaîne littérale imprimée
        m = re.search(r"""['"]([^'"]+)['"]""", clean)
        if not m:
            continue
        text = m.group(1).strip().lower()

        if any(w in text for w in label_words):
            return True
        if ":" in text or "=" in text:
            return True
    return False


def detect_output_label_in_stdout(stdout: str) -> bool:
    s = (stdout or "").lower()
    label_words = (
        "result:", "output:", "answer:", "value:", "computed:",
        "enter ", "input:", "please", "the result"
    )
    return any(x in s for x in label_words)


def detect_hardcoded_inputs_strong(code: str) -> bool:
    """
    Détecte les valeurs de démonstration hardcodées.
    C'est un signal candidat, pas une preuve parfaite.
    Évite de flagger les constantes normales comme if (n == 0) ou do i=1,n.
    """
    c = clean_code_fences(code)
    lc = c.lower()
    read_pos = lc.find("read")
    before_read = lc if read_pos == -1 else lc[:read_pos]

    patterns = [
        r"^\s*(n|m|k|x|y|z|num|number|val|value|input)\s*=\s*[-+]?\d+(\.\d+)?([de][+-]?\d+)?\b",
        r"^\s*\w+\s*=\s*\[\s*[-+0-9.,\s]+\s*\]",
        r"^\s*\w+\s*=\s*\(/\s*[-+0-9.,\s]+\s*/\)",
        r"^\s*data\s+\w+\s*/",
        r"""^\s*(s|str|text|input)\s*=\s*['"][^'"]+['"]""",
    ]
    for pat in patterns:
        if re.search(pat, before_read, flags=re.I | re.M):
            return True

    if "read" not in lc:
        numeric_assignments = re.findall(
            r"^\s*\w+\s*=\s*[-+]?\d+(\.\d+)?([de][+-]?\d+)?\b",
            lc,
            flags=re.I | re.M,
        )
        array_literals = re.findall(r"\[.*?\]|\(/.*?/\)", lc, flags=re.S)
        if len(numeric_assignments) >= 2 or bool(array_literals):
            return True

    return False


def detect_intent_in_modified_strong(code: str) -> List[str]:
    """
    Détecte les modifications de variables intent(in), scalaires ou tableaux :
      n = ...
      a(i) = ...
      a(:) = ...
      read(*,*) n
      read(*,*) a(i)
    """
    c = clean_code_fences(code)
    lines = [remove_fortran_comment(line).rstrip() for line in c.splitlines()]
    intent_in_vars = set()

    for line in lines:
        low = line.lower()
        if "intent" not in low or "::" not in line:
            continue
        if not re.search(r"intent\s*\(\s*in\s*\)", low):
            continue

        after = line.split("::", 1)[1]
        for part in after.split(","):
            name = part.strip()
            name = re.sub(r"\(.*?\)", "", name).strip()
            name = name.split()[0] if name else ""
            name = name.lower()
            if re.match(r"^[a-z_]\w*$", name):
                intent_in_vars.add(name)

    modified = []

    for raw in lines:
        line = raw.strip().lower()
        if not line:
            continue

        for var in intent_in_vars:
            if re.match(rf"^{re.escape(var)}\s*=", line):
                modified.append(var)
                continue
            if re.match(rf"^{re.escape(var)}\s*\([^)]*\)\s*=", line):
                modified.append(var)
                continue
            if re.search(rf"\bread\s*\([^)]*\).*\b{re.escape(var)}\b", line):
                modified.append(var)
                continue

    return sorted(set(modified))


def detect_external_dependencies(code: str) -> List[str]:
    defined = set()
    used = set()
    for line in (code or "").splitlines():
        ls = remove_fortran_comment(line).strip()
        m = re.match(r"^\s*module\s+([a-zA-Z_][a-zA-Z0-9_]*)", ls, re.I)
        if m and not re.match(r"^\s*module\s+procedure\b", ls, re.I):
            defined.add(m.group(1).lower())

        m = re.match(r"^\s*use\s*(?:,\s*intrinsic\s*)?::?\s*([a-zA-Z_][a-zA-Z0-9_]*)", ls, re.I)
        if m:
            used.add(m.group(1).lower())

    return sorted(u for u in used if u not in EXTERNAL_MODULE_WHITELIST and u not in defined)


def has_array_read_line_by_line_eof_risk(code: str, stdin_contract: str = "") -> bool:
    if "line by line" in (stdin_contract or "").lower():
        return False
    return bool(re.search(
        r"do\s+\w+\s*=\s*1\s*,\s*\w+[\s\S]{0,200}?read\s*\(\s*\*\s*,\s*\*\s*\)\s+\w+\s*\(\s*\w+\s*\)",
        code or "",
        flags=re.I,
    ))


def analyze_static_risks(code: str, stdin_contract: str = "") -> RiskReport:
    c = clean_code_fences(code)
    lc = c.lower()
    rr = RiskReport()
    rr.line_count = code_line_count(c)
    rr.exact_hash = sha256_text(c.strip())
    rr.normalized_hash = sha256_text(normalize_code_for_hash(c))

    if not c.strip():
        rr.add("empty_code")
        return rr

    if "```" in code:
        rr.add("markdown_fence")

    # Longueur
    if rr.line_count > 300:
        rr.add("very_long_code_gt300")
    elif rr.line_count > 220:
        rr.add("long_code_gt220")
    elif rr.line_count > 180:
        rr.add("long_code_gt180")

    # Structure
    if not re.search(r"^\s*program\s+\w+", c, re.I | re.M):
        # Pas fatal pour une source, mais pour la reconstruction on veut un programme complet.
        rr.add("no_program_statement")
    if not re.search(r"^\s*implicit\s+none\b", c, re.I | re.M):
        rr.add("missing_implicit_none")

    # I/O externe / HPC / nondéterminisme
    pattern_flags = {
        "external_file_open": r"\bopen\s*\(",
        "external_file_inquire": r"\binquire\s*\(",
        "external_file_close": r"\bclose\s*\(",
        "rewind_backspace": r"\b(rewind|backspace)\b",
        "mpi_detected": r"\buse\s+mpi\b|\bmpi_|\bcall\s+mpi_",
        "openmp_detected": r"!\$omp|\bomp_|\bopenmp\b",
        "openacc_detected": r"!\$acc|\bopenacc\b",
        "coarray_detected": r"\bcodimension\b|\bsync\s+all\b|\bsync\s+images\b|\[\*\]",
        "random_or_time": r"\brandom_number\s*\(|\brandom_seed\s*\(|\bsystem_clock\s*\(|\bdate_and_time\s*\(|\bcpu_time\s*\(",
        "old_fortran_goto_labels": r"\bgoto\b|\bgo\s+to\b|^\s*\d+\s+(continue|format)\b|\bcommon\b|\bequivalence\b|\bpause\b",
        "print_parentheses_syntax": r"^\s*print\s*\(\s*\*\s*,\s*\*\s*\)",
        "write_star_no_paren": r"^\s*write\s+\*",
        "mod_infix": r"\b[a-zA-Z0-9_)\]]+\s+mod\s+[a-zA-Z0-9_(\[]+",
        "sum_range": r"\bsum\s*\(\s*\d+\s*:\s*\w+\s*\)",
        "c_like_signature": r"\b(function|subroutine)\s+\w+\s*\([^)]*\b(int|float|double|char)\s+\w|[\w]+\[\]",
        "declaration_after_executable_candidate": r"^\s*(if|do|call|print|write|read|\w+\s*=).*?\n\s*(integer|real|logical|character|type)\b",
        "contains_nested_candidate": r"\bcontains\b[\s\S]*\bcontains\b",
        "bad_result_name": r"\bfunction\s+(\w+)\b[^\n]*\bresult\s*\(\s*\1\s*\)",
        "character_len_star_local_candidate": r"^\s*character\s*\(\s*len\s*=\s*\*\s*\)\s*::",
    }

    for flag, pat in pattern_flags.items():
        if re.search(pat, c, flags=re.I | re.M):
            rr.add(flag)

    deps = detect_external_dependencies(c)
    if deps:
        rr.add("external_dependencies", deps)

    if detect_output_label_in_code(c):
        rr.add("output_label_result")

    if detect_hardcoded_inputs_strong(c):
        rr.add("hardcoded_input_candidate")

    if re.search(r"\bread\s*\(\s*\*\s*,", lc) or re.search(r"\bread\s+\*", lc):
        rr.add("uses_stdin_read")
    else:
        rr.add("no_stdin_read_detected")

    if has_array_read_line_by_line_eof_risk(c, stdin_contract):
        rr.add("array_read_line_by_line_eof_risk")

    modified = detect_intent_in_modified_strong(c)
    if modified:
        rr.add("intent_in_modified_candidate", modified)

    if re.search(r"intent\s*\(\s*out\s*\)[^\n:]*::\s*\w+\s*\(:\)", lc) and re.search(r"\ballocate\s*\(", lc):
        if "allocatable" not in lc:
            rr.add("allocatable_output_missing_allocatable_candidate")

    return rr


def classify_source_quality(rr: RiskReport) -> Dict[str, Any]:
    return {
        "was_duplicate": False,
        "was_hardcoded": "hardcoded_input_candidate" in rr.flags,
        "had_labeled_output": "output_label_result" in rr.flags,
        "had_no_stdin": "no_stdin_read_detected" in rr.flags,
        "was_long_code": any(f in rr.flags for f in ("long_code_gt180", "long_code_gt220", "very_long_code_gt300")),
        "had_external_files": any(f.startswith("external_file") for f in rr.flags),
        "had_parallel_hpc": any(f in rr.flags for f in ("mpi_detected", "openmp_detected", "openacc_detected", "coarray_detected")),
        "had_random_or_time": "random_or_time" in rr.flags,
        "had_old_fortran_labels": "old_fortran_goto_labels" in rr.flags,
        "line_count": rr.line_count,
    }


# =============================================================================
# Décision source et famille
# =============================================================================

TASK_FAMILY_KEYWORDS = {
    "integer_digits": [
        "digit", "digits", "prime", "factor", "largest prime", "odd digit", "even digit",
        "integer", "collatz", "gcd", "lcm", "factorial", "divisor"
    ],
    "modulo": ["modulo", "mod ", "modp", "power", "remainder"],
    "factorization": ["factorize", "factorization", "prime factor", "factors"],
    "array": [
        "array", "list", "vector", "sort", "filter", "element", "elements", "threshold",
        "unique", "maximum", "minimum", "monotonic", "pairs", "triples"
    ],
    "string": [
        "string", "substring", "char", "character", "vowel", "bracket", "parenth",
        "shift", "decode", "encode", "palindrome"
    ],
    "bool": ["true", "false", "boolean", "check", "valid", "correct", "has_close"],
    "floating": ["float", "real", "rescale", "deviation", "derivative", "mean", "average", "distance"],
    "tuple": ["tuple", "pair", "two values", "three values", "even odd", "count of even"],
    "scientific": ["matrix", "simulation", "equation", "eigen", "hpc", "parallel", "monte carlo"],
    "procedure": ["function", "subroutine", "module", "intent"],
}


def estimate_task_family(instruction: str, code: str) -> str:
    text = (instruction + "\n" + code).lower()
    scores = {}
    for fam, kws in TASK_FAMILY_KEYWORDS.items():
        score = 0
        for kw in kws:
            if kw in text:
                score += 1
        if score:
            scores[fam] = score
    if not scores:
        return "unknown"
    return max(scores, key=scores.get)


def heuristic_decision_from_source(rr: RiskReport, instruction: str, code: str) -> Tuple[str, str]:
    flags = set(rr.flags)
    if "empty_code" in flags or not instruction.strip():
        return "delete", "empty_code_or_instruction"

    if any(f in flags for f in ("mpi_detected", "openmp_detected", "openacc_detected", "coarray_detected")):
        return "isolate", "parallel_hpc_not_humaneval_like"

    if any(f.startswith("external_file") for f in flags) or "rewind_backspace" in flags or "external_dependencies" in flags:
        return "isolate", "external_files_or_dependencies_not_humaneval_like"

    if "random_or_time" in flags:
        return "isolate", "random_or_time_nondeterministic"

    if "very_long_code_gt300" in flags:
        return "isolate", "very_long_code_gt300"
    if "long_code_gt220" in flags:
        return "split", "long_code_gt220_split_into_microtasks"

    return "keep_rebuild", "rebuild_to_clean_humaneval_like"


# =============================================================================
# LLM
# =============================================================================


_SESSION = None
_SEMAPHORE = None
_CLIENT_LOCK = threading.Lock()


def init_llm_client(max_concurrency=1, pool_maxsize=None):
    """Initialize a shared HTTP client for vLLM/OpenAI-compatible servers."""
    global _SESSION, _SEMAPHORE

    if requests is None:
        raise RuntimeError("requests is not installed. Install it or use --analysis-only.")

    with _CLIENT_LOCK:
        if _SESSION is None:
            pool = pool_maxsize or max(10, int(max_concurrency or 1))
            session = requests.Session()
            adapter = HTTPAdapter(
                pool_connections=pool,
                pool_maxsize=pool,
                max_retries=0,
            )
            session.mount("http://", adapter)
            session.mount("https://", adapter)
            _SESSION = session

        if _SEMAPHORE is None:
            _SEMAPHORE = threading.BoundedSemaphore(int(max_concurrency or 1))

def call_llm(
    prompt: str,
    model: str,
    base_url: str,
    api_key: Optional[str],
    temperature: float,
    max_tokens: int,
    timeout: int,
    endpoints: Optional[List[str]] = None,
) -> str:
    """Call a vLLM/OpenAI-compatible chat-completions endpoint.

    Same public signature as the original script, but using a shared
    requests.Session and bounded semaphore like the vLLM pipelines.
    """
    if requests is None:
        raise RuntimeError("requests is not installed. Install it or use --analysis-only.")

    if _SESSION is None or _SEMAPHORE is None:
        init_llm_client(max_concurrency=1)

    endpoints = endpoints or DEFAULT_ENDPOINTS

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False,
    }

    errors = []

    for ep in endpoints:
        url = f"{base_url.rstrip('/')}{ep}"

        try:
            with _SEMAPHORE:
                r = _SESSION.post(url, headers=headers, json=payload, timeout=timeout)

            if r.status_code == 200:
                obj = r.json()

                if "choices" in obj and obj["choices"]:
                    msg = obj["choices"][0].get("message", {})
                    if isinstance(msg, dict):
                        content = msg.get("content", "")
                    else:
                        content = str(msg)
                    if content:
                        return content

                if "message" in obj and isinstance(obj["message"], dict):
                    content = obj["message"].get("content", "")
                    if content:
                        return content

                if "response" in obj and obj["response"]:
                    return obj["response"]

                errors.append(f"{url}: empty response payload {str(obj)[:300]}")
            else:
                errors.append(f"{url}: HTTP {r.status_code} {r.text[:300]}")

        except Exception as e:
            errors.append(f"{url}: {e}")

    raise RuntimeError("All vLLM endpoints failed:\n" + "\n".join(errors))


def extract_json_object(response: str) -> Optional[Dict[str, Any]]:
    if not response:
        return None
    t = response.strip()

    try:
        obj = json.loads(t)
        return obj if isinstance(obj, dict) else None
    except Exception:
        pass

    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", t, re.S)
    if m:
        try:
            obj = json.loads(m.group(1))
            return obj if isinstance(obj, dict) else None
        except Exception:
            pass

    s, e = t.find("{"), t.rfind("}")
    if s != -1 and e > s:
        try:
            obj = json.loads(t[s:e + 1])
            return obj if isinstance(obj, dict) else None
        except Exception:
            pass

    return None


# =============================================================================
# Prompts
# =============================================================================

def build_reconstruction_prompt(
    original_instruction: str,
    original_code: str,
    record_id: str,
    source_risks: RiskReport,
    decision_hint: str,
    reason_hint: str,
) -> str:
    source_flags = ", ".join(source_risks.flags[:50]) if source_risks.flags else "none"

    return f"""You are reconstructing a Fortran Type A dataset for HumanEval-like evaluation.

Record id: {record_id}
Initial decision hint: {decision_hint}
Initial reason hint: {reason_hint}
Detected source risk flags: {source_flags}

TASK:
Reconstruct the original task into a clean HumanEval-like Fortran 90 task.

{FORTRAN_EXTENDED_RULES}

{TYPE_A_INSTRUCTION_RULES}

DECISION POLICY:
- keep_rebuild: the task is useful but must be rebuilt.
- split: the source is too long and should become one clean micro-task preserving a core skill.
- isolate: useful scientifically but not HumanEval-like, e.g. MPI, files, random/time, long simulation.
- delete: empty, incoherent, unreconstructible, or impossible to test.

For keep_rebuild/split:
- Preserve the scientific or algorithmic intent.
- Preserve the same identifiable source method whenever possible.
- The rewritten_instruction must describe the exact computation, not only the general topic.
- If the source uses a recurrence, stencil, tensor contraction, enumeration, packed indexing, interpolation, factorization, or stride convention, state that method/convention in the instruction.
- You may simplify a large code into a close micro-task only if semantic_change_level is "simplified" or "split_from_large_code".
- Generate stdin/stdout contracts and 5 tests.
- Do not hardcode test values inside the Fortran program.

Return JSON only, with this exact schema:
{{
  "decision": "keep_rebuild | split | isolate | delete",
  "reason": "...",
  "source_type": "A",
  "original_id": "{record_id}",
  "task_family": "integer_digits | array | string | bool | floating | tuple | scientific | io | procedure | modulo | factorization",
  "original_intent_preserved": true,
  "semantic_change_level": "same | close_variant | simplified | split_from_large_code",
  "rewritten_instruction": "...",
  "fortran_code": "...",
  "code_form": "program | function | subroutine | module",
  "stdin_contract": "...",
  "stdout_contract": "...",
  "tests": [
    {{"input": "...", "expected_output": "..."}}
  ],
  "risk_flags": []
}}

ORIGINAL INSTRUCTION:
{original_instruction[:5000]}

ORIGINAL CODE:
{original_code[:12000]}
"""


def build_retry_prompt(
    current_obj: Dict[str, Any],
    failure_type: str,
    diagnostics: Dict[str, Any],
    original_instruction: str,
    original_code: str,
) -> str:
    diagnostics_text = json.dumps(diagnostics, indent=2, ensure_ascii=False)[:6000]
    current_json = json.dumps(current_obj, indent=2, ensure_ascii=False)[:14000]

    return f"""The reconstructed Fortran task failed validation.

Failure type: {failure_type}

Diagnostics:
{diagnostics_text}

Fix the reconstruction. Keep the same original scientific/algorithmic intent.

{FORTRAN_EXTENDED_RULES}

{TYPE_A_INSTRUCTION_RULES}

Specific correction guidance:
- invalid_json/schema: return valid JSON only with all required fields.
- hardcoded_input_candidate: read all inputs from stdin; do not assign demo values internally.
- output_label_result/stdout_label: remove labels; print only the result values.
- array_read_line_by_line_eof_risk: use read(*,*) (a(i), i = 1, n).
- intent_in_modified_candidate: use a local copy and do not modify intent(in).
- compile: fix compiler errors without introducing hardcoding or labels.
- runtime: fix memory/input/EOF/runtime issue.
- wrong_output: fix the algorithm, not only formatting.
- rewritten_instruction: if vague, incomplete, missing computational verb, or not aligned with the source method, rewrite it while preserving the same code/tests.
- character_len_star_local_candidate: use character(len=256) locally.
- mod_infix: use mod(a,b).
- sum_range: use formula or sum(arr(1:i)).

Return JSON only with the same schema as before.

ORIGINAL INSTRUCTION:
{original_instruction[:4000]}

ORIGINAL CODE:
{original_code[:8000]}

CURRENT RECONSTRUCTION JSON:
{current_json}
"""


# =============================================================================
# Validation
# =============================================================================

@dataclass
class ValidationResult:
    ok: bool
    stage: str
    diagnostics: Dict[str, Any] = field(default_factory=dict)
    risk_report: Optional[RiskReport] = None


def validate_reconstruction_schema(obj: Dict[str, Any]) -> ValidationResult:
    required = [
        "decision", "reason", "source_type", "original_id", "task_family",
        "original_intent_preserved", "semantic_change_level",
        "rewritten_instruction", "fortran_code", "code_form",
        "stdin_contract", "stdout_contract", "tests", "risk_flags",
    ]
    missing = [k for k in required if k not in obj]
    if missing:
        return ValidationResult(False, "schema", {"missing_fields": missing})

    if obj["decision"] not in DECISIONS:
        return ValidationResult(False, "schema", {"bad_decision": obj["decision"]})

    if obj["decision"] in ("isolate", "delete"):
        return ValidationResult(True, "schema", {"decision": obj["decision"]})

    if obj.get("code_form") not in CODE_FORMS:
        return ValidationResult(False, "schema", {"bad_code_form": obj.get("code_form")})

    tests = obj.get("tests")
    if not isinstance(tests, list) or len(tests) < 3:
        return ValidationResult(False, "schema", {"tests_count": len(tests) if isinstance(tests, list) else "not_list"})

    for i, t in enumerate(tests):
        if not isinstance(t, dict) or "input" not in t or "expected_output" not in t:
            return ValidationResult(False, "schema", {"bad_test_index": i, "test": t})

    code = obj.get("fortran_code")
    if not isinstance(code, str) or not code.strip():
        return ValidationResult(False, "schema", {"empty_fortran_code": True})

    return ValidationResult(True, "schema")


def validate_static_policy(obj: Dict[str, Any]) -> ValidationResult:
    if obj.get("decision") in ("isolate", "delete"):
        return ValidationResult(True, "static_policy")

    code = obj.get("fortran_code", "")
    stdin_contract = obj.get("stdin_contract", "")
    tests = obj.get("tests", [])
    rr = analyze_static_risks(code, stdin_contract=stdin_contract)

    fatal_flags = {
        "markdown_fence",
        "external_file_open",
        "external_file_inquire",
        "mpi_detected",
        "openmp_detected",
        "openacc_detected",
        "coarray_detected",
        "random_or_time",
        "output_label_result",
        "hardcoded_input_candidate",
        "array_read_line_by_line_eof_risk",
        "intent_in_modified_candidate",
        "character_len_star_local_candidate",
        "mod_infix",
        "sum_range",
        "c_like_signature",
        "allocatable_output_missing_allocatable_candidate",
        "print_parentheses_syntax",
        "write_star_no_paren",
    }

    # Exiger stdin uniquement si les tests fournissent une entrée non vide.
    tests_have_input = any(str(t.get("input", "")).strip() for t in tests if isinstance(t, dict))
    if tests_have_input:
        fatal_flags.add("no_stdin_read_detected")

    found = sorted(fatal_flags.intersection(rr.flags))
    if found:
        return ValidationResult(False, "static_policy", {"fatal_flags": found, "all_flags": rr.flags, "counts": rr.counts}, rr)

    return ValidationResult(True, "static_policy", {"flags": rr.flags}, rr)


def compile_fortran(code: str, workdir: str, timeout: int = 30) -> Dict[str, Any]:
    src = os.path.join(workdir, "candidate.f90")
    exe = os.path.join(workdir, "candidate.out")
    with open(src, "w", encoding="utf-8") as f:
        f.write(clean_code_fences(code))

    cmd = [
        "gfortran",
        "-std=f2008",
        "-Wall",
        "-Wextra",
        "-fcheck=all",
        "-fbacktrace",
        "-ffree-line-length-none",
        src,
        "-o",
        exe,
    ]

    try:
        r = subprocess.run(cmd, cwd=workdir, capture_output=True, text=True, timeout=timeout)
        return {
            "ok": r.returncode == 0,
            "cmd": " ".join(cmd),
            "stdout": r.stdout,
            "stderr": r.stderr,
            "exe_path": exe,
            "returncode": r.returncode,
        }
    except subprocess.TimeoutExpired:
        return {"ok": False, "cmd": " ".join(cmd), "stdout": "", "stderr": "Compilation timeout", "exe_path": exe, "returncode": -999}


def run_one_test(exe_path: str, input_data: str, workdir: str, timeout: int = 10) -> Dict[str, Any]:
    try:
        r = subprocess.run(
            [exe_path],
            input=input_data,
            cwd=workdir,
            capture_output=True,
            text=True,
            timeout=timeout,
            env={**os.environ, "GFORTRAN_UNBUFFERED_ALL": "1"},
        )
        return {"ok": r.returncode == 0, "stdout": r.stdout, "stderr": r.stderr, "returncode": r.returncode}
    except subprocess.TimeoutExpired:
        return {"ok": False, "stdout": "", "stderr": "Execution timeout", "returncode": -999}
    except Exception as e:
        return {"ok": False, "stdout": "", "stderr": str(e), "returncode": -998}


def normalize_output(s: str) -> str:
    return "\n".join(" ".join(line.strip().split()) for line in (s or "").strip().splitlines() if line.strip())


def _as_bool_token(x: str) -> Optional[bool]:
    v = x.strip().lower()
    if v in (".true.", "true", "t", "1"):
        return True
    if v in (".false.", "false", "f", "0"):
        return False
    return None


def outputs_match(actual: str, expected: str, float_tol: float = 1e-6) -> bool:
    a = normalize_output(actual)
    e = normalize_output(expected)
    if a == e:
        return True

    a_tokens = a.split()
    e_tokens = e.split()
    if len(a_tokens) != len(e_tokens):
        return False

    for x, y in zip(a_tokens, e_tokens):
        bx = _as_bool_token(x)
        by = _as_bool_token(y)
        if bx is not None and by is not None:
            if bx != by:
                return False
            continue

        try:
            fx = float(x.replace("d", "e").replace("D", "e"))
            fy = float(y.replace("d", "e").replace("D", "e"))
            if not math.isfinite(fx) or not math.isfinite(fy):
                if fx != fy:
                    return False
            elif abs(fx - fy) > float_tol * max(1.0, abs(fy)):
                return False
            continue
        except Exception:
            pass

        if x != y:
            return False

    return True


def validate_compile_and_tests(
    obj: Dict[str, Any],
    compile_timeout: int,
    run_timeout: int,
    float_tol: float,
    validation_workers: int = 1,
) -> ValidationResult:
    if obj.get("decision") in ("isolate", "delete"):
        return ValidationResult(True, "compile_tests", {"decision": obj.get("decision")})

    code = obj.get("fortran_code", "")
    tests = obj.get("tests", [])

    with tempfile.TemporaryDirectory(prefix="a_rebuilt_val_") as tmpdir:
        comp = compile_fortran(code, tmpdir, compile_timeout)
        if not comp["ok"]:
            return ValidationResult(False, "compile", {
                "compile_cmd": comp["cmd"],
                "compile_stderr": comp["stderr"][:5000],
                "compile_stdout": comp["stdout"][:1500],
                "returncode": comp["returncode"],
            })

        def evaluate_test(i: int, t: Dict[str, Any]) -> Optional[Dict[str, Any]]:
            input_data = str(t.get("input", ""))
            expected = str(t.get("expected_output", ""))
            run = run_one_test(comp["exe_path"], input_data, tmpdir, run_timeout)

            if not run["ok"]:
                return {
                    "test_index": i,
                    "input": input_data,
                    "expected_output": expected,
                    "actual_stdout": run["stdout"],
                    "stderr": run["stderr"],
                    "returncode": run["returncode"],
                    "failure": "runtime_error",
                }

            if detect_output_label_in_stdout(run["stdout"]):
                return {
                    "test_index": i,
                    "input": input_data,
                    "expected_output": expected,
                    "actual_stdout": run["stdout"],
                    "stderr": run["stderr"],
                    "failure": "stdout_label_detected",
                }

            if not outputs_match(run["stdout"], expected, float_tol=float_tol):
                return {
                    "test_index": i,
                    "input": input_data,
                    "expected_output": expected,
                    "actual_stdout": run["stdout"],
                    "stderr": run["stderr"],
                    "failure": "wrong_output",
                }

            return None

        failures = []
        workers = max(1, int(validation_workers or 1))

        if workers == 1 or len(tests) <= 1:
            for i, t in enumerate(tests):
                failure = evaluate_test(i, t)
                if failure is not None:
                    failures.append(failure)
        else:
            # Parallelize local test execution for the same compiled executable.
            # LLM calls remain sequential; only validation subprocesses are parallel here.
            with ThreadPoolExecutor(max_workers=min(workers, len(tests))) as pool:
                future_to_index = {
                    pool.submit(evaluate_test, i, t): i
                    for i, t in enumerate(tests)
                }
                for fut in as_completed(future_to_index):
                    failure = fut.result()
                    if failure is not None:
                        failures.append(failure)

            failures.sort(key=lambda x: x.get("test_index", 0))

        if failures:
            ftypes = Counter(f["failure"] for f in failures)
            stage = "wrong_output"
            if "runtime_error" in ftypes:
                stage = "runtime"
            elif "stdout_label_detected" in ftypes:
                stage = "stdout_label"
            return ValidationResult(False, stage, {
                "failures": failures[:5],
                "num_failures": len(failures),
                "failure_types": dict(ftypes),
            })

    return ValidationResult(True, "compile_tests", {"tests_passed": len(tests), "tests_total": len(tests)})


# =============================================================================
# Anti-fuite HumanEval
# =============================================================================

def load_humaneval_index(path: Optional[str]) -> Optional[List[Dict[str, str]]]:
    if not path:
        return None
    data = load_json_or_jsonl(path)
    if not isinstance(data, list):
        return None

    items = []
    for rec in data:
        if not isinstance(rec, dict):
            continue
        task_id = str(rec.get("task_id") or rec.get("name") or rec.get("id") or "")
        entry = str(rec.get("entry_point") or rec.get("function_name") or "")
        prompt = str(rec.get("prompt") or rec.get("declaration") or rec.get("instruction") or "")
        tests = str(rec.get("test") or rec.get("tests") or "")
        items.append({
            "task_id": task_id,
            "entry_point": entry,
            "prompt": prompt,
            "tests": tests,
        })
    return items


def validate_antileak(obj: Dict[str, Any], humaneval_index: Optional[List[Dict[str, str]]]) -> ValidationResult:
    if not humaneval_index or obj.get("decision") in ("isolate", "delete"):
        return ValidationResult(True, "antileak")

    instr = (obj.get("rewritten_instruction") or "").lower()
    code = (obj.get("fortran_code") or "").lower()
    tests_blob = json.dumps(obj.get("tests", []), ensure_ascii=False).lower()

    hits = []
    for item in humaneval_index:
        task_id = (item.get("task_id") or "").lower()
        entry = (item.get("entry_point") or "").lower()
        prompt = (item.get("prompt") or "").lower()
        tests = (item.get("tests") or "").lower()

        if task_id and len(task_id) > 2 and task_id in instr:
            hits.append({"kind": "task_id_in_instruction", "task_id": task_id})

        if entry and len(entry) > 2:
            if re.search(rf"\b{re.escape(entry)}\b", code):
                hits.append({"kind": "entry_point_in_code", "entry_point": entry})

        # Exact large prompt snippet copied
        prompt_snip = " ".join(prompt.split())[:200]
        if len(prompt_snip) > 80 and prompt_snip in " ".join(instr.split()):
            hits.append({"kind": "prompt_snippet_in_instruction", "task_id": task_id})

        # Exact tests copied: cautious, only long snippets.
        tests_snip = " ".join(tests.split())[:200]
        if len(tests_snip) > 80 and tests_snip in " ".join(tests_blob.split()):
            hits.append({"kind": "test_snippet_in_tests", "task_id": task_id})

    if hits:
        return ValidationResult(False, "antileak", {"hits": hits[:10]})
    return ValidationResult(True, "antileak")


# =============================================================================
# Buckets, report, checkpoints
# =============================================================================

def build_output_paths(outdir: str) -> Dict[str, Path]:
    p = Path(outdir)
    return {
        "clean": p / "A_rebuilt_clean.json",
        "targeted": p / "A_rebuilt_targeted.json",
        "manual": p / "A_rebuilt_manual_review.json",
        "isolated": p / "A_rebuilt_isolated.json",
        "deleted": p / "A_rebuilt_deleted.json",
        "report": p / "A_rebuilt_report.json",
    }


def load_existing_outputs(paths: Dict[str, Path]) -> Dict[str, List[Dict[str, Any]]]:
    outputs = {}
    for key in ("clean", "targeted", "manual", "isolated", "deleted"):
        if paths[key].exists():
            outputs[key] = load_json_or_jsonl(str(paths[key]))
        else:
            outputs[key] = []
    return outputs


def save_outputs(paths: Dict[str, Path], outputs: Dict[str, List[Dict[str, Any]]]) -> None:
    for key in ("clean", "targeted", "manual", "isolated", "deleted"):
        save_json(paths[key], outputs[key])


def final_bucket_for(obj: Dict[str, Any]) -> str:
    if obj.get("decision") == "isolate":
        return "isolated"
    if obj.get("decision") == "delete":
        return "deleted"
    fam = obj.get("task_family", "unknown")
    if fam in TARGETED_FAMILIES:
        return "targeted"
    return "clean"


def build_source_record(
    record_id: str,
    instruction: str,
    code: str,
    reason: str,
    decision: str,
    risks: RiskReport,
    rec: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "original_id": record_id,
        "decision": decision,
        "reason": reason,
        "original_instruction": instruction,
        "original_output": code,
        "source_quality_flags": classify_source_quality(risks),
        "source_risk_flags": risks.flags,
        "source_risk_counts": risks.counts,
        "source_metadata": {
            k: v for k, v in rec.items()
            if k not in ("output", "completion", "answer", "code", "generated_code", "source_code", "fortran_code")
        },
    }


def build_report(
    data: List[Dict[str, Any]],
    outputs: Dict[str, List[Dict[str, Any]]],
    source_duplicate_counts: Dict[str, int],
) -> Dict[str, Any]:
    decision_counts = Counter()
    family_counts = Counter()
    risk_counts = Counter()
    validation_counts = Counter()
    retry_counts = Counter()

    for bucket, items in outputs.items():
        for it in items:
            decision_counts[it.get("decision", bucket)] += 1
            family_counts[it.get("task_family", "unknown")] += 1
            for f in it.get("risk_flags", []) or []:
                risk_counts[f] += 1
            for f in it.get("source_risk_flags", []) or []:
                risk_counts["source:" + f] += 1
            val = it.get("validation", {})
            if isinstance(val, dict):
                validation_counts[val.get("final_status", "unknown")] += 1
                retry_counts[str(val.get("retry_attempts", 0))] += 1

    return {
        "total_input": len(data),
        "output_buckets": {k: len(v) for k, v in outputs.items()},
        "decision_counts": dict(decision_counts),
        "task_family_counts": dict(family_counts),
        "risk_counts_top80": dict(risk_counts.most_common(80)),
        "validation_counts": dict(validation_counts),
        "retry_attempts_distribution": dict(retry_counts),
        "source_duplicate_summary": {
            "unique_normalized_outputs": len(source_duplicate_counts),
            "duplicate_groups": sum(1 for v in source_duplicate_counts.values() if v > 1),
            "examples_in_duplicate_groups": sum(v for v in source_duplicate_counts.values() if v > 1),
        },
        "notes": [
            "Accepted examples are not guaranteed to improve the base model.",
            "Manual review includes duplicates and possible HumanEval leakage.",
            "Targeted bucket is based on task_family.",
        ],
    }


# =============================================================================
# Process one record
# =============================================================================

def reconstruct_one(
    rec: Dict[str, Any],
    idx: int,
    args: argparse.Namespace,
    accepted_hashes: set,
    humaneval_index: Optional[List[Dict[str, str]]],
    source_hash_counts: Dict[str, int],
    source_hash_first_idx: Dict[str, int],
    accepted_hashes_lock: Optional[threading.Lock] = None,
) -> Tuple[str, Dict[str, Any]]:
    record_id = get_record_id(rec, idx)
    instruction = get_instruction(rec)
    original_code = get_code(rec)
    source_risks = analyze_static_risks(original_code)

    # Duplicate source handling.
    source_norm = source_risks.normalized_hash
    if args.drop_source_duplicates and source_hash_counts.get(source_norm, 0) > 1 and source_hash_first_idx.get(source_norm) != idx:
        item = build_source_record(
            record_id, instruction, original_code,
            "normalized_source_duplicate_dropped",
            "delete", source_risks, rec
        )
        item["source_quality_flags"]["was_duplicate"] = True
        return "deleted", item

    decision_hint, reason_hint = heuristic_decision_from_source(source_risks, instruction, original_code)

    if decision_hint == "delete":
        return "deleted", build_source_record(record_id, instruction, original_code, reason_hint, "delete", source_risks, rec)

    if decision_hint == "isolate" and args.isolate_without_llm:
        return "isolated", build_source_record(record_id, instruction, original_code, reason_hint, "isolate", source_risks, rec)

    if args.analysis_only:
        bucket = "manual"
        if decision_hint == "isolate":
            bucket = "isolated"
        item = build_source_record(record_id, instruction, original_code, reason_hint, decision_hint, source_risks, rec)
        item["task_family"] = estimate_task_family(instruction, original_code)
        item["status"] = "analysis_only"
        return bucket, item

    prompt = build_reconstruction_prompt(
        original_instruction=instruction,
        original_code=original_code,
        record_id=record_id,
        source_risks=source_risks,
        decision_hint=decision_hint,
        reason_hint=reason_hint,
    )

    current_obj = None
    retry_history = []
    last_failure = None

    for attempt in range(args.max_total_retries + 1):
        try:
            if attempt == 0:
                response = call_llm(
                    prompt,
                    model=args.model,
                    base_url=args.base_url,
                    api_key=args.api_key or os.environ.get("OPENWEBUI_API_KEY") or os.environ.get("OPENAI_API_KEY"),
                    temperature=args.temperature,
                    max_tokens=args.max_tokens,
                    timeout=args.llm_timeout,
                )
            else:
                retry_prompt = build_retry_prompt(
                    current_obj or {},
                    failure_type=last_failure.stage if last_failure else "unknown",
                    diagnostics=last_failure.diagnostics if last_failure else {},
                    original_instruction=instruction,
                    original_code=original_code,
                )
                response = call_llm(
                    retry_prompt,
                    model=args.model,
                    base_url=args.base_url,
                    api_key=args.api_key or os.environ.get("OPENWEBUI_API_KEY") or os.environ.get("OPENAI_API_KEY"),
                    temperature=min(args.temperature + 0.05 * attempt, 0.35),
                    max_tokens=args.max_tokens,
                    timeout=args.llm_timeout,
                )
        except Exception as e:
            item = build_source_record(record_id, instruction, original_code, "llm_call_failed", "manual_review", source_risks, rec)
            item["error"] = str(e)
            item["retry_history"] = retry_history
            return "manual", item

        obj = extract_json_object(response)
        if obj is None:
            last_failure = ValidationResult(False, "invalid_json", {"response_preview": response[:1500]})
            retry_history.append({"attempt": attempt, "failure": last_failure.stage, "diagnostics": last_failure.diagnostics})
            continue

        current_obj = obj
        obj.setdefault("source_type", "A")
        obj.setdefault("original_id", record_id)

        obj["original_instruction"] = instruction
        obj["original_output"] = original_code
        obj["source_quality_flags"] = classify_source_quality(source_risks)
        obj["source_risk_flags"] = source_risks.flags
        obj["source_risk_counts"] = source_risks.counts
        obj["retry_history"] = retry_history

        vr = validate_reconstruction_schema(obj)
        if not vr.ok:
            last_failure = vr
            retry_history.append({"attempt": attempt, "failure": vr.stage, "diagnostics": vr.diagnostics})
            continue

        if obj["decision"] == "delete":
            obj["validation"] = {"final_status": "deleted_by_llm", "retry_attempts": attempt}
            return "deleted", obj

        if obj["decision"] == "isolate":
            obj["validation"] = {"final_status": "isolated_by_llm", "retry_attempts": attempt}
            return "isolated", obj

        vr = validate_static_policy(obj)
        if not vr.ok:
            last_failure = vr
            retry_history.append({"attempt": attempt, "failure": vr.stage, "diagnostics": vr.diagnostics})
            continue

        code_rr = vr.risk_report or analyze_static_risks(obj.get("fortran_code", ""), obj.get("stdin_contract", ""))

        # Dedup reconstructed output: manual_review, not automatic delete.
        if code_rr.normalized_hash in accepted_hashes:
            obj["validation"] = {
                "final_status": "manual_review_duplicate_reconstructed_output",
                "retry_attempts": attempt,
            }
            obj["risk_flags"] = sorted(set(obj.get("risk_flags", []) + ["duplicate_reconstructed_output"]))
            obj["normalized_hash"] = code_rr.normalized_hash
            return "manual", obj

        vr = validate_compile_and_tests(obj, args.compile_timeout, args.run_timeout, args.float_tol, args.validation_workers)
        if not vr.ok:
            last_failure = vr
            retry_history.append({"attempt": attempt, "failure": vr.stage, "diagnostics": vr.diagnostics})
            continue

        vr = validate_antileak(obj, humaneval_index)
        if not vr.ok:
            obj["validation"] = {
                "final_status": "manual_review_possible_humaneval_leak",
                "antileak": vr.diagnostics,
                "retry_attempts": attempt,
            }
            obj["risk_flags"] = sorted(set(obj.get("risk_flags", []) + ["possible_humaneval_leak"]))
            return "manual", obj

        obj["validation"] = {
            "final_status": "accepted",
            "compile": "ok",
            "run": "ok",
            "tests_passed": len(obj.get("tests", [])),
            "tests_total": len(obj.get("tests", [])),
            "retry_attempts": attempt,
        }
        obj["exact_hash"] = code_rr.exact_hash
        obj["normalized_hash"] = code_rr.normalized_hash

        if accepted_hashes_lock is not None:
            with accepted_hashes_lock:
                if code_rr.normalized_hash in accepted_hashes:
                    obj["validation"] = {
                        "final_status": "manual_review_duplicate_reconstructed_output",
                        "retry_attempts": attempt,
                    }
                    obj["risk_flags"] = sorted(set(obj.get("risk_flags", []) + ["duplicate_reconstructed_output"]))
                    return "manual", obj
                accepted_hashes.add(code_rr.normalized_hash)
        else:
            accepted_hashes.add(code_rr.normalized_hash)

        return final_bucket_for(obj), obj

    # Failure after retries.
    if current_obj is None:
        current_obj = {}
    current_obj["original_id"] = record_id
    current_obj["original_instruction"] = instruction
    current_obj["original_output"] = original_code
    current_obj["source_quality_flags"] = classify_source_quality(source_risks)
    current_obj["source_risk_flags"] = source_risks.flags
    current_obj["source_risk_counts"] = source_risks.counts
    current_obj["retry_history"] = retry_history
    current_obj["validation"] = {
        "final_status": "manual_review_after_retries",
        "last_failure_stage": last_failure.stage if last_failure else None,
        "last_diagnostics": last_failure.diagnostics if last_failure else None,
        "retry_attempts": args.max_total_retries,
    }
    return "manual", current_obj


# =============================================================================
# Main
# =============================================================================

def main() -> None:
    ap = argparse.ArgumentParser(
        description="Rebuild Type A into clean HumanEval-like Fortran dataset, V2 sequential.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    ap.add_argument("--input", required=True, help="Input train_A.json/jsonl or equivalent.")
    ap.add_argument("--output-dir", required=True, help="Output directory.")
    ap.add_argument("--model", default=None, help="LLM model name.")
    ap.add_argument("--base-url", default=None, help="OpenAI-compatible base URL, e.g. http://localhost:8086")
    ap.add_argument("--api-key", default=None)
    ap.add_argument("--benchmark", default=None, help="Optional benchmark.json for anti-leak checks.")
    ap.add_argument("--max-items", type=int, default=None)
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--analysis-only", action="store_true")
    ap.add_argument("--isolate-without-llm", action="store_true")
    ap.add_argument("--drop-source-duplicates", action="store_true", help="Drop normalized duplicate source outputs except first.")
    ap.add_argument("--checkpoint-every", type=int, default=10)
    ap.add_argument("--sleep", type=float, default=0.0)
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--max-tokens", type=int, default=4096)
    ap.add_argument("--llm-timeout", type=int, default=240)
    ap.add_argument("--compile-timeout", type=int, default=30)
    ap.add_argument("--run-timeout", type=int, default=10)
    ap.add_argument("--float-tol", type=float, default=1e-6)
    ap.add_argument("--validation-workers", type=int, default=1, help="Parallel workers for local test execution after compilation.")
    ap.add_argument("--llm-concurrency", type=int, default=1, help="Parallel workers for LLM reconstruction calls.")
    ap.add_argument("--max-total-retries", type=int, default=5)
    args = ap.parse_args()

    if not args.analysis_only and (not args.model or not args.base_url):
        raise SystemExit("--model and --base-url are required unless --analysis-only is used.")

    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    paths = build_output_paths(str(outdir))

    data = load_json_or_jsonl(args.input)
    if not isinstance(data, list):
        raise SystemExit("Input must be a JSON list or JSONL file.")
    if args.max_items:
        data = data[:args.max_items]

    # Source duplicate statistics.
    source_norm_hashes = []
    source_hash_first_idx = {}
    for idx, rec in enumerate(data, 1):
        code = get_code(rec)
        h = sha256_text(normalize_code_for_hash(code))
        source_norm_hashes.append(h)
        if h not in source_hash_first_idx:
            source_hash_first_idx[h] = idx
    source_hash_counts = Counter(source_norm_hashes)

    humaneval_index = load_humaneval_index(args.benchmark)

    outputs = load_existing_outputs(paths) if args.resume else {
        "clean": [],
        "targeted": [],
        "manual": [],
        "isolated": [],
        "deleted": [],
    }

    done_ids = set()
    accepted_hashes = set()
    accepted_hashes_lock = threading.Lock()

    for bucket_items in outputs.values():
        for item in bucket_items:
            oid = item.get("original_id")
            if oid:
                done_ids.add(str(oid))
            nh = item.get("normalized_hash")
            if nh:
                accepted_hashes.add(nh)

    print("=" * 100)
    print("Type A HumanEval-like reconstruction V3")
    print("=" * 100)
    print(f"Input records                 : {len(data)}")
    print(f"Output dir                    : {outdir}")
    print(f"Analysis only                 : {args.analysis_only}")
    print(f"Resume                        : {args.resume}")
    print(f"Already done                  : {len(done_ids)}")
    print(f"Unique normalized source codes: {len(source_hash_counts)}")
    print(f"Source duplicate groups       : {sum(1 for v in source_hash_counts.values() if v > 1)}")
    print(f"Drop source duplicates        : {args.drop_source_duplicates}")
    print(f"Validation workers            : {args.validation_workers}")
    print(f"LLM concurrency               : {args.llm_concurrency}")
    print("=" * 100)

    if not args.analysis_only:
        init_llm_client(max_concurrency=args.llm_concurrency)

    t0 = time.time()
    processed = 0

    pending = []
    for idx, rec in enumerate(data, 1):
        record_id = get_record_id(rec, idx)
        if args.resume and record_id in done_ids:
            continue
        pending.append((idx, rec, record_id))

    def run_record(idx_rec_record_id):
        idx, rec, record_id = idx_rec_record_id
        bucket, obj = reconstruct_one(
            rec=rec,
            idx=idx,
            args=args,
            accepted_hashes=accepted_hashes,
            humaneval_index=humaneval_index,
            source_hash_counts=source_hash_counts,
            source_hash_first_idx=source_hash_first_idx,
            accepted_hashes_lock=accepted_hashes_lock,
        )
        return idx, rec, record_id, bucket, obj

    def handle_finished(idx, rec, record_id, bucket, obj):
        nonlocal processed

        outputs[bucket].append(obj)
        done_ids.add(record_id)
        processed += 1

        status = obj.get("validation", {}).get("final_status", obj.get("decision", bucket))
        fam = obj.get("task_family", "?")
        print(f"[{idx}/{len(data)}] id={record_id} -> {bucket} status={status} family={fam}")

        if processed % args.checkpoint_every == 0:
            save_outputs(paths, outputs)
            report = build_report(data, outputs, source_hash_counts)
            save_json(paths["report"], report)
            print(
                f"  checkpoint: clean={len(outputs['clean'])} "
                f"targeted={len(outputs['targeted'])} manual={len(outputs['manual'])} "
                f"isolated={len(outputs['isolated'])} deleted={len(outputs['deleted'])}"
            )

        if args.sleep > 0:
            time.sleep(args.sleep)

    if args.llm_concurrency <= 1 or args.analysis_only:
        for item in pending:
            idx, rec, record_id, bucket, obj = run_record(item)
            handle_finished(idx, rec, record_id, bucket, obj)
    else:
        with ThreadPoolExecutor(max_workers=args.llm_concurrency) as pool:
            future_map = {pool.submit(run_record, item): item for item in pending}

            for fut in as_completed(future_map):
                idx, rec, record_id = future_map[fut]
                try:
                    idx, rec, record_id, bucket, obj = fut.result()
                except Exception as e:
                    instruction = get_instruction(rec)
                    original_code = get_code(rec)
                    source_risks = analyze_static_risks(original_code)
                    obj = build_source_record(
                        record_id=record_id,
                        instruction=instruction,
                        code=original_code,
                        reason="worker_crashed",
                        decision="manual_review",
                        risks=source_risks,
                        rec=rec,
                    )
                    obj["error"] = str(e)
                    bucket = "manual"

                handle_finished(idx, rec, record_id, bucket, obj)

    save_outputs(paths, outputs)
    report = build_report(data, outputs, source_hash_counts)
    report["duration_minutes"] = round((time.time() - t0) / 60, 2)
    save_json(paths["report"], report)

    print("=" * 100)
    print("DONE")
    print(f"Duration min : {report['duration_minutes']}")
    print(f"Clean        : {len(outputs['clean'])} -> {paths['clean']}")
    print(f"Targeted     : {len(outputs['targeted'])} -> {paths['targeted']}")
    print(f"Manual       : {len(outputs['manual'])} -> {paths['manual']}")
    print(f"Isolated     : {len(outputs['isolated'])} -> {paths['isolated']}")
    print(f"Deleted      : {len(outputs['deleted'])} -> {paths['deleted']}")
    print(f"Report       : {paths['report']}")
    print("=" * 100)


if __name__ == "__main__":
    main()
