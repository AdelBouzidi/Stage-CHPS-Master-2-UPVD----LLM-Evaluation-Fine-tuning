#!/usr/bin/env python3
"""
Rebuild Fortran sources into autonomous executable Fortran 90 programs.

V3 — Améliorations majeures :
  1. COMPILE-RETRY LOOP : quand la compilation échoue, le message d'erreur
     est renvoyé au LLM pour correction (max 2 retries). Cible les 11/12
     skips du test mixed18 qui étaient des compile_failed.
  2. PROMPT ANTI-PATTERNS : règles explicites contre les erreurs LLM
     fréquentes (use externe non défini, kind params non déclarés,
     function result naming, contains imbriqué).
  3. Hardcoded-only : tous les programmes sont autonomes sans stdin.
  4. Corrections v2-fix conservées (-w, run_timeout=10, fixed→free rules,
     pas de faux positif read(variable,...)).

Architecture :
  Level 1: generate + compile + retry(2) + run
  Level 2: fidelity check
  Level 3: repair degraded code
"""

import argparse
import json
import os
import re
import subprocess
import tempfile
import time
from typing import Any, Dict, List, Optional

import requests


def call_openwebui(prompt, model, base_url, api_key=None, temperature=0.0,
                   max_tokens=4096, timeout=240):
    headers = {"Content-Type": "application/json"}
    if api_key: headers["Authorization"] = f"Bearer {api_key}"
    endpoints = ["/api/chat/completions", "/v1/chat/completions",
                 "/ollama/v1/chat/completions"]
    errors = []
    for ep in endpoints:
        try:
            r = requests.post(f"{base_url}{ep}", headers=headers,
                json={"model": model, "messages": [{"role":"user","content":prompt}],
                      "temperature": temperature, "max_tokens": max_tokens,
                      "stream": False}, timeout=timeout)
            if r.status_code == 200:
                res = r.json()
                if "choices" in res and res["choices"]:
                    return res["choices"][0]["message"]["content"]
                if "message" in res and isinstance(res["message"], dict):
                    return res["message"].get("content", "")
                if "response" in res: return res["response"]
            errors.append(f"{ep}: HTTP {r.status_code}")
        except Exception as e:
            errors.append(f"{ep}: {e}")
    raise RuntimeError("All endpoints failed:\n" + "\n".join(errors))


def get_record_id(rec):
    return rec.get("merged_id", rec.get("id", rec.get("origin_id")))

def get_original_code(rec):
    return rec.get("code") or rec.get("generated_code") or rec.get("source_code") or ""

def get_record_metadata(rec):
    keys = ["merged_id","source","source_file","original_id","path","repo","ext",
            "extension","source_extension","source_form","size","code_hash",
            "requires_preprocessing","has_legacy_markers","has_io_markers",
            "license_type","detected_licenses","language","is_vendor","is_generated","rebuilt_target"]
    meta = {k: rec.get(k) for k in keys if k in rec}
    if isinstance(rec.get("metadata"), dict): meta["input_metadata"] = rec["metadata"]
    return meta

def describe_source_kind(rec):
    ext = str(rec.get("ext") or rec.get("source_extension") or rec.get("extension") or "").lstrip(".")
    sf = rec.get("source_form",""); src = rec.get("source",""); path = rec.get("path","")
    d = []
    if src: d.append(f"source={src}")
    if path: d.append(f"path={path}")
    if ext: d.append(f"extension=.{ext}")
    if sf: d.append(f"source_form={sf}")
    return ", ".join(d) if d else "unknown"

def is_legacy_source(rec):
    form = rec.get("source_form","")
    if "legacy" in form.lower() or "fixed" in form.lower(): return True
    return str(rec.get("ext","")).lower().lstrip(".") in ("f","for","ftn","f77")

def has_forbidden_io(code):
    c = code.lower()
    if re.search(r"\bopen\s*\(", c): return True
    if re.search(r"\binquire\s*\(", c): return True
    if re.search(r"\bclose\s*\(", c): return True
    if re.search(r"\brewind\s*\(", c): return True
    if re.search(r"\bbackspace\s*\(", c): return True
    if re.search(r"\bread\s*\(\s*unit\s*=", c): return True
    if re.search(r"\bread\s*\(\s*(?!\*|5\s*[,)])\d+\s*,", c): return True
    if re.search(r"\bread\s*\(\s*\*\s*,", c): return True
    if re.search(r"\bread\s+\*", c): return True
    if re.search(r"\bread\s*\(\s*5\s*,", c): return True
    return False


FIXED_TO_FREE = """
FIXED-FORM CONVERSION:
- Column 1 comments (C,c,*) → "!" ; continuation col 6 → "&" at end of prev line
- Labeled DO → DO...END DO ; COMMON → local vars ; EQUIVALENCE → assignments
- IMPLICIT REAL*8 → implicit none + explicit decls ; REAL*8 → double precision
- Hollerith → character strings
"""

ANTI_PATTERNS = """
CRITICAL ANTI-PATTERN RULES:
1. NO EXTERNAL USE: Do NOT write "use somemodule" unless you DEFINE that module
   in the SAME file ABOVE. Only iso_fortran_env and iso_c_binding are allowed.
2. KIND PARAMS: Replace I4B→4, DP/RK→kind(1.0d0), SP→kind(1.0), CK→kind('A').
   Do NOT reference nrtype, nrutil, nr or similar external modules.
3. FUNCTION RESULT: "function foo() result(foo)" is ILLEGAL. Use result(res).
4. NO NESTED CONTAINS: Move internal procedures to program's contains section.
5. IMPLICIT NONE: Declare every variable explicitly.
6. ARRAY SHAPES: Ensure dimensions match. Use (:) for allocatable deferred shape.
"""


def build_generation_prompt(original_code, source_info="", is_legacy=False):
    legacy_section = FIXED_TO_FREE if is_legacy else ""
    return f"""Transform the following Fortran source into ONE autonomous executable Fortran 90 program.

SOURCE: {source_info}
{legacy_section}
TARGET: ONE Fortran 90 free-form file, autonomous, compilable with gfortran.

GOAL: Preserve the core scientific/mathematical behavior faithfully.

SCIENTIFIC RULES:
1. PRESERVE math expressions, loops, conditions, array ops, scientific logic.
2. Do NOT simplify or replace algorithms. If impossible, return SKIP.
{ANTI_PATTERNS}
TRANSFORMATIONS ALLOWED:
- Add program wrapper, implicit none, declarations.
- Hardcode representative small input values (replace ALL reads).
- Inline helpers, replace external deps with faithful local equivalents.
- Add PRINT for visible output.

FORBIDDEN: read(*,*), read *, read(5,*), open(file=...), read(unit=...),
MPI, OpenMP, OpenACC, external libraries.

STUB RULE: If a function cannot be reconstructed faithfully:
! STUB: original implementation not available
print *, 'WARNING: stub function called'

COMPILE WITH: gfortran -O0 -ffree-line-length-none -w

OUTPUT: JSON only, no markdown.
{{ "mode": "hardcoded", "code": "<Fortran 90 code>", "stdin_data": null }}
If impossible: SKIP

Source code:
{original_code}
"""


def build_compile_fix_prompt(original_code, generated_code, compile_error, attempt):
    return f"""The Fortran 90 program below FAILS to compile.

COMPILATION ERROR:
{compile_error[:1500]}

COMMON FIXES:
- "has no IMPLICIT type" / "not been declared": declare the variable or define
  kind params locally (I4B=4, DP=kind(1.0d0), SP=kind(1.0), CK=kind('A')).
- "Cannot open module file": remove USE and define everything locally.
  Only iso_fortran_env/iso_c_binding allowed.
- "RESULT variable must be different": rename result variable.
- "already in a contained program unit": flatten nested contains.
- "exceeds the range of INTEGER": use INT(x,kind=8).
- "Explicit shaped array" + allocatable: use (:) for deferred shape.

Fix it. Compile with: gfortran -O0 -ffree-line-length-none -w
Keep autonomous hardcoded (no stdin, no file I/O). Preserve scientific logic.

OUTPUT: JSON only:
{{ "mode": "hardcoded", "code": "<fixed code>", "stdin_data": null }}
If impossible: SKIP

ORIGINAL (reference):
{original_code[:3000]}

CODE THAT FAILS:
{generated_code}
"""


def build_fidelity_prompt(original_code, generated_code, source_info=""):
    return f"""Compare ORIGINAL with GENERATED Fortran 90. Was scientific content preserved?

SOURCE: {source_info}

Allowed: syntax modernization, wrapper, declarations, hardcoded inputs, prints.
Not allowed: simplifying algorithms, removing formulas, stubbing central logic.

JSON only:
{{ "body_preserved": true/false, "stub_functions": [...], "simplified_expressions": [...],
   "quality": "faithful" or "degraded" or "skeleton_only" }}

ORIGINAL:
{original_code}

GENERATED:
{generated_code}
"""


def build_repair_prompt(original_code, generated_code, issues, source_info=""):
    probs = []
    if issues.get("stub_functions"):
        probs.append(f"Stubs: {', '.join(map(str, issues['stub_functions']))}")
    for s in issues.get("simplified_expressions", []):
        probs.append(f"Simplified: {s}")
    prob_text = "\n".join(probs) if probs else "General degradation"
    return f"""Fix the GENERATED Fortran 90 to restore ORIGINAL scientific content.
SOURCE: {source_info}
PROBLEMS: {prob_text}
Keep autonomous hardcoded. Compile with gfortran -O0 -ffree-line-length-none -w.
JSON only: {{ "mode":"hardcoded", "code":"<fixed>", "stdin_data":null }}
If impossible: SKIP

ORIGINAL:
{original_code}

GENERATED TO FIX:
{generated_code}
"""


def clean_fortran_code(code):
    code = code.strip().replace("```fortran","").replace("```f90","").replace("```","").strip()
    for p in ["Here is the code:","Here's the code:","Here is the Fortran code:",
              "Standalone program:","Program:","Code:"]:
        if code.startswith(p): code = code[len(p):].strip()
    return code

def extract_json(response):
    if not response: return None
    t = response.strip()
    if t == "SKIP": return {"skip": True}
    try: return json.loads(t)
    except: pass
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", t, re.DOTALL)
    if m:
        try: return json.loads(m.group(1))
        except: pass
    s, e = t.find("{"), t.rfind("}")
    if s != -1 and e > s:
        try: return json.loads(t[s:e+1])
        except: pass
    return None

def parse_response(response):
    p = extract_json(response)
    if not p: return {"ok":False,"reason":"invalid_json_response","code":None}
    if p.get("skip"): return {"ok":False,"reason":"model_skip","code":None}
    code = p.get("code")
    if not isinstance(code,str) or not code.strip():
        return {"ok":False,"reason":"empty_code","code":code}
    return {"ok":True,"reason":None,"code":clean_fortran_code(code)}


def compile_fortran(code, workdir, timeout=30):
    src = os.path.join(workdir,"candidate.f90")
    exe = os.path.join(workdir,"candidate.out")
    with open(src,"w",encoding="utf-8") as f: f.write(code)
    cmd = ["gfortran",src,"-O0","-ffree-line-length-none","-w","-o",exe]
    try:
        r = subprocess.run(cmd,capture_output=True,text=True,timeout=timeout,cwd=workdir)
        return {"ok":r.returncode==0,"stderr":r.stderr,"exe_path":exe,"cmd":" ".join(cmd)}
    except subprocess.TimeoutExpired:
        return {"ok":False,"stderr":"Compilation timeout","exe_path":exe,"cmd":" ".join(cmd)}

def run_executable(exe_path, workdir, timeout=10):
    try:
        r = subprocess.run([exe_path],input="",capture_output=True,text=True,
                          timeout=timeout,cwd=workdir,
                          env={**os.environ,"GFORTRAN_UNBUFFERED_ALL":"1"})
        return {"ok":r.returncode==0,"stdout":r.stdout,"stderr":r.stderr}
    except subprocess.TimeoutExpired:
        return {"ok":False,"stdout":"","stderr":"Execution timeout"}
    except Exception as e:
        return {"ok":False,"stdout":"","stderr":str(e)}

def load_json(path):
    if not os.path.exists(path): return []
    with open(path,"r",encoding="utf-8") as f: return json.load(f)

def save_json(path, data):
    os.makedirs(os.path.dirname(path) or ".",exist_ok=True)
    tmp = path+".tmp"
    with open(tmp,"w",encoding="utf-8") as f: json.dump(data,f,indent=2,ensure_ascii=False)
    os.replace(tmp,path)


# =============================================================================
# Level 1 — avec compile-retry
# =============================================================================

def level1(rec, model, base_url, api_key, llm_timeout, compile_timeout,
           run_timeout, max_retries=2):
    oid = get_record_id(rec)
    orig = get_original_code(rec)
    info = describe_source_kind(rec)
    legacy = is_legacy_source(rec)

    res = {"origin_id":oid,"original_code":orig,"source_metadata":get_record_metadata(rec),
           "status":"skipped","reason":None,"generated_code":None,"input_mode":None,
           "run_stdout":None,"compile_stderr":None,"run_stderr":None,
           "compile_cmd":None,"compile_retries":0}

    if not orig or not orig.strip():
        res["reason"] = "empty_input_code"; return res

    prompt = build_generation_prompt(orig, source_info=info, is_legacy=legacy)
    try:
        response = call_openwebui(prompt, model, base_url, api_key, 0.0, 4096, llm_timeout)
    except Exception as e:
        res["reason"] = "llm_call_failed"; res["run_stderr"] = str(e); return res

    parsed = parse_response(response)
    if not parsed["ok"]:
        res["reason"] = parsed["reason"]; res["generated_code"] = parsed.get("code"); return res

    code = parsed["code"]
    if has_forbidden_io(code):
        res["reason"] = "forbidden_io"; res["generated_code"] = code; return res

    # Compile + retry loop
    for attempt in range(1 + max_retries):
        with tempfile.TemporaryDirectory(prefix=f"f90_l1_a{attempt}_") as tmpdir:
            comp = compile_fortran(code, tmpdir, compile_timeout)
            res["compile_cmd"] = comp.get("cmd")

            if comp["ok"]:
                run = run_executable(comp["exe_path"], tmpdir, run_timeout)
                if run["ok"]:
                    res["status"] = "level1_passed"
                    res["generated_code"] = code
                    res["input_mode"] = "hardcoded"
                    res["run_stdout"] = run["stdout"]
                    res["compile_retries"] = attempt
                    return res
                else:
                    res["reason"] = "run_failed"
                    res["generated_code"] = code
                    res["input_mode"] = "hardcoded"
                    res["run_stderr"] = run["stderr"]
                    res["compile_retries"] = attempt
                    return res

            if attempt >= max_retries:
                break

            # Retry: send error to LLM
            fix_prompt = build_compile_fix_prompt(orig, code, comp["stderr"], attempt+1)
            try:
                fix_resp = call_openwebui(fix_prompt, model, base_url, api_key,
                                          0.1*(attempt+1), 4096, llm_timeout)
            except: break

            fix_parsed = parse_response(fix_resp)
            if not fix_parsed["ok"]: break

            new_code = fix_parsed["code"]
            if has_forbidden_io(new_code): break
            code = new_code

    res["reason"] = "compile_failed"
    res["generated_code"] = code
    res["input_mode"] = "hardcoded"
    res["compile_stderr"] = comp["stderr"]
    res["compile_retries"] = attempt
    return res


def level2(orig, gen, model, base_url, api_key, llm_timeout, source_info=""):
    prompt = build_fidelity_prompt(orig, gen, source_info)
    default = {"body_preserved":False,"stub_functions":[],"simplified_expressions":["check failed"],"quality":"degraded"}
    try:
        r = call_openwebui(prompt, model, base_url, api_key, 0.0, 1024, llm_timeout)
    except: return default
    p = extract_json(r)
    if not p or p.get("skip"): return default
    q = p.get("quality","degraded")
    if q not in ("faithful","degraded","skeleton_only"): q = "degraded"
    st = p.get("stub_functions",[])
    if not isinstance(st,list): st = [str(st)]
    si = p.get("simplified_expressions",[])
    if not isinstance(si,list): si = [str(si)]
    return {"body_preserved":bool(p.get("body_preserved",False)),"stub_functions":st,
            "simplified_expressions":si,"quality":q}


def level3(orig, gen, issues, model, base_url, api_key,
           llm_timeout, compile_timeout, run_timeout, source_info=""):
    prompt = build_repair_prompt(orig, gen, issues, source_info)
    try:
        r = call_openwebui(prompt, model, base_url, api_key, 0.0, 4096, llm_timeout)
    except: return None
    p = parse_response(r)
    if not p["ok"]: return None
    code = p["code"]
    if has_forbidden_io(code): return None
    with tempfile.TemporaryDirectory(prefix="f90_l3_") as tmpdir:
        comp = compile_fortran(code, tmpdir, compile_timeout)
        if not comp["ok"]: return None
        run = run_executable(comp["exe_path"], tmpdir, run_timeout)
        if not run["ok"]: return None
    return {"generated_code":code,"run_stdout":run["stdout"]}


def process_one(rec, model, base_url, api_key, llm_timeout, compile_timeout,
                run_timeout, do_l2=True, do_l3=True, max_retries=2):
    info = describe_source_kind(rec)
    l1 = level1(rec, model, base_url, api_key, llm_timeout, compile_timeout,
                run_timeout, max_retries)

    if l1["status"] != "level1_passed":
        return {**l1, "fidelity": None}

    if not do_l2:
        l1["quality"] = "unchecked"; l1["status"] = "accepted"; l1["fidelity"] = None
        return l1

    fid = level2(l1["original_code"], l1["generated_code"], model, base_url,
                 api_key, llm_timeout, info)
    q = fid["quality"]

    if q == "faithful":
        l1["status"] = "accepted"; l1["quality"] = "faithful"; l1["fidelity"] = fid
        return l1

    if q == "degraded" and do_l3:
        repair = level3(l1["original_code"], l1["generated_code"], fid,
                        model, base_url, api_key, llm_timeout, compile_timeout,
                        run_timeout, info)
        if repair:
            fid2 = level2(l1["original_code"], repair["generated_code"],
                          model, base_url, api_key, llm_timeout, info)
            if fid2["quality"] == "faithful":
                l1["status"] = "accepted"; l1["quality"] = "repaired_faithful"
                l1["generated_code"] = repair["generated_code"]
                l1["run_stdout"] = repair["run_stdout"]; l1["fidelity"] = fid2
                return l1
            l1["status"] = "accepted_degraded"; l1["reason"] = "repair_insufficient"
            l1["quality"] = "degraded"; l1["generated_code"] = repair["generated_code"]
            l1["run_stdout"] = repair["run_stdout"]; l1["fidelity"] = fid2
            return l1

    l1["status"] = "accepted_degraded" if q == "degraded" else "skipped"
    l1["reason"] = f"quality_{q}"; l1["quality"] = q; l1["fidelity"] = fid
    return l1


def rebuild_dataset(input_file, faithful_file, degraded_file, skipped_file,
                    model, base_url, api_key, llm_timeout, compile_timeout,
                    run_timeout, max_items, checkpoint_every, sleep_sec,
                    do_l2, do_l3, max_retries):
    data = load_json(input_file)
    if max_items: data = data[:max_items]

    faithful = load_json(faithful_file)
    degraded = load_json(degraded_file)
    skipped = load_json(skipped_file)

    done_ids = set()
    for lst in (faithful, degraded, skipped):
        for item in lst:
            if "origin_id" in item: done_ids.add(item["origin_id"])

    next_id = 1
    for lst in (faithful, degraded):
        for item in lst:
            if isinstance(item.get("id"),int) and item["id"] >= next_id:
                next_id = item["id"] + 1

    remaining = sum(1 for r in data if get_record_id(r) not in done_ids)

    print(f"Input records      : {len(data)}")
    print(f"Already faithful   : {len(faithful)}")
    print(f"Already degraded   : {len(degraded)}")
    print(f"Already skipped    : {len(skipped)}")
    print(f"Remaining          : {remaining}")
    print(f"Model              : {model}")
    print(f"Compile retries    : {max_retries}")
    print(f"Level 2/3          : {'ON' if do_l2 else 'OFF'}/{'ON' if do_l3 else 'OFF'}")
    print()

    n_done = 0; t0 = time.time()

    for idx, rec in enumerate(data, 1):
        oid = get_record_id(rec)
        if oid in done_ids: continue

        result = process_one(rec, model, base_url, api_key, llm_timeout,
                             compile_timeout, run_timeout, do_l2, do_l3, max_retries)

        retries = result.get("compile_retries", 0)
        rs = f" r={retries}" if retries > 0 else ""

        entry = {"id": next_id, "origin_id": result["origin_id"],
                 "quality": result.get("quality"),
                 "generated_code": result.get("generated_code"),
                 "input_mode": "hardcoded", "stdin_data": None,
                 "needs_stdin": False, "run_stdout": result.get("run_stdout"),
                 "source_metadata": result.get("source_metadata"),
                 "compile_retries": retries}

        st = result.get("status","skipped")
        q = result.get("quality")

        if st == "accepted" and q in ("faithful","repaired_faithful","unchecked"):
            faithful.append(entry); next_id += 1
            disp = f"✓ FAITHFUL ({q}{rs})"
        elif st == "accepted_degraded":
            entry["fidelity"] = result.get("fidelity")
            degraded.append(entry); next_id += 1
            disp = f"⚠ DEGRADED{rs}"
        else:
            skipped.append({"origin_id": result["origin_id"],
                "source_metadata": result.get("source_metadata"),
                "reason": result.get("reason"), "quality": q,
                "generated_code": result.get("generated_code"),
                "compile_stderr": result.get("compile_stderr"),
                "run_stderr": result.get("run_stderr"),
                "compile_retries": retries})
            disp = f"✗ SKIP ({result.get('reason')}{rs})"

        n_done += 1; done_ids.add(oid)
        meta = result.get("source_metadata") or {}
        ext = meta.get("ext") or "?"
        form = meta.get("source_form") or "?"
        src = meta.get("source") or "?"
        elapsed = time.time() - t0
        eta = (elapsed/n_done * (remaining-n_done) / 60) if n_done else 0

        print(f"[{idx}/{len(data)}] oid={str(oid):>8s} src={str(src):>14s} "
              f".{str(ext):>3s} {str(form):>20s} {disp} (ETA {eta:.0f}min)")

        if n_done % checkpoint_every == 0:
            save_json(faithful_file, faithful)
            save_json(degraded_file, degraded)
            save_json(skipped_file, skipped)
            print(f"  ↳ Checkpoint: faithful={len(faithful)} degraded={len(degraded)} skipped={len(skipped)}")

        if sleep_sec > 0: time.sleep(sleep_sec)

    save_json(faithful_file, faithful)
    save_json(degraded_file, degraded)
    save_json(skipped_file, skipped)

    print(f"\n{'='*60}")
    print(f"Duration : {(time.time()-t0)/60:.1f} min")
    print(f"Faithful : {len(faithful):>5d} → {faithful_file}")
    print(f"Degraded : {len(degraded):>5d} → {degraded_file}")
    print(f"Skipped  : {len(skipped):>5d} → {skipped_file}")
    print("="*60)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Rebuild Fortran 90 (v3 — compile-retry)")
    p.add_argument("--input", required=True)
    p.add_argument("--faithful-output", required=True)
    p.add_argument("--degraded-output", required=True)
    p.add_argument("--skipped-output", required=True)
    p.add_argument("--model", required=True)
    p.add_argument("--base-url", required=True)
    p.add_argument("--api-key", default=None)
    p.add_argument("--llm-timeout", type=int, default=240)
    p.add_argument("--compile-timeout", type=int, default=30)
    p.add_argument("--run-timeout", type=int, default=10)
    p.add_argument("--max-items", type=int, default=None)
    p.add_argument("--max-compile-retries", type=int, default=2)
    p.add_argument("--checkpoint-every", type=int, default=5)
    p.add_argument("--sleep", type=float, default=0.5)
    p.add_argument("--no-level2", action="store_true")
    p.add_argument("--no-level3", action="store_true")
    a = p.parse_args()
    rebuild_dataset(
        a.input, a.faithful_output, a.degraded_output, a.skipped_output,
        a.model, a.base_url, a.api_key or os.environ.get("OPENWEBUI_API_KEY"),
        a.llm_timeout, a.compile_timeout, a.run_timeout,
        a.max_items, a.checkpoint_every, a.sleep,
        not a.no_level2, not a.no_level3, a.max_compile_retries
    )