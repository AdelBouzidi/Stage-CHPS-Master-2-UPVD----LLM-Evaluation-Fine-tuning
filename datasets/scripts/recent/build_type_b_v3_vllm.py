#!/usr/bin/env python3
"""
Build Type B dataset — V2 final pipeline.

Final Type B format:
  instruction = error signal + buggy code
  output      = clean corrected code

Main improvements:
- clean runtime errors
- clean compile errors
- truncate noisy ineq outputs
- exclude weak ineq patterns
- assign Type B axes from injected pattern, not from Type A axes
"""

import os, json, sys, re, time, random, argparse, tempfile, subprocess, logging, requests
from pathlib import Path
from datetime import datetime
from collections import Counter

DEFAULT_MODEL = "gpt-oss:120b"
DEFAULT_BASE_URL = "http://localhost:8082"

COMPILE_TIMEOUT = 20
RUN_TIMEOUT = 15
MAX_LLM_RETRIES = 2
GFORTRAN_FLAGS = ["-O0", "-ffree-line-length-none", "-w", "-fcheck=bounds"]

MAX_COMPILE_ERRORS_IN_INSTRUCTION = 5
MAX_INEQ_OUTPUT_LINES = 15
MAX_INEQ_FULL_OUTPUT_LINES = 30
MAX_INEQ_FULL_OUTPUT_CHARS = 3000
MAX_DIFF_BLOCKS = 3
DIFF_CONTEXT_LINES = 1


WEAK_INEQ_PATTERNS = {
    "extra_output_elements",
    "missing_output_elements",
    "missing_output_line",
    "output_format_mismatch",
    "whitespace_mismatch",
    "bool_output_mismatch",
}

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
    "missing_main_program": "syntax",
    "syntax_error": "syntax",
    "syntax_missing_end": "syntax",
    "syntax_missing_parenthesis": "syntax",
    "type_mismatch": "syntax",
    "undeclared_variable": "syntax",

    # runtime
    "array_bounds_runtime": "runtime",
    "division_by_zero": "runtime",
    "floating_point_exception": "runtime",
    "integer_overflow": "runtime",
    "segmentation_fault": "runtime",
    "unallocated_access": "runtime",
    "allocation_runtime_error": "runtime",

    # logic / numerical
    "wrong_numeric_result": "logic",
    "off_by_one_error": "logic",
    "wrong_loop_bounds": "logic",
    "wrong_index_base": "logic",
    "incorrect_condition": "logic",
    "comparison_operator_swap": "logic",
    "wrong_update_rule": "logic",
    "accumulation_error": "logic",
    "precision_loss": "numerical",
    "convergence_error": "numerical",
    "edge_case_failure": "logic",
}

PATTERN_SPECIFIC_HINTS = {
    "implicit_none_missing": """
Do not only remove 'implicit none'.
Create a real undeclared-variable compile error.
""",

    "division_by_zero": """
Force a real integer division-by-zero executed at runtime.
Avoid floating-point Infinity-only behavior.
""",

    "floating_point_exception": """
Force a real runtime arithmetic failure.
Avoid silent NaN/Infinity generation.
""",

    "allocation_runtime_error": """
Force a real invalid allocation or allocatable misuse that crashes at runtime.
""",

    "unallocated_access": """
Force a real access to an unallocated allocatable array.
""",

    "integer_overflow": """
Prefer overflow leading to invalid indexing or runtime failure.
""",

    "precision_loss": """
Introduce visible numerical precision degradation in printed output.
""",

    "wrong_loop_bounds": """
Modify a computation loop bound that changes numerical results.
""",

    "wrong_index_base": """
Modify indexing while remaining in-bounds so the program still runs.
""",

    "off_by_one_error": """
Introduce a realistic off-by-one error affecting computation.
""",

    "incorrect_condition": """
Modify an important algorithmic condition.
""",

    "comparison_operator_swap": """
Swap a comparison operator in meaningful logic.
""",

    "wrong_update_rule": """
Modify an important numerical update rule.
""",
}


import threading
from requests.adapters import HTTPAdapter

# Shared HTTP session + bounded concurrency limiter, configured once.
_SESSION = None
_SEMAPHORE = None
_CLIENT_LOCK = threading.Lock()


def init_llm_client(max_concurrency, pool_maxsize=None):
    """Initialize a shared requests.Session and a bounded semaphore.

    Must be called once before any (possibly concurrent) call_llm calls.
    The connection pool is sized to match concurrency so threads don't
    block waiting for a free connection.
    """
    global _SESSION, _SEMAPHORE
    with _CLIENT_LOCK:
        if _SESSION is None:
            pool = pool_maxsize or max(10, max_concurrency)
            session = requests.Session()
            adapter = HTTPAdapter(
                pool_connections=pool,
                pool_maxsize=pool,
                max_retries=0,  # retries handled in try_inject_pattern
            )
            session.mount("http://", adapter)
            session.mount("https://", adapter)
            _SESSION = session
        if _SEMAPHORE is None:
            _SEMAPHORE = threading.BoundedSemaphore(max_concurrency)


            
def setup_logging(log_file):
    logger = logging.getLogger("type_b")
    logger.setLevel(logging.INFO)
    if logger.handlers:
        logger.handlers.clear()

    os.makedirs(os.path.dirname(log_file) or ".", exist_ok=True)

    fh = logging.FileHandler(log_file, mode="a", encoding="utf-8")
    fh.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))

    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(logging.Formatter("%(message)s"))

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


log = logging.getLogger("type_b")


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


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


def call_llm(system_prompt, user_prompt, model, base_url, api_key=None,
             temperature=0.2, max_tokens=2048, timeout=1200,
             endpoint="/v1/chat/completions"):

    # Lazy single-flight fallback if the caller forgot to init.
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

    # Concurrency control: never exceed max_concurrency in-flight requests.
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





INJECTION_SYSTEM = """You are an expert Fortran bug injection system.

Your task: inject EXACTLY ONE bug of type "{pattern_name}" ({error_type}) into the provided Fortran code.

Rules:
- The bug must cause a {expected_behavior}.
- Keep the code realistic and structurally identical.
- Do NOT add comments explaining the bug.
- Do NOT add or remove READ/WRITE/PRINT statements.
- Do NOT change the program name or subroutine names.
- Output ONLY the full modified Fortran source code, no explanation.
- Do NOT wrap the code in markdown fences.
"""

EXPECTED_BEHAVIORS = {
    "compile_err": "compilation error, so gfortran must reject the code",
    "runtime_err": "runtime crash, such as array bounds error, segmentation fault, floating point exception, or non-zero exit code",
    "ineq": "wrong output, so the program must compile and run but produce different results",
}


def build_injection_prompt(code, pattern_name, error_type):
    expected = EXPECTED_BEHAVIORS.get(error_type, "detectable error")

    pattern_hint = PATTERN_SPECIFIC_HINTS.get(
        pattern_name,
        "Ensure the injected bug really produces the requested behavior."
    )

    system = INJECTION_SYSTEM.format(
        pattern_name=pattern_name,
        error_type=error_type,
        expected_behavior=expected,
    )

    system += "\n\nPattern-specific guidance:\n" + pattern_hint.strip()

    return system, code


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


def compile_fortran(src_path, exe_path):
    return subprocess.run(
        ["gfortran"] + GFORTRAN_FLAGS + [src_path, "-o", exe_path],
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
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=RUN_TIMEOUT,
        text=True,
        env=env,
    )


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

INEQ_IGNORE_MARKERS = [
    "elapsed time",
    "execution time",
    "cpu time",
    "mflops",
    "seconds",
]


def _has_crash_markers(stderr):
    s = (stderr or "").lower()
    return any(m in s for m in RUNTIME_CRASH_MARKERS)


def _has_spurious_markers(stderr):
    s = (stderr or "").lower()
    return any(m in s for m in SPURIOUS_RUNTIME_MARKERS)


def normalize_stdout(text):
    if not text:
        return ""

    normalized = []

    for line in text.strip().splitlines():
        cleaned = re.sub(r"\s+", " ", line.strip())

        if not cleaned:
            continue

        low = cleaned.lower()

        if any(marker in low for marker in INEQ_IGNORE_MARKERS):
            continue

        normalized.append(cleaned)

    return "\n".join(normalized)


def truncate_lines(text, max_lines=15):
    if not text:
        return ""

    lines = text.strip().splitlines()

    if len(lines) <= max_lines:
        return "\n".join(lines).strip()

    kept = lines[:max_lines]
    kept.append(f"... [truncated: {len(lines) - max_lines} more lines]")

    return "\n".join(kept).strip()


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


def clean_output_for_instruction(text):
    if not text:
        return ""

    cleaned = []

    timestamp_patterns = [
        r"^\d{1,2}\s+[A-Za-z]+\s+\d{4}.*$",
        r"^Timestamp:\s*\d{8}\s+\d+.*$",
    ]

    for line in text.strip().splitlines():
        raw = line.rstrip()
        low = raw.lower().strip()

        if any(re.match(p, raw.strip()) for p in timestamp_patterns):
            continue

        if any(marker in low for marker in INEQ_IGNORE_MARKERS):
            continue

        cleaned.append(raw)

    return "\n".join(cleaned).strip()



def is_short_clean_output(expected, actual):
    expected_clean = clean_output_for_instruction(expected)
    actual_clean = clean_output_for_instruction(actual)

    total_lines = len(expected_clean.splitlines()) + len(actual_clean.splitlines())
    total_chars = len(expected_clean) + len(actual_clean)

    if total_lines <= MAX_INEQ_FULL_OUTPUT_LINES and total_chars <= MAX_INEQ_FULL_OUTPUT_CHARS:
        return True

    return False


def build_output_diff(expected, actual, max_blocks=8, context=1):
    expected_lines = clean_output_for_instruction(expected).splitlines()
    actual_lines = clean_output_for_instruction(actual).splitlines()

    max_len = max(len(expected_lines), len(actual_lines))
    diff_indices = []

    for i in range(max_len):
        e = expected_lines[i] if i < len(expected_lines) else "<missing>"
        a = actual_lines[i] if i < len(actual_lines) else "<missing>"

        if re.sub(r"\s+", " ", e.strip()) != re.sub(r"\s+", " ", a.strip()):
            diff_indices.append(i)

    if not diff_indices:
        return "No textual difference remained after normalization, but raw program output differed."

    blocks = []
    used = set()

    for idx in diff_indices:
        if len(blocks) >= max_blocks:
            break
        if idx in used:
            continue

        start = max(0, idx - context)
        end = min(max_len, idx + context + 1)

        for j in range(start, end):
            used.add(j)

        block = [f"Difference around output line {idx + 1}:"]

        for j in range(start, end):
            e = expected_lines[j] if j < len(expected_lines) else "<missing>"
            a = actual_lines[j] if j < len(actual_lines) else "<missing>"

            if re.sub(r"\s+", " ", e.strip()) == re.sub(r"\s+", " ", a.strip()):
                block.append(f"  Context : {e}")
            else:
                block.append(f"  Expected: {e}")
                block.append(f"  Actual  : {a}")

        blocks.append("\n".join(block))

    remaining = len(diff_indices) - len(blocks)
    if remaining > 0:
        blocks.append(f"... [truncated: {remaining} more differing regions]")

    return "\n\n".join(blocks).strip()


def validate_behavior(error_type, compile_result, run_result, ref_stdout):
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

    if error_type == "ineq":
        if run_result is None or run_result.returncode != 0:
            return False

        return normalize_stdout(run_result.stdout) != normalize_stdout(ref_stdout)

    return False


def build_type_b_instruction(error_type, buggy_code, compile_stderr="", run_stderr="",
                             expected_output=None, actual_output=None, output_diff=None,
                             ineq_signal_mode="expected_actual"):

    if error_type == "compile_err":
        return (
            "The following Fortran 90 code fails to compile with this error:\n\n"
            f"{compile_stderr.strip()}\n\n"
            "Fix the code:\n\n"
            f"{buggy_code.strip()}"
        )

    if error_type == "runtime_err":
        return (
            "The following Fortran 90 code compiles successfully but crashes at runtime with:\n\n"
            f"{run_stderr.strip()}\n\n"
            "Fix the code:\n\n"
            f"{buggy_code.strip()}"
        )

    if error_type == "ineq":
        if ineq_signal_mode == "diff":
            return (
                "The following Fortran 90 code compiles and runs but produces incorrect results.\n\n"
                "Observed output difference:\n"
                f"{(output_diff or '').strip()}\n\n"
                "Fix the code:\n\n"
                f"{buggy_code.strip()}"
            )

        return (
            "The following Fortran 90 code compiles and runs but produces incorrect results.\n\n"
            "Expected output:\n"
            f"{(expected_output or '').strip()}\n\n"
            "Actual output:\n"
            f"{(actual_output or '').strip()}\n\n"
            "Fix the code:\n\n"
            f"{buggy_code.strip()}"
        )

    return (
        "The following Fortran 90 code contains an error.\n\n"
        "Fix the code:\n\n"
        f"{buggy_code.strip()}"
    )

def get_type_b_axes(pattern_name, target_group):
    primary = PATTERN_AXIS_MAP.get(pattern_name)

    if primary is None:
        if target_group == "compile_err":
            primary = "syntax"
        elif target_group == "runtime_err":
            primary = "runtime"
        elif target_group == "ineq":
            primary = "logic"
        else:
            primary = "logic"

    secondary = []

    if target_group == "compile_err" and primary != "syntax":
        secondary.append("syntax")

    if target_group == "runtime_err" and primary != "runtime":
        secondary.append("runtime")

    if target_group == "ineq" and primary != "logic":
        secondary.append("logic")

    return primary, secondary


def try_inject_pattern(code, pattern_name, error_type, ref_stdout,
                       model, base_url, api_key):

    system_prompt, user_prompt = build_injection_prompt(code, pattern_name, error_type)

    raw_response = None
    last_error = None

    for attempt in range(1, MAX_LLM_RETRIES + 1):
        try:
            raw_response = call_llm(
                system_prompt,
                user_prompt,
                model,
                base_url,
                api_key,
                temperature=0.2,
                max_tokens=2048,
                timeout=1200,
            )
            break

        except Exception as e:
            last_error = e
            if attempt < MAX_LLM_RETRIES:
                time.sleep(2)

    if raw_response is None:
        return {
            "pattern_name": pattern_name,
            "error_type": error_type,
            "validation_success": False,
            "failure_reason": f"llm_error: {last_error}",
        }

    injected_code = extract_code(raw_response)

    if injected_code.strip() == code.strip():
        return {
            "pattern_name": pattern_name,
            "error_type": error_type,
            "validation_success": False,
            "failure_reason": "injected_code_identical_to_original",
        }

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            src_path = str(Path(tmpdir) / "test.f90")
            exe_path = str(Path(tmpdir) / "a.out")

            Path(src_path).write_text(injected_code, encoding="utf-8")

            compile_result = compile_fortran(src_path, exe_path)
            run_result = None

            if compile_result.returncode == 0 and error_type in ("runtime_err", "ineq"):
                try:
                    run_result = run_executable(exe_path)
                except subprocess.TimeoutExpired:
                    run_result = type(
                        "R",
                        (),
                        {"returncode": -1, "stdout": "", "stderr": "TIMEOUT"},
                    )()

            valid = validate_behavior(error_type, compile_result, run_result, ref_stdout)

            result = {
                "pattern_name": pattern_name,
                "error_type": error_type,
                "validation_success": valid,
                "injected_code": injected_code,
                "compile_returncode": compile_result.returncode,
                "compile_stdout": compile_result.stdout or "",
                "compile_stderr": clean_compile_error(
                    compile_result.stderr or "",
                    max_errors=MAX_COMPILE_ERRORS_IN_INSTRUCTION,
                ),
            }

            if run_result is not None:
                result["run_returncode"] = run_result.returncode
                result["run_stdout"] = run_result.stdout or ""
                result["run_stderr"] = run_result.stderr or ""

            if not valid:
                if error_type == "compile_err" and compile_result.returncode == 0:
                    result["failure_reason"] = "code_compiled_when_it_should_not"

                elif error_type == "runtime_err" and run_result and run_result.returncode == 0:
                    result["failure_reason"] = "ran_successfully_when_should_crash"

                elif error_type == "runtime_err" and run_result and run_result.returncode != 0 and _has_spurious_markers(run_result.stderr):
                    result["failure_reason"] = "spurious_io_artifact"

                elif error_type == "ineq" and run_result:
                    if normalize_stdout(run_result.stdout) == normalize_stdout(ref_stdout):
                        result["failure_reason"] = "output_unchanged"
                    else:
                        result["failure_reason"] = "unexpected_behavior"

                else:
                    result["failure_reason"] = "validation_failed"

            return result

    except Exception as e:
        return {
            "pattern_name": pattern_name,
            "error_type": error_type,
            "validation_success": False,
            "failure_reason": f"compile_run_error: {e}",
        }


def process_assignment(assignment, code, model, base_url, api_key):
    origin_id = assignment["origin_id"]
    target_group = assignment["target_group"]

    candidate_patterns = list(assignment["candidate_patterns"])

    # Skip weak ineq patterns before spending LLM calls.
    # if target_group == "ineq":
    #    candidate_patterns = [
    #        p for p in candidate_patterns
    #        if p not in WEAK_INEQ_PATTERNS
    #    ]

    random.shuffle(candidate_patterns)

    target_successes = assignment.get("target_successes", 1)
    ref_stdout = assignment.get("run_stdout", "") or ""

    successes = []
    failures = []

    if not candidate_patterns:
        return [], [{
            "pattern_name": None,
            "failure_reason": "no_candidate_patterns_after_filtering",
        }]

    for pattern_name in candidate_patterns:
        if len(successes) >= target_successes:
            break

        result = try_inject_pattern(
            code=code,
            pattern_name=pattern_name,
            error_type=target_group,
            ref_stdout=ref_stdout,
            model=model,
            base_url=base_url,
            api_key=api_key,
        )

        if result["validation_success"]:
            buggy_code = result["injected_code"]

            compiler_output = None
            runtime_error = None
            expected_output = None
            actual_output = None
            output_diff = None
            ineq_signal_mode = None
            signal_type = None
            observed_group = target_group

            if target_group == "compile_err":
                compiler_output = result.get("compile_stderr", "")
                signal_type = "compiler_message"

            elif target_group == "runtime_err":
                runtime_error = clean_runtime_error(result.get("run_stderr", ""))
                signal_type = "runtime_crash"

            elif target_group == "ineq":
                expected_clean = clean_output_for_instruction(ref_stdout)
                actual_clean = clean_output_for_instruction(result.get("run_stdout", ""))

                if is_short_clean_output(expected_clean, actual_clean):
                    # Cas simple : on garde le format classique The Stack V1
                    expected_output = expected_clean
                    actual_output = actual_clean
                    output_diff = None
                    ineq_signal_mode = "expected_actual"

                else:
                    # Cas long/bruité : on garde seulement les différences utiles
                    expected_output = None
                    actual_output = None

                    output_diff = build_output_diff(
                        expected_clean,
                        actual_clean,
                        max_blocks=MAX_DIFF_BLOCKS,
                        context=DIFF_CONTEXT_LINES,
                    )

                    if output_diff.startswith("No textual difference remained"):
                        failures.append({
                            "pattern_name": pattern_name,
                            "failure_reason": "no_useful_output_diff_after_cleaning",
                        })
                        continue

                    ineq_signal_mode = "diff"

                signal_type = "output_diff"
            

            primary_axis, secondary_axes = get_type_b_axes(pattern_name, target_group)

            instruction = build_type_b_instruction(
                error_type=target_group,
                buggy_code=buggy_code,
                compile_stderr=compiler_output or "",
                run_stderr=runtime_error or "",
                expected_output=expected_output,
                actual_output=actual_output,
                output_diff=output_diff,
                ineq_signal_mode=ineq_signal_mode or "expected_actual",
            )

            entry = {
                "type": "B",
                "source_origin_id": origin_id,
                "instruction": instruction,
                "output": code,
                "primary_axis": primary_axis,
                "secondary_axes": secondary_axes,
                "metadata": {
                    "target_pattern": pattern_name,
                    "target_group": target_group,
                    "observed_group": observed_group,
                    "pattern_match_status": "group_only",
                    "signal_type": signal_type,
                    "num_attempts": 1,

                    "compiler_output": compiler_output,
                    "runtime_error": runtime_error,

                    "expected_output": expected_output,
                    "actual_output": actual_output,

                    "output_diff": output_diff,
                    "ineq_signal_mode": ineq_signal_mode,

                    "compile_returncode": result.get("compile_returncode"),
                    "run_returncode": result.get("run_returncode"),
                },
            }

            successes.append(entry)

        else:
            failures.append({
                "pattern_name": pattern_name,
                "failure_reason": result.get("failure_reason", "unknown"),
            })

    return successes, failures

from concurrent.futures import ThreadPoolExecutor, as_completed


def build_type_b(assignments_path, faithful_path, type_a_path,
                 output_path, errors_path, model, base_url,
                 api_key, sleep_sec, log_file, max_concurrency=8):

    setup_logging(log_file)
    init_llm_client(max_concurrency)

    log.info("=" * 60)
    log.info(f"TYPE B BUILD V2 (vLLM, concurrency={max_concurrency}) — "
             f"{datetime.now():%Y-%m-%d %H:%M:%S}")
    log.info("=" * 60)

    assignments = load_json(assignments_path)
    faithful = load_json(faithful_path)
    faithful_lookup = build_lookup(faithful, "origin_id")

    dataset, all_errors = [], []
    if os.path.exists(output_path):
        try: dataset = load_json(output_path)
        except Exception: dataset = []
    if os.path.exists(errors_path):
        try: all_errors = load_json(errors_path)
        except Exception: all_errors = []

    done_ids = {item.get("source_origin_id") or item.get("origin_id")
                for item in dataset}
    done_ids.discard(None)

    remaining = [a for a in assignments if a["origin_id"] not in done_ids]
    log.info(f"Remaining: {len(remaining)} | Model: {model}")
    if not remaining:
        log.info("Nothing to process.")
        return

    write_lock = threading.Lock()
    counter = {"done": 0, "succ": 0, "fail": 0, "next_id": len(dataset) + 1}
    run_start = time.time()

    def worker(assignment):
        oid = assignment["origin_id"]
        entry = faithful_lookup.get(oid)
        if not entry:
            return oid, [], [{"pattern_name": None, "failure_reason": "code_not_found"}]
        code = entry.get("generated_code", "")
        if not code:
            return oid, [], [{"pattern_name": None, "failure_reason": "empty_code"}]
        successes, failures = process_assignment(
            assignment=assignment, code=code, model=model,
            base_url=base_url, api_key=api_key,
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
                log.error(f"  oid={oid}: worker crashed: {e}")
                continue

            with write_lock:
                for s in successes:
                    s["id"] = f"type_b_{counter['next_id']:04d}"
                    counter["next_id"] += 1
                    dataset.append(s)
                if failures:
                    all_errors.append({
                        "origin_id": oid,
                        "target_group": assignment["target_group"],
                        "failures": failures,
                    })
                counter["done"] += 1
                counter["succ"] += len(successes)
                counter["fail"] += len(failures)
                d = counter["done"]

                # Checkpoint periodically (every item is also fine, just chattier).
                if d % 10 == 0 or d == len(remaining):
                    save_json(output_path, dataset)
                    save_json(errors_path, all_errors)

            elapsed = time.time() - run_start
            eta = elapsed / d * (len(remaining) - d) / 60 if d else 0
            log.info(f"[{d}/{len(remaining)}] oid={oid:>4d} "
                     f"✓{len(successes)} ✗{len(failures)} ETA {eta:.0f}min")

    with write_lock:
        save_json(output_path, dataset)
        save_json(errors_path, all_errors)

    log.info(f"DONE — {counter['succ']} successes, {counter['fail']} failures, "
             f"{(time.time() - run_start) / 60:.1f} min")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Build Type B dataset — inject bugs and validate"
    )

    parser.add_argument("--assignments", required=True)
    parser.add_argument("--faithful", required=True)
    parser.add_argument("--type-a-dataset", required=True)

    parser.add_argument("--output", default="dataset/type_b_v2/type_b_v2_dataset.json")
    parser.add_argument("--errors-output", default="dataset/type_b_v2/type_b_v2_errors.json")

    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--concurrency", type=int, default=10)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--api-key", default=None)
    parser.add_argument("--sleep", type=float, default=0.5)
    parser.add_argument("--log-file", default="dataset/type_b_v2/type_b_v2_build.log")

    args = parser.parse_args()

    build_type_b(
        assignments_path=args.assignments,
        faithful_path=args.faithful,
        type_a_path=args.type_a_dataset,
        output_path=args.output,
        errors_path=args.errors_output,
        model=args.model,
        base_url=args.base_url,
        api_key=args.api_key or os.environ.get("OPENWEBUI_API_KEY"),
        sleep_sec=args.sleep,
        log_file=args.log_file,
        max_concurrency=args.concurrency,
    )