#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build Type C dataset — V2 vLLM pipeline.

Type C definition:
  instruction = generic debugging instruction + buggy code
  output      = clean corrected code

Difference from Type B:
  - no compiler error shown in the instruction
  - no runtime error shown in the instruction
  - no expected/actual output shown
  - hidden diagnostic is kept only in metadata

Main design:
  - based on build_type_b_v3_vllm.py architecture
  - uses accepted_faithful_v3.json for clean source code
  - uses reference_with_patterns.json for applicable patterns and eligibility
  - uses type_b_v3_dataset.json to avoid reusing the same Type B group when possible
  - Type C groups: compile_err + runtime_err only
  - no ineq for this first Type C V2, to stay consistent with The Stack V1 Type C
  - validates injected bug by real gfortran compile/run
  - parallel vLLM injection with ThreadPoolExecutor
  - checkpointed JSON outputs

Important quality protections:
  - runtime timeout is NOT accepted as a runtime crash
  - newly inserted STOP / ERROR STOP is rejected for runtime_err
  - runtime I/O artifacts are rejected
  - clean baseline code is revalidated before injection
  - FP/overflow runtime patterns use selective gfortran trap flags
"""

import os
import re
import sys
import json
import time
import random
import argparse
import tempfile
import logging
import threading
import subprocess
import requests
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.adapters import HTTPAdapter


# =============================================================================
# Configuration
# =============================================================================

DEFAULT_MODEL = "gpt-oss-120b"
DEFAULT_BASE_URL = "http://localhost:8086"

COMPILE_TIMEOUT = 20
RUN_TIMEOUT = 15
MAX_LLM_RETRIES = 2
GFORTRAN_FLAGS = ["-O0", "-ffree-line-length-none", "-w", "-fcheck=bounds"]

# Extra flags used only for runtime patterns whose failure is otherwise often
# silent with gfortran. They are applied both to the clean baseline check and
# to the injected buggy program, so validation remains fair.
FP_TRAP_FLAGS = ["-ffpe-trap=invalid,zero,overflow"]
OVERFLOW_TRAP_FLAGS = ["-ftrapv"]


ALLOWED_C_GROUPS = {"compile_err", "runtime_err"}

EXCLUDED_RUNTIME_IO_PATTERNS = {
    "eof_input",
    "interactive_prompt_leak",
    "stdin_format_mismatch",
    "invalid_numeric_input",
}

LOW_PRIORITY_RUNTIME_PATTERNS = {
    "floating_point_exception",
}

INSTRUCTION_TEMPLATES = [
    "The following Fortran 90 code contains a bug. Find and fix it.\n\n{code}",
    "Debug the following Fortran 90 program.\n\n{code}",
    "This Fortran 90 program does not work correctly. Identify and correct the error.\n\n{code}",
    "Fix the bug in this Fortran 90 code.\n\n{code}",
    "The following Fortran 90 code has an error. Correct it.\n\n{code}",
    "Find and fix the issue in this Fortran 90 program.\n\n{code}",
]


PATTERN_AXIS_MAP = {
    # compile / syntax
    "allocation_error": "syntax",
    "character_length_mismatch": "syntax",
    "contains_section_error": "syntax",
    "data_attribute_conflict": "syntax",
    "implicit_none_missing": "syntax",
    "intent_violation": "syntax",
    "invalid_array_bounds": "syntax",
    "invalid_dummy_argument": "syntax",
    "invalid_token_or_name": "syntax",
    "missing_interface_block": "syntax",
    "missing_main_program": "syntax",
    "module_use_error": "syntax",
    "pointer_declaration_error": "syntax",
    "subroutine_function_mismatch": "syntax",
    "syntax_error": "syntax",
    "syntax_invalid_condition": "syntax",
    "syntax_invalid_expression": "syntax",
    "syntax_invalid_write": "syntax",
    "syntax_loop_error": "syntax",
    "syntax_missing_end": "syntax",
    "syntax_missing_parenthesis": "syntax",
    "syntax_missing_then": "syntax",
    "syntax_unexpected_statement": "syntax",
    "type_mismatch": "syntax",
    "undeclared_type": "syntax",
    "undeclared_variable": "syntax",
    "undefined_reference": "syntax",
    "wrong_kind_specifier": "syntax",

    # runtime
    "allocation_runtime_error": "runtime",
    "array_bounds_runtime": "runtime",
    "division_by_zero": "runtime",
    "floating_point_exception": "runtime",
    "integer_overflow": "runtime",
    "malloc_corruption": "runtime",
    "segmentation_fault": "runtime",
    "unallocated_access": "runtime",
}


PATTERN_SPECIFIC_HINTS = {
    "implicit_none_missing": """
Do not only remove 'implicit none'.
Create a real undeclared-variable compile error.
""",
    "undeclared_variable": """
Remove the declaration of a variable that is actually used later.
The modified program must fail to compile because the symbol has no implicit type.
""",
    "intent_violation": """
Modify an INTENT(IN) dummy argument inside a subroutine or function.
The modified program must fail to compile.
""",
    "allocation_error": """
Use ALLOCATE incorrectly, for example on a non-allocatable variable.
The modified program must fail to compile.
""",
    "data_attribute_conflict": """
Add conflicting Fortran attributes to one declaration, such as PARAMETER and ALLOCATABLE.
The modified program must fail to compile.
""",
    "contains_section_error": """
Break the CONTAINS section structure in a realistic way.
The modified program must fail to compile.
""",
    "character_length_mismatch": """
Create a character length or substring range error that gfortran rejects at compile time.
Prefer modifying a declaration length or substring bound.
""",
    "invalid_array_bounds": """
Create invalid array bounds that gfortran rejects at compile time.
Avoid changes that are accepted as valid Fortran bounds.
""",
    "missing_interface_block": """
Create a realistic missing or incompatible explicit interface problem.
The modified code must fail to compile.
""",
    "pointer_declaration_error": """
Introduce an invalid POINTER/TARGET declaration or pointer-related declaration error.
The modified code must fail to compile.
""",
    "wrong_kind_specifier": """
Introduce an invalid kind specifier or invalid kind use that causes a compile error.
""",

    "array_bounds_runtime": """
Introduce an array index that is out of bounds during execution.
The code must still compile, then crash at runtime with bounds checking.
Do not use STOP or ERROR STOP.
""",
    "division_by_zero": """
Force a real INTEGER division by zero that is executed at runtime.
Avoid floating-point Infinity-only behavior.
The program must terminate abnormally or return non-zero.
Do not use STOP or ERROR STOP.
""",
    "floating_point_exception": """
Force a real runtime arithmetic failure.
Avoid silent NaN or Infinity generation.
Prefer an operation that reliably terminates abnormally.
Do not use STOP or ERROR STOP.
""",
    "integer_overflow": """
Prefer overflow leading to invalid indexing or runtime failure.
The program must compile and then crash or terminate abnormally.
Do not use STOP or ERROR STOP.
""",
    "segmentation_fault": """
Force a real invalid memory access during execution.
Prefer unallocated access or invalid pointer/array access that causes a crash.
Do not use STOP or ERROR STOP.
""",
    "unallocated_access": """
Use an allocatable array before it is allocated.
The program must compile and crash at runtime.
Do not use STOP or ERROR STOP.
""",
    "allocation_runtime_error": """
Force a real allocation misuse at runtime, such as allocating an already allocated variable.
The program must compile and then fail during execution.
Do not use STOP or ERROR STOP.
""",
    "malloc_corruption": """
Force a runtime memory corruption or invalid memory behavior.
The program must compile and then fail during execution.
Do not use STOP or ERROR STOP.
""",
}


RUNTIME_CRASH_MARKERS = [
    "segmentation fault", "segfault",
    "floating point exception", "floating-point exception",
    "backtrace", "forrtl", "severe",
    "invalid memory reference", "out of bounds",
    "stack smashing", "buffer overflow",
    "abort", "core dumped",
]

SPURIOUS_RUNTIME_MARKERS = [
    "end of file",
    "unit 5",
    "stdin",
    "input/output",
    "read(unit=5",
    "no such file",
    "cannot open",
]


# =============================================================================
# Shared vLLM HTTP client
# =============================================================================

_SESSION = None
_SEMAPHORE = None
_CLIENT_LOCK = threading.Lock()

# Baseline validation cache. Key = (origin_id, tuple(extra_flags)).
# This avoids recompiling/rerunning the same clean program for each retry/pattern.
_BASELINE_CACHE = {}
_BASELINE_LOCK = threading.Lock()



def init_llm_client(max_concurrency, pool_maxsize=None):
    global _SESSION, _SEMAPHORE

    with _CLIENT_LOCK:
        if _SESSION is None:
            pool = pool_maxsize or max(10, max_concurrency)
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
            _SEMAPHORE = threading.BoundedSemaphore(max_concurrency)


def call_llm(system_prompt, user_prompt, model, base_url, api_key=None,
             temperature=0.2, max_tokens=2048, timeout=1200,
             endpoint="/v1/chat/completions"):
    if _SESSION is None or _SEMAPHORE is None:
        init_llm_client(max_concurrency=1)

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    url = f"{base_url.rstrip('/')}{endpoint}"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False,
    }

    with _SEMAPHORE:
        resp = _SESSION.post(url, headers=headers, json=payload, timeout=timeout)

    if resp.status_code != 200:
        raise RuntimeError(f"vLLM HTTP {resp.status_code}: {resp.text[:500]}")

    result = resp.json()
    choices = result.get("choices")
    if not choices:
        raise RuntimeError(f"vLLM returned no choices: {result}")

    content = (choices[0].get("message") or {}).get("content")
    if not content:
        raise RuntimeError(f"vLLM returned empty content: {result}")

    return content.strip()


# =============================================================================
# Logging / JSON utils
# =============================================================================


def setup_logging(log_file):
    logger = logging.getLogger("type_c")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        logger.handlers.clear()

    os.makedirs(os.path.dirname(log_file) or ".", exist_ok=True)

    fh = logging.FileHandler(log_file, mode="a", encoding="utf-8")
    fh.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))

    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(logging.Formatter("%(message)s"))

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


log = logging.getLogger("type_c")


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def safe_load_json(path, default=None):
    if default is None:
        default = []
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else default
    except Exception:
        return default


def save_json(path, data):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)


def build_lookup(data, key="origin_id"):
    out = {}
    for x in data:
        k = x.get(key)
        if k is not None and k not in out:
            out[k] = x
    return out


# =============================================================================
# Prompt construction
# =============================================================================

INJECTION_SYSTEM = """You are an expert Fortran bug injection system.

Your task: inject EXACTLY ONE bug of type "{pattern_name}" ({error_type}) into the provided Fortran code.

Rules:
- The bug must cause a {expected_behavior}.
- Keep the code realistic and structurally identical.
- Do NOT add comments explaining the bug.
- Do NOT add or remove READ/WRITE/PRINT statements.
- Do NOT add STOP or ERROR STOP statements to force failure.
- Do NOT change the program name or subroutine names.
- Output ONLY the full modified Fortran source code, no explanation.
- Do NOT wrap the code in markdown fences.
"""

EXPECTED_BEHAVIORS = {
    "compile_err": "compilation error, so gfortran must reject the code",
    "runtime_err": "runtime crash, such as array bounds error, segmentation fault, floating point exception, or non-zero exit code caused by the injected bug",
}


def build_injection_prompt(code, pattern_name, error_type):
    expected = EXPECTED_BEHAVIORS.get(error_type, "detectable error")
    hint = PATTERN_SPECIFIC_HINTS.get(
        pattern_name,
        "Ensure the injected bug really produces the requested behavior.",
    )

    system = INJECTION_SYSTEM.format(
        pattern_name=pattern_name,
        error_type=error_type,
        expected_behavior=expected,
    )

    system += "\n\nPattern-specific guidance:\n" + hint.strip()

    return system, code


def build_type_c_instruction(buggy_code, origin_id):
    try:
        idx = int(origin_id) % len(INSTRUCTION_TEMPLATES)
    except Exception:
        idx = abs(hash(str(origin_id))) % len(INSTRUCTION_TEMPLATES)

    template = INSTRUCTION_TEMPLATES[idx]
    return template.format(code=buggy_code.strip())


# =============================================================================
# Code extraction / compile / run
# =============================================================================


def extract_code(text):
    text = text.strip()

    m = re.search(
        r"```(?:fortran|f90|f95|f03)?\s*\n(.*?)```",
        text,
        re.DOTALL | re.IGNORECASE,
    )
    if m:
        return m.group(1).strip()

    lines = text.split("\n")
    code_lines = []
    in_code = False

    starters = [
        "program ", "module ", "subroutine ", "function ",
        "implicit ", "integer", "real", "double precision",
        "character", "logical", "complex", "type ", "use ", "!",
    ]

    for line in lines:
        low = line.strip().lower()
        if not in_code and any(low.startswith(k) for k in starters):
            in_code = True
        if in_code:
            code_lines.append(line)

    if code_lines:
        return "\n".join(code_lines).strip()

    return text


def get_extra_gfortran_flags(pattern_name, error_type):
    """Return pattern-specific compiler/runtime trap flags.

    Floating-point exceptions and signed integer overflow are not reliably
    observable with the default flags alone. These flags make such failures
    visible during validation when those patterns are selected.

    Note: division_by_zero intentionally uses the default flags. Integer
    division by zero already raises SIGFPE independently of -ffpe-trap, and
    applying FP trap flags to the clean baseline can unnecessarily reject
    otherwise valid scientific programs.
    """
    if error_type != "runtime_err":
        return []

    if pattern_name == "floating_point_exception":
        return list(FP_TRAP_FLAGS)

    if pattern_name == "integer_overflow":
        return list(OVERFLOW_TRAP_FLAGS)

    return []


def compile_fortran(src_path, exe_path, extra_flags=None):
    flags = list(GFORTRAN_FLAGS)
    if extra_flags:
        flags.extend(extra_flags)

    return subprocess.run(
        ["gfortran"] + flags + [src_path, "-o", exe_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=COMPILE_TIMEOUT,
        text=True,
    )


def run_executable(exe_path):
    env = os.environ.copy()
    env["GFORTRAN_UNBUFFERED_ALL"] = "1"

    return subprocess.run(
        [exe_path],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=RUN_TIMEOUT,
        text=True,
        env=env,
    )


def _has_crash_markers(stderr):
    s = (stderr or "").lower()
    return any(m in s for m in RUNTIME_CRASH_MARKERS)


def _has_spurious_markers(stderr):
    s = (stderr or "").lower()
    return any(m in s for m in SPURIOUS_RUNTIME_MARKERS)


def clean_compile_error(stderr, max_errors=5):
    if not stderr:
        return ""

    stderr = re.sub(r"/tmp/[^\s]+/test\.f90", "test.f90", stderr)

    lines = stderr.strip().splitlines()
    kept = []
    error_count = 0

    for line in lines:
        kept.append(line)

        if line.strip().lower().startswith("error:"):
            error_count += 1

        if error_count >= max_errors:
            break

    return "\n".join(kept).strip()


def clean_runtime_error(stderr):
    if not stderr:
        return ""

    lines = stderr.strip().splitlines()
    kept = []

    for line in lines:
        low = line.lower()
        if "backtrace" in low:
            break

        line = re.sub(r"/tmp/[^\s]+/test\.f90", "test.f90", line)
        line = re.sub(r"0x[0-9a-fA-F]+", "0xADDR", line)
        kept.append(line)

    return "\n".join(kept).strip()


def has_new_stop_statement(original_code, injected_code):
    """Reject runtime injections that only force failure using STOP/ERROR STOP.

    Uses Counter rather than set comparison, so adding a second identical STOP
    line is still detected.
    """
    stop_pattern = re.compile(
        r"^\s*(error\s+stop|stop)(\s+[^!\n]*)?(?:!.*)?$",
        re.IGNORECASE | re.MULTILINE,
    )

    def collect_counts(code):
        return Counter(
            re.sub(r"\s+", " ", m.group(0).strip().lower())
            for m in stop_pattern.finditer(code or "")
        )

    original_stops = collect_counts(original_code)
    injected_stops = collect_counts(injected_code)

    for stop_line, count in injected_stops.items():
        if count > original_stops.get(stop_line, 0):
            return True

    return False


# =============================================================================
# Validation / injection
# =============================================================================


def revalidate_clean_baseline(origin_id, clean_code, extra_flags=None, run_baseline=True):
    """Revalidate the clean corrected code before creating a Type C item.

    For compile_err Type C tasks, the clean baseline only needs to compile:
      clean code compiles -> injected code fails to compile.

    For runtime_err Type C tasks, the clean baseline must compile and run with
    return code 0 under the same validation flags:
      clean code runs successfully -> injected code crashes at runtime.

    Results are cached per (origin_id, extra_flags, run_baseline).
    """
    flags_key = tuple(extra_flags or [])
    cache_key = (origin_id, flags_key, bool(run_baseline))

    with _BASELINE_LOCK:
        cached = _BASELINE_CACHE.get(cache_key)
    if cached is not None:
        return cached

    result = {
        "baseline_valid": False,
        "baseline_failure_reason": None,
        "baseline_compile_returncode": None,
        "baseline_run_returncode": None,
        "baseline_compile_stderr": None,
        "baseline_runtime_stderr": None,
        "baseline_extra_flags": list(extra_flags or []),
        "baseline_run_executed": bool(run_baseline),
    }

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            src_path = str(Path(tmpdir) / "clean.f90")
            exe_path = str(Path(tmpdir) / "clean.out")

            Path(src_path).write_text(clean_code, encoding="utf-8")

            compile_result = compile_fortran(src_path, exe_path, extra_flags=extra_flags)
            result["baseline_compile_returncode"] = compile_result.returncode
            result["baseline_compile_stderr"] = clean_compile_error(compile_result.stderr or "")

            if compile_result.returncode != 0:
                result["baseline_failure_reason"] = "clean_code_compile_failed"

            elif not run_baseline:
                # For compile_err tasks, compiling clean code is sufficient.
                result["baseline_valid"] = True

            else:
                try:
                    run_result = run_executable(exe_path)
                    result["baseline_run_returncode"] = run_result.returncode
                    result["baseline_runtime_stderr"] = clean_runtime_error(run_result.stderr or "")

                    if run_result.returncode != 0:
                        result["baseline_failure_reason"] = "clean_code_nonzero_exit"
                    else:
                        result["baseline_valid"] = True

                except subprocess.TimeoutExpired:
                    result["baseline_failure_reason"] = "clean_code_timeout"

    except Exception as e:
        result["baseline_failure_reason"] = f"clean_code_baseline_error: {e}"

    with _BASELINE_LOCK:
        _BASELINE_CACHE[cache_key] = result

    return result

def validate_behavior(error_type, compile_result, run_result):
    if error_type == "compile_err":
        return compile_result.returncode != 0

    if compile_result.returncode != 0:
        return False

    if error_type == "runtime_err":
        if run_result is None:
            return False

        if run_result.returncode != 0:
            if _has_spurious_markers(run_result.stderr):
                return False
            return True

        if _has_crash_markers(run_result.stderr):
            return True

        return False

    return False


def try_inject_pattern(code, pattern_name, error_type, model, base_url, api_key, extra_flags=None):
    system_prompt, user_prompt = build_injection_prompt(code, pattern_name, error_type)

    last_error = None

    for attempt in range(1, MAX_LLM_RETRIES + 1):
        try:
            raw_response = call_llm(
                system_prompt,
                user_prompt,
                model,
                base_url,
                api_key,
                temperature=0.2 + (attempt - 1) * 0.1,
                max_tokens=2048,
                timeout=1200,
            )
        except Exception as e:
            last_error = e
            if attempt < MAX_LLM_RETRIES:
                time.sleep(2)
                continue
            return {
                "pattern_name": pattern_name,
                "error_type": error_type,
                "validation_success": False,
                "failure_reason": f"llm_error: {last_error}",
                "num_attempts": attempt,
            }

        injected_code = extract_code(raw_response)

        if not injected_code or len(injected_code.strip()) < 20:
            last_error = "empty_or_too_short_code"
            if attempt < MAX_LLM_RETRIES:
                continue
            return {
                "pattern_name": pattern_name,
                "error_type": error_type,
                "validation_success": False,
                "failure_reason": "empty_or_too_short_code",
                "num_attempts": attempt,
            }

        if injected_code.strip() == code.strip():
            last_error = "injected_code_identical_to_original"
            if attempt < MAX_LLM_RETRIES:
                continue
            return {
                "pattern_name": pattern_name,
                "error_type": error_type,
                "validation_success": False,
                "failure_reason": "injected_code_identical_to_original",
                "num_attempts": attempt,
            }

        if error_type == "runtime_err" and has_new_stop_statement(code, injected_code):
            last_error = "new_stop_statement_detected"
            if attempt < MAX_LLM_RETRIES:
                continue
            return {
                "pattern_name": pattern_name,
                "error_type": error_type,
                "validation_success": False,
                "failure_reason": "new_stop_statement_detected",
                "num_attempts": attempt,
            }

        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                src_path = str(Path(tmpdir) / "test.f90")
                exe_path = str(Path(tmpdir) / "a.out")

                Path(src_path).write_text(injected_code, encoding="utf-8")

                compile_result = compile_fortran(src_path, exe_path, extra_flags=extra_flags)
                run_result = None

                if compile_result.returncode == 0 and error_type == "runtime_err":
                    try:
                        run_result = run_executable(exe_path)
                    except subprocess.TimeoutExpired:
                        last_error = "runtime_timeout_not_crash"
                        if attempt < MAX_LLM_RETRIES:
                            continue
                        return {
                            "pattern_name": pattern_name,
                            "error_type": error_type,
                            "validation_success": False,
                            "failure_reason": "runtime_timeout_not_crash",
                            "num_attempts": attempt,
                        }

                valid = validate_behavior(error_type, compile_result, run_result)

                result = {
                    "pattern_name": pattern_name,
                    "error_type": error_type,
                    "validation_success": valid,
                    "injected_code": injected_code,
                    "compile_returncode": compile_result.returncode,
                    "compile_stdout": compile_result.stdout or "",
                    "compile_stderr": clean_compile_error(compile_result.stderr or ""),
                    "num_attempts": attempt,
                }

                if run_result is not None:
                    result["run_returncode"] = run_result.returncode
                    result["run_stdout"] = run_result.stdout or ""
                    result["run_stderr"] = run_result.stderr or ""

                if valid:
                    return result

                if error_type == "compile_err" and compile_result.returncode == 0:
                    result["failure_reason"] = "code_compiled_when_it_should_not"
                elif error_type == "runtime_err" and compile_result.returncode != 0:
                    result["failure_reason"] = "compile_failed_when_runtime_expected"
                elif error_type == "runtime_err" and run_result and run_result.returncode == 0:
                    result["failure_reason"] = "ran_successfully_when_should_crash"
                elif error_type == "runtime_err" and run_result and run_result.returncode != 0 and _has_spurious_markers(run_result.stderr):
                    result["failure_reason"] = "spurious_io_artifact"
                else:
                    result["failure_reason"] = "validation_failed"

                last_error = result["failure_reason"]

                if attempt < MAX_LLM_RETRIES:
                    continue
                return result

        except Exception as e:
            last_error = f"compile_run_error: {e}"
            if attempt < MAX_LLM_RETRIES:
                continue
            return {
                "pattern_name": pattern_name,
                "error_type": error_type,
                "validation_success": False,
                "failure_reason": last_error,
                "num_attempts": attempt,
            }

    return {
        "pattern_name": pattern_name,
        "error_type": error_type,
        "validation_success": False,
        "failure_reason": f"all_attempts_failed: {last_error}",
        "num_attempts": MAX_LLM_RETRIES,
    }


# =============================================================================
# Type C planning
# =============================================================================


def build_pattern_to_group(patterns_db):
    out = {}
    for p in patterns_db:
        raw = p.get("raw_pattern")
        group = p.get("error_type")
        if raw and group:
            out[raw] = group
    return out


def get_type_b_groups(type_b_dataset):
    by_oid = defaultdict(set)
    by_oid_pattern = defaultdict(set)

    for item in type_b_dataset:
        oid = item.get("source_origin_id") or item.get("origin_id")
        meta = item.get("metadata", {})
        group = meta.get("target_group") or meta.get("injected_group")
        pattern = meta.get("target_pattern") or meta.get("injected_pattern")

        if oid is None:
            continue
        if group:
            by_oid[oid].add(group)
        if pattern:
            by_oid_pattern[oid].add(pattern)

    return by_oid, by_oid_pattern


def code_needs_stdin(code):
    c = (code or "").lower()
    return (
        "read(*" in c
        or "read (*" in c
        or "read(5" in c
        or "read (5" in c
    )


def build_c_candidates(ref_entry, code, pattern_to_group, type_b_groups, type_b_patterns):
    allowed_groups = set()

    if ref_entry.get("type_c") is False:
        return {}

    if ref_entry.get("type_b_compile"):
        allowed_groups.add("compile_err")
    if ref_entry.get("type_b_runtime"):
        allowed_groups.add("runtime_err")

    allowed_groups &= ALLOWED_C_GROUPS

    if code_needs_stdin(code):
        allowed_groups.discard("runtime_err")

    out = defaultdict(list)

    # First pass: avoid Type B groups and Type B exact patterns.
    for pattern in ref_entry.get("applicable_patterns", []):
        group = pattern_to_group.get(pattern)
        if group is None:
            continue
        if group not in allowed_groups:
            continue
        if group in type_b_groups:
            continue
        if pattern in type_b_patterns:
            continue
        if pattern in EXCLUDED_RUNTIME_IO_PATTERNS:
            continue
        if pattern in LOW_PRIORITY_RUNTIME_PATTERNS:
            # Keep possible as fallback only, not first-pass candidate.
            continue

        out[group].append(pattern)

    # Fallback 1: still avoid exact Type B pattern, but allow same Type B group.
    if not out:
        for pattern in ref_entry.get("applicable_patterns", []):
            group = pattern_to_group.get(pattern)
            if group is None:
                continue
            if group not in allowed_groups:
                continue
            if pattern in type_b_patterns:
                continue
            if pattern in EXCLUDED_RUNTIME_IO_PATTERNS:
                continue
            if pattern in LOW_PRIORITY_RUNTIME_PATTERNS:
                continue

            out[group].append(pattern)

    # Fallback 2: allow low-priority runtime patterns if no other option exists.
    if not out:
        for pattern in ref_entry.get("applicable_patterns", []):
            group = pattern_to_group.get(pattern)
            if group is None:
                continue
            if group not in allowed_groups:
                continue
            if pattern in type_b_patterns:
                continue
            if pattern in EXCLUDED_RUNTIME_IO_PATTERNS:
                continue

            out[group].append(pattern)

    return out


def choose_group_and_patterns(candidates, group_counts, pattern_counts, n_candidates):
    available = [g for g, pats in candidates.items() if pats]
    if not available:
        return None, []

    chosen_group = min(available, key=lambda g: group_counts[g])
    patterns = sorted(candidates[chosen_group], key=lambda p: pattern_counts[p])

    return chosen_group, patterns[:n_candidates]


def plan_type_c_assignments(reference, faithful_lookup, patterns_db, type_b_dataset,
                            max_assignments=None, candidates_per_code=3):
    pattern_to_group = build_pattern_to_group(patterns_db)
    type_b_groups_by_oid, type_b_patterns_by_oid = get_type_b_groups(type_b_dataset)

    assignments = []
    skipped = []
    stats = Counter()
    group_counts = Counter()
    pattern_counts = Counter()

    for ref_entry in sorted(reference, key=lambda x: x.get("origin_id", 10**18)):
        oid = ref_entry.get("origin_id")
        if oid is None:
            continue

        code_entry = faithful_lookup.get(oid)
        if not code_entry:
            stats["skip_code_not_found"] += 1
            skipped.append({"origin_id": oid, "skip_reason": "code_not_found"})
            continue

        if ref_entry.get("decision") != "keep":
            stats["skip_not_keep"] += 1
            continue

        code = code_entry.get("generated_code", "") or ""
        if not code.strip():
            stats["skip_empty_code"] += 1
            skipped.append({"origin_id": oid, "skip_reason": "empty_code"})
            continue

        type_b_groups = type_b_groups_by_oid.get(oid, set())
        type_b_patterns = type_b_patterns_by_oid.get(oid, set())

        candidates = build_c_candidates(
            ref_entry=ref_entry,
            code=code,
            pattern_to_group=pattern_to_group,
            type_b_groups=type_b_groups,
            type_b_patterns=type_b_patterns,
        )

        group, selected_patterns = choose_group_and_patterns(
            candidates=candidates,
            group_counts=group_counts,
            pattern_counts=pattern_counts,
            n_candidates=candidates_per_code,
        )

        if not group or not selected_patterns:
            stats["skip_no_available_pattern"] += 1
            skipped.append({
                "origin_id": oid,
                "skip_reason": "no_available_pattern",
                "type_b_groups": sorted(type_b_groups),
                "type_b_patterns": sorted(type_b_patterns),
            })
            continue

        assignment = {
            "origin_id": oid,
            "target_group": group,
            "candidate_patterns": selected_patterns,
            "target_successes": 1,
            "type_b_groups": sorted(type_b_groups),
            "type_b_patterns": sorted(type_b_patterns),
            "run_stdout": code_entry.get("run_stdout"),
            "quality": ref_entry.get("quality"),
        }

        assignments.append(assignment)
        group_counts[group] += 1
        for p in selected_patterns:
            pattern_counts[p] += 1
        stats["created"] += 1

        if max_assignments and len(assignments) >= max_assignments:
            break

    return assignments, skipped, stats, group_counts, pattern_counts


# =============================================================================
# Type C entry creation
# =============================================================================


def get_type_c_axes(pattern_name, target_group):
    primary = PATTERN_AXIS_MAP.get(pattern_name)

    if primary is None:
        if target_group == "compile_err":
            primary = "syntax"
        elif target_group == "runtime_err":
            primary = "runtime"
        else:
            primary = "logic"

    secondary = []
    if target_group == "compile_err" and primary != "syntax":
        secondary.append("syntax")
    if target_group == "runtime_err" and primary != "runtime":
        secondary.append("runtime")

    return primary, secondary


def process_type_c_assignment(assignment, code, model, base_url, api_key):
    origin_id = assignment["origin_id"]
    target_group = assignment["target_group"]
    candidate_patterns = list(assignment.get("candidate_patterns", []))

    # Keep planned balance order; do not shuffle.
    successes = []
    failures = []

    if not candidate_patterns:
        return [], [{
            "pattern_name": None,
            "failure_reason": "no_candidate_patterns",
        }]

    for pattern_name in candidate_patterns:
        if successes:
            break

        extra_flags = get_extra_gfortran_flags(pattern_name, target_group)

        run_baseline = (target_group == "runtime_err")

        baseline = revalidate_clean_baseline(
            origin_id=origin_id,
            clean_code=code,
            extra_flags=extra_flags,
            run_baseline=run_baseline,
        )

        if not baseline.get("baseline_valid"):
            failures.append({
                "pattern_name": pattern_name,
                "failure_reason": baseline.get("baseline_failure_reason", "clean_baseline_failed"),
                "baseline_compile_returncode": baseline.get("baseline_compile_returncode"),
                "baseline_run_returncode": baseline.get("baseline_run_returncode"),
                "baseline_extra_flags": baseline.get("baseline_extra_flags", []),
                "baseline_run_executed": baseline.get("baseline_run_executed", False),
                "baseline_compile_stderr": baseline.get("baseline_compile_stderr"),
                "baseline_runtime_stderr": baseline.get("baseline_runtime_stderr"),
            })
            continue

        result = try_inject_pattern(
            code=code,
            pattern_name=pattern_name,
            error_type=target_group,
            model=model,
            base_url=base_url,
            api_key=api_key,
            extra_flags=extra_flags,
        )

        if not result.get("validation_success"):
            failures.append({
                "pattern_name": pattern_name,
                "failure_reason": result.get("failure_reason", "unknown"),
            })
            continue

        buggy_code = result["injected_code"]
        instruction = build_type_c_instruction(buggy_code, origin_id)
        primary_axis, secondary_axes = get_type_c_axes(pattern_name, target_group)

        hidden_compiler_output = None
        hidden_runtime_error = None
        compile_returncode = result.get("compile_returncode")
        run_returncode = result.get("run_returncode")

        if target_group == "compile_err":
            hidden_compiler_output = result.get("compile_stderr", "")
        elif target_group == "runtime_err":
            hidden_runtime_error = clean_runtime_error(result.get("run_stderr", ""))

        entry = {
            "type": "C",
            "source_origin_id": origin_id,
            "instruction": instruction,
            "output": code,
            "primary_axis": primary_axis,
            "secondary_axes": secondary_axes,
            "metadata": {
                "injected_pattern": pattern_name,
                "injected_group": target_group,
                "signal_type": "none",
                "num_attempts": result.get("num_attempts", 1),
                "type_b_groups": assignment.get("type_b_groups", []),
                "type_b_patterns": assignment.get("type_b_patterns", []),
                "observed_group": target_group,
                "pattern_match_status": "group_only",
                "hidden_compiler_output": hidden_compiler_output,
                "hidden_runtime_error": hidden_runtime_error,
                "compile_returncode": compile_returncode,
                "run_returncode": run_returncode,
                "baseline_compile_returncode": baseline.get("baseline_compile_returncode"),
                "baseline_run_returncode": baseline.get("baseline_run_returncode"),
                "baseline_run_executed": baseline.get("baseline_run_executed", False),
                "extra_gfortran_flags": extra_flags,
            },
        }

        successes.append(entry)

    return successes, failures


# =============================================================================
# Build Type C
# =============================================================================


def build_type_c(
    faithful_path,
    reference_path,
    patterns_path,
    type_b_dataset_path,
    output_path,
    assignments_output,
    skipped_output,
    errors_output,
    model,
    base_url,
    api_key,
    log_file,
    max_concurrency,
    candidates_per_code,
    max_assignments,
    rebuild_assignments,
):
    setup_logging(log_file)
    init_llm_client(max_concurrency)

    log.info("=" * 70)
    log.info(f"TYPE C BUILD V2 adjusted (vLLM, concurrency={max_concurrency}) — {datetime.now():%Y-%m-%d %H:%M:%S}")
    log.info("=" * 70)

    faithful = load_json(faithful_path)
    reference = load_json(reference_path)
    patterns_db = load_json(patterns_path)
    type_b_dataset = safe_load_json(type_b_dataset_path, [])

    faithful_lookup = build_lookup(faithful, "origin_id")

    log.info(f"Faithful codes : {len(faithful_lookup)}")
    log.info(f"Reference rows : {len(reference)}")
    log.info(f"Type B entries : {len(type_b_dataset)}")
    log.info("Type C groups  : compile_err + runtime_err only")
    log.info(f"Trap flags     : FP={FP_TRAP_FLAGS}, overflow={OVERFLOW_TRAP_FLAGS}")
    log.info("Protections    : baseline compile-only for compile_err, compile+run for runtime_err")
    log.info("                 stdin isolated with DEVNULL, timeout rejected, new STOP/ERROR STOP rejected")
    log.info("")

    if rebuild_assignments or not os.path.exists(assignments_output):
        assignments, skipped, stats, group_counts, pattern_counts = plan_type_c_assignments(
            reference=reference,
            faithful_lookup=faithful_lookup,
            patterns_db=patterns_db,
            type_b_dataset=type_b_dataset,
            max_assignments=max_assignments,
            candidates_per_code=candidates_per_code,
        )

        save_json(assignments_output, assignments)
        save_json(skipped_output, skipped)

        log.info("Planning done:")
        log.info(f"  assignments : {len(assignments)}")
        log.info(f"  skipped     : {len(skipped)}")
        log.info("")
        log.info("Planning stats:")
        for k, v in stats.most_common():
            log.info(f"  {k:30s}: {v}")
        log.info("")
        log.info("Planned groups:")
        for g, c in group_counts.most_common():
            log.info(f"  {g:15s}: {c}")
        log.info("")
        log.info("Top planned patterns:")
        for p, c in pattern_counts.most_common(20):
            log.info(f"  {p:35s}: {c}")
        log.info("")
    else:
        assignments = load_json(assignments_output)
        log.info(f"Loaded existing assignments: {len(assignments)}")

    dataset = safe_load_json(output_path, [])
    errors = safe_load_json(errors_output, [])

    done_ids = set()
    for item in dataset:
        oid = item.get("source_origin_id") or item.get("origin_id")
        if oid is not None:
            done_ids.add(oid)

    remaining = [a for a in assignments if a["origin_id"] not in done_ids]

    log.info(f"Already done : {len(done_ids)}")
    log.info(f"Remaining    : {len(remaining)}")
    log.info(f"Model        : {model}")
    log.info(f"Base URL     : {base_url}")
    log.info("")

    if not remaining:
        log.info("Nothing to process.")
        return

    write_lock = threading.Lock()
    counter = {
        "done": 0,
        "succ": 0,
        "fail": 0,
        "next_id": len(dataset) + 1,
    }

    group_counts_final = Counter()
    pattern_counts_final = Counter()
    failure_reasons = Counter()

    run_start = time.time()

    def worker(assignment):
        oid = assignment["origin_id"]
        code_entry = faithful_lookup.get(oid)

        if not code_entry:
            return oid, [], [{"pattern_name": None, "failure_reason": "code_not_found"}]

        code = code_entry.get("generated_code", "") or ""
        if not code.strip():
            return oid, [], [{"pattern_name": None, "failure_reason": "empty_code"}]

        successes, failures = process_type_c_assignment(
            assignment=assignment,
            code=code,
            model=model,
            base_url=base_url,
            api_key=api_key,
        )

        return oid, successes, failures

    with ThreadPoolExecutor(max_workers=max_concurrency) as pool:
        futures = {pool.submit(worker, a): a for a in remaining}

        for fut in as_completed(futures):
            assignment = futures[fut]
            oid = assignment["origin_id"]

            try:
                oid, successes, failures = fut.result()
            except Exception as e:
                successes = []
                failures = [{
                    "pattern_name": None,
                    "failure_reason": f"worker_crashed: {e}",
                }]

            with write_lock:
                for s in successes:
                    s["id"] = f"type_c_{counter['next_id']:04d}"
                    counter["next_id"] += 1
                    dataset.append(s)

                    group_counts_final[s["metadata"]["injected_group"]] += 1
                    pattern_counts_final[s["metadata"]["injected_pattern"]] += 1

                if failures:
                    errors.append({
                        "origin_id": oid,
                        "target_group": assignment.get("target_group"),
                        "candidate_patterns": assignment.get("candidate_patterns", []),
                        "type_b_groups": assignment.get("type_b_groups", []),
                        "type_b_patterns": assignment.get("type_b_patterns", []),
                        "failures": failures,
                    })
                    for f in failures:
                        failure_reasons[f.get("failure_reason", "unknown")] += 1

                counter["done"] += 1
                counter["succ"] += len(successes)
                counter["fail"] += len(failures)
                d = counter["done"]

                if d % 10 == 0 or d == len(remaining):
                    save_json(output_path, dataset)
                    save_json(errors_output, errors)

                current_done = counter["done"]
                current_succ = counter["succ"]
                current_fail = counter["fail"]

            elapsed = time.time() - run_start
            eta = elapsed / current_done * (len(remaining) - current_done) / 60

            pats_ok = [s["metadata"]["injected_pattern"] for s in successes]
            pats_fail = [f.get("pattern_name") for f in failures]

            log.info(
                f"[{current_done}/{len(remaining)}] oid={oid:>5d} "
                f"✓{len(successes)} ✗{len(failures)} "
                f"group={assignment.get('target_group')} "
                f"ok={pats_ok} fail={pats_fail} "
                f"ETA {eta:.0f}min"
            )

    with write_lock:
        save_json(output_path, dataset)
        save_json(errors_output, errors)

    total_time = (time.time() - run_start) / 60

    group_counts_final = Counter()
    pattern_counts_final = Counter()
    axis_counts_final = Counter()
    match_status_counts = Counter()

    for item in dataset:
        meta = item.get("metadata", {})
        group_counts_final[meta.get("injected_group", "?")] += 1
        pattern_counts_final[meta.get("injected_pattern", "?")] += 1
        axis_counts_final[item.get("primary_axis", "?")] += 1
        match_status_counts[meta.get("pattern_match_status", "?")] += 1

    failure_reasons = Counter()
    for e in errors:
        for f in e.get("failures", []):
            failure_reasons[f.get("failure_reason", "unknown")] += 1

    log.info("")
    log.info("=" * 70)
    log.info(f"TYPE C V2 DONE — {datetime.now():%Y-%m-%d %H:%M:%S}")
    log.info(f"Duration       : {total_time:.1f} min")
    log.info(f"Dataset size   : {len(dataset)} -> {output_path}")
    log.info(f"Errors         : {len(errors)} -> {errors_output}")
    log.info(f"Assignments    : {assignments_output}")
    log.info(f"Successes      : {counter['succ']}")
    log.info(f"Failures       : {counter['fail']}")

    if counter["done"] > 0:
        log.info(f"Assignment success rate: {100 * counter['succ'] / counter['done']:.1f}%")

    log.info("")
    log.info("Group distribution:")
    for g, c in group_counts_final.most_common():
        log.info(f"  {g:15s}: {c}")

    log.info("")
    log.info("Primary axis distribution:")
    for a, c in axis_counts_final.most_common():
        log.info(f"  {a:15s}: {c}")

    log.info("")
    log.info("Pattern match status:")
    for s, c in match_status_counts.most_common():
        log.info(f"  {s:20s}: {c}")

    log.info("")
    log.info("Top patterns:")
    for p, c in pattern_counts_final.most_common(20):
        log.info(f"  {p:35s}: {c}")

    log.info("")
    log.info("Failure reasons:")
    for r, c in failure_reasons.most_common(20):
        log.info(f"  {r:35s}: {c}")

    log.info("=" * 70)


# =============================================================================
# CLI
# =============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Build Type C V2 dataset — autonomous debugging without signal"
    )

    parser.add_argument("--faithful", required=True)
    parser.add_argument("--reference", required=True)
    parser.add_argument("--patterns", required=True)
    parser.add_argument("--type-b-dataset", required=True)

    parser.add_argument("--output", default="dataset/type_c_v2/type_c_v2_dataset.json")
    parser.add_argument("--assignments-output", default="dataset/type_c_v2/type_c_v2_assignments.json")
    parser.add_argument("--skipped-output", default="dataset/type_c_v2/type_c_v2_skipped.json")
    parser.add_argument("--errors-output", default="dataset/type_c_v2/type_c_v2_errors.json")

    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--api-key", default=None)
    parser.add_argument("--concurrency", type=int, default=64)

    parser.add_argument("--candidates-per-code", type=int, default=3)
    parser.add_argument("--max-assignments", type=int, default=None)
    parser.add_argument("--rebuild-assignments", action="store_true")

    parser.add_argument("--log-file", default="dataset/type_c_v2/type_c_v2_build.log")

    args = parser.parse_args()

    build_type_c(
        faithful_path=args.faithful,
        reference_path=args.reference,
        patterns_path=args.patterns,
        type_b_dataset_path=args.type_b_dataset,
        output_path=args.output,
        assignments_output=args.assignments_output,
        skipped_output=args.skipped_output,
        errors_output=args.errors_output,
        model=args.model,
        base_url=args.base_url,
        api_key=args.api_key or os.environ.get("OPENWEBUI_API_KEY"),
        log_file=args.log_file,
        max_concurrency=args.concurrency,
        candidates_per_code=args.candidates_per_code,
        max_assignments=args.max_assignments,
        rebuild_assignments=args.rebuild_assignments,
    )
