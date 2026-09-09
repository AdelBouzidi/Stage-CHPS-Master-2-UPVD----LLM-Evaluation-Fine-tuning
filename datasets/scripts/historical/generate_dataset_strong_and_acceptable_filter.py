import json
import os
import argparse
from typing import List, Dict, Any, Tuple


def load_json(path: str) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"{path} must contain a JSON list")
    return data


def save_json(path: str, data: Any):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_features(rec: Dict[str, Any]) -> Dict[str, Any]:
    f = rec.get("features", {})
    if isinstance(f, dict):
        return f
    return {}


def is_acceptable_eligible(rec: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Retourne:
      - True, "acceptable_valid" si le code acceptable est retenu
      - False, <raison> sinon
    """
    f = get_features(rec)

    if f.get("has_stub", False):
        return False, "has_stub"

    code_lines = f.get("num_code_lines", 0)
    if code_lines < 12:
        return False, f"num_code_lines={code_lines}<12"

    score = f.get("complexity_score", 0)
    if score < 5:
        return False, f"complexity_score={score}<5"

    return True, "acceptable_valid"


def build_clean_base_dataset(
    input_path: str,
    output_path: str,
    rejected_path: str,
    stats_path: str,
):
    """
    Construit une base propre de codes Fortran validés à partir de final_keep.json.

    Cette base est utilisée ensuite comme source commune pour :
      - Type A : génération
      - Type B : correction guidée
      - Type C : correction autonome

    La logique reste identique à l'ancien filtre Type A :
      - garder tous les strong
      - garder les acceptable suffisamment propres
      - rejeter les cas faibles, stubs ou trop simples
    """
    data = load_json(input_path)

    kept: List[Dict[str, Any]] = []
    rejected: List[Dict[str, Any]] = []

    stats = {
        "input_total": len(data),
        "clean_base_kept_total": 0,
        "clean_base_rejected_total": 0,
        "strong_kept": 0,
        "acceptable_kept": 0,
        "acceptable_rejected": 0,
        "good_for_type_a_false_rejected": 0,
        "other_category_rejected": 0,
        "reject_reasons": {},
    }

    for rec in data:
        cat = rec.get("category", "")
        origin_id = rec.get("origin_id")
        features = get_features(rec)
        good_for_type_a = rec.get("good_for_type_a", False)

        # Règle 0 : on garde la même logique historique.
        # Même si la base sert maintenant à A/B/C, ce filtre reste basé sur good_for_type_a.
        if good_for_type_a is not True:
            reason = "good_for_type_a_false"
            rejected.append({
                "origin_id": origin_id,
                "category": cat,
                "reject_reason": reason,
                "features": features,
            })
            stats["clean_base_rejected_total"] += 1
            stats["good_for_type_a_false_rejected"] += 1
            stats["reject_reasons"][reason] = stats["reject_reasons"].get(reason, 0) + 1
            continue

        # Règle 1 : tous les strong sont gardés
        if cat == "strong":
            kept.append(rec)
            stats["clean_base_kept_total"] += 1
            stats["strong_kept"] += 1
            continue

        # Règle 2 : les acceptable passent le filtre heuristique
        if cat == "acceptable":
            eligible, reason = is_acceptable_eligible(rec)
            if eligible:
                kept.append(rec)
                stats["clean_base_kept_total"] += 1
                stats["acceptable_kept"] += 1
            else:
                rejected.append({
                    "origin_id": origin_id,
                    "category": cat,
                    "reject_reason": reason,
                    "features": features,
                })
                stats["clean_base_rejected_total"] += 1
                stats["acceptable_rejected"] += 1
                stats["reject_reasons"][reason] = stats["reject_reasons"].get(reason, 0) + 1
            continue

        # Cas inattendu : autre catégorie
        reason = f"unexpected_category:{cat}"
        rejected.append({
            "origin_id": origin_id,
            "category": cat,
            "reject_reason": reason,
            "features": features,
        })
        stats["clean_base_rejected_total"] += 1
        stats["other_category_rejected"] += 1
        stats["reject_reasons"][reason] = stats["reject_reasons"].get(reason, 0) + 1

    save_json(output_path, kept)
    save_json(rejected_path, rejected)
    save_json(stats_path, stats)

    print(f"Input total                 : {stats['input_total']}")
    print(f"Clean base kept total       : {stats['clean_base_kept_total']} → {output_path}")
    print(f"Clean base rejected total   : {stats['clean_base_rejected_total']} → {rejected_path}")
    print()
    print(f"Strong kept                 : {stats['strong_kept']}")
    print(f"Acceptable kept             : {stats['acceptable_kept']}")
    print(f"Acceptable rejected         : {stats['acceptable_rejected']}")
    print(f"Rejected (good_for_type_a)  : {stats['good_for_type_a_false_rejected']}")
    print(f"Rejected (other category)   : {stats['other_category_rejected']}")
    print(f"Stats saved                 : {stats_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Build clean base Fortran codes dataset for Type A/B/C from final_keep.json"
    )
    parser.add_argument("--input", required=True, help="Path to final_keep.json")
    parser.add_argument("--output", required=True, help="Path to clean base codes JSON")
    parser.add_argument("--rejected", required=True, help="Path to rejected clean base records JSON")
    parser.add_argument("--stats", required=True, help="Path to clean base stats JSON")
    args = parser.parse_args()

    build_clean_base_dataset(
        input_path=args.input,
        output_path=args.output,
        rejected_path=args.rejected,
        stats_path=args.stats,
    )