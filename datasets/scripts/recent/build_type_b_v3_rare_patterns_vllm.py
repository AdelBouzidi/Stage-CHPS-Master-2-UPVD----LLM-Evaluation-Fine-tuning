#!/usr/bin/env python3
"""
Build Type B rare-pattern extension.

Goal:
- generate additional Type B examples only for rare patterns
- write results to a separate dataset
- avoid modifying the main type_b_v3_dataset.json
- allow several Type B examples from the same origin_id if the pattern differs
"""

import os
import sys
import time
import json
import argparse
import logging
import threading
from datetime import datetime
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import the existing validated pipeline.
# This file must be in the same directory as build_type_b_v3_vllm.py
from build_type_b_v3_vllm import (
    load_json,
    save_json,
    build_lookup,
    setup_logging,
    init_llm_client,
    process_assignment,
)


RARE_TARGET_PATTERNS = {
    "missing_interface_block",
    "output_format_mismatch",
    "allocation_runtime_error",
    "character_length_mismatch",
    "invalid_array_bounds",
    "segmentation_fault",
    "undeclared_type",
    "division_by_zero",
    "floating_point_exception",
    "malloc_corruption",
    "pointer_declaration_error",
    "whitespace_mismatch",
}


def existing_source_pattern_pairs(dataset):
    pairs = set()
    pattern_counts = Counter()

    for item in dataset:
        oid = item.get("source_origin_id")
        pattern = item.get("metadata", {}).get("target_pattern")

        if oid is not None and pattern:
            pairs.add((oid, pattern))
            pattern_counts[pattern] += 1

    return pairs, pattern_counts


def expand_rare_assignments(assignments, existing_pairs, existing_pattern_counts,
                            target_per_pattern, max_new_per_pattern):
    """
    Convert normal assignments into rare-pattern assignments.

    Original assignment:
      origin_id + target_group + candidate_patterns=[p1,p2,p3]

    Rare assignment:
      origin_id + same target_group + candidate_patterns=[rare_pattern]

    This forces the build step to try one specific rare pattern.
    """

    rare_by_pattern = defaultdict(list)

    for a in assignments:
        oid = a.get("origin_id")
        target_group = a.get("target_group")
        candidate_patterns = a.get("candidate_patterns", [])

        for pattern in candidate_patterns:
            if pattern not in RARE_TARGET_PATTERNS:
                continue

            if (oid, pattern) in existing_pairs:
                continue

            rare_assignment = dict(a)
            rare_assignment["candidate_patterns"] = [pattern]
            rare_assignment["target_successes"] = 1
            rare_assignment["rare_pattern_mode"] = True
            rare_assignment["original_target_group"] = target_group

            rare_by_pattern[pattern].append(rare_assignment)

    selected = []
    selected_counts = Counter()

    for pattern in sorted(RARE_TARGET_PATTERNS):
        current_count = existing_pattern_counts.get(pattern, 0)

        if current_count >= target_per_pattern:
            continue

        needed = target_per_pattern - current_count

        if max_new_per_pattern is not None:
            needed = min(needed, max_new_per_pattern)

        candidates = rare_by_pattern.get(pattern, [])

        # deterministic order for reproducibility
        candidates = sorted(candidates, key=lambda x: x["origin_id"])

        chosen = candidates[:needed]

        selected.extend(chosen)
        selected_counts[pattern] = len(chosen)

    # Interleave patterns so we do not process all examples of one pattern first.
    selected = sorted(
        selected,
        key=lambda x: (
            selected_counts.get(x["candidate_patterns"][0], 0),
            x["candidate_patterns"][0],
            x["origin_id"],
        )
    )

    return selected, selected_counts


def build_rare_patterns(
    assignments_path,
    faithful_path,
    existing_dataset_path,
    output_path,
    errors_path,
    model,
    base_url,
    api_key,
    log_file,
    max_concurrency,
    target_per_pattern,
    max_new_per_pattern,
):
    setup_logging(log_file)
    init_llm_client(max_concurrency)

    log = logging.getLogger("type_b")

    log.info("=" * 70)
    log.info(f"TYPE B RARE PATTERNS BUILD — {datetime.now():%Y-%m-%d %H:%M:%S}")
    log.info("=" * 70)
    log.info(f"Model              : {model}")
    log.info(f"Base URL           : {base_url}")
    log.info(f"Concurrency        : {max_concurrency}")
    log.info(f"Target per pattern : {target_per_pattern}")
    log.info(f"Max new per pattern: {max_new_per_pattern}")
    log.info("")

    assignments = load_json(assignments_path)
    faithful = load_json(faithful_path)
    faithful_lookup = build_lookup(faithful, "origin_id")

    existing_dataset = []
    if existing_dataset_path and os.path.exists(existing_dataset_path):
        existing_dataset = load_json(existing_dataset_path)

    output_dataset = []
    all_errors = []

    if os.path.exists(output_path):
        try:
            output_dataset = load_json(output_path)
        except Exception:
            output_dataset = []

    if os.path.exists(errors_path):
        try:
            all_errors = load_json(errors_path)
        except Exception:
            all_errors = []

    existing_pairs_main, existing_counts_main = existing_source_pattern_pairs(existing_dataset)
    existing_pairs_out, existing_counts_out = existing_source_pattern_pairs(output_dataset)

    existing_pairs = existing_pairs_main | existing_pairs_out
    existing_pattern_counts = existing_counts_main + existing_counts_out

    rare_assignments, selected_counts = expand_rare_assignments(
        assignments=assignments,
        existing_pairs=existing_pairs,
        existing_pattern_counts=existing_pattern_counts,
        target_per_pattern=target_per_pattern,
        max_new_per_pattern=max_new_per_pattern,
    )

    log.info("Existing rare pattern counts:")
    for p in sorted(RARE_TARGET_PATTERNS):
        log.info(f"  {p:35s}: {existing_pattern_counts.get(p, 0)}")

    log.info("")
    log.info("New rare assignments selected:")
    for p in sorted(RARE_TARGET_PATTERNS):
        log.info(f"  {p:35s}: {selected_counts.get(p, 0)}")

    log.info("")
    log.info(f"Total rare assignments: {len(rare_assignments)}")
    log.info("")

    if not rare_assignments:
        log.info("Nothing to process.")
        return

    write_lock = threading.Lock()
    counter = {
        "done": 0,
        "succ": 0,
        "fail": 0,
        "next_id": len(output_dataset) + 1,
    }

    group_counts = Counter()
    pattern_success_counts = Counter()
    pattern_failure_counts = Counter()

    run_start = time.time()

    def worker(assignment):
        oid = assignment["origin_id"]
        pattern = assignment["candidate_patterns"][0]

        entry = faithful_lookup.get(oid)
        if not entry:
            return oid, pattern, [], [{
                "pattern_name": pattern,
                "failure_reason": "code_not_found",
            }]

        code = entry.get("generated_code", "")
        if not code:
            return oid, pattern, [], [{
                "pattern_name": pattern,
                "failure_reason": "empty_code",
            }]

        successes, failures = process_assignment(
            assignment=assignment,
            code=code,
            model=model,
            base_url=base_url,
            api_key=api_key,
        )

        return oid, pattern, successes, failures

    with ThreadPoolExecutor(max_workers=max_concurrency) as pool:
        futures = {pool.submit(worker, a): a for a in rare_assignments}

        for fut in as_completed(futures):
            assignment = futures[fut]
            oid = assignment["origin_id"]
            pattern = assignment["candidate_patterns"][0]

            try:
                oid, pattern, successes, failures = fut.result()
            except Exception as e:
                successes = []
                failures = [{
                    "pattern_name": pattern,
                    "failure_reason": f"worker_crashed: {e}",
                }]

            with write_lock:
                for s in successes:
                    s["id"] = f"type_b_rare_{counter['next_id']:04d}"
                    s.setdefault("metadata", {})
                    s["metadata"]["rare_pattern_extension"] = True

                    counter["next_id"] += 1
                    output_dataset.append(s)

                    group_counts[s["metadata"]["target_group"]] += 1
                    pattern_success_counts[s["metadata"]["target_pattern"]] += 1

                if failures:
                    all_errors.append({
                        "origin_id": oid,
                        "target_group": assignment["target_group"],
                        "candidate_patterns": assignment["candidate_patterns"],
                        "failures": failures,
                    })

                    for f in failures:
                        pattern_failure_counts[f.get("pattern_name") or pattern] += 1

                counter["done"] += 1
                counter["succ"] += len(successes)
                counter["fail"] += len(failures)

                d = counter["done"]

                if d % 10 == 0 or d == len(rare_assignments):
                    save_json(output_path, output_dataset)
                    save_json(errors_path, all_errors)

            elapsed = time.time() - run_start
            eta = elapsed / counter["done"] * (len(rare_assignments) - counter["done"]) / 60

            log.info(
                f"[{counter['done']}/{len(rare_assignments)}] "
                f"oid={oid:>5d} pattern={pattern:35s} "
                f"✓{len(successes)} ✗{len(failures)} ETA {eta:.0f}min"
            )

    with write_lock:
        save_json(output_path, output_dataset)
        save_json(errors_path, all_errors)

    total_time = (time.time() - run_start) / 60

    log.info("")
    log.info("=" * 70)
    log.info("RARE PATTERNS BUILD DONE")
    log.info(f"Duration        : {total_time:.1f} min")
    log.info(f"Successes       : {counter['succ']}")
    log.info(f"Failures        : {counter['fail']}")
    log.info(f"Output dataset  : {output_path}")
    log.info(f"Errors output   : {errors_path}")

    log.info("")
    log.info("Successes by pattern:")
    for p, c in pattern_success_counts.most_common():
        log.info(f"  {p:35s}: {c}")

    log.info("")
    log.info("Failures by pattern:")
    for p, c in pattern_failure_counts.most_common():
        log.info(f"  {p:35s}: {c}")

    log.info("")
    log.info("Successes by group:")
    for g, c in group_counts.most_common():
        log.info(f"  {g:15s}: {c}")

    log.info("=" * 70)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Build additional Type B examples for rare patterns only"
    )

    parser.add_argument("--assignments", required=True)
    parser.add_argument("--faithful", required=True)

    parser.add_argument(
        "--existing-dataset",
        default="dataset/type_b_v2/type_b_v3_dataset.json",
        help="Main Type B dataset used to compute existing pattern counts",
    )

    parser.add_argument(
        "--output",
        default="dataset/type_b_v2/type_b_v3_rare_patterns_dataset.json",
    )

    parser.add_argument(
        "--errors-output",
        default="dataset/type_b_v2/type_b_v3_rare_patterns_errors.json",
    )

    parser.add_argument("--model", default="gpt-oss-120b")
    parser.add_argument("--base-url", default="http://localhost:8086")
    parser.add_argument("--api-key", default=None)

    parser.add_argument("--concurrency", type=int, default=64)

    parser.add_argument(
        "--target-per-pattern",
        type=int,
        default=25,
        help="Desired total count per rare pattern after considering the existing dataset",
    )

    parser.add_argument(
        "--max-new-per-pattern",
        type=int,
        default=30,
        help="Maximum new attempts per rare pattern",
    )

    parser.add_argument(
        "--log-file",
        default="dataset/type_b_v2/type_b_v3_rare_patterns_build.log",
    )

    args = parser.parse_args()

    build_rare_patterns(
        assignments_path=args.assignments,
        faithful_path=args.faithful,
        existing_dataset_path=args.existing_dataset,
        output_path=args.output,
        errors_path=args.errors_output,
        model=args.model,
        base_url=args.base_url,
        api_key=args.api_key or os.environ.get("OPENWEBUI_API_KEY"),
        log_file=args.log_file,
        max_concurrency=args.concurrency,
        target_per_pattern=args.target_per_pattern,
        max_new_per_pattern=args.max_new_per_pattern,
    )