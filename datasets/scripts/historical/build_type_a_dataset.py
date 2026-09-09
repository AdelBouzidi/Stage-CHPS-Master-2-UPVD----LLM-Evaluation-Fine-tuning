"""
Construction du dataset Type A — v4 finale.

v4 :
  - Règles 9-12 dans le prompt
  - Détection + réécriture des instructions faibles
  - Préfixe standardisé déterministe ("Write a Fortran 90 program that...")
  - Pas d'axes dans le prompt LLM
"""

import json
import requests
import argparse
import os
import re
import sys
import time
import logging
from datetime import datetime
from collections import Counter
from typing import Dict, Any, List, Optional, Set, Tuple


# =============================================================================
#                          LOGGING
# =============================================================================

def setup_logging(log_file: str):
    logger = logging.getLogger("type_a")
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


log = logging.getLogger("type_a")


# =============================================================================
#                    MAPPING PATTERNS → AXES
# =============================================================================

PATTERN_TO_AXIS = {
    "explanation_leak": "format", "markdown_wrapping": "format",
    "utf8_decode_error": "format",

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

    "eof_input": "io", "interactive_prompt_leak": "io",
    "stdin_format_mismatch": "io", "invalid_numeric_input": "io",
    "output_format_mismatch": "io", "missing_output_elements": "io",
    "extra_output_elements": "io", "partial_output": "io",
    "wrong_string_output": "io", "bool_output_mismatch": "io",

    "allocation_runtime_error": "logic", "array_bounds_runtime": "logic",
    "division_by_zero": "logic", "floating_point_exception": "logic",
    "integer_overflow": "logic", "malloc_corruption": "logic",
    "segmentation_fault": "logic", "unallocated_access": "logic",
    "edge_case_failure": "logic", "incorrect_condition": "logic",
    "off_by_one_error": "logic", "precision_loss": "logic",
    "whitespace_mismatch": "logic", "wrong_index_base": "logic",
    "wrong_loop_bounds": "logic", "wrong_numeric_result": "logic",

    "invalid_directive_syntax": "parallel", "loop_dependency_violation": "parallel",
    "missing_private_clause": "parallel", "missing_reduction_clause": "parallel",
    "openacc_openmp_mistranslation": "parallel", "race_condition": "parallel",
    "wrong_shared_variable": "parallel",
}


def compute_axes(rec: Dict[str, Any]) -> List[str]:
    axes: Set[str] = set()
    for p in rec.get("applicable_patterns", []):
        ax = PATTERN_TO_AXIS.get(p)
        if ax:
            axes.add(ax)

    code = (rec.get("generated_code", "") or "").lower()
    features = rec.get("features", {})

    if ("read(" in code or "open(" in code or
        "write(" in code or "format(" in code):
        axes.add("io")
    if "!$omp" in code or "!$acc" in code or "!$claw" in code:
        axes.add("parallel")
    if features.get("num_loops", 0) > 0 or features.get("num_ifs", 0) > 0:
        axes.add("logic")

    if not axes:
        axes.add("syntax")

    return sorted(axes)


# =============================================================================
#                    PREFIXES & ENFORCEMENT
# =============================================================================

# Préfixes standardisés — avec espace dans "Fortran 90"
PREFIXES = [
    "Write a Fortran 90 program that",
    "Create a Fortran 90 program that",
    "Develop a Fortran 90 program that",
    "Generate a Fortran 90 program that",
    "Implement a Fortran 90 program that",
    "Design a Fortran 90 program that",
]

# Verbes d'ouverture que le LLM utilise souvent
OPENING_VERBS = [
    "implement", "compute", "design", "develop", "build",
    "construct", "create", "write", "generate", "calculate",
    "determine", "perform", "evaluate", "produce",
]


def _verb_to_third_person(verb: str) -> str:
    """Conjugue un verbe à la 3ème personne du singulier (anglais)."""
    v = verb.lower()
    if v.endswith("sh") or v.endswith("ch") or v.endswith("x") or v.endswith("ss"):
        return v + "es"
    if v.endswith("y") and len(v) > 1 and v[-2] not in "aeiou":
        return v[:-1] + "ies"
    return v + "s"


def enforce_prefix(text: str, origin_id: int) -> str:
    """Standardise le début de l'instruction avec un préfixe déterministe.

    - Choix du préfixe basé sur origin_id (reproductible)
    - Conjugaison correcte du verbe après "that"
    - Gestion des cas où le LLM a déjà mis un préfixe conforme
    """
    text = text.strip()
    lowered = text.lower()

    # Si déjà conforme, on garde tel quel
    for p in PREFIXES:
        if lowered.startswith(p.lower()):
            return text

    # Aussi accepter les variantes avec "Fortran" au lieu de "Fortran 90"
    for p in PREFIXES:
        variant = p.replace("Fortran 90", "Fortran")
        if lowered.startswith(variant.lower()):
            return text

    # Trouver le verbe d'ouverture existant
    found_verb = None
    rest = text
    for v in OPENING_VERBS:
        pattern = v + " "
        if lowered.startswith(pattern):
            found_verb = v
            rest = text[len(pattern):]
            break

    # Retirer "a Fortran 90 program that" si présent après le verbe
    stripped_program_that = False
    rest_lower = rest.lower().strip()
    for suffix in ["a fortran 90 program that ",
                    "a fortran program that ",
                    "a fortran90 program that "]:
        if rest_lower.startswith(suffix):
            rest = rest[len(suffix):]
            stripped_program_that = True
            break

    # Retirer les phrases structurelles ("a function that", "a subroutine that")
    # qui sont redondantes avec "a Fortran 90 program that"
    rest_lower = rest.lower().strip()
    for structural in ["a function that ",
                       "a subroutine that ",
                       "a module that ",
                       "a program that "]:
        if rest_lower.startswith(structural):
            rest = rest[len(structural):]
            stripped_program_that = True  # le reste est déjà conjugué
            break

    # Retirer aussi "in Fortran..." si présent (sera remis par le préfixe)
    if not stripped_program_that:
        rest_lower = rest.lower().strip()
        for suffix in ["in fortran 90 ",
                        "in fortran, ",
                        "in fortran 90, ",
                        "in fortran "]:
            if rest_lower.startswith(suffix):
                rest = rest[len(suffix):]
                break

    rest = rest.strip()

    # Logique de conjugaison :
    # 3 cas possibles :
    #
    # Cas A : "Compute the mean..." → found_verb="compute", rest="the mean..."
    #         → conjuguer le verbe trouvé → "computes the mean..."
    #
    # Cas B : "Implement a Fortran 90 program that computes the mean..."
    #         → found_verb="implement", stripped_program_that=True, rest="computes the mean..."
    #         → rest est déjà correct, ne rien ajouter
    #
    # Cas C : "a Fortran program that compute the mean..." (verbe non conjugué après strip)
    #         → conjuguer le premier mot de rest
    if rest:
        first_word = rest.split()[0].lower()

        if stripped_program_that:
            # Cas B : rest est déjà conjugué après "program that"
            # Juste s'assurer que la première lettre est en minuscule
            if rest[0].isupper():
                rest = rest[0].lower() + rest[1:]
        elif found_verb and first_word not in OPENING_VERBS:
            # Cas A : "Compute the mean..." → rest = "the mean..."
            # → remettre le verbe conjugué
            conjugated = _verb_to_third_person(found_verb)
            rest = conjugated + " " + rest
        elif first_word in OPENING_VERBS:
            # Cas C : verbe à l'infinitif → conjuguer
            conjugated = _verb_to_third_person(first_word)
            rest = conjugated + rest[len(first_word):]
        else:
            # Pas de verbe trouvé, juste lowercase
            if rest[0].isupper():
                rest = rest[0].lower() + rest[1:]

    # Choix déterministe du préfixe basé sur origin_id
    prefix = PREFIXES[origin_id % len(PREFIXES)]

    result = f"{prefix} {rest}"

    # Nettoyer "in Fortran" ou "in Fortran 90" en fin de phrase (redondant avec le préfixe)
    result = re.sub(r',?\s+in Fortran(\s+90)?\s*\.?\s*$', '.', result, flags=re.IGNORECASE)

    # S'assurer de la ponctuation finale
    result = result.strip()
    if result and result[-1] not in ".!?":
        result += "."

    return result


# =============================================================================
#                    DETECTION D'INSTRUCTIONS FAIBLES
# =============================================================================

WEAK_MARKERS = [
    "print", "display", "output the", "show the",
    "main program", "subroutine", "function that calls",
    "module", "nested loop", "loop that", "initialize",
    "wrapper", "helper subroutine", "helper function",
]


def instruction_needs_rewrite(text: str) -> bool:
    t = text.lower()
    if any(m in t for m in WEAK_MARKERS):
        return True
    if t.count(" then ") >= 2:
        return True
    if len(text) > 300:
        return True
    return False


# =============================================================================
#                          OPENWEBUI CLIENT
# =============================================================================

def call_openwebui(
    system_prompt: str,
    user_prompt: str,
    model: str,
    base_url: str,
    api_key: Optional[str] = None,
    temperature: float = 0.15,
    max_tokens: int = 256,
    timeout: int = 120,
) -> str:
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    endpoints = [
        "/api/chat/completions",
        "/v1/chat/completions",
        "/ollama/v1/chat/completions",
    ]
    errors = []

    for ep in endpoints:
        try:
            resp = requests.post(
                f"{base_url}{ep}",
                headers=headers,
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "stream": False,
                },
                timeout=timeout,
            )
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
#                    PROMPTS
# =============================================================================

SYSTEM_PROMPT = """You generate concise task descriptions for a Fortran code generation benchmark.

Given a Fortran program, write a SHORT instruction describing WHAT the program does,
not HOW it is implemented.

STRICT RULES:

1. Describe the COMPUTATIONAL TASK only.
   GOOD: "Compute the mean, standard deviation, and standard error of a numeric array."
   BAD: "Write a program that declares an array, loops from 1 to N, accumulates a sum..."

2. Do NOT mention variable names, loop indices, or implementation details.
   GOOD: "Implement the SAXPY operation (y = alpha*x + y) with stride support."
   BAD: "Write code that uses variables sx, sy, alpha, strideX, strideY..."

3. Do NOT describe the program structure.
   Do NOT mention: main program, subroutines, functions, modules, print statements,
   initialization steps, wrapper code, helper subroutines, or how results are displayed.
   GOOD: "Implement a spatial interpolation that fills missing values in a 2D grid
          using inverse-distance weighting from neighboring points."
   BAD: "Create a main program that calls a function oil_spill_fill, which uses
         nested do loops and prints the resulting grid."

4. Keep it to 1-3 sentences. Be precise about the computation.

5. Start the instruction with a natural request for Fortran 90 code.
   Preferred openings:
   "Write a Fortran 90 program that...",
   "Create a Fortran 90 program that...",
   "Develop a Fortran 90 program that...",
   "Implement a Fortran 90 program that...",
   "Design a Fortran 90 program that..."

6. If the code involves a known algorithm or numerical method, NAME it.

7. The instruction must explicitly mention Fortran 90 in the opening.

8. Output ONLY the instruction text. No quotes, no JSON, no markdown, no preamble.

9. Do NOT enumerate sequential operations from the code.
   Avoid "compute X, then add Y, then generate Z".
   Prefer a single functional description of the overall task.

10. Do NOT describe trivial output actions as the main task.
    Avoid "print", "display", "output", "show"
    unless the core task is genuinely about formatting.

11. For parallel code, describe the computational goal, not the parallel structure.
    Do NOT say "Implement a nested parallel loop..." or "Use OpenMP to ...".

12. If the code is very simple or mainly demonstrative, produce the shortest
    acceptable high-level task description possible.
"""


REWRITE_SYSTEM_PROMPT = """You rewrite weak Fortran benchmark instructions.

Goal: turn a code-structure-based or overly detailed instruction into a concise
functional task description.

STRICT RULES:
1. Keep the meaning, but make it more abstract and benchmark-style.
2. Do NOT mention printing, displaying, loops, initialization, wrapper code,
   subroutines, modules, or helper functions.
3. Focus on the computational goal.
4. Keep it short: 1-2 sentences maximum.
5. Start with a verb like "Compute...", "Implement...", "Determine...", etc.
6. Output ONLY the rewritten instruction text. No quotes, no markdown.
"""


def build_user_prompt(rec: Dict[str, Any]) -> str:
    code = rec.get("generated_code", "")
    stdout = rec.get("run_stdout", "") or ""
    if len(stdout) > 400:
        stdout = stdout[:400] + "\n[... truncated]"

    return f"""Write a concise task instruction for the following Fortran program.

Runtime output (shows what the program computes):
{stdout if stdout else "<no output captured>"}

Code:
{code}

Output ONLY the instruction text.
"""


def build_rewrite_prompt(instruction: str, rec: Dict[str, Any]) -> str:
    stdout = rec.get("run_stdout", "") or ""
    code = rec.get("generated_code", "")
    if len(stdout) > 300:
        stdout = stdout[:300] + "\n[... truncated]"

    return f"""Rewrite this instruction so it describes the computational task
rather than the code structure.

Current instruction:
{instruction}

Runtime output:
{stdout if stdout else "<no output captured>"}

Code:
{code}

Output ONLY the rewritten instruction text.
"""


# =============================================================================
#                    NETTOYAGE
# =============================================================================

def clean_instruction(text: str) -> str:
    text = text.strip()
    if len(text) > 2 and text[0] in '"\'`' and text[-1] == text[0]:
        text = text[1:-1].strip()

    for p in ["Instruction:", "Task:", "Task description:",
              "Here is the instruction:", "The instruction is:",
              "Here is the task:", "The task is:"]:
        if text.lower().startswith(p.lower()):
            text = text[len(p):].strip()

    text = text.replace("```", "").strip()

    lines = text.split("\n")
    while lines and not lines[0].strip():
        lines.pop(0)
    text = "\n".join(lines).strip()

    if text and text[-1] not in ".!?":
        text += "."

    return text


# =============================================================================
#                    JSON I/O
# =============================================================================

def load_input_json(path: str) -> List[Dict[str, Any]]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Input file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"{path} must contain a JSON list")
    if len(data) == 0:
        raise ValueError(f"{path} is an empty list")
    return data


def load_output_json(path: str) -> List[Dict[str, Any]]:
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError):
        backup = path + f".corrupt.{int(time.time())}"
        try:
            os.rename(path, backup)
        except OSError:
            pass
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
#                    PIPELINE
# =============================================================================

def generate_instruction(
    rec: Dict[str, Any],
    origin_id: int,
    model: str,
    base_url: str,
    api_key: Optional[str],
    llm_timeout: int,
) -> Tuple[str, bool]:
    """Génère une instruction avec réécriture si nécessaire.
    Retourne (instruction, was_rewritten).
    """

    # === Passe 1 ===
    raw = call_openwebui(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=build_user_prompt(rec),
        model=model, base_url=base_url, api_key=api_key,
        temperature=0.15, max_tokens=256, timeout=llm_timeout,
    )
    instruction = clean_instruction(raw)
    instruction = enforce_prefix(instruction, origin_id)

    if not instruction or len(instruction) < 20:
        raise ValueError(f"Instruction too short: '{instruction}'")

    # === Passe 2 si faible ===
    if instruction_needs_rewrite(instruction):
        try:
            raw2 = call_openwebui(
                system_prompt=REWRITE_SYSTEM_PROMPT,
                user_prompt=build_rewrite_prompt(instruction, rec),
                model=model, base_url=base_url, api_key=api_key,
                temperature=0.1, max_tokens=200, timeout=llm_timeout,
            )
            rewritten = clean_instruction(raw2)
            rewritten = enforce_prefix(rewritten, origin_id)

            if rewritten and len(rewritten) >= 20:
                if not instruction_needs_rewrite(rewritten) or len(rewritten) < len(instruction):
                    return rewritten, True
        except Exception:
            pass

    return instruction, False


def build_dataset(
    input_path: str,
    output_path: str,
    errors_path: str,
    model: str,
    base_url: str,
    api_key: Optional[str],
    llm_timeout: int,
    max_items: Optional[int],
    sleep_sec: float,
    log_file: str,
):
    setup_logging(log_file)

    log.info("=" * 60)
    log.info(f"TYPE A BUILD v4 — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log.info("=" * 60)

    try:
        data = load_input_json(input_path)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
        log.error(f"FATAL: {e}")
        sys.exit(1)

    if max_items:
        data = data[:max_items]

    dataset = load_output_json(output_path)
    errors = load_output_json(errors_path)

    done_ids = set()
    for item in dataset:
        oid = item.get("source_origin_id")
        if oid is not None:
            done_ids.add(oid)
    for item in errors:
        oid = item.get("source_origin_id")
        if oid is not None:
            done_ids.add(oid)

    remaining = [r for r in data if r.get("origin_id") not in done_ids]
    next_id = len(dataset) + 1

    log.info(f"Input            : {len(data)}")
    log.info(f"Already done     : {len(done_ids)}")
    log.info(f"Remaining        : {len(remaining)}")
    log.info(f"Model            : {model}")
    log.info("")

    if not remaining:
        log.info("Nothing to process.")
        return

    run_start = time.time()
    done = 0
    rewrite_count = 0

    for rec in data:
        origin_id = rec.get("origin_id")
        if origin_id in done_ids:
            continue

        t0 = time.time()
        axes = compute_axes(rec)
        code = rec.get("generated_code", "")

        try:
            instruction, was_rewritten = generate_instruction(
                rec, origin_id, model, base_url, api_key, llm_timeout,
            )
            if was_rewritten:
                rewrite_count += 1

        except Exception as e:
            log.warning(f"  Error oid={origin_id}: {e}")
            errors.append({
                "source_origin_id": origin_id,
                "error": str(e)[:200],
            })
            done += 1
            done_ids.add(origin_id)
            save_json(output_path, dataset)
            save_json(errors_path, errors)

            elapsed = time.time() - run_start
            eta = (elapsed / done * (len(remaining) - done) / 60) if done else 0
            log.info(f"[{done}/{len(remaining)}] oid={origin_id:>4d}  "
                     f"✗ ERROR  ({time.time()-t0:.1f}s, ETA {eta:.0f}min)")
            if sleep_sec > 0:
                time.sleep(sleep_sec)
            continue

        entry = {
            "id": f"type_a_{next_id:04d}",
            "type": "A",
            "source_origin_id": origin_id,
            "instruction": instruction,
            "output": code,
            "axes": axes,
            "metadata": {
                "category": rec.get("category"),
                "quality": rec.get("quality"),
                "complexity_score": rec.get("features", {}).get("complexity_score"),
                "applicable_patterns": rec.get("applicable_patterns", []),
                "run_stdout": rec.get("run_stdout"),
                "was_rewritten": was_rewritten,
            },
        }

        dataset.append(entry)
        next_id += 1
        done += 1
        done_ids.add(origin_id)

        elapsed = time.time() - run_start
        eta = (elapsed / done * (len(remaining) - done) / 60) if done else 0
        preview = instruction[:55] + "..." if len(instruction) > 55 else instruction
        rw_tag = " [RW]" if was_rewritten else ""

        log.info(f"[{done}/{len(remaining)}] oid={origin_id:>4d}  "
                 f"✓ {axes}  \"{preview}\"{rw_tag}  "
                 f"({time.time()-t0:.1f}s, ETA {eta:.0f}min)")

        save_json(output_path, dataset)
        save_json(errors_path, errors)

        if sleep_sec > 0:
            time.sleep(sleep_sec)

    total = (time.time() - run_start) / 60
    axis_counts = Counter()
    for item in dataset:
        for ax in item.get("axes", []):
            axis_counts[ax] += 1

    log.info("")
    log.info("=" * 60)
    log.info(f"TYPE A DONE — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log.info(f"Duration       : {total:.1f} min")
    log.info(f"Dataset size   : {len(dataset)} → {output_path}")
    log.info(f"Errors         : {len(errors)} → {errors_path}")
    log.info(f"Rewritten      : {rewrite_count}/{done}")
    log.info(f"Axes coverage  :")
    for ax, cnt in axis_counts.most_common():
        log.info(f"  {ax:>10s} : {cnt}")
    log.info("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Build Type A dataset v4 final"
    )
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--errors-output",
                        default="dataset/type_a/type_a_errors.json")
    parser.add_argument("--model", required=True)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--api-key", default=None)
    parser.add_argument("--llm-timeout", type=int, default=120)
    parser.add_argument("--max-items", type=int, default=None)
    parser.add_argument("--sleep", type=float, default=0.5)
    parser.add_argument("--log-file",
                        default="dataset/type_a/type_a_build.log")

    args = parser.parse_args()

    build_dataset(
        input_path=args.input,
        output_path=args.output,
        errors_path=args.errors_output,
        model=args.model,
        base_url=args.base_url,
        api_key=args.api_key or os.environ.get("OPENWEBUI_API_KEY"),
        llm_timeout=args.llm_timeout,
        max_items=args.max_items,
        sleep_sec=args.sleep,
        log_file=args.log_file,
    )