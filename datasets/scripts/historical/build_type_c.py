"""
Pipeline Type C — Correction autonome (sans signal).

Le modèle reçoit un code buggé SANS indication sur l'erreur.
Il doit diagnostiquer et corriger seul.

Améliorations :
  - type_c_assignments.json pour tracer les décisions de planification
  - pattern_match_status dans les metadata (cohérent avec Type B)
  - type_b_groups dans les erreurs pour faciliter le debug
  - --retry-errors : option pour retenter les codes échoués

Règles :
  - Groupe différent de celui utilisé en Type B pour le même code
  - Uniquement compile_err et runtime_err (ineq exclu)
  - Validation comportementale identique à Type B
  - Aucun signal dans l'instruction
  - 6 formulations d'instruction, choix déterministe (origin_id % 6)
  - Signal caché dans metadata (prefixé hidden_) pour analyse post-training
  - Codes sans Type B : éligibles sans exclusion de groupe
  - Cap de 10 par pattern (séparé du cap Type B)

Input :
  - dataset_base_clean_codes.json (codes sources)
  - type_b_dataset.json (pour connaître les groupes utilisés)

Output :
  - dataset/type_c/type_c_dataset.json
  - dataset/type_c/type_c_assignments.json
  - dataset/type_c/type_c_errors.json
  - dataset/type_c/type_c_build.log
"""

import json
import requests
import subprocess
import argparse
import os
import re
import sys
import time
import uuid
import logging
from datetime import datetime
from collections import Counter
from typing import Dict, Any, List, Optional, Tuple, Set


# =============================================================================
#                          TAXONOMIE
# =============================================================================

TAXONOMY = {
    "compile_err": [
        "allocation_error", "character_length_mismatch", "contains_section_error",
        "data_attribute_conflict", "implicit_none_missing", "intent_violation",
        "invalid_array_bounds", "invalid_dummy_argument", "invalid_token_or_name",
        "missing_interface_block", "missing_main_program", "module_use_error",
        "pointer_declaration_error", "subroutine_function_mismatch", "syntax_error",
        "syntax_invalid_condition", "syntax_invalid_expression", "syntax_invalid_write",
        "syntax_loop_error", "syntax_missing_end", "syntax_missing_parenthesis",
        "syntax_missing_then", "syntax_unexpected_statement", "type_mismatch",
        "undeclared_type", "undeclared_variable", "undefined_reference",
        "wrong_kind_specifier",
    ],
    "runtime_err": [
        "allocation_runtime_error", "array_bounds_runtime", "division_by_zero",
        "eof_input", "floating_point_exception", "integer_overflow",
        "interactive_prompt_leak", "invalid_numeric_input", "malloc_corruption",
        "segmentation_fault", "stdin_format_mismatch", "unallocated_access",
    ],
}

PATTERN_TO_GROUP: Dict[str, str] = {}
for g, pats in TAXONOMY.items():
    for p in pats:
        PATTERN_TO_GROUP[p] = g

ALLOWED_C_GROUPS = {"compile_err", "runtime_err"}

RUNTIME_IO_PATTERNS = {
    "eof_input", "interactive_prompt_leak",
    "stdin_format_mismatch", "invalid_numeric_input",
}

SPURIOUS_CRASH_MARKERS = [
    "end of file", "eof", "input/output",
    "unit 5", "read(unit=5",
    "recursive i/o", "no such file",
]


# =============================================================================
#                    INSTRUCTION TEMPLATES (6 variantes)
# =============================================================================

INSTRUCTION_TEMPLATES = [
    "The following Fortran 90 code contains a bug. Find and fix it.\n\n{code}",
    "Debug the following Fortran 90 program.\n\n{code}",
    "This Fortran 90 program does not work correctly. Identify and correct the error.\n\n{code}",
    "Fix the bug in this Fortran 90 code.\n\n{code}",
    "The following Fortran 90 code has an error. Correct it.\n\n{code}",
    "Find and fix the issue in this Fortran 90 program.\n\n{code}",
]


def build_type_c_instruction(buggy_code: str, origin_id: int) -> str:
    template = INSTRUCTION_TEMPLATES[origin_id % len(INSTRUCTION_TEMPLATES)]
    return template.format(code=buggy_code)


# =============================================================================
#                          LOGGING
# =============================================================================

def setup_logging(log_file: str):
    logger = logging.getLogger("type_c")
    logger.setLevel(logging.INFO)
    if logger.handlers:
        logger.handlers.clear()
    os.makedirs(os.path.dirname(log_file) or ".", exist_ok=True)

    fh = logging.FileHandler(log_file, mode="a", encoding="utf-8")
    fh.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-7s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


log = logging.getLogger("type_c")


# =============================================================================
#                    OPENWEBUI CLIENT
# =============================================================================

def call_openwebui(
    system_prompt: str, user_prompt: str,
    model: str, base_url: str,
    api_key: Optional[str] = None,
    temperature: float = 0.3,
    max_tokens: int = 2048,
    timeout: int = 180,
) -> str:
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    endpoints = ["/api/chat/completions", "/v1/chat/completions",
                 "/ollama/v1/chat/completions"]
    errors = []
    for ep in endpoints:
        try:
            resp = requests.post(
                f"{base_url}{ep}", headers=headers,
                json={"model": model, "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ], "temperature": temperature, "max_tokens": max_tokens,
                   "stream": False}, timeout=timeout)
            if resp.status_code == 200:
                result = resp.json()
                if "choices" in result and result["choices"]:
                    return result["choices"][0]["message"]["content"].strip()
                if "message" in result and isinstance(result["message"], dict):
                    return result["message"].get("content", "").strip()
                if "response" in result:
                    return str(result["response"]).strip()
            errors.append(f"{ep}: HTTP {resp.status_code}")
        except Exception as e:
            errors.append(f"{ep}: {e}")
    raise RuntimeError("All endpoints failed:\n" + "\n".join(errors))


# =============================================================================
#                    JSON I/O
# =============================================================================

def load_input_json(path: str) -> List[Dict[str, Any]]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list) or len(data) == 0:
        raise ValueError(f"{path} must be a non-empty JSON list")
    return data


def load_output_json(path: str) -> List[Dict[str, Any]]:
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError):
        return []


def save_json(path: str, data: Any):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    tmp = path + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(tmp, path)
    except Exception:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


# =============================================================================
#                    FORTRAN COMPILATION & EXECUTION
# =============================================================================

WORK_DIR = "/tmp/fortran_inject"


def ensure_work_dir():
    os.makedirs(WORK_DIR, exist_ok=True)


def compile_fortran(code: str) -> Tuple[bool, str, str]:
    ensure_work_dir()
    uid = uuid.uuid4().hex[:12]
    src = os.path.join(WORK_DIR, f"inj_{uid}.f90")
    binary = os.path.join(WORK_DIR, f"inj_{uid}")

    with open(src, "w", encoding="utf-8") as f:
        f.write(code)
    try:
        result = subprocess.run(
            ["gfortran", "-o", binary, src,
             "-ffree-line-length-none", "-w", "-fcheck=bounds"],
            capture_output=True, text=True, timeout=30)
        try:
            os.remove(src)
        except OSError:
            pass
        if result.returncode == 0:
            return True, binary, result.stderr.strip()
        return False, "", result.stderr.strip()
    except subprocess.TimeoutExpired:
        return False, "", "compilation_timeout"
    except Exception as e:
        return False, "", str(e)


def run_fortran(binary_path: str, timeout_sec: int = 10) -> Tuple[bool, str, str, int]:
    try:
        result = subprocess.run(
            [binary_path], input=None,
            capture_output=True, text=True, timeout=timeout_sec,
            env={**os.environ, "GFORTRAN_UNBUFFERED_ALL": "1"})
        return result.returncode == 0, result.stdout, result.stderr.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return False, "", "execution_timeout", -99
    except Exception as e:
        return False, "", str(e), -1
    finally:
        try:
            os.remove(binary_path)
        except OSError:
            pass


def is_spurious_crash(stderr: str, returncode: int) -> bool:
    if returncode == -99:
        return True
    low = stderr.lower()
    return any(m in low for m in SPURIOUS_CRASH_MARKERS)


# =============================================================================
#                    INJECTION (même prompt que Type B)
# =============================================================================

INJECTION_SYSTEM = """You are a Fortran error injection tool.

Given a correct Fortran program and an error pattern name, you must introduce
EXACTLY ONE realistic bug that matches the specified pattern.

STRICT RULES:
1. Modify the code to introduce exactly ONE error matching the pattern.
2. The error must be realistic — something a human programmer could actually make.
3. Do NOT add comments indicating where the error is.
4. Do NOT add explanations before or after the code.
5. Output ONLY the complete modified Fortran code, nothing else.
6. Do NOT wrap the code in markdown backticks.
7. Keep the rest of the program unchanged.
8. The error should be subtle but detectable.
9. Do NOT add or remove READ/WRITE/PRINT statements.
10. Do NOT change the program's I/O structure.
"""

PATTERN_HINTS = {
    "undeclared_variable": "Remove a variable declaration or use a variable that was never declared.",
    "type_mismatch": "Assign a value of the wrong type where it causes a compilation error.",
    "syntax_missing_end": "Remove an END statement (END DO, END IF, END SUBROUTINE, etc.).",
    "syntax_missing_parenthesis": "Remove a closing parenthesis in an expression or function call.",
    "implicit_none_missing": "Remove 'implicit none' AND remove the declaration of one variable so it gets an implicit type. Choose a variable whose implicit type (based on first letter: I-N=integer, else=real) CONFLICTS with how it is actually used in the code.",
    "intent_violation": "Modify an INTENT(IN) argument inside the subroutine.",
    "syntax_error": "Introduce a syntax error (misspell a keyword, wrong operator, etc.).",
    "syntax_unexpected_statement": "Put a statement where it doesn't belong syntactically.",
    "allocation_error": "Use ALLOCATE incorrectly or on a non-allocatable variable.",
    "missing_interface_block": "Call a function with wrong argument types without an interface.",
    "syntax_invalid_expression": "Write an invalid expression (wrong operator precedence, etc.).",
    "syntax_missing_then": "Remove THEN after an IF condition.",
    "syntax_loop_error": "Introduce an error in a DO loop syntax.",
    "division_by_zero": "Make a division where the denominator becomes zero at runtime.",
    "array_bounds_runtime": "Access an array with an index that goes out of bounds at runtime.",
    "segmentation_fault": "Access unallocated memory or dereference a null pointer.",
    "unallocated_access": "Use an allocatable array before it is allocated.",
    "floating_point_exception": "Cause a floating-point exception (overflow, invalid operation).",
    "integer_overflow": "Make an integer computation that overflows.",
    "allocation_runtime_error": "Deallocate an already deallocated variable or allocate an already allocated one.",
}


def build_injection_prompt(code: str, pattern: str, group: str) -> str:
    hint = PATTERN_HINTS.get(pattern, f"Introduce a {pattern} error.")
    behavior = {
        "compile_err": "The modified code must FAIL to compile with gfortran.",
        "runtime_err": "The modified code must compile but CRASH at runtime.",
    }
    return f"""Inject exactly ONE error of type "{pattern}" (group: {group}) into this Fortran program.

Hint: {hint}

{behavior.get(group, "")}

IMPORTANT: Do NOT change any READ, WRITE, or PRINT statements. Do NOT change the I/O structure.

Output ONLY the complete modified Fortran code:

{code}
"""


def extract_fortran_code(text: str) -> str:
    text = text.strip()
    m = re.search(r"```(?:fortran|f90)?\s*\n(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1).strip()
    first_line = text.split("\n")[0].strip().lower()
    if any(first_line.startswith(kw) for kw in
           ["program", "module", "subroutine", "function", "!"]):
        return text
    for i, line in enumerate(text.split("\n")):
        stripped = line.strip().lower()
        if any(stripped.startswith(kw) for kw in
               ["program", "module", "subroutine", "function", "!"]):
            return "\n".join(text.split("\n")[i:]).strip()
    return text


# =============================================================================
#                    VALIDATION COMPORTEMENTALE
# =============================================================================

def validate_injection(
    buggy_code: str,
    target_group: str,
    target_pattern: str,
) -> Tuple[bool, str, Dict[str, Any]]:
    meta: Dict[str, Any] = {
        "target_pattern": target_pattern,
        "target_group": target_group,
    }

    compiled, binary, compile_stderr = compile_fortran(buggy_code)

    if target_group == "compile_err":
        if not compiled:
            meta["hidden_compiler_output"] = compile_stderr[:500]
            meta["observed_group"] = "compile_err"
            meta["pattern_match_status"] = "group_only"
            return True, "compile_failed_as_expected", meta
        try:
            os.remove(binary)
        except OSError:
            pass
        meta["observed_group"] = "no_effect"
        meta["pattern_match_status"] = "group_mismatch"
        return False, "compile_unexpected_success", meta

    if not compiled:
        meta["observed_group"] = "compile_err"
        meta["hidden_compiler_output"] = compile_stderr[:200]
        meta["pattern_match_status"] = "group_mismatch"
        return False, "compile_unexpected_failure", meta

    ran_ok, stdout, run_stderr, returncode = run_fortran(binary)

    if target_group == "runtime_err":
        if not ran_ok:
            if is_spurious_crash(run_stderr, returncode):
                meta["observed_group"] = "spurious_crash"
                meta["hidden_runtime_error"] = run_stderr[:300]
                meta["pattern_match_status"] = "spurious"
                return False, "runtime_spurious_crash", meta
            meta["hidden_runtime_error"] = run_stderr[:500]
            meta["observed_group"] = "runtime_err"
            meta["pattern_match_status"] = "group_only"
            return True, "runtime_crash_as_expected", meta
        meta["observed_group"] = "no_effect"
        meta["pattern_match_status"] = "group_mismatch"
        return False, "runtime_missing_crash", meta

    meta["pattern_match_status"] = "group_mismatch"
    return False, f"unknown_group_{target_group}", meta


# =============================================================================
#                    AXES
# =============================================================================

GROUP_TO_PRIMARY_AXIS = {"compile_err": "syntax", "runtime_err": "logic"}

PATTERN_TO_AXIS = {
    "allocation_error": "syntax", "character_length_mismatch": "syntax",
    "contains_section_error": "syntax", "data_attribute_conflict": "syntax",
    "implicit_none_missing": "syntax", "intent_violation": "syntax",
    "invalid_array_bounds": "syntax", "invalid_dummy_argument": "syntax",
    "invalid_token_or_name": "syntax", "missing_interface_block": "syntax",
    "missing_main_program": "syntax", "module_use_error": "syntax",
    "pointer_declaration_error": "syntax", "subroutine_function_mismatch": "syntax",
    "syntax_error": "syntax", "syntax_invalid_condition": "syntax",
    "syntax_invalid_expression": "syntax", "syntax_invalid_write": "syntax",
    "syntax_loop_error": "syntax", "syntax_missing_end": "syntax",
    "syntax_missing_parenthesis": "syntax", "syntax_missing_then": "syntax",
    "syntax_unexpected_statement": "syntax", "type_mismatch": "syntax",
    "undeclared_type": "syntax", "undeclared_variable": "syntax",
    "undefined_reference": "syntax", "wrong_kind_specifier": "syntax",
    "allocation_runtime_error": "logic", "array_bounds_runtime": "logic",
    "division_by_zero": "logic", "floating_point_exception": "logic",
    "integer_overflow": "logic", "malloc_corruption": "logic",
    "segmentation_fault": "logic", "unallocated_access": "logic",
}


def compute_axes(pattern: str, group: str, rec: Dict[str, Any]) -> Tuple[str, List[str]]:
    primary = PATTERN_TO_AXIS.get(pattern, GROUP_TO_PRIMARY_AXIS.get(group, "syntax"))
    secondary: Set[str] = set()
    code = (rec.get("generated_code", "") or "").lower()
    features = rec.get("features", {})
    if "read(" in code or "open(" in code or "write(" in code or "format(" in code:
        secondary.add("io")
    if "!$omp" in code or "!$acc" in code or "!$claw" in code:
        secondary.add("parallel")
    if features.get("num_loops", 0) > 0 or features.get("num_ifs", 0) > 0:
        secondary.add("logic")
    secondary.discard(primary)
    return primary, sorted(secondary)


# =============================================================================
#                    POST-PROCESSING
# =============================================================================

def clean_output_code(code: str) -> str:
    lines = code.split("\n")
    cleaned = []
    for line in lines:
        stripped = line.strip().lower()
        if stripped.startswith("! { dg-") or stripped.startswith("! { scan-"):
            continue
        if "dg-do" in stripped or "dg-final" in stripped:
            continue
        cleaned.append(line)
    return "\n".join(cleaned)


# =============================================================================
#                    PLANNING
# =============================================================================

def get_type_b_groups(type_b_path: str) -> Dict[int, Set[str]]:
    """Lit type_b_dataset.json et retourne {origin_id: {groupes utilisés}}."""
    type_b = load_output_json(type_b_path)
    b_groups: Dict[int, Set[str]] = {}
    for item in type_b:
        oid = item.get("source_origin_id")
        group = item.get("metadata", {}).get("target_group")
        if oid is not None and group:
            b_groups.setdefault(oid, set()).add(group)
    return b_groups


def get_available_c_patterns(rec: Dict[str, Any], excluded_groups: Set[str]) -> Dict[str, List[str]]:
    """Retourne les patterns disponibles pour Type C, excluant les groupes de Type B."""
    result: Dict[str, List[str]] = {}
    for p in rec.get("applicable_patterns", []):
        g = PATTERN_TO_GROUP.get(p)
        if not g or g not in ALLOWED_C_GROUPS:
            continue
        if g in excluded_groups:
            continue
        if p in RUNTIME_IO_PATTERNS:
            continue
        result.setdefault(g, []).append(p)
    return result


def plan_type_c(
    data: List[Dict[str, Any]],
    b_groups: Dict[int, Set[str]],
    max_per_pattern: int = 10,
) -> List[Dict[str, Any]]:
    """Planifie les assignations Type C."""
    global_pattern_counts: Counter = Counter()
    global_group_counts: Counter = Counter()
    plans: List[Dict[str, Any]] = []

    for rec in data:
        origin_id = rec.get("origin_id")
        excluded = b_groups.get(origin_id, set())

        avail = get_available_c_patterns(rec, excluded)

        if not avail:
            plans.append({
                "origin_id": origin_id,
                "group_c": None,
                "pattern_c": None,
                "type_b_groups": sorted(excluded),
                "skip_reason": "no_available_c_group",
            })
            continue

        # Essayer les groupes par ordre de représentation croissante
        sorted_groups = sorted(avail.keys(), key=lambda g: global_group_counts[g])

        chosen_group = None
        chosen_pattern = None

        for try_group in sorted_groups:
            pats = avail[try_group]
            sorted_pats = sorted(pats, key=lambda p: global_pattern_counts[p])
            eligible = [p for p in sorted_pats
                        if global_pattern_counts[p] < max_per_pattern]
            if eligible:
                chosen_group = try_group
                chosen_pattern = eligible[0]
                break

        if not chosen_pattern:
            plans.append({
                "origin_id": origin_id,
                "group_c": None,
                "pattern_c": None,
                "type_b_groups": sorted(excluded),
                "skip_reason": "all_patterns_at_cap",
            })
            continue

        global_group_counts[chosen_group] += 1
        global_pattern_counts[chosen_pattern] += 1

        plans.append({
            "origin_id": origin_id,
            "group_c": chosen_group,
            "pattern_c": chosen_pattern,
            "type_b_groups": sorted(excluded),
        })

    return plans


# =============================================================================
#                    INJECTION + VALIDATION
# =============================================================================

def inject_and_validate(
    rec: Dict[str, Any],
    pattern: str,
    group: str,
    model: str,
    base_url: str,
    api_key: Optional[str],
    llm_timeout: int,
    max_retries: int = 2,
) -> Tuple[Optional[str], Optional[Dict[str, Any]], int, str]:
    code = rec.get("generated_code", "")

    for attempt in range(1, max_retries + 1):
        try:
            raw = call_openwebui(
                system_prompt=INJECTION_SYSTEM,
                user_prompt=build_injection_prompt(code, pattern, group),
                model=model, base_url=base_url, api_key=api_key,
                temperature=0.3 + (attempt - 1) * 0.1,
                max_tokens=2048, timeout=llm_timeout)

            buggy_code = extract_fortran_code(raw)

            if not buggy_code or len(buggy_code) < 20:
                log.info(f"      attempt {attempt}: llm_output_empty")
                continue
            if buggy_code.strip() == code.strip():
                log.info(f"      attempt {attempt}: buggy_code_identical")
                continue

            valid, reason, meta = validate_injection(buggy_code, group, pattern)

            if valid:
                return buggy_code, meta, attempt, reason
            log.info(f"      attempt {attempt}: {reason}")

        except Exception as e:
            log.warning(f"      attempt {attempt} error: {e}")

    return None, None, max_retries, "all_attempts_failed"


# =============================================================================
#                    PIPELINE
# =============================================================================

def build_type_c_dataset(
    input_path: str,
    type_b_path: str,
    output_path: str,
    assignments_path: str,
    errors_path: str,
    model: str,
    base_url: str,
    api_key: Optional[str],
    llm_timeout: int,
    max_items: Optional[int],
    sleep_sec: float,
    log_file: str,
    max_retries: int = 2,
    max_per_pattern: int = 10,
    retry_errors: bool = False,
):
    setup_logging(log_file)

    log.info("=" * 60)
    log.info(f"TYPE C BUILD — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if retry_errors:
        log.info("  MODE: retry-errors (re-processing failed codes)")
    log.info("=" * 60)

    try:
        data = load_input_json(input_path)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
        log.error(f"FATAL: {e}")
        sys.exit(1)

    if max_items:
        data = data[:max_items]

    # Lire les groupes RÉELLEMENT utilisés en Type B
    log.info(f"Loading Type B results from {type_b_path}...")
    b_groups = get_type_b_groups(type_b_path)
    log.info(f"  Codes with Type B: {len(b_groups)}")

    # Phase 1 : planification
    log.info(f"Planning Type C for {len(data)} codes...")
    plans = plan_type_c(data, b_groups, max_per_pattern)

    valid_plans = [p for p in plans if p.get("group_c")]
    skipped = [p for p in plans if not p.get("group_c")]

    log.info(f"  Valid assignments : {len(valid_plans)}")
    log.info(f"  Skipped           : {len(skipped)}")

    skip_reasons = Counter(s.get("skip_reason", "?") for s in skipped)
    for r, c in skip_reasons.most_common():
        log.info(f"    {r}: {c}")

    group_dist = Counter(p["group_c"] for p in valid_plans)
    for g, c in group_dist.most_common():
        log.info(f"    {g:>15s} : {c}")
    log.info("")

    # Sauvegarder le plan d'assignation
    save_json(assignments_path, plans)
    log.info(f"  Assignments saved : {assignments_path}")

    # Phase 2 : injection
    dataset = load_output_json(output_path)
    errors = load_output_json(errors_path)

    # Construire done_keys
    done_keys = set()
    for item in dataset:
        done_keys.add(item.get("source_origin_id"))

    if not retry_errors:
        # Mode normal : les erreurs sont aussi dans done_keys
        for item in errors:
            done_keys.add(item.get("source_origin_id"))
    else:
        # Mode retry : on retire les erreurs précédentes pour les retenter
        old_error_count = len(errors)
        errors = []  # reset errors
        log.info(f"  Retry mode: cleared {old_error_count} previous errors")

    next_id = len(dataset) + 1
    data_by_id = {r["origin_id"]: r for r in data}

    run_start = time.time()
    done = 0
    success_count = 0
    total_todo = sum(1 for p in valid_plans if p["origin_id"] not in done_keys)

    log.info(f"  Remaining to process: {total_todo}")
    log.info("")

    for plan in valid_plans:
        origin_id = plan["origin_id"]
        if origin_id in done_keys:
            continue

        group = plan["group_c"]
        pattern = plan["pattern_c"]
        rec = data_by_id.get(origin_id)
        if not rec:
            continue

        t0 = time.time()
        done += 1

        buggy_code, meta, attempts, status = inject_and_validate(
            rec, pattern, group, model, base_url, api_key, llm_timeout, max_retries)

        elapsed_item = time.time() - t0
        elapsed_total = time.time() - run_start
        remaining = total_todo - done
        eta = (elapsed_total / done * remaining / 60) if done else 0

        if buggy_code and meta:
            clean_code = clean_output_code(rec.get("generated_code", ""))
            instruction = build_type_c_instruction(buggy_code, origin_id)
            primary_axis, secondary_axes = compute_axes(pattern, group, rec)

            entry = {
                "id": f"type_c_{next_id:04d}",
                "type": "C",
                "source_origin_id": origin_id,
                "instruction": instruction,
                "output": clean_code,
                "primary_axis": primary_axis,
                "secondary_axes": secondary_axes,
                "metadata": {
                    "injected_pattern": pattern,
                    "injected_group": group,
                    "signal_type": "none",
                    "num_attempts": attempts,
                    "type_b_groups": plan["type_b_groups"],
                    "observed_group": meta.get("observed_group"),
                    "pattern_match_status": meta.get("pattern_match_status"),
                    "hidden_compiler_output": meta.get("hidden_compiler_output"),
                    "hidden_runtime_error": meta.get("hidden_runtime_error"),
                },
            }
            dataset.append(entry)
            next_id += 1
            success_count += 1

            log.info(
                f"[{done}/{total_todo}] oid={origin_id:>4d} "
                f"✓ {group}/{pattern} obs={meta.get('observed_group')} "
                f"att={attempts} ({elapsed_item:.1f}s, ETA {eta:.0f}min)")
        else:
            errors.append({
                "source_origin_id": origin_id,
                "target_pattern": pattern,
                "target_group": group,
                "type_b_groups": plan["type_b_groups"],
                "failure_reason": status,
                "attempts": attempts,
            })
            log.info(
                f"[{done}/{total_todo}] oid={origin_id:>4d} "
                f"✗ {group}/{pattern} ({status}) "
                f"({elapsed_item:.1f}s, ETA {eta:.0f}min)")

        done_keys.add(origin_id)
        save_json(output_path, dataset)
        save_json(errors_path, errors)

        if sleep_sec > 0:
            time.sleep(sleep_sec)

    # Bilan
    total_time = (time.time() - run_start) / 60

    c_group_final = Counter()
    c_pattern_final = Counter()
    c_axis_final = Counter()
    c_match_status = Counter()
    for item in dataset:
        m = item.get("metadata", {})
        c_group_final[m.get("injected_group", "?")] += 1
        c_pattern_final[m.get("injected_pattern", "?")] += 1
        c_axis_final[item.get("primary_axis", "?")] += 1
        c_match_status[m.get("pattern_match_status", "?")] += 1

    fail_reasons = Counter()
    for item in errors:
        fail_reasons[item.get("failure_reason", "?")] += 1

    log.info("")
    log.info("=" * 60)
    log.info(f"TYPE C DONE — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log.info(f"Duration       : {total_time:.1f} min")
    log.info(f"Dataset size   : {len(dataset)} → {output_path}")
    log.info(f"Errors         : {len(errors)} → {errors_path}")
    log.info(f"Assignments    : {assignments_path}")
    log.info(f"Success rate   : {success_count}/{done} "
             f"({100 * success_count / max(done, 1):.0f}%)")

    log.info("Group distribution:")
    for g, c in c_group_final.most_common():
        log.info(f"  {g:>15s} : {c}")
    log.info("Pattern match status:")
    for s, c in c_match_status.most_common():
        log.info(f"  {s:>20s} : {c}")
    log.info("Primary axis distribution:")
    for a, c in c_axis_final.most_common():
        log.info(f"  {a:>15s} : {c}")
    log.info("Failure reasons:")
    for r, c in fail_reasons.most_common():
        log.info(f"  {r:>30s} : {c}")
    log.info("Top 10 patterns:")
    for p, c in c_pattern_final.most_common(10):
        log.info(f"  {p:>30s} : {c}")
    log.info("=" * 60)


# =============================================================================
#                    MAIN
# =============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Type C: autonomous debugging, no signal, different group from Type B")
    parser.add_argument("--input", required=True,
                        help="dataset_base_clean_codes.json")
    parser.add_argument("--type-b-dataset", required=True,
                        help="dataset/type_b/type_b_dataset.json")
    parser.add_argument("--output", required=True,
                        help="dataset/type_c/type_c_dataset.json")
    parser.add_argument("--assignments-output",
                        default="dataset/type_c/type_c_assignments.json",
                        help="Planning decisions (groups, patterns, skips)")
    parser.add_argument("--errors-output",
                        default="dataset/type_c/type_c_errors.json")
    parser.add_argument("--model", required=True)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--api-key", default=None)
    parser.add_argument("--llm-timeout", type=int, default=180)
    parser.add_argument("--max-items", type=int, default=None)
    parser.add_argument("--max-retries", type=int, default=2)
    parser.add_argument("--max-per-pattern", type=int, default=10)
    parser.add_argument("--sleep", type=float, default=0.5)
    parser.add_argument("--log-file",
                        default="dataset/type_c/type_c_build.log")
    parser.add_argument("--retry-errors", action="store_true",
                        help="Re-process previously failed codes (ignores errors in done_keys)")

    args = parser.parse_args()

    build_type_c_dataset(
        input_path=args.input,
        type_b_path=args.type_b_dataset,
        output_path=args.output,
        assignments_path=args.assignments_output,
        errors_path=args.errors_output,
        model=args.model,
        base_url=args.base_url,
        api_key=args.api_key or os.environ.get("OPENWEBUI_API_KEY"),
        llm_timeout=args.llm_timeout,
        max_items=args.max_items,
        sleep_sec=args.sleep,
        log_file=args.log_file,
        max_retries=args.max_retries,
        max_per_pattern=args.max_per_pattern,
        retry_errors=args.retry_errors,
    )