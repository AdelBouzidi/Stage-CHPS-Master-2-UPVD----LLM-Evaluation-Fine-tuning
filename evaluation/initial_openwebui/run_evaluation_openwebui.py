import json
import argparse
import time
import os
from datetime import datetime
from evaluate import evaluation
from generate_with_openwebui import generate_solutions


def run_full_evaluation(benchmark_file: str, model: str, 
                       base_url: str = "http://localhost:8080", 
                       output_dir: str = "results", api_key: str = None,
                       model_family: str = None):
    """
    Complete pipeline: generate solutions and evaluate them using Open WebUI
    
    Args:
        model_family: Override auto-detection. Options: mistral, qwen, deepseek, codellama,
                     gpt, llama3, gemma, phi, generic-instruct, base
    """
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Define output files
    model_safe = model.replace(':', '_').replace('/', '_')
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    solutions_file = f"{output_dir}/{model_safe}_{timestamp}_solutions.json"
    results_file = f"{output_dir}/{model_safe}_{timestamp}_results.json"
    
    print(f"\n{'='*60}")
    print(f"Running evaluation for model: {model}")
    print(f"Using Open WebUI at: {base_url}")
    if model_family:
        print(f"Prompt format: {model_family} (manual)")
    else:
        print(f"Prompt format: auto-detect")
    print(f"{'='*60}\n")
    
    # Track start time
    start_time = time.time()
    
    # Step 1: Generate solutions
    print("Step 1: Generating solutions with Open WebUI...")
    generate_start = time.time()
    generate_solutions(benchmark_file, solutions_file, model, base_url=base_url, 
                      api_key=api_key, model_family=model_family)
    generate_time = time.time() - generate_start
    
    # Step 2: Load benchmark and solutions
    print("\nStep 2: Loading benchmark and solutions...")
    with open(benchmark_file, 'r') as f:
        benchmark = json.load(f)
    
    with open(solutions_file, 'r') as f:
        inference = json.load(f)
    
    # Step 3: Evaluate
    print("\nStep 3: Evaluating solutions...")
    eval_start = time.time()
    counts, logs = evaluation(benchmark, inference)
    eval_time = time.time() - eval_start
    
    total_time = time.time() - start_time
    
    # Step 4: Calculate and display results
    print("\n" + "="*60)
    print("EVALUATION RESULTS")
    print("="*60)
    
    total = len(inference)
    passed = counts['ok']
    
    print(f"\nModel: {model}")
    print(f"Total problems: {total}")
    print(f"Passed: {passed} ({100*passed/total:.2f}%)")
    print(f"\nBreakdown:")
    print(f"  ✓ OK:            {counts['ok']:3d} ({100*counts['ok']/total:5.2f}%)")
    print(f"  ✗ Compile Error: {counts['compile_err']:3d} ({100*counts['compile_err']/total:5.2f}%)")
    print(f"  ✗ Runtime Error: {counts['runtime_err']:3d} ({100*counts['runtime_err']/total:5.2f}%)")
    print(f"  ✗ Wrong Output:  {counts['ineq']:3d} ({100*counts['ineq']/total:5.2f}%)")
    print(f"  ✗ Exception:     {counts['exception']:3d} ({100*counts['exception']/total:5.2f}%)")
    
    print(f"\nTiming:")
    print(f"  Generation time: {generate_time:.2f}s ({generate_time/total:.2f}s per problem)")
    print(f"  Evaluation time: {eval_time:.2f}s")
    print(f"  Total time: {total_time:.2f}s")
    
    # Save detailed results
    results = {
        'model': model,
        'base_url': base_url,
        'model_family': model_family,
        'total': total,
        'passed': passed,
        'pass_rate': passed / total,
        'counts': counts,
        'logs': logs,
        'timing': {
            'generation_time': generate_time,
            'evaluation_time': eval_time,
            'total_time': total_time,
            'per_problem_time': generate_time / total
        }
    }
    
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDetailed results saved to: {results_file}")
    print(f"Solutions saved to: {solutions_file}")
    
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Fortran-HumanEval evaluation with Open WebUI')
    parser.add_argument('--benchmark', type=str, required=True,
                        help='Path to benchmark JSON file')
    parser.add_argument('--model', type=str, required=True,
                        help='Model name (e.g., qwen2.5-coder:32b)')
    parser.add_argument('--base-url', type=str, default='http://localhost:8080',
                        help='Open WebUI base URL')
    parser.add_argument('--api-key', type=str, default=None,
                        help='API key for Open WebUI authentication')
    parser.add_argument('--model-family', type=str, default=None,
                        choices=['mistral', 'qwen', 'deepseek', 'codellama', 'gpt',
                                'llama3', 'gemma', 'phi', 'generic-instruct', 'base'],
                        help='Model family for prompt format (auto-detected if not specified)')
    parser.add_argument('--output-dir', type=str, default='results',
                        help='Directory to save results')
    
    args = parser.parse_args()
    
    # Get API key from environment if not provided
    api_key = args.api_key or os.environ.get('OPENWEBUI_API_KEY')
    
    run_full_evaluation(args.benchmark, args.model, args.base_url, args.output_dir, api_key, args.model_family)


