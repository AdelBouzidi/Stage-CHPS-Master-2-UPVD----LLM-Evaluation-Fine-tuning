"""
Pipeline de reconstruction de programmes Fortran autonomes avec vérification de fidélité.

Niveau 1 : Génération du wrapper + compilation + exécution
Niveau 2 : Vérification de fidélité sémantique par LLM (même modèle)
Niveau 3 : Re-génération ciblée des cas "degraded"

Sortie :
  - accepted_faithful.json   : code fidèle, prêt pour le dataset
  - accepted_degraded.json   : code compilable mais sémantique altérée (à corriger)
  - skipped.json             : échecs de compilation/exécution/SKIP


- Le LLM génère d’abord une version autonome du code.
- Le script la compile et l’exécute.
- Si ça marche, il redonne ce code au LLM pour vérifier la fidélité scientifique.
- Si le LLM dit faithful, le code va dans le fichier des fidèles.
- Si le LLM dit degraded, le script peut demander une seule réparation.
- Cette version réparée est ensuite recompilée, réexécutée, puis revérifiée.

Le mot “revérifiée” veut seulement dire ceci :
le LLM a déjà généré une première version,
puis, si elle est degraded, il génère une seule version réparée,
ensuite cette version réparée est contrôlée à nouveau, mais pas réparée une deuxième fois.
"""

import json
import requests
import argparse
import os
import re
import time
import tempfile
import subprocess
from typing import Dict, Any, List, Optional


# =============================================================================
#                          OPEN WEBUI CLIENT
# =============================================================================

def call_openwebui(
    prompt: str,
    model: str,
    base_url: str = "http://localhost:8080",
    api_key: str = None,
    temperature: float = 0.0,
    max_tokens: int = 4096,
    timeout: int = 240,
) -> str:
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    endpoints_to_try = [
        "/api/chat/completions",
        "/v1/chat/completions",
        "/ollama/v1/chat/completions",
    ]
    errors = []

    for endpoint in endpoints_to_try:
        try:
            response = requests.post(
                f"{base_url}{endpoint}",
                headers=headers,
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "stream": False,
                },
                timeout=timeout,
            )
            if response.status_code == 200:
                try:
                    result = response.json()
                except Exception:
                    errors.append(f"{endpoint}: HTTP 200 but invalid JSON")
                    continue

                if "choices" in result and len(result["choices"]) > 0:
                    return result["choices"][0]["message"]["content"]
                if "message" in result and isinstance(result["message"], dict):
                    if "content" in result["message"]:
                        return result["message"]["content"]
                if "response" in result:
                    return result["response"]
                errors.append(f"{endpoint}: HTTP 200 but no usable content")
                continue
            else:
                errors.append(f"{endpoint}: HTTP {response.status_code}")
                continue
        except Exception as e:
            errors.append(f"{endpoint}: {e}")
            continue

    raise RuntimeError("All endpoints failed:\n" + "\n".join(errors))


# =============================================================================
#                          PROMPTS
# =============================================================================

def build_generation_prompt(original_code: str) -> str:
    """Prompt de Niveau 1 : génération du wrapper autonome.
    
    AMÉLIORÉ par rapport à la v1 :
    - Exige explicitement la préservation du corps mathématique
    - Interdit la simplification des expressions
    - Demande des stubs MARQUÉS si une dépendance est irrésoluble
    """
    return f"""Transform the following Fortran source into ONE autonomous executable Fortran 90 program.

CRITICAL RULES — READ CAREFULLY:

1. PRESERVE ALL MATHEMATICAL EXPRESSIONS EXACTLY AS THEY ARE.
   Do NOT simplify, replace, or approximate any formula, equation,
   or computation in subroutines/functions. The scientific content
   MUST remain identical to the original.

2. You may ONLY modify:
   - Add a "program main ... end program main" wrapper
   - Add hardcoded input data (small realistic arrays/scalars)
   - Replace "include" files by inlining the needed declarations
   - Replace external module "use" statements by local declarations
   - Add "implicit none" if missing
   - Print results so the program produces visible output

3. If a called subroutine/function is NOT defined in the source
   and you cannot implement it, insert a stub with this exact comment:
   ! STUB: original implementation not available
   And print a warning at runtime: print *, 'WARNING: stub function called'

4. The program MUST compile with: gfortran -O0
5. The program MUST run without: MPI, OpenMP, OpenACC, external files,
   external libraries, user input (read from stdin), or network access.
6. If it is truly impossible to make it autonomous, return exactly: SKIP

7. Output ONLY the Fortran code. No markdown. No explanations.
   No ``` markers. Just pure Fortran source code.

Source code to transform:
{original_code}
"""


def build_fidelity_check_prompt(original_code: str, generated_code: str) -> str:
    """Prompt de Niveau 2 : vérification de fidélité sémantique."""
    return f"""You are a Fortran code reviewer. Compare the ORIGINAL code with the GENERATED
autonomous version. Your task is to check if the scientific/mathematical content
was preserved faithfully.

Answer ONLY with a JSON object, no other text, no markdown, no explanation.
The JSON must have exactly these fields:

{{
  "body_preserved": true or false,
  "stub_functions": ["list of function names replaced by empty stubs"],
  "simplified_expressions": ["list of descriptions of any math that was changed"],
  "quality": "faithful" or "degraded" or "skeleton_only"
}}

Definitions:
- "faithful": all mathematical expressions, loops, and logic are identical
  to the original. Only the wrapper (program main, hardcoded data, print
  statements) was added. Minor formatting changes are OK.
- "degraded": the program compiles and runs, but some mathematical expressions
  were simplified, some functions were stubbed, or some logic was altered.
  The overall structure is preserved but results may differ.
- "skeleton_only": the body of the main subroutine/function was largely
  rewritten, replaced by trivial code, or the mathematical content is gone.

ORIGINAL:
{original_code}

GENERATED:
{generated_code}
"""


def build_repair_prompt(original_code: str, generated_code: str, issues: dict) -> str:
    """Prompt de Niveau 3 : réparation d'un code dégradé."""
    problems = []
    if issues.get("stub_functions"):
        problems.append(f"- Stub functions: {', '.join(issues['stub_functions'])}")
    if issues.get("simplified_expressions"):
        for s in issues["simplified_expressions"]:
            problems.append(f"- Simplified: {s}")

    problem_text = "\n".join(problems) if problems else "- General degradation detected"

    return f"""The following GENERATED Fortran program compiles and runs, but its scientific
content was degraded compared to the ORIGINAL. Fix the GENERATED code to
restore the ORIGINAL mathematical content exactly.

PROBLEMS DETECTED:
{problem_text}

RULES:
1. Keep the "program main" wrapper and hardcoded data from GENERATED
2. RESTORE all mathematical expressions from ORIGINAL exactly
3. If a function from ORIGINAL cannot be implemented, keep the stub
   but add: ! STUB: original implementation not available
4. Output ONLY Fortran code, no markdown, no explanations
5. If impossible, return exactly: SKIP

ORIGINAL:
{original_code}

GENERATED (to fix):
{generated_code}
"""


# =============================================================================
#                    CODE EXTRACTION & CLEANING
# =============================================================================

def extract_fortran_code_or_skip(response: str) -> str:
    if not response:
        return "SKIP"
    text = response.strip()
    if text == "SKIP":
        return "SKIP"

    patterns = [
        r"```fortran\s*(.*?)```",
        r"```f90\s*(.*?)```",
        r"```\s*(.*?)```",
    ]
    for pattern in patterns:
        matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
        if matches:
            code = matches[0].strip()
            if code:
                return clean_fortran_code(code)

    return clean_fortran_code(text)


def clean_fortran_code(code: str) -> str:
    code = code.strip()
    code = code.replace("```fortran", "").replace("```f90", "").replace("```", "").strip()

    prefixes_to_remove = [
        "Here is the code:", "Here's the code:",
        "Here is the Fortran code:", "Here is the autonomous Fortran program:",
        "Here is a standalone program:", "Standalone program:",
        "Program:", "Code:",
    ]
    for prefix in prefixes_to_remove:
        if code.startswith(prefix):
            code = code[len(prefix):].strip()

    return code.strip()


def extract_json_from_response(response: str) -> Optional[dict]:
    """Extrait un objet JSON de la réponse du LLM, même si entouré de texte."""
    if not response:
        return None
    text = response.strip()

    # Essayer de parser directement
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Chercher un bloc JSON dans la réponse
    # Pattern: trouver { ... } le plus externe
    brace_start = text.find("{")
    brace_end = text.rfind("}")
    if brace_start != -1 and brace_end != -1 and brace_end > brace_start:
        candidate = text[brace_start:brace_end + 1]
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass

    # Chercher dans un bloc markdown ```json ... ```
    json_block = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if json_block:
        try:
            return json.loads(json_block.group(1))
        except json.JSONDecodeError:
            pass

    return None


# =============================================================================
#                    COMPILATION & EXECUTION
# =============================================================================

def compile_fortran(code: str, workdir: str, timeout: int = 30) -> Dict[str, Any]:
    src_path = os.path.join(workdir, "candidate.f90")
    exe_path = os.path.join(workdir, "candidate.out")

    with open(src_path, "w", encoding="utf-8") as f:
        f.write(code)

    cmd = ["gfortran", src_path, "-O0", "-o", exe_path]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True,
                                timeout=timeout, cwd=workdir)
        return {
            "ok": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exe_path": exe_path,
        }
    except subprocess.TimeoutExpired:
        return {"ok": False, "returncode": None, "stdout": "",
                "stderr": "Compilation timeout", "exe_path": exe_path}


def run_executable(exe_path: str, workdir: str, timeout: int = 5) -> Dict[str, Any]:
    try:
        result = subprocess.run([exe_path], input="", capture_output=True,
                                text=True, timeout=timeout, cwd=workdir)
        return {
            "ok": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except subprocess.TimeoutExpired:
        return {"ok": False, "returncode": None, "stdout": "",
                "stderr": "Execution timeout"}
    except Exception as e:
        return {"ok": False, "returncode": None, "stdout": "",
                "stderr": str(e)}


# =============================================================================
#                    JSON I/O
# =============================================================================

def load_json_file(path: str) -> List[Dict[str, Any]]:
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json_file(path: str, data: Any):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# =============================================================================
#               NIVEAU 1 : GENERATION + COMPILE + RUN
# =============================================================================

def level1_generate_and_validate(
    record: Dict[str, Any],
    model: str,
    base_url: str,
    api_key: Optional[str],
    llm_timeout: int,
    compile_timeout: int,
    run_timeout: int,
) -> Dict[str, Any]:
    """Niveau 1 : génère le wrapper, compile, exécute."""
    origin_id = record.get("id")
    original_code = record.get("code", "")

    result = {
        "origin_id": origin_id,
        "original_code": original_code,
        "status": "skipped",
        "reason": None,
        "generated_code": None,
        "run_stdout": None,
        "compile_stderr": None,
        "run_stderr": None,
    }

    if not original_code or not original_code.strip():
        result["reason"] = "empty_input_code"
        return result

    prompt = build_generation_prompt(original_code)

    try:
        response = call_openwebui(
            prompt=prompt, model=model, base_url=base_url,
            api_key=api_key, temperature=0.0, max_tokens=4096,
            timeout=llm_timeout,
        )
    except Exception as e:
        result["reason"] = "llm_call_failed"
        return result

    cleaned = extract_fortran_code_or_skip(response)

    if cleaned == "SKIP":
        result["reason"] = "model_skip"
        return result

    if not cleaned.strip():
        result["reason"] = "empty_model_output"
        return result

    with tempfile.TemporaryDirectory(prefix="fortran_l1_") as tmpdir:
        comp = compile_fortran(cleaned, tmpdir, timeout=compile_timeout)
        if not comp["ok"]:
            result["reason"] = "compile_failed"
            result["generated_code"] = cleaned
            result["compile_stderr"] = comp["stderr"]
            return result

        run = run_executable(comp["exe_path"], tmpdir, timeout=run_timeout)
        if not run["ok"]:
            result["reason"] = "run_failed"
            result["generated_code"] = cleaned
            result["run_stderr"] = run["stderr"]
            return result

    result["status"] = "level1_passed"
    result["generated_code"] = cleaned
    result["run_stdout"] = run["stdout"]
    return result


# =============================================================================
#               NIVEAU 2 : VERIFICATION DE FIDELITE
# =============================================================================

def level2_check_fidelity(
    original_code: str,
    generated_code: str,
    model: str,
    base_url: str,
    api_key: Optional[str],
    llm_timeout: int,
) -> Dict[str, Any]:
    """Niveau 2 : demande au LLM de vérifier la fidélité sémantique."""
    prompt = build_fidelity_check_prompt(original_code, generated_code)

    default_result = {
        "body_preserved": False,
        "stub_functions": [],
        "simplified_expressions": ["fidelity check failed"],
        "quality": "degraded",
    }

    try:
        response = call_openwebui(
            prompt=prompt, model=model, base_url=base_url,
            api_key=api_key, temperature=0.0, max_tokens=1024,
            timeout=llm_timeout,
        )
    except Exception:
        return default_result

    parsed = extract_json_from_response(response)
    if not parsed:
        return default_result

    # Valider les champs attendus
    quality = parsed.get("quality", "degraded")
    if quality not in ("faithful", "degraded", "skeleton_only"):
        quality = "degraded"

    return {
        "body_preserved": parsed.get("body_preserved", False),
        "stub_functions": parsed.get("stub_functions", []),
        "simplified_expressions": parsed.get("simplified_expressions", []),
        "quality": quality,
    }


# =============================================================================
#               NIVEAU 3 : REPARATION DES DEGRADES
# =============================================================================

def level3_repair(
    original_code: str,
    generated_code: str,
    fidelity_issues: dict,
    model: str,
    base_url: str,
    api_key: Optional[str],
    llm_timeout: int,
    compile_timeout: int,
    run_timeout: int,
) -> Optional[str]:
    """Niveau 3 : tente de réparer un code dégradé. Retourne le code corrigé ou None."""
    prompt = build_repair_prompt(original_code, generated_code, fidelity_issues)

    try:
        response = call_openwebui(
            prompt=prompt, model=model, base_url=base_url,
            api_key=api_key, temperature=0.0, max_tokens=4096,
            timeout=llm_timeout,
        )
    except Exception:
        return None

    cleaned = extract_fortran_code_or_skip(response)
    if cleaned == "SKIP" or not cleaned.strip():
        return None

    # Vérifier que le code réparé compile et s'exécute
    with tempfile.TemporaryDirectory(prefix="fortran_l3_") as tmpdir:
        comp = compile_fortran(cleaned, tmpdir, timeout=compile_timeout)
        if not comp["ok"]:
            return None
        run = run_executable(comp["exe_path"], tmpdir, timeout=run_timeout)
        if not run["ok"]:
            return None

    return cleaned


# =============================================================================
#                    PIPELINE PRINCIPAL
# =============================================================================

def process_one_full_pipeline(
    record: Dict[str, Any],
    model: str,
    base_url: str,
    api_key: Optional[str],
    llm_timeout: int,
    compile_timeout: int,
    run_timeout: int,
    do_level2: bool = True,
    do_level3: bool = True,
) -> Dict[str, Any]:
    """Pipeline complet : L1 → L2 → L3."""

    # === NIVEAU 1 ===
    l1 = level1_generate_and_validate(
        record, model, base_url, api_key,
        llm_timeout, compile_timeout, run_timeout,
    )

    if l1["status"] != "level1_passed":
        return {
            "origin_id": l1["origin_id"],
            "status": "skipped",
            "reason": l1["reason"],
            "quality": None,
            "generated_code": l1.get("generated_code"),
            "compile_stderr": l1.get("compile_stderr"),
            "run_stderr": l1.get("run_stderr"),
            "fidelity": None,
        }

    if not do_level2:
        return {
            "origin_id": l1["origin_id"],
            "status": "accepted",
            "reason": None,
            "quality": "unchecked",
            "generated_code": l1["generated_code"],
            "run_stdout": l1.get("run_stdout"),
            "fidelity": None,
        }

    # === NIVEAU 2 ===
    fidelity = level2_check_fidelity(
        l1["original_code"], l1["generated_code"],
        model, base_url, api_key, llm_timeout,
    )

    quality = fidelity["quality"]

    # Si fidèle, on accepte directement
    if quality == "faithful":
        return {
            "origin_id": l1["origin_id"],
            "status": "accepted",
            "reason": None,
            "quality": "faithful",
            "generated_code": l1["generated_code"],
            "run_stdout": l1.get("run_stdout"),
            "fidelity": fidelity,
        }

    # Si dégradé et qu'on fait le niveau 3
    if quality == "degraded" and do_level3:
        repaired = level3_repair(
            l1["original_code"], l1["generated_code"], fidelity,
            model, base_url, api_key,
            llm_timeout, compile_timeout, run_timeout,
        )

        if repaired:
            # Re-vérifier la fidélité du code réparé
            fidelity2 = level2_check_fidelity(
                l1["original_code"], repaired,
                model, base_url, api_key, llm_timeout,
            )

            if fidelity2["quality"] == "faithful":
                return {
                    "origin_id": l1["origin_id"],
                    "status": "accepted",
                    "reason": None,
                    "quality": "repaired_faithful",
                    "generated_code": repaired,
                    "run_stdout": None,  # Stdout du code réparé
                    "fidelity": fidelity2,
                }
            else:
                # Réparation tentée mais toujours dégradé
                return {
                    "origin_id": l1["origin_id"],
                    "status": "accepted_degraded",
                    "reason": "repair_insufficient",
                    "quality": "degraded",
                    "generated_code": repaired,
                    "run_stdout": None,
                    "fidelity": fidelity2,
                }

    # Dégradé sans réparation, ou skeleton_only
    return {
        "origin_id": l1["origin_id"],
        "status": "accepted_degraded" if quality == "degraded" else "skipped",
        "reason": f"quality_{quality}",
        "quality": quality,
        "generated_code": l1["generated_code"],
        "run_stdout": l1.get("run_stdout"),
        "fidelity": fidelity,
    }


# =============================================================================
#                    ORCHESTRATION
# =============================================================================

def rebuild_dataset(
    input_file: str,
    faithful_file: str,
    degraded_file: str,
    skipped_file: str,
    model: str,
    base_url: str,
    api_key: Optional[str],
    llm_timeout: int,
    compile_timeout: int,
    run_timeout: int,
    max_items: Optional[int],
    checkpoint_every: int,
    sleep_sec: float,
    do_level2: bool,
    do_level3: bool,
):
    data = load_json_file(input_file)
    if max_items is not None:
        data = data[:max_items]

    faithful = load_json_file(faithful_file)
    degraded = load_json_file(degraded_file)
    skipped = load_json_file(skipped_file)

    processed_ids = set()
    for lst in [faithful, degraded, skipped]:
        for x in lst:
            if "origin_id" in x:
                processed_ids.add(x["origin_id"])

    next_id = 1
    for lst in [faithful, degraded]:
        for x in lst:
            if x.get("id", 0) >= next_id:
                next_id = x["id"] + 1

    processed_this_run = 0

    print(f"Input records     : {len(data)}")
    print(f"Already faithful  : {len(faithful)}")
    print(f"Already degraded  : {len(degraded)}")
    print(f"Already skipped   : {len(skipped)}")
    print(f"Model             : {model}")
    print(f"Level 2 (fidelity): {'ON' if do_level2 else 'OFF'}")
    print(f"Level 3 (repair)  : {'ON' if do_level3 else 'OFF'}")
    print()

    for idx, record in enumerate(data, start=1):
        origin_id = record.get("id")
        if origin_id in processed_ids:
            continue

        result = process_one_full_pipeline(
            record, model, base_url, api_key,
            llm_timeout, compile_timeout, run_timeout,
            do_level2, do_level3,
        )

        entry = {
            "id": next_id,
            "origin_id": result["origin_id"],
            "quality": result.get("quality"),
            "generated_code": result.get("generated_code"),
            "run_stdout": result.get("run_stdout"),
        }

        if result["status"] == "accepted" and result.get("quality") in (
            "faithful", "repaired_faithful", "unchecked"
        ):
            faithful.append(entry)
            next_id += 1
            status_display = f"✓ FAITHFUL ({result['quality']})"

        elif result["status"] == "accepted_degraded":
            entry["fidelity"] = result.get("fidelity")
            degraded.append(entry)
            next_id += 1
            status_display = f"⚠ DEGRADED"

        else:
            skipped.append({
                "origin_id": result["origin_id"],
                "reason": result.get("reason"),
                "quality": result.get("quality"),
                "compile_stderr": result.get("compile_stderr"),
                "run_stderr": result.get("run_stderr"),
            })
            status_display = f"✗ SKIP ({result.get('reason')})"

        processed_this_run += 1
        print(f"[{idx}/{len(data)}] origin_id={origin_id:>4d}  {status_display}")

        if processed_this_run % checkpoint_every == 0:
            save_json_file(faithful_file, faithful)
            save_json_file(degraded_file, degraded)
            save_json_file(skipped_file, skipped)
            print(f"  ↳ Checkpoint: faithful={len(faithful)} "
                  f"degraded={len(degraded)} skipped={len(skipped)}")

        if sleep_sec > 0:
            time.sleep(sleep_sec)

    save_json_file(faithful_file, faithful)
    save_json_file(degraded_file, degraded)
    save_json_file(skipped_file, skipped)

    print()
    print("=" * 60)
    print(f"Faithful  : {len(faithful):>4d}  → {faithful_file}")
    print(f"Degraded  : {len(degraded):>4d}  → {degraded_file}")
    print(f"Skipped   : {len(skipped):>4d}  → {skipped_file}")
    print("=" * 60)


# =============================================================================
#                    MAIN
# =============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Rebuild autonomous Fortran programs with fidelity verification"
    )
    parser.add_argument("--input", required=True,
                        help="Input JSON (fortran_candidates.json)")
    parser.add_argument("--faithful-output", required=True,
                        help="Output: faithful codes")
    parser.add_argument("--degraded-output", required=True,
                        help="Output: degraded codes (compilable but altered)")
    parser.add_argument("--skipped-output", required=True,
                        help="Output: skipped/failed codes")
    parser.add_argument("--model", required=True,
                        help='Model name, e.g. "gpt-oss:120b"')
    parser.add_argument("--base-url", required=True,
                        help='OpenWebUI URL, e.g. "http://localhost:8082"')
    parser.add_argument("--api-key", default=None)
    parser.add_argument("--llm-timeout", type=int, default=240)
    parser.add_argument("--compile-timeout", type=int, default=30)
    parser.add_argument("--run-timeout", type=int, default=5)
    parser.add_argument("--max-items", type=int, default=None)
    parser.add_argument("--checkpoint-every", type=int, default=5)
    parser.add_argument("--sleep", type=float, default=0.5)
    parser.add_argument("--no-level2", action="store_true",
                        help="Skip fidelity check (Level 2)")
    parser.add_argument("--no-level3", action="store_true",
                        help="Skip repair attempts (Level 3)")

    args = parser.parse_args()
    api_key = args.api_key or os.environ.get("OPENWEBUI_API_KEY")

    rebuild_dataset(
        input_file=args.input,
        faithful_file=args.faithful_output,
        degraded_file=args.degraded_output,
        skipped_file=args.skipped_output,
        model=args.model,
        base_url=args.base_url,
        api_key=api_key,
        llm_timeout=args.llm_timeout,
        compile_timeout=args.compile_timeout,
        run_timeout=args.run_timeout,
        max_items=args.max_items,
        checkpoint_every=args.checkpoint_every,
        sleep_sec=args.sleep,
        do_level2=not args.no_level2,
        do_level3=not args.no_level3,
    )