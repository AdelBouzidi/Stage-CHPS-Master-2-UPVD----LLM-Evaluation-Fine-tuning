import json
import requests
from tqdm import tqdm
import argparse
import re
import os


def call_openwebui(prompt: str, model: str, base_url: str = "http://localhost:8080", 
                   api_key: str = None, temperature: float = 0.7, use_ollama_direct: bool = False) -> str:
    """
    Calls Open WebUI API to generate code completion
    """
    try:
        headers = {
            'Content-Type': 'application/json',
        }
        
        # Add API key if provided
        if api_key:
            headers['Authorization'] = f'Bearer {api_key}'
        
        # Try Ollama direct API first if requested
        if use_ollama_direct:
            return call_ollama_direct(prompt, model, base_url, headers, temperature)
        
        # Open WebUI uses OpenAI-compatible API
        endpoints_to_try = [
            '/api/chat/completions',
            '/v1/chat/completions',
            '/ollama/v1/chat/completions'
        ]
        
        last_error = None
        for endpoint in endpoints_to_try:
            try:
                response = requests.post(
                    f'{base_url}{endpoint}',
                    headers=headers,
                    json={
                        'model': model,
                        'messages': [
                            {
                                'role': 'user',
                                'content': prompt
                            }
                        ],
                        'temperature': temperature,
                        'max_tokens': 2048,
                        'stream': False
                    },
                    timeout=300
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if 'choices' in result and len(result['choices']) > 0:
                        return result['choices'][0]['message']['content']
                
                elif response.status_code == 401:
                    last_error = f"Authentication required at {endpoint}"
                    continue
                
                else:
                    last_error = f"{endpoint}: HTTP {response.status_code}"
                    continue
                    
            except Exception as e:
                last_error = f"{endpoint}: {e}"
                continue
        
        # If all attempts failed, try Ollama direct API
        print(f"OpenAI-compatible endpoints failed, trying Ollama direct API...")
        return call_ollama_direct(prompt, model, base_url, headers, temperature)
            
    except Exception as e:
        print(f"Error calling Open WebUI: {e}")
        return ""


def call_ollama_direct(prompt: str, model: str, base_url: str, headers: dict, temperature: float) -> str:
    """
    Try calling Ollama's native API directly through Open WebUI
    """
    ollama_endpoints = [
        '/ollama/api/generate',
        '/api/generate'
    ]
    
    for endpoint in ollama_endpoints:
        try:
            response = requests.post(
                f'{base_url}{endpoint}',
                headers=headers,
                json={
                    'model': model,
                    'prompt': prompt,
                    'stream': False,
                    'options': {
                        'temperature': temperature,
                        'num_predict': 2048
                    }
                },
                timeout=300
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'response' in result:
                    return result['response']
            elif response.status_code == 401:
                print(f"Authentication required at {endpoint}")
            else:
                print(f"{endpoint}: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"Error with {endpoint}: {e}")
            continue
    
    print("All API endpoints failed. Please check authentication.")
    return ""


def extract_fortran_code(response: str) -> str:
    """
    Extracts Fortran code from the model response.
    Removes markdown, explanations, and ensures clean executable code.
    """
    # Try to find code blocks with fortran/f90 markers
    patterns = [
        r'```fortran\s*(.*?)```',
        r'```f90\s*(.*?)```',
        r'```\s*(program\s+\w+.*?end\s+program.*?)```',
        r'```\s*(.*?)```',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, response, re.DOTALL | re.IGNORECASE)
        if matches:
            code = matches[0].strip()
            if 'program' in code.lower() or 'implicit none' in code.lower():
                # Clean up the code
                code = clean_fortran_code(code)
                return code
    
    # Try to find program blocks without markdown
    program_pattern = r'(program\s+\w+.*?end\s+program\s+\w+)'
    matches = re.findall(program_pattern, response, re.DOTALL | re.IGNORECASE)
    if matches:
        return clean_fortran_code(matches[0].strip())
    
    # If response itself is Fortran code
    if 'program' in response.lower() and 'end program' in response.lower():
        return clean_fortran_code(response.strip())
    
    return response.strip()


def clean_fortran_code(code: str) -> str:
    """
    Clean Fortran code to ensure it's directly executable.
    Removes common artifacts and formatting issues.
    """
    # Remove leading/trailing whitespace
    code = code.strip()
    
    # Remove any remaining markdown artifacts
    code = code.replace('```fortran', '').replace('```f90', '').replace('```', '')
    
    # Remove common prefixes that models add
    prefixes_to_remove = [
        'Here is the code:',
        'Here\'s the code:',
        'Here is the Fortran program:',
        'Here\'s the Fortran program:',
        'Solution:',
        'Program:',
    ]
    
    for prefix in prefixes_to_remove:
        if code.startswith(prefix):
            code = code[len(prefix):].strip()
    
    # Remove any text after 'end program'
    end_pattern = r'(.*end\s+program\s+\w+)'
    match = re.search(end_pattern, code, re.DOTALL | re.IGNORECASE)
    if match:
        code = match.group(1)
    
    return code.strip()


def detect_model_family(model_name: str) -> str:
    """
    Auto-detect model family from model name
    """
    model_lower = model_name.lower()
    
    if 'mistral' in model_lower and 'instruct' in model_lower:
        return 'mistral'
    elif 'qwen' in model_lower or 'qwq' in model_lower:
        return 'qwen'
    elif 'deepseek' in model_lower and 'instruct' in model_lower:
        return 'deepseek'
    elif 'codellama' in model_lower and 'instruct' in model_lower:
        return 'codellama'
    elif 'gpt' in model_lower or 'chatgpt' in model_lower:
        return 'gpt'
    elif 'llama-3' in model_lower or 'llama3' in model_lower:
        return 'llama3'
    elif 'gemma' in model_lower:
        return 'gemma'
    elif 'phi' in model_lower:
        return 'phi'
    elif 'instruct' in model_lower or 'chat' in model_lower:
        return 'generic-instruct'
    else:
        return 'base'


def create_prompt_mistral(problem_text: str) -> str:
    """Mistral-Instruct format"""
    base_instruction = """You are an expert Fortran programmer. Write a complete, working Fortran 90 program.

Requirements:
- Write ONLY the Fortran code, nothing else
- Include: program name, implicit none, variable declarations, logic, and end program
- Code must compile with gfortran
- NO explanations before or after the code"""

    return f"""[INST] {base_instruction}

Problem:
{problem_text}

Write the complete Fortran 90 program now: [/INST]

```fortran
"""


def create_prompt_qwen(problem_text: str) -> str:
    """Qwen/Qwen2.5-Coder format (ChatML-style)"""
    return f"""<|im_start|>system
You are Qwen, an expert Fortran programmer. Generate only valid, compilable Fortran 90 code.<|im_end|>
<|im_start|>user
Write a complete Fortran 90 program that solves this problem. Include program name, implicit none, declarations, logic, and end program. Output ONLY the code in a ```fortran block, no explanations.

Problem:
{problem_text}<|im_end|>
<|im_start|>assistant
```fortran
"""


def create_prompt_deepseek(problem_text: str) -> str:
    """DeepSeek-Coder-Instruct format"""
    return f"""### System:
You are an AI programming assistant specialized in Fortran. Generate only valid, compilable code.

### Instruction:
Write a complete Fortran 90 program that solves the following problem.

Requirements:
- Full program structure: program name, implicit none, variable declarations, logic, end program
- Must compile with gfortran
- Output ONLY code, no explanations

Problem:
{problem_text}

### Response:
```fortran
"""


def create_prompt_codellama(problem_text: str) -> str:
    """CodeLlama-Instruct format"""
    return f"""[INST] Write a complete Fortran 90 program that solves this problem.

Include the full program structure with program name, implicit none, variable declarations, and end program.

Problem:
{problem_text}
[/INST]

```fortran
"""


def create_prompt_gpt(problem_text: str) -> str:
    """GPT/ChatGPT format (OpenAI-style) - IMPROVED"""
    return f"""You are an expert Fortran programmer. Your task is to write a COMPLETE, WORKING Fortran 90 program that SOLVES THE EXACT PROBLEM DESCRIBED BELOW.

CRITICAL REQUIREMENTS:
- READ THE PROBLEM CAREFULLY and solve EXACTLY what is asked
- DO NOT write a generic "Hello World" program
- DO NOT write example/demo code
- Write code that SOLVES THE SPECIFIC PROBLEM
- Include full program structure: program name, implicit none, declarations, logic, end program
- Handle ALL inputs and outputs as specified in the problem
- Code must compile with gfortran and PRODUCE CORRECT OUTPUT

PROBLEM TO SOLVE:
{problem_text}

Now write the COMPLETE Fortran 90 program that solves THIS SPECIFIC PROBLEM:

```fortran
"""


def create_prompt_llama3(problem_text: str) -> str:
    """Llama 3 Instruct format"""
    return f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are an expert Fortran programmer. Generate only valid, compilable Fortran 90 code.<|eot_id|><|start_header_id|>user<|end_header_id|>

Write a complete Fortran 90 program for this problem. Include program name, implicit none, declarations, logic, and end program. Output ONLY code.

Problem:
{problem_text}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

```fortran
"""


def create_prompt_gemma(problem_text: str) -> str:
    """Gemma/CodeGemma format"""
    return f"""<start_of_turn>user
Write a complete Fortran 90 program that solves this problem. Include full program structure. Output only code.

Problem:
{problem_text}<end_of_turn>
<start_of_turn>model
```fortran
"""


def create_prompt_phi(problem_text: str) -> str:
    """Phi models format"""
    return f"""<|system|>
You are an expert Fortran programmer.<|end|>
<|user|>
Write a complete Fortran 90 program for: {problem_text}

Include program name, implicit none, declarations, and end program. Output ONLY code.<|end|>
<|assistant|>
```fortran
"""


def create_prompt_generic_instruct(problem_text: str) -> str:
    """Generic instruction-following format - IMPROVED"""
    return f"""### Instruction:
You are an expert Fortran programmer. Write a COMPLETE Fortran 90 program that solves the EXACT problem described below.

IMPORTANT:
- READ the problem carefully
- Solve THE SPECIFIC PROBLEM, not a generic example
- Include program name, implicit none, variable declarations, logic, and end program
- Handle inputs and outputs EXACTLY as specified
- Code must compile with gfortran and produce CORRECT results

### Problem:
{problem_text}

### Response:
```fortran
"""


def create_prompt_base(problem_text: str) -> str:
    """Base models (non-instruct) - completion style"""
    return f"""! Problem: {problem_text}
! Solution in Fortran 90:

program solution
    implicit none
    
"""


def create_prompt(problem: dict, model_family: str = None, model_name: str = None) -> str:
    """
    Creates a prompt based on model family.
    Auto-detects family from model name if not specified.
    
    Handles both formats:
    - Standard: {"prompt": "...", ...}
    - HumanEval: {"task": "...", "signature": "...", "example": "...", ...}
    """
    # Try to get prompt from different possible fields
    problem_text = problem.get('prompt', '')
    
    # If no prompt, try HumanEval format
    if not problem_text:
        task = problem.get('task', '')
        signature = problem.get('signature', '')
        example = problem.get('example', '')
        
        if task:
            problem_text = f"""You are an assistant for writing Fortran90 code.

Task: {task}

Function Signature (in pseudocode): {signature}

Example Input/Output: {example}

CRITICAL REQUIREMENTS:
1. Write a COMPLETE Fortran 90 program (not just a function)
2. Include full program structure: 'program name' ... 'end program name'
3. Include 'implicit none' and all necessary variable declarations
4. Read input from stdin EXACTLY as shown in the example
5. Write output to stdout EXACTLY as shown in the example
6. For boolean outputs, use '.true.' or '.false.' (lowercase with dots)
7. For arrays in output, separate elements with spaces
8. If output strings contain spaces, use [s] instead of space (for array compatibility)
9. The code must be ready to compile with gfortran and execute directly

Format Notes:
- Input arrays: elements separated by whitespaces
- Input parameters: separated by newlines (\\n)
- Output arrays: elements separated by spaces
- Boolean values: .true. or .false. (Fortran format)

Write ONLY the executable Fortran code, no explanations."""
    
    # Auto-detect if not specified
    if model_family is None and model_name:
        model_family = detect_model_family(model_name)
    elif model_family is None:
        model_family = 'generic-instruct'
    
    # Route to appropriate prompt format
    prompt_functions = {
        'mistral': create_prompt_mistral,
        'qwen': create_prompt_qwen,
        'deepseek': create_prompt_deepseek,
        'codellama': create_prompt_codellama,
        'gpt': create_prompt_gpt,
        'llama3': create_prompt_llama3,
        'gemma': create_prompt_gemma,
        'phi': create_prompt_phi,
        'generic-instruct': create_prompt_generic_instruct,
        'base': create_prompt_base
    }
    
    prompt_func = prompt_functions.get(model_family, create_prompt_generic_instruct)
    return prompt_func(problem_text)


def generate_solutions(benchmark_file: str, output_file: str, model: str, 
                      base_url: str = "http://localhost:8080", api_key: str = None,
                      model_family: str = None):
    """
    Generate solutions for all problems in the benchmark using Open WebUI
    
    Args:
        model_family: Override auto-detection. Options: mistral, qwen, deepseek, codellama,
                     gpt, llama3, gemma, phi, generic-instruct, base
    """
    # Load benchmark
    with open(benchmark_file, 'r') as f:
        benchmark = json.load(f)
    
    # Auto-detect or use specified family
    if model_family is None:
        model_family = detect_model_family(model)
        print(f"Auto-detected model family: {model_family}")
    else:
        print(f"Using specified model family: {model_family}")
    
    results = []
    
    print(f"Generating solutions using Open WebUI at: {base_url}")
    print(f"Model: {model}")
    print(f"Prompt format: {model_family}")
    print(f"Total problems: {len(benchmark)}")
    print("")
    
    failed_extractions = 0
    
    for i, problem in enumerate(tqdm(benchmark, desc="Generating")):
        # Create prompt with appropriate format
        prompt = create_prompt(problem, model_family=model_family, model_name=model)
        
        # Get response from Open WebUI
        response = call_openwebui(prompt, model, base_url=base_url, api_key=api_key)
        
        # Extract code
        code = extract_fortran_code(response)
        
        # Warn if extraction seems to have failed
        if not code or len(code) < 50 or 'program' not in code.lower():
            failed_extractions += 1
            print(f"\n⚠ Warning: Problem {i} - extracted code looks invalid")
            print(f"   Response length: {len(response)}, Code length: {len(code)}")
            if response:
                print(f"   First 100 chars of response: {response[:100]}...")
        
        # Store result
        result = {
            'task_id': problem.get('task_id', i),
            'code': code,
            'raw_response': response
        }
        results.append(result)
        
        # Save intermediate results every 10 problems
        if (i + 1) % 10 == 0:
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)
    
    # Save final results
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"Generation complete! Saved to {output_file}")
    print(f"Model family used: {model_family}")
    print(f"Failed extractions: {failed_extractions}/{len(benchmark)}")
    if failed_extractions > len(benchmark) * 0.5:
        print("⚠ WARNING: More than 50% of extractions failed!")
        print("   Consider adjusting model-family or trying a different model")
    print(f"{'='*60}\n")
    
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate Fortran solutions using Open WebUI')
    parser.add_argument('--benchmark', type=str, required=True, 
                        help='Path to benchmark JSON file')
    parser.add_argument('--output', type=str, required=True,
                        help='Output file for generated solutions')
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
    
    args = parser.parse_args()
    
    # Get API key from environment if not provided
    api_key = args.api_key or os.environ.get('OPENWEBUI_API_KEY')
    
    generate_solutions(args.benchmark, args.output, args.model, args.base_url, api_key, args.model_family)


