#!/usr/bin/env python3
"""
Script d'analyse fusionnée - VERSION CORRIGÉE
Combine l'analyse Fortran avec les résultats d'exécution
BUG FIX: Calcul correct du pass_rate
"""

import json
import re
import argparse
import sys
from pathlib import Path
from typing import List, Dict, Optional, Tuple

def load_json_file(file_path: Path) -> Optional[Dict]:
    """Charge un fichier JSON"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        print(f"⚠️  Erreur JSON dans {file_path.name}: {str(e)}")
        return None

def is_fortran_code(response: str, min_keywords: int = 2) -> bool:
    """Vérifie si le texte contient du code Fortran"""
    if not response or not response.strip():
        return False
    
    fortran_keywords = [
        r'\bprogram\b', r'\bsubroutine\b', r'\bfunction\b', r'\bmodule\b',
        r'\bimplicit\s+none\b', r'\binteger\b', r'\breal\b', r'\bcharacter\b',
        r'\blogical\b', r'\bcomplex\b', r'\bend\s+program\b', r'\bend\s+subroutine\b',
        r'\bend\s+function\b', r'\bend\s+module\b', r'\bdo\b', r'\bif\s*\(',
        r'\bread\s*\(', r'\bwrite\s*\(',
    ]
    
    matches = sum(1 for keyword in fortran_keywords if re.search(keyword, response, re.IGNORECASE))
    return matches >= min_keywords

def extract_exception_types(exceptions_log: List) -> Dict[str, int]:
    """Extrait les types d'exceptions"""
    exception_types = {}
    
    for exc in exceptions_log:
        if not exc:
            continue
        
        if "utf-8" in str(exc).lower() and "codec" in str(exc).lower():
            exception_types["UTF-8 codec error"] = exception_types.get("UTF-8 codec error", 0) + 1
        elif "dict" in str(exc).lower():
            exception_types["Dict encode error"] = exception_types.get("Dict encode error", 0) + 1
        else:
            exception_types["Other exception"] = exception_types.get("Other exception", 0) + 1
    
    return exception_types

def analyze_single_file_pair(solutions_path: Path, results_path: Path, min_keywords: int = 2) -> Optional[Dict]:
    """Analyse une paire de fichiers (solutions + results)"""
    # Charger les données
    solutions_data = load_json_file(solutions_path)
    results_data = load_json_file(results_path)
    
    if solutions_data is None or results_data is None:
        return None
    
    # Extraire le nom du modèle
    model_name = solutions_path.stem.replace('_solutions', '')
    
    # Analyser les solutions
    valid_tasks = []
    empty_tasks = []
    invalid_tasks = []
    
    if isinstance(solutions_data, list):
        for task in solutions_data:
            task_id = task.get('task_id')
            raw_response = task.get('raw_response', '').strip()
            
            if not raw_response:
                empty_tasks.append(task_id)
            elif not is_fortran_code(raw_response, min_keywords=min_keywords):
                invalid_tasks.append(task_id)
            else:
                valid_tasks.append(task_id)
    
    total_solutions = len(solutions_data) if isinstance(solutions_data, list) else 0
    solutions_success_rate = (len(valid_tasks) / total_solutions * 100) if total_solutions > 0 else 0
    
    # EXTRACTION DU PASS_RATE - CORRECTEMENT
    # Le pass_rate peut être en format décimal (0.414) ou pourcentage (41.4)
    pass_rate_raw = results_data.get('pass_rate', 0.0)
    
    # Déterminer le format et convertir en pourcentage
    if pass_rate_raw <= 1.0:
        # Format décimal: 0.414 -> 41.4%
        pass_rate_value = pass_rate_raw * 100.0
    else:
        # Format pourcentage: 41.4 -> 41.4%
        pass_rate_value = float(pass_rate_raw)
    
    # Extraire les autres métriques
    total_tasks = results_data.get('total', 0)
    passed = results_data.get('passed', 0)
    
    counts = results_data.get('counts', {})
    ineq_count = counts.get('ineq', 0)
    runtime_err_count = counts.get('runtime_err', 0)
    ok_count = counts.get('ok', 0)
    exception_count = counts.get('exception', 0)
    compile_err_count = counts.get('compile_err', 0)
    
    # Extraire les logs pour les comptages exacts
    exceptions_log = results_data.get('logs', {}).get('exception', [])
    exception_types = extract_exception_types(exceptions_log)
    
    compile_err_log = results_data.get('logs', {}).get('compile_err', [])
    runtime_err_log = results_data.get('logs', {}).get('runtime_err', [])
    
    return {
        "model_name": model_name,
        "solutions_file": solutions_path.name,
        "results_file": results_path.name,
        
        # Analyse Fortran
        "fortran_analysis": {
            "total_tasks": total_solutions,
            "valid_code": len(valid_tasks),
            "empty_code": len(empty_tasks),
            "invalid_code": len(invalid_tasks),
            "success_rate": round(solutions_success_rate, 2),
            "valid_task_ids": sorted(valid_tasks),
            "empty_task_ids": sorted(empty_tasks),
            "invalid_task_ids": sorted(invalid_tasks),
        },
        
        # Métriques d'exécution
        "execution_metrics": {
            "total_tasks": total_tasks,
            "passed": passed,
            "pass_rate": round(pass_rate_value, 2),  # ✅ CORRIGÉ: utilise pass_rate_value
            "compile_errors": compile_err_count,
            "runtime_errors": runtime_err_count,
            "incorrect_output": ineq_count,
            "exceptions": exception_count,
            "success_tests": ok_count,
        },
        
        # Détails exceptions
        "exception_details": {
            "total_exceptions": exception_count,
            "exception_types": exception_types,
            "exception_logs": exceptions_log[:5] if exceptions_log else [],
        },
        
        # Résumé
        "summary": {
            "model_name": model_name,
            "code_quality_rate": round(solutions_success_rate, 2),
            "execution_pass_rate": round(pass_rate_value, 2),  # ✅ CORRIGÉ
            "combined_score": round((solutions_success_rate + pass_rate_value) / 2, 2),  # ✅ CORRIGÉ
        }
    }

def find_file_pairs(directory: Path) -> List[Tuple[Path, Path]]:
    """Trouve les paires de fichiers (solutions, results)"""
    pairs = []
    
    solutions_files = list(directory.glob('*_solutions.json'))
    
    for solutions_file in sorted(solutions_files):
        model_name = solutions_file.stem.replace('_solutions', '')
        results_file = directory / f"{model_name}_results.json"
        
        if results_file.exists():
            pairs.append((solutions_file, results_file))
    
    return pairs

def analyze_all_pairs(directory: Path = Path('.'), min_keywords: int = 2, verbose: bool = False) -> Dict:
    """Analyse tous les fichiers appairés"""
    file_pairs = find_file_pairs(directory)
    
    if not file_pairs:
        print(f"❌ Aucune paire de fichiers trouvée dans {directory}")
        return {"success": False, "error": "No file pairs found"}
    
    print(f"📁 Paires trouvées: {len(file_pairs)}")
    print("-" * 80)
    
    results = []
    
    for solutions_path, results_path in file_pairs:
        print(f"📄 Analyse: {solutions_path.name}...", end=" ", flush=True)
        
        result = analyze_single_file_pair(solutions_path, results_path, min_keywords=min_keywords)
        
        if result:
            results.append(result)
            pass_rate = result['execution_metrics']['pass_rate']
            fortran_valid = result['fortran_analysis']['valid_code']
            fortran_total = result['fortran_analysis']['total_tasks']
            print(f"✓ (Fortran: {fortran_valid}/{fortran_total}, Pass rate: {pass_rate:.2f}%)")
            
            if verbose:
                print(f"   Score combiné: {result['summary']['combined_score']:.2f}%")
        else:
            print("✗ (Erreur)")
    
    # Trier par score combiné
    results.sort(key=lambda x: x['summary']['combined_score'], reverse=True)
    
    # Calculer statistiques globales
    total_fortran_valid = sum(r['fortran_analysis']['valid_code'] for r in results)
    total_tasks_analyzed = sum(r['fortran_analysis']['total_tasks'] for r in results)
    
    # Moyenne des pass rates
    avg_pass_rate = sum(r['execution_metrics']['pass_rate'] for r in results) / len(results) if results else 0
    avg_code_quality = (total_fortran_valid / total_tasks_analyzed * 100) if total_tasks_analyzed > 0 else 0
    
    summary = {
        "success": True,
        "summary": {
            "total_files": len(file_pairs),
            "total_tasks_analyzed": total_tasks_analyzed,
            "total_fortran_valid": total_fortran_valid,
            "average_code_quality": round(avg_code_quality, 2),
            "average_execution_pass_rate": round(avg_pass_rate, 2),  # ✅ CORRIGÉ: moyenne correcte
        },
        "models": results,
    }
    
    return summary

def print_summary(summary: Dict, verbose: bool = False) -> None:
    """Affiche le résumé"""
    print("\n" + "=" * 80)
    print("📊 RÉSUMÉ CONSOLIDÉ - SOLUTIONS + RÉSULTATS D'EXÉCUTION")
    print("=" * 80)
    
    s = summary.get("summary", {})
    print(f"\n📈 Statistiques globales:")
    print(f"   Nombre de modèles: {s.get('total_files', 0)}")
    print(f"   Total des tâches: {s.get('total_tasks_analyzed', 0)}")
    print(f"   ✓ Code Fortran valide: {s.get('total_fortran_valid', 0)}")
    print(f"   📊 Qualité code moyenne: {s.get('average_code_quality', 0):.2f}%")
    print(f"   📊 Pass rate d'exécution moyen: {s.get('average_execution_pass_rate', 0):.2f}%")
    
    print(f"\n🏆 Résultats par modèle (triés par score):")
    print("-" * 80)
    
    for i, model in enumerate(summary.get("models", []), 1):
        summary_data = model['summary']
        exec_m = model['execution_metrics']
        fortran = model['fortran_analysis']
        
        print(f"\n  #{i}. {summary_data['model_name']}:")
        print(f"     Code Fortran: {fortran['valid_code']}/{fortran['total_tasks']} ({fortran['success_rate']:.2f}%)")
        print(f"     Exécution: {exec_m['passed']}/{exec_m['total_tasks']} tests ({exec_m['pass_rate']:.2f}%)")
        
        if model.get('exception_details', {}).get('exception_types'):
            exc_types = model['exception_details']['exception_types']
            print(f"     Exceptions: {', '.join(f'{k}: {v}' for k, v in exc_types.items())}")
        
        print(f"     Score combiné: {summary_data['combined_score']:.2f}%")
    
    print("\n" + "=" * 80)

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(
        description="Analyse les fichiers *_solutions.json et *_results.json",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Exemples:\n  python script.py\n  python script.py -v -o rapport.json"
    )
    
    parser.add_argument('-d', '--directory', type=str, default='.',
                       help="Répertoire à analyser (défaut: courant)")
    parser.add_argument('-o', '--output', dest='output_file',
                       help="Fichier JSON de sortie")
    parser.add_argument('-v', '--verbose', action='store_true',
                       help="Mode verbeux")
    parser.add_argument('-m', '--min-keywords', type=int, default=2,
                       help="Mots-clés Fortran min (défaut: 2)")
    
    args = parser.parse_args()
    
    directory = Path(args.directory)
    if not directory.exists():
        print(f"❌ Erreur: {args.directory} n'existe pas")
        sys.exit(1)
    
    print("=" * 80)
    print("ANALYSE COMPLÈTE - SOLUTIONS + RÉSULTATS D'EXÉCUTION (CORRIGÉE)")
    print("=" * 80)
    print(f"📂 Répertoire: {directory.absolute()}\n")
    
    summary = analyze_all_pairs(directory, args.min_keywords, args.verbose)
    
    print_summary(summary, args.verbose)
    
    if args.output_file:
        output_path = Path(args.output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Résultats sauvegardés dans: {output_path.absolute()}")
    
    sys.exit(0 if summary.get("success") else 1)

if __name__ == "__main__":
    main()
