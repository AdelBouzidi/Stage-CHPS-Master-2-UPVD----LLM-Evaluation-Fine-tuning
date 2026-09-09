#!/usr/bin/env python3
"""
Test different prompt formats with Open WebUI to see which works best
"""

import requests
import json
import os
from generate_with_openwebui import (
    create_prompt, extract_fortran_code, detect_model_family, call_openwebui
)


def test_prompt_format(model: str, model_family: str, base_url: str, api_key: str = None):
    """
    Test a specific prompt format with a simple problem
    """
    test_problem = {
        'prompt': 'Write a program that reads two integers from the user and prints their sum.'
    }
    
    print(f"\n{'='*70}")
    print(f"Testing: {model_family} format with model {model}")
    print(f"{'='*70}\n")
    
    # Create prompt
    prompt = create_prompt(test_problem, model_family=model_family)
    
    print("Generated prompt:")
    print("-" * 70)
    print(prompt[:500])
    if len(prompt) > 500:
        print("... (truncated)")
    print("-" * 70)
    
    # Call Open WebUI
    print("\nCalling Open WebUI...")
    try:
        generated = call_openwebui(prompt, model, base_url=base_url, api_key=api_key, temperature=0.7)
        
        if not generated:
            print("✗ No response received")
            return None
        
        print(f"\n✓ Generated {len(generated)} characters")
        
        # Extract code
        code = extract_fortran_code(generated)
        
        print(f"\nExtracted code ({len(code)} chars):")
        print("-" * 70)
        print(code[:500])
        if len(code) > 500:
            print("... (truncated)")
        print("-" * 70)
        
        # Check if it looks like valid Fortran
        checks = {
            'Has "program"': 'program' in code.lower(),
            'Has "implicit none"': 'implicit none' in code.lower(),
            'Has "end program"': 'end program' in code.lower(),
            'Long enough': len(code) > 50,
        }
        
        print("\nCode quality checks:")
        all_passed = True
        for check, passed in checks.items():
            status = "✓" if passed else "✗"
            print(f"  {status} {check}")
            if not passed:
                all_passed = False
        
        if all_passed:
            print(f"\n✓✓✓ {model_family} format looks GOOD for this model!")
        else:
            print(f"\n⚠ {model_family} format may need adjustment")
        
        return code
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return None


def compare_all_formats(model: str, base_url: str, api_key: str = None):
    """
    Test all available prompt formats
    """
    formats = [
        'mistral', 'qwen', 'deepseek', 'codellama', 'gpt',
        'llama3', 'gemma', 'phi', 'generic-instruct', 'base'
    ]
    
    # Auto-detect
    detected = detect_model_family(model)
    
    print(f"\n{'='*70}")
    print(f"TESTING ALL PROMPT FORMATS FOR: {model}")
    print(f"Auto-detected family: {detected}")
    print(f"{'='*70}")
    
    results = {}
    
    for fmt in formats:
        print(f"\n\n{'#'*70}")
        print(f"# Format: {fmt}")
        print(f"{'#'*70}")
        
        code = test_prompt_format(model, fmt, base_url, api_key)
        
        if code:
            score = 0
            if 'program' in code.lower():
                score += 1
            if 'implicit none' in code.lower():
                score += 1
            if 'end program' in code.lower():
                score += 1
            if len(code) > 50:
                score += 1
            
            results[fmt] = {
                'score': score,
                'code_length': len(code)
            }
        else:
            results[fmt] = {
                'score': 0,
                'code_length': 0
            }
    
    # Summary
    print(f"\n\n{'='*70}")
    print("SUMMARY - Best to Worst")
    print(f"{'='*70}\n")
    
    sorted_results = sorted(results.items(), key=lambda x: x[1]['score'], reverse=True)
    
    print(f"{'Format':<20} {'Score':<10} {'Code Length':<15} {'Recommendation'}")
    print("-" * 70)
    
    for fmt, data in sorted_results:
        score = data['score']
        length = data['code_length']
        
        if score == 4:
            rec = "✓✓✓ EXCELLENT"
        elif score == 3:
            rec = "✓✓ GOOD"
        elif score >= 2:
            rec = "✓ OK"
        else:
            rec = "✗ POOR"
        
        marker = " ← AUTO-DETECTED" if fmt == detected else ""
        print(f"{fmt:<20} {score}/4       {length:<15} {rec}{marker}")
    
    best_format = sorted_results[0][0]
    print(f"\n{'='*70}")
    print(f"RECOMMENDATION: Use --model-family {best_format}")
    print(f"{'='*70}\n")
    
    return best_format


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Test prompt formats for Open WebUI')
    parser.add_argument('--model', type=str, required=True,
                        help='Model to test (e.g., qwen2.5-coder:7b)')
    parser.add_argument('--base-url', type=str, default='http://localhost:8080',
                        help='Open WebUI base URL')
    parser.add_argument('--api-key', type=str, default=None,
                        help='API key for authentication')
    parser.add_argument('--format', type=str, default=None,
                        choices=['mistral', 'qwen', 'deepseek', 'codellama', 'gpt',
                                'llama3', 'gemma', 'phi', 'generic-instruct', 'base'],
                        help='Test specific format (default: test all)')
    parser.add_argument('--compare-all', action='store_true',
                        help='Compare all formats and recommend best one')
    
    args = parser.parse_args()
    
    # Get API key from environment if not provided
    api_key = args.api_key or os.environ.get('OPENWEBUI_API_KEY')
    
    if not api_key:
        print("⚠ Warning: No API key provided. This might fail if authentication is required.")
        print("  Set OPENWEBUI_API_KEY environment variable or use --api-key")
    
    if args.compare_all or args.format is None:
        # Test all formats
        best = compare_all_formats(args.model, args.base_url, api_key)
        print(f"\nTo use the best format, run:")
        print(f"  export OPENWEBUI_API_KEY='your-key'")
        print(f"  python run_evaluation_openwebui.py \\")
        print(f"    --benchmark benchmark.json \\")
        print(f"    --model {args.model} \\")
        print(f"    --base-url {args.base_url} \\")
        print(f"    --model-family {best}")
    else:
        # Test specific format
        test_prompt_format(args.model, args.format, args.base_url, api_key)


