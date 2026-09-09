"""
Pipeline Type B — Injection d'erreurs contrôlée (v4).

Corrections v4 (par rapport à v3-fix) :
  1. SPURIOUS_CRASH_MARKERS : retiré "fortran runtime error" qui créait
     des faux positifs sur les vrais crashes de bounds checking
  2. division_by_zero : traité comme dual runtime/ineq — si le code
     produit Inf/NaN sans crasher, accepté comme ineq valide
  3. implicit_none_missing : hint amélioré pour que le LLM retire
     aussi une déclaration de variable (pas juste implicit none)
  4. plan_assignments : fallback across groups — quand le groupe
     le moins représenté a tous ses patterns au cap, on essaie les
     autres groupes au lieu d'abandonner. Cap relevé de 12 à 15.
     Résultat : 215/224 codes assignés (96%) au lieu de 155 (69%).

Conservé :
  - has_stdin détecté depuis le code source
  - exclusion des patterns runtime I/O
  - pattern_match_status, primary_axis/secondary_axes
  - UUID, -fcheck=bounds, stats enrichies
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
    "ineq": [
        "bool_output_mismatch", "edge_case_failure", "extra_output_elements",
        "incorrect_condition", "missing_output_elements", "off_by_one_error",
        "output_format_mismatch", "partial_output", "precision_loss",
        "whitespace_mismatch", "wrong_index_base", "wrong_loop_bounds",
        "wrong_numeric_result", "wrong_string_output",
    ],
}

PATTERN_TO_GROUP: Dict[str, str] = {}
for g, pats in TAXONOMY.items():
    for p in pats:
        PATTERN_TO_GROUP[p] = g

ALLOWED_GROUPS = {"compile_err", "runtime_err", "ineq"}

# Patterns runtime qui modifient le I/O — exclus du pipeline Type B
RUNTIME_IO_PATTERNS = {
    "eof_input", "interactive_prompt_leak",
    "stdin_format_mismatch", "invalid_numeric_input",
}

# Marqueurs de crashes parasites (non liés au bug ciblé)
# NOTE v4 : "fortran runtime error" RETIRÉ — c'est le préfixe standard
# de TOUS les messages d'erreur gfortran, y compris les vrais crashes
# de bounds checking (-fcheck=bounds). Le garder créait des faux positifs.
SPURIOUS_CRASH_MARKERS = [
    "end of file", "eof", "input/output",
    "unit 5", "read(unit=5",
    "recursive i/o", "no such file",
]


# =============================================================================
#                          LOGGING
# =============================================================================

def setup_logging(log_file: str):
    logger = logging.getLogger("type_b")
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


log = logging.getLogger("type_b")


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


def _unique_prefix() -> str:
    return uuid.uuid4().hex[:15]


def code_needs_stdin(code: str) -> bool:
    """Détecte si le code lit depuis stdin (read(*,...) ou read(5,...))."""
    lc = code.lower()
    # read(*, ...) ou read *, ...
    if re.search(r'\bread\s*\(\s*\*', lc):
        return True
    # read(5, ...) — unit 5 = stdin
    if re.search(r'\bread\s*\(\s*5\s*,', lc):
        return True
    return False


def compile_fortran(code: str) -> Tuple[bool, str, str]:
    """
    Compile du code Fortran avec -fcheck=bounds pour détecter les bugs mémoire.
    Retourne (success, binary_path, stderr).
    """
    ensure_work_dir()
    uid = _unique_prefix()
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


def run_fortran(
    binary_path: str,
    stdin_data: Optional[str] = None,
    timeout_sec: int = 10,
) -> Tuple[bool, str, str, int]:
    """Exécute un binaire. Retourne (success, stdout, stderr, returncode)."""
    try:
        result = subprocess.run(
            [binary_path],
            input=stdin_data,
            capture_output=True, text=True, timeout=timeout_sec,
            env={**os.environ, "GFORTRAN_UNBUFFERED_ALL": "1"})
        success = result.returncode == 0
        return success, result.stdout, result.stderr.strip(), result.returncode
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
    """Détecte les crashes parasites (EOF, I/O, timeout)."""
    if returncode == -99:
        return True
    low = stderr.lower()
    return any(marker in low for marker in SPURIOUS_CRASH_MARKERS)


# =============================================================================
#                    INJECTION PROMPT
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
    "off_by_one_error": "Change a loop bound by 1 (e.g., 1,N becomes 0,N or 1,N-1).",
    "wrong_loop_bounds": "Change loop start or end to produce wrong iteration count.",
    "wrong_numeric_result": "Modify a mathematical expression to produce a wrong result.",
    "incorrect_condition": "Change a comparison operator (e.g., .gt. to .ge., .eq. to .ne.).",
    "precision_loss": "Change a double precision to single precision or lose precision.",
    "edge_case_failure": "Make the code fail on boundary values (0, 1, max, etc.).",
    "wrong_index_base": "Change array indexing (e.g., Fortran 1-based to 0-based).",
}


def build_injection_prompt(code: str, pattern: str, group: str) -> str:
    hint = PATTERN_HINTS.get(pattern, f"Introduce a {pattern} error.")
    behavior = {
        "compile_err": "The modified code must FAIL to compile with gfortran.",
        "runtime_err": "The modified code must compile but CRASH at runtime.",
        "ineq": "The modified code must compile, run without crash, but produce DIFFERENT output.",
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
    original_stdout: Optional[str],
    stdin_data: Optional[str],
) -> Tuple[bool, str, Dict[str, Any]]:
    """
    Valide le code buggé par compilation + exécution.
    Retourne (valid, reason, metadata).
    """
    meta: Dict[str, Any] = {
        "target_pattern": target_pattern,
        "target_group": target_group,
    }

    compiled, binary, compile_stderr = compile_fortran(buggy_code)

    if target_group == "compile_err":
        if not compiled:
            meta["observed_group"] = "compile_err"
            meta["compiler_output"] = compile_stderr[:500]
            meta["signal_type"] = "compiler_message"
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
        meta["compiler_output"] = compile_stderr[:200]
        meta["pattern_match_status"] = "group_mismatch"
        return False, "compile_unexpected_failure", meta

    ran_ok, stdout, run_stderr, returncode = run_fortran(binary, stdin_data=stdin_data)

    if target_group == "runtime_err":
        if not ran_ok:
            if is_spurious_crash(run_stderr, returncode):
                meta["observed_group"] = "spurious_crash"
                meta["runtime_error"] = run_stderr[:300]
                meta["pattern_match_status"] = "spurious"
                return False, "runtime_spurious_crash", meta

            meta["observed_group"] = "runtime_err"
            meta["runtime_error"] = run_stderr[:500]
            meta["signal_type"] = "runtime_crash"
            meta["pattern_match_status"] = "group_only"
            return True, "runtime_crash_as_expected", meta

        # v4 : traitement spécial pour division_by_zero
        # En Fortran, 1.0/0.0 produit Inf (IEEE 754) sans crasher.
        # Si le target est division_by_zero et que la sortie contient
        # Inf/NaN, on accepte comme ineq (résultat incorrect).
        if target_pattern == "division_by_zero" and original_stdout is not None:
            out_clean = stdout.strip()
            orig_clean = original_stdout.strip()
            out_lower = out_clean.lower()

            has_special = any(marker in out_lower for marker in
                             ["inf", "nan", "infinity", "-infinity", "+infinity"])

            if has_special and out_clean != orig_clean:
                meta["observed_group"] = "ineq"
                meta["expected_output"] = orig_clean[:500]
                meta["actual_output"] = out_clean[:500]
                meta["signal_type"] = "output_diff"
                meta["pattern_match_status"] = "group_only"
                meta["note"] = "division_by_zero_accepted_as_ineq"
                return True, "division_by_zero_ineq_fallback", meta

        meta["observed_group"] = "no_effect"
        meta["pattern_match_status"] = "group_mismatch"
        return False, "runtime_missing_crash", meta

    if target_group == "ineq":
        if not ran_ok:
            crash_type = "spurious_crash" if is_spurious_crash(run_stderr, returncode) else "runtime_err"
            meta["observed_group"] = crash_type
            meta["runtime_error"] = run_stderr[:200]
            meta["pattern_match_status"] = "group_mismatch"
            return False, "runtime_unexpected_crash", meta

        if original_stdout is None:
            meta["observed_group"] = "unknown"
            meta["pattern_match_status"] = "missing_reference"
            return False, "missing_stdout", meta

        out_clean = stdout.strip()
        orig_clean = original_stdout.strip()

        if out_clean == orig_clean:
            meta["observed_group"] = "no_effect"
            meta["pattern_match_status"] = "group_mismatch"
            return False, "ineq_output_identical", meta

        meta["observed_group"] = "ineq"
        meta["expected_output"] = orig_clean[:500]
        meta["actual_output"] = out_clean[:500]
        meta["signal_type"] = "output_diff"
        meta["pattern_match_status"] = "group_only"
        return True, "output_differs_as_expected", meta

    return False, f"unknown_group_{target_group}", meta


# =============================================================================
#                    INSTRUCTION BUILDERS
# =============================================================================

def build_type_b_instruction(buggy_code: str, group: str, meta: Dict[str, Any]) -> str:
    # v4 : utiliser signal_type pour déterminer le format d'instruction.
    # Cela gère le cas division_by_zero accepté comme ineq (signal_type="output_diff"
    # mais group="runtime_err").
    signal_type = meta.get("signal_type", "")

    if signal_type == "compiler_message" or group == "compile_err":
        msg = meta.get("compiler_output", "compilation error")
        return (
            f"The following Fortran 90 code fails to compile with this error:\n\n"
            f"{msg}\n\n"
            f"Fix the code:\n\n{buggy_code}")

    if signal_type == "output_diff":
        expected = meta.get("expected_output", "<unknown>")
        actual = meta.get("actual_output", "<unknown>")
        return (
            f"The following Fortran 90 code compiles and runs "
            f"but produces incorrect results.\n\n"
            f"Expected output:\n{expected}\n\n"
            f"Actual output:\n{actual}\n\n"
            f"Fix the code:\n\n{buggy_code}")

    if signal_type == "runtime_crash" or group == "runtime_err":
        msg = meta.get("runtime_error", "runtime error")
        return (
            f"The following Fortran 90 code compiles successfully "
            f"but crashes at runtime with:\n\n"
            f"{msg}\n\n"
            f"Fix the code:\n\n{buggy_code}")

    return f"Fix the bug in this Fortran 90 code:\n\n{buggy_code}"


# =============================================================================
#                    AXES
# =============================================================================

GROUP_TO_PRIMARY_AXIS = {
    "compile_err": "syntax",
    "runtime_err": "logic",
    "ineq": "logic",
}

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
    "edge_case_failure": "logic", "incorrect_condition": "logic",
    "off_by_one_error": "logic", "precision_loss": "logic",
    "wrong_index_base": "logic", "wrong_loop_bounds": "logic",
    "wrong_numeric_result": "logic",
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
#                    PLANNING — CORRECTION CRITIQUE
# =============================================================================

def get_available_patterns_by_group(rec: Dict[str, Any]) -> Dict[str, List[str]]:
    result: Dict[str, List[str]] = {}
    for p in rec.get("applicable_patterns", []):
        g = PATTERN_TO_GROUP.get(p)
        if not g or g not in ALLOWED_GROUPS:
            continue
        if g == "runtime_err" and p in RUNTIME_IO_PATTERNS:
            continue
        result.setdefault(g, []).append(p)
    return result


def plan_assignments(
    data: List[Dict[str, Any]],
    max_examples_per_pattern: int = 15,
) -> List[Dict[str, Any]]:
    """
    v4 fix : au lieu de choisir UN groupe et abandonner si ses patterns
    sont au cap, on essaie TOUS les groupes candidats par ordre de
    représentation croissante. Cap relevé de 12 à 15.
    """
    global_group_counts: Counter = Counter()
    global_pattern_counts: Counter = Counter()
    plans: List[Dict[str, Any]] = []

    for rec in data:
        origin_id = rec.get("origin_id")
        code = rec.get("generated_code", "") or ""
        avail = get_available_patterns_by_group(rec)

        needs_stdin = code_needs_stdin(code)

        valid_groups = {g: pats for g, pats in avail.items() if len(pats) >= 1}

        if not valid_groups:
            plans.append({
                "origin_id": origin_id,
                "group_b": None,
                "patterns_b": [],
                "available_groups": {},
                "needs_stdin": needs_stdin,
                "skip_reason": "no_valid_group",
            })
            continue

        candidates = dict(valid_groups)

        # ineq nécessite une sortie de référence
        if "ineq" in candidates and rec.get("run_stdout") is None:
            del candidates["ineq"]

        # Si le code lit depuis stdin, exclure runtime_err et ineq
        if needs_stdin:
            for g in ["runtime_err", "ineq"]:
                candidates.pop(g, None)

        if not candidates:
            plans.append({
                "origin_id": origin_id,
                "group_b": None,
                "patterns_b": [],
                "available_groups": {g: p for g, p in avail.items()},
                "needs_stdin": needs_stdin,
                "skip_reason": "no_executable_group",
            })
            continue

        # CORRECTION v4 : essayer TOUS les groupes candidats
        # par ordre de représentation croissante, jusqu'à trouver
        # un groupe avec des patterns non plafonnés.
        sorted_groups = sorted(candidates.keys(),
                                key=lambda g: global_group_counts[g])

        chosen_group = None
        selected = []

        for try_group in sorted_groups:
            group_pats = candidates[try_group]
            sorted_pats = sorted(group_pats,
                                  key=lambda p: global_pattern_counts[p])
            eligible = [p for p in sorted_pats
                        if global_pattern_counts[p] < max_examples_per_pattern]

            if eligible:
                selected = eligible[:2] if len(eligible) >= 2 else eligible[:1]
                chosen_group = try_group
                break

        if not selected:
            plans.append({
                "origin_id": origin_id,
                "group_b": None,
                "patterns_b": [],
                "available_groups": {g: p for g, p in avail.items()},
                "needs_stdin": needs_stdin,
                "skip_reason": "all_patterns_at_cap",
            })
            continue

        global_group_counts[chosen_group] += len(selected)
        for p in selected:
            global_pattern_counts[p] += 1

        plans.append({
            "origin_id": origin_id,
            "group_b": chosen_group,
            "patterns_b": selected,
            "available_groups": {g: p for g, p in avail.items()},
            "needs_stdin": needs_stdin,
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
    original_stdout = rec.get("run_stdout")
    stdin_data = None  # nos codes sont autonomes

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

            valid, reason, meta = validate_injection(
                buggy_code, group, pattern, original_stdout, stdin_data)

            if valid:
                return buggy_code, meta, attempt, reason

            log.info(f"      attempt {attempt}: {reason}")

        except Exception as e:
            log.warning(f"      attempt {attempt} error: {e}")

    return None, None, max_retries, "all_attempts_failed"


# =============================================================================
#                    PIPELINE
# =============================================================================

def build_type_b_dataset(
    input_path: str,
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
    max_examples_per_pattern: int = 15,
):
    setup_logging(log_file)

    log.info("=" * 60)
    log.info(f"TYPE B BUILD v4 — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log.info("=" * 60)

    try:
        data = load_input_json(input_path)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
        log.error(f"FATAL: {e}")
        sys.exit(1)

    if max_items:
        data = data[:max_items]

    # Phase 1 : planification
    log.info(f"Planning assignments for {len(data)} codes...")
    plans = plan_assignments(data, max_examples_per_pattern)

    valid_plans = [p for p in plans if p.get("group_b")]
    skipped = [p for p in plans if not p.get("group_b")]

    log.info(f"  Valid assignments : {len(valid_plans)}")
    log.info(f"  Skipped           : {len(skipped)}")
    for s in skipped:
        log.info(f"    oid={s['origin_id']}: {s.get('skip_reason', '?')}")

    total_injections = sum(len(p["patterns_b"]) for p in valid_plans)
    log.info(f"  Total injections  : {total_injections}")

    group_dist = Counter()
    for p in valid_plans:
        group_dist[p["group_b"]] += len(p["patterns_b"])
    for g, c in group_dist.most_common():
        log.info(f"    {g:>15s} : {c}")

    # Vérifier la distribution
    needs_stdin_count = sum(1 for p in plans if p.get("needs_stdin"))
    log.info(f"  Codes needing stdin : {needs_stdin_count}")
    log.info("")

    save_json(assignments_path, plans)

    # Phase 2 : injection
    dataset = load_output_json(output_path)
    errors = load_output_json(errors_path)

    done_keys = set()
    for item in dataset:
        m = item.get("metadata", {})
        done_keys.add(f"{item.get('source_origin_id')}_{m.get('target_pattern', '')}")
    for item in errors:
        done_keys.add(f"{item.get('source_origin_id')}_{item.get('target_pattern', '')}")

    next_id = len(dataset) + 1
    data_by_id = {r["origin_id"]: r for r in data}

    run_start = time.time()
    done = 0
    success_count = 0

    for plan in valid_plans:
        origin_id = plan["origin_id"]
        group = plan["group_b"]
        patterns = plan["patterns_b"]
        rec = data_by_id.get(origin_id)
        if not rec:
            continue

        for pattern in patterns:
            key = f"{origin_id}_{pattern}"
            if key in done_keys:
                continue

            t0 = time.time()
            done += 1

            buggy_code, meta, attempts, status = inject_and_validate(
                rec, pattern, group, model, base_url, api_key,
                llm_timeout, max_retries)

            elapsed_item = time.time() - t0
            elapsed_total = time.time() - run_start
            remaining = total_injections - done
            eta = (elapsed_total / done * remaining / 60) if done else 0

            if buggy_code and meta:
                clean_code = clean_output_code(rec.get("generated_code", ""))
                instruction = build_type_b_instruction(buggy_code, group, meta)
                primary_axis, secondary_axes = compute_axes(pattern, group, rec)

                entry = {
                    "id": f"type_b_{next_id:04d}",
                    "type": "B",
                    "source_origin_id": origin_id,
                    "instruction": instruction,
                    "output": clean_code,
                    "primary_axis": primary_axis,
                    "secondary_axes": secondary_axes,
                    "metadata": {
                        "target_pattern": pattern,
                        "target_group": group,
                        "observed_group": meta.get("observed_group"),
                        "pattern_match_status": meta.get("pattern_match_status"),
                        "signal_type": meta.get("signal_type"),
                        "num_attempts": attempts,
                        "compiler_output": meta.get("compiler_output"),
                        "runtime_error": meta.get("runtime_error"),
                        "expected_output": meta.get("expected_output"),
                        "actual_output": meta.get("actual_output"),
                    },
                }
                dataset.append(entry)
                next_id += 1
                success_count += 1

                log.info(
                    f"[{done}/{total_injections}] oid={origin_id:>4d} "
                    f"✓ {group}/{pattern} obs={meta.get('observed_group')} "
                    f"att={attempts} ({elapsed_item:.1f}s, ETA {eta:.0f}min)")
            else:
                errors.append({
                    "source_origin_id": origin_id,
                    "target_pattern": pattern,
                    "target_group": group,
                    "failure_reason": status,
                    "attempts": attempts,
                })
                log.info(
                    f"[{done}/{total_injections}] oid={origin_id:>4d} "
                    f"✗ {group}/{pattern} reason={status} "
                    f"({elapsed_item:.1f}s, ETA {eta:.0f}min)")

            done_keys.add(key)
            save_json(output_path, dataset)
            save_json(errors_path, errors)

            if sleep_sec > 0:
                time.sleep(sleep_sec)

    # Bilan
    total_time = (time.time() - run_start) / 60

    target_group_final = Counter()
    observed_group_final = Counter()
    pattern_final = Counter()
    match_status = Counter()
    primary_axis_final = Counter()

    for item in dataset:
        m = item.get("metadata", {})
        target_group_final[m.get("target_group", "?")] += 1
        observed_group_final[m.get("observed_group", "?")] += 1
        pattern_final[m.get("target_pattern", "?")] += 1
        match_status[m.get("pattern_match_status", "?")] += 1
        primary_axis_final[item.get("primary_axis", "?")] += 1

    fail_reasons = Counter()
    for item in errors:
        fail_reasons[item.get("failure_reason", "?")] += 1

    succeeded_codes = set(item.get("source_origin_id") for item in dataset)
    failed_codes = set(item.get("source_origin_id") for item in errors) - succeeded_codes

    log.info("")
    log.info("=" * 60)
    log.info(f"TYPE B DONE — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log.info(f"Duration       : {total_time:.1f} min")
    log.info(f"Dataset size   : {len(dataset)} → {output_path}")
    log.info(f"Errors         : {len(errors)} → {errors_path}")
    log.info(f"Success rate   : {success_count}/{done} "
             f"({100 * success_count / max(done, 1):.0f}%)")
    log.info(f"Succeeded codes: {len(succeeded_codes)}")
    log.info(f"Failed-only codes: {len(failed_codes)}")

    log.info("Target group distribution:")
    for g, c in target_group_final.most_common():
        log.info(f"  {g:>15s} : {c}")
    log.info("Observed group distribution:")
    for g, c in observed_group_final.most_common():
        log.info(f"  {g:>15s} : {c}")
    log.info("Pattern match status:")
    for s, c in match_status.most_common():
        log.info(f"  {s:>20s} : {c}")
    log.info("Primary axis distribution:")
    for a, c in primary_axis_final.most_common():
        log.info(f"  {a:>15s} : {c}")
    log.info("Failure reasons:")
    for r, c in fail_reasons.most_common():
        log.info(f"  {r:>30s} : {c}")
    log.info("Top 10 patterns:")
    for p, c in pattern_final.most_common(10):
        log.info(f"  {p:>30s} : {c}")
    log.info("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Type B: LLM error injection + behavioral validation (v4)")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--assignments-output",
                        default="dataset/type_b/type_b_assignments.json")
    parser.add_argument("--errors-output",
                        default="dataset/type_b/type_b_errors.json")
    parser.add_argument("--model", required=True)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--api-key", default=None)
    parser.add_argument("--llm-timeout", type=int, default=180)
    parser.add_argument("--max-items", type=int, default=None)
    parser.add_argument("--max-retries", type=int, default=2)
    parser.add_argument("--max-per-pattern", type=int, default=15,
                        help="Max examples per pattern globally (default: 15)")
    parser.add_argument("--sleep", type=float, default=0.5)
    parser.add_argument("--log-file",
                        default="dataset/type_b/type_b_build.log")

    args = parser.parse_args()

    build_type_b_dataset(
        input_path=args.input,
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
        max_examples_per_pattern=args.max_per_pattern,
    )