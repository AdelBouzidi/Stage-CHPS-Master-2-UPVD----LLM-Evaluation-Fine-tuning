"""
Filtrage binaire (keep/reject) des programmes Fortran fidèles.
Version finale — taxonomie alignée sur les 64 patterns officiels.

Stratégie :
  1. Préfiltrage heuristique → reject immédiat si trivial
  2. Passe 1 LLM → keep/reject avec confiance
  3. Si ambigu : passe 2 avec contexte de la passe 1
  4. Si toujours ambigu : passe 3 finale forcée
  5. Doute persistant → reject par sécurité

Sortie : 2 fichiers
  - final_keep.json
  - final_reject.json
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
from typing import Dict, Any, List, Optional, Tuple


# =============================================================================
#        TAXONOMIE OFFICIELLE — 64 PATTERNS, 5 GROUPES
# =============================================================================

TAXONOMY = {
    "compile_err": [
        "allocation_error",
        "character_length_mismatch",
        "contains_section_error",
        "data_attribute_conflict",
        "implicit_none_missing",
        "intent_violation",
        "invalid_array_bounds",
        "invalid_dummy_argument",
        "invalid_token_or_name",
        "missing_interface_block",
        "missing_main_program",
        "module_use_error",
        "pointer_declaration_error",
        "subroutine_function_mismatch",
        "syntax_error",
        "syntax_invalid_condition",
        "syntax_invalid_expression",
        "syntax_invalid_write",
        "syntax_loop_error",
        "syntax_missing_end",
        "syntax_missing_parenthesis",
        "syntax_missing_then",
        "syntax_unexpected_statement",
        "type_mismatch",
        "undeclared_type",
        "undeclared_variable",
        "undefined_reference",
        "wrong_kind_specifier",
    ],
    "runtime_err": [
        "allocation_runtime_error",
        "array_bounds_runtime",
        "division_by_zero",
        "eof_input",
        "floating_point_exception",
        "integer_overflow",
        "interactive_prompt_leak",
        "invalid_numeric_input",
        "malloc_corruption",
        "segmentation_fault",
        "stdin_format_mismatch",
        "unallocated_access",
    ],
    "ineq": [
        "bool_output_mismatch",
        "edge_case_failure",
        "extra_output_elements",
        "incorrect_condition",
        "missing_output_elements",
        "off_by_one_error",
        "output_format_mismatch",
        "partial_output",
        "precision_loss",
        "whitespace_mismatch",
        "wrong_index_base",
        "wrong_loop_bounds",
        "wrong_numeric_result",
        "wrong_string_output",
    ],
    "parallel_err": [
        "invalid_directive_syntax",
        "loop_dependency_violation",
        "missing_private_clause",
        "missing_reduction_clause",
        "openacc_openmp_mistranslation",
        "race_condition",
        "wrong_shared_variable",
    ],
    "exception": [
        "explanation_leak",
        "markdown_wrapping",
        "utf8_decode_error",
    ],
}

# Ensembles dérivés pour validation rapide
VALID_GROUPS = set(TAXONOMY.keys())
VALID_PATTERNS = set()
for patterns in TAXONOMY.values():
    VALID_PATTERNS.update(patterns)

# Chaîne formatée pour le prompt LLM
def _build_taxonomy_prompt_block() -> str:
    lines = []
    for group, patterns in TAXONOMY.items():
        lines.append(f"  {group}:")
        for p in patterns:
            lines.append(f"    - {p}")
    return "\n".join(lines)

TAXONOMY_PROMPT_BLOCK = _build_taxonomy_prompt_block()


# =============================================================================
#                          LOGGING
# =============================================================================

def setup_logging(log_file: str = "filter.log"):
    logger = logging.getLogger("filter")
    logger.setLevel(logging.INFO)
    if logger.handlers:
        logger.handlers.clear()

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


log = logging.getLogger("filter")


# =============================================================================
#                          OPENWEBUI CLIENT
# =============================================================================

def call_openwebui(
    system_prompt: str,
    user_prompt: str,
    model: str,
    base_url: str,
    api_key: Optional[str] = None,
    temperature: float = 0.0,
    max_tokens: int = 768,
    timeout: int = 180,
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


def extract_json(text: str) -> Dict[str, Any]:
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end > start:
        try:
            return json.loads(text[start:end + 1])
        except json.JSONDecodeError:
            pass

    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass

    raise ValueError(f"Cannot parse JSON: {text[:300]}")


# =============================================================================
#                    JSON I/O ROBUSTE
# =============================================================================

def load_json(path: str) -> List[Dict[str, Any]]:
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError) as e:
        log.warning(f"  {path} corrompu ({e}), sauvegarde et reset")
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


def get_processed_ids(*lists) -> set:
    ids = set()
    for lst in lists:
        for x in lst:
            oid = x.get("origin_id")
            if oid is not None:
                ids.add(oid)
    return ids


# =============================================================================
#                    HEURISTIC PREFILTER
# =============================================================================

def compute_features(code: str) -> Dict[str, Any]:
    lines = code.splitlines()
    nonempty = [l for l in lines if l.strip()]
    comments = [l for l in nonempty
                if l.strip().startswith("!") or l.strip().lower().startswith("c ")]
    code_lines = len(nonempty) - len(comments)

    lc = code.lower()

    features = {
        "num_lines_nonempty": len(nonempty),
        "num_code_lines": code_lines,
        "num_comment_lines": len(comments),
        "num_prints": len(re.findall(r"\bprint\b|\bwrite\b", lc)),
        "num_loops": len(re.findall(r"\bdo\b", lc)),
        "num_ifs": len(re.findall(r"\bif\b", lc)),
        "num_calls": len(re.findall(r"\bcall\b", lc)),
        "num_allocates": len(re.findall(r"\ballocate\b", lc)),
        "has_program": bool(re.search(r"\bprogram\b", lc)),
        "has_subroutine": bool(re.search(r"\bsubroutine\b", lc)),
        "has_function": bool(re.search(r"\bfunction\b", lc)),
        "has_module": bool(re.search(r"\bmodule\b", lc)),
        "has_contains": "contains" in lc,
        "has_implicit_none": "implicit none" in lc,
        "has_array_syntax": bool(re.search(
            r"dimension|allocatable|\([^)]*:[^)]*\)", lc)),
        "has_stub": "! stub:" in lc or "warning: stub" in lc,
        "has_derived_type": bool(re.search(r"\btype\s*::", lc) or
                                 re.search(r"\btype\s*\(", lc)),
        "has_select_type": "select type" in lc,
        "has_pointer": bool(re.search(r"\bpointer\b", lc)),
        "has_recursion": bool(re.search(r"\brecursive\b", lc)),
    }

    score = 0
    score += min(features["num_loops"], 5) * 2
    score += min(features["num_ifs"], 5) * 2
    score += min(features["num_calls"], 4)
    score += 2 if features["has_array_syntax"] else 0
    score += 2 if features["has_subroutine"] or features["has_function"] else 0
    score += 1 if features["has_contains"] else 0
    score += 1 if features["has_module"] else 0
    score += 2 if features["has_derived_type"] else 0
    score += 2 if features["has_select_type"] else 0
    score += 1 if features["has_pointer"] else 0
    score += 1 if features["has_recursion"] else 0
    features["complexity_score"] = score

    return features


def heuristic_reject(code: str, features: Dict) -> Optional[str]:
    if not code.strip():
        return "empty_code"
    if features["num_code_lines"] < 5:
        return "too_few_code_lines"
    if features["num_lines_nonempty"] > 500:
        return "too_long"
    if features["complexity_score"] < 2:
        return "too_trivial"
    return None


# =============================================================================
#                    PROMPTS LLM
# =============================================================================

SYSTEM_PROMPT = """You are reviewing autonomous Fortran programs for a fine-tuning dataset.
You MUST return ONLY a valid JSON object with the exact fields specified.
No markdown, no explanation, no text outside the JSON."""


PASS1_TEMPLATE = """Evaluate this Fortran program for inclusion in a fine-tuning dataset.

Return ONLY JSON with these exact fields:
{{
  "decision": "keep" or "reject",
  "confidence": "high" or "low",
  "good_for_type_a": true/false,
  "good_for_type_b": true/false,
  "applicable_error_groups": ["group1", ...],
  "applicable_patterns": ["pattern1", ...],
  "category": "strong" or "acceptable" or "borderline" or "poor",
  "reason_short": "one sentence"
}}

Rules:
- "keep" = useful, non-trivial, has real computational logic worth learning from
- "reject" = too trivial, only prints, no real logic, not pedagogically useful
- "confidence": "high" if certain, "low" if borderline or unsure
- Type A = good for direct code generation tasks
- Type B = good base for injecting controlled errors for debugging tasks

IMPORTANT: You MUST choose patterns ONLY from the official taxonomy below.
Do NOT invent new pattern names. Only list patterns that could REALISTICALLY
be injected into THIS specific code.

Official taxonomy (5 groups, 64 patterns):
{taxonomy}

Code metrics:
- Lines of code: {num_code_lines}
- Loops: {num_loops}, Ifs: {num_ifs}, Calls: {num_calls}
- Has subroutine: {has_subroutine}, Has function: {has_function}
- Arrays: {has_array_syntax}, Derived types: {has_derived_type}
- Complexity score: {complexity_score}

Runtime output (first 600 chars):
{run_stdout}

Code:
{code}
"""


PASS2_TEMPLATE = """You previously evaluated this Fortran program with LOW confidence.

Your previous assessment:
  decision: {prev_decision}
  reason: {prev_reason}

Re-examine carefully. Focus on:
1. Does it contain real computational logic (math, algorithms, data structures)?
2. Could a student learn something useful from this code?
3. Is there enough structure to inject realistic Fortran errors?

Keep if the code has clear pedagogical value or realistic injection potential.
Reject if it is truly just a demo wrapper with no substance.

Return ONLY JSON with the same fields:
{{
  "decision": "keep" or "reject",
  "confidence": "high" or "low",
  "good_for_type_a": true/false,
  "good_for_type_b": true/false,
  "applicable_error_groups": [...],
  "applicable_patterns": [...],
  "category": "strong" or "acceptable" or "borderline" or "poor",
  "reason_short": "one sentence"
}}

IMPORTANT: patterns MUST come from the official taxonomy only:
{taxonomy}

Code:
{code}
"""


PASS3_TEMPLATE = """FINAL evaluation. You reviewed this code twice with uncertain results.

Previous assessments:
  Pass 1: decision={p1_decision}, confidence={p1_confidence}, reason="{p1_reason}"
  Pass 2: decision={p2_decision}, confidence={p2_confidence}, reason="{p2_reason}"

Give a DEFINITIVE answer. No ambiguity. Choose "keep" or "reject".
Conservative guideline: if truly borderline with no clear value, choose "reject".

Return ONLY JSON:
{{
  "decision": "keep" or "reject",
  "confidence": "high",
  "good_for_type_a": true/false,
  "good_for_type_b": true/false,
  "applicable_error_groups": [...],
  "applicable_patterns": [...],
  "category": "strong" or "acceptable" or "borderline" or "poor",
  "reason_short": "one sentence"
}}

Patterns MUST come from official taxonomy only:
{taxonomy}

Code:
{code}
"""


def format_pass1(rec: Dict, features: Dict) -> str:
    code = rec.get("generated_code", "")
    stdout = rec.get("run_stdout", "") or ""
    return PASS1_TEMPLATE.format(
        taxonomy=TAXONOMY_PROMPT_BLOCK,
        num_code_lines=features["num_code_lines"],
        num_loops=features["num_loops"],
        num_ifs=features["num_ifs"],
        num_calls=features["num_calls"],
        has_subroutine=features["has_subroutine"],
        has_function=features["has_function"],
        has_array_syntax=features["has_array_syntax"],
        has_derived_type=features["has_derived_type"],
        complexity_score=features["complexity_score"],
        run_stdout=stdout[:600] if stdout else "<empty>",
        code=code,
    )


def format_pass2(code: str, prev: Dict) -> str:
    return PASS2_TEMPLATE.format(
        taxonomy=TAXONOMY_PROMPT_BLOCK,
        prev_decision=prev.get("decision", "unknown"),
        prev_reason=prev.get("reason_short", ""),
        code=code,
    )


def format_pass3(code: str, p1: Dict, p2: Dict) -> str:
    return PASS3_TEMPLATE.format(
        taxonomy=TAXONOMY_PROMPT_BLOCK,
        p1_decision=p1.get("decision", "unknown"),
        p1_confidence=p1.get("confidence", "unknown"),
        p1_reason=p1.get("reason_short", ""),
        p2_decision=p2.get("decision", "unknown"),
        p2_confidence=p2.get("confidence", "unknown"),
        p2_reason=p2.get("reason_short", ""),
        code=code,
    )


# =============================================================================
#                    SANITIZE — FILTRAGE STRICT
# =============================================================================

def sanitize_review(obj: Dict) -> Dict:
    decision = obj.get("decision", "reject")
    if decision not in ("keep", "reject"):
        decision = "reject"

    confidence = obj.get("confidence", "low")
    if confidence not in ("high", "low"):
        confidence = "low"

    category = obj.get("category", "borderline")
    if category not in ("strong", "acceptable", "borderline", "poor"):
        category = "borderline"

    # FILTRAGE STRICT : seuls les groupes officiels
    groups = [g for g in obj.get("applicable_error_groups", [])
              if isinstance(g, str) and g in VALID_GROUPS]

    # FILTRAGE STRICT : seuls les patterns officiels
    raw_patterns = obj.get("applicable_patterns", [])
    if not isinstance(raw_patterns, list):
        raw_patterns = []
    patterns = [p for p in raw_patterns
                if isinstance(p, str) and p.strip() in VALID_PATTERNS]

    # Cohérence : vérifier que les patterns appartiennent aux groupes déclarés
    if groups and patterns:
        valid_for_groups = set()
        for g in groups:
            valid_for_groups.update(TAXONOMY.get(g, []))
        patterns = [p for p in patterns if p in valid_for_groups]

    return {
        "decision": decision,
        "confidence": confidence,
        "good_for_type_a": bool(obj.get("good_for_type_a", False)),
        "good_for_type_b": bool(obj.get("good_for_type_b", False)),
        "applicable_error_groups": groups,
        "applicable_patterns": patterns[:15],
        "category": category,
        "reason_short": str(obj.get("reason_short", "")).strip()[:200] or "no_reason",
    }


def needs_another_pass(review: Dict) -> bool:
    if review["confidence"] == "low":
        return True
    if review["category"] == "borderline":
        return True
    if review["decision"] == "keep" and review["category"] == "poor":
        return True
    if review["decision"] == "reject" and review["category"] == "strong":
        return True
    return False


# =============================================================================
#                    EVALUATION MULTI-PASS
# =============================================================================

def evaluate_with_llm(
    rec: Dict,
    features: Dict,
    model: str,
    base_url: str,
    api_key: Optional[str],
    llm_timeout: int,
) -> Tuple[Dict, int, str]:

    code = rec.get("generated_code", "")

    # === PASSE 1 ===
    try:
        raw1 = call_openwebui(SYSTEM_PROMPT, format_pass1(rec, features),
                              model, base_url, api_key,
                              temperature=0.0, max_tokens=768,
                              timeout=llm_timeout)
        review1 = sanitize_review(extract_json(raw1))
    except Exception as e:
        log.warning(f"  Pass 1 error: {e}")
        return _make_reject(f"llm_error_pass1: {str(e)[:80]}"), 1, "llm_error"

    if not needs_another_pass(review1):
        return review1, 1, "llm_pass1"

    log.info(f"    → Pass 1 ambigu (conf={review1['confidence']}, "
             f"cat={review1['category']}), pass 2...")

    # === PASSE 2 ===
    try:
        raw2 = call_openwebui(SYSTEM_PROMPT, format_pass2(code, review1),
                              model, base_url, api_key,
                              temperature=0.1, max_tokens=768,
                              timeout=llm_timeout)
        review2 = sanitize_review(extract_json(raw2))
    except Exception as e:
        log.warning(f"  Pass 2 error: {e}")
        review1["confidence"] = "high"
        return review1, 2, "llm_pass2_error"

    if not needs_another_pass(review2):
        return review2, 2, "llm_pass2"

    if review1["decision"] == review2["decision"]:
        review2["confidence"] = "high"
        return review2, 2, "llm_pass2_agreement"

    log.info(f"    → Contradiction p1={review1['decision']} vs "
             f"p2={review2['decision']}, pass 3 finale...")

    # === PASSE 3 ===
    try:
        raw3 = call_openwebui(SYSTEM_PROMPT, format_pass3(code, review1, review2),
                              model, base_url, api_key,
                              temperature=0.0, max_tokens=768,
                              timeout=llm_timeout)
        review3 = sanitize_review(extract_json(raw3))
        review3["confidence"] = "high"
        return review3, 3, "llm_pass3"
    except Exception as e:
        log.warning(f"  Pass 3 error: {e}")
        return _make_reject("tiebreak_reject_after_3_passes"), 3, "tiebreak_reject"


def _make_reject(reason: str) -> Dict:
    return {
        "decision": "reject",
        "confidence": "high",
        "good_for_type_a": False,
        "good_for_type_b": False,
        "applicable_error_groups": [],
        "applicable_patterns": [],
        "category": "poor",
        "reason_short": reason,
    }


# =============================================================================
#                    PIPELINE
# =============================================================================

def process_dataset(
    input_path: str,
    keep_path: str,
    reject_path: str,
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
    log.info(f"FILTER START — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log.info(f"Taxonomy: {len(VALID_GROUPS)} groups, {len(VALID_PATTERNS)} patterns")
    log.info("=" * 60)

    data = load_json(input_path)
    if not data:
        log.error(f"No data in {input_path}")
        return
    if max_items:
        data = data[:max_items]

    keep = load_json(keep_path)
    reject = load_json(reject_path)
    processed_ids = get_processed_ids(keep, reject)
    remaining = [r for r in data if r.get("origin_id") not in processed_ids]

    log.info(f"Input            : {len(data)}")
    log.info(f"Already kept     : {len(keep)}")
    log.info(f"Already rejected : {len(reject)}")
    log.info(f"Remaining        : {len(remaining)}")
    log.info(f"Model            : {model}")
    log.info("")

    if not remaining:
        log.info("Nothing to process.")
        return

    counts = {"keep": 0, "rej_heur": 0, "rej_llm": 0}
    pass_counts = {1: 0, 2: 0, 3: 0}
    run_start = time.time()
    done = 0

    for rec in data:
        origin_id = rec.get("origin_id")
        if origin_id in processed_ids:
            continue

        t0 = time.time()
        code = rec.get("generated_code", "") or ""
        features = compute_features(code)

        # --- Heuristique ---
        rej = heuristic_reject(code, features)
        if rej:
            reject.append({
                "origin_id": origin_id,
                "decision": "reject",
                "decision_stage": "heuristic",
                "num_passes": 0,
                "reason_short": rej,
                "features": features,
            })
            counts["rej_heur"] += 1
            done += 1
            status = f"✗ REJECT (heuristic: {rej})"

        else:
            # --- LLM multi-pass ---
            review, npasses, stage = evaluate_with_llm(
                rec, features, model, base_url, api_key, llm_timeout)
            pass_counts[npasses] = pass_counts.get(npasses, 0) + 1

            entry = {
                "origin_id": origin_id,
                "decision": review["decision"],
                "decision_stage": stage,
                "num_passes": npasses,
                "good_for_type_a": review["good_for_type_a"],
                "good_for_type_b": review["good_for_type_b"],
                "applicable_error_groups": review["applicable_error_groups"],
                "applicable_patterns": review["applicable_patterns"],
                "category": review["category"],
                "reason_short": review["reason_short"],
                "features": features,
            }

            if review["decision"] == "keep":
                entry["generated_code"] = code
                entry["run_stdout"] = rec.get("run_stdout")
                entry["quality"] = rec.get("quality")
                keep.append(entry)
                counts["keep"] += 1
                np_str = len(review["applicable_patterns"])
                status = (f"✓ KEEP  p={npasses} cat={review['category']} "
                          f"A={review['good_for_type_a']} "
                          f"B={review['good_for_type_b']} "
                          f"patterns={np_str}")
            else:
                reject.append(entry)
                counts["rej_llm"] += 1
                status = (f"✗ REJECT p={npasses} "
                          f"({review['reason_short'][:50]})")

            done += 1

        processed_ids.add(origin_id)

        elapsed = time.time() - run_start
        eta = (elapsed / done * (len(remaining) - done) / 60) if done else 0

        log.info(f"[{done}/{len(remaining)}] "
                 f"oid={origin_id:>4d}  {status}  "
                 f"({time.time()-t0:.1f}s, ETA {eta:.0f}min)")

        save_json(keep_path, keep)
        save_json(reject_path, reject)

        if sleep_sec > 0:
            time.sleep(sleep_sec)

    total = (time.time() - run_start) / 60
    log.info("")
    log.info("=" * 60)
    log.info(f"FILTER DONE — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log.info(f"Duration : {total:.1f} min")
    log.info(f"Keep     : {len(keep):>4d}  → {keep_path}")
    log.info(f"Reject   : {len(reject):>4d}  → {reject_path}")
    log.info(f"This run : keep={counts['keep']} "
             f"rej_heur={counts['rej_heur']} rej_llm={counts['rej_llm']}")
    log.info(f"Passes   : 1-pass={pass_counts.get(1,0)} "
             f"2-pass={pass_counts.get(2,0)} 3-pass={pass_counts.get(3,0)}")
    log.info("=" * 60)


# =============================================================================
#                    MAIN
# =============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Binary filter (keep/reject) with official 64-pattern taxonomy"
    )
    parser.add_argument("--input", required=True)
    parser.add_argument("--keep-output", required=True)
    parser.add_argument("--reject-output", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--api-key", default=None)
    parser.add_argument("--llm-timeout", type=int, default=180)
    parser.add_argument("--max-items", type=int, default=None)
    parser.add_argument("--sleep", type=float, default=0.5)
    parser.add_argument("--log-file", default="filter.log")

    args = parser.parse_args()

    process_dataset(
        input_path=args.input,
        keep_path=args.keep_output,
        reject_path=args.reject_output,
        model=args.model,
        base_url=args.base_url,
        api_key=args.api_key or os.environ.get("OPENWEBUI_API_KEY"),
        llm_timeout=args.llm_timeout,
        max_items=args.max_items,
        sleep_sec=args.sleep,
        log_file=args.log_file,
    )