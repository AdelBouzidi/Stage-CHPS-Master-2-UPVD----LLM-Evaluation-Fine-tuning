import json
import requests
from tqdm import tqdm
import argparse
import re
import os
import time
from datetime import datetime


def estimate_model_size(model_name: str) -> int:
    """
    Estimate model size in billions of parameters from model name.
    Returns the estimated parameter count, or 0 if unknown.
    
    Prefers explicit size mentions (like "87B") over derived sizes (like "2x32B")
    """
    model_lower = model_name.lower()
    
    # First, try to find explicit large model sizes (70B+)
    # These are usually the actual model size, not component sizes
    explicit_large = re.search(r'(?:^|[^\d])([7-9]\d|[1-9]\d{2,})b(?:[^\d]|$)', model_lower)
    if explicit_large:
        return int(explicit_large.group(1))
    
    # Then try patterns in order of specificity
    size_patterns = [
        # MoE and multi-model patterns
        (r'(\d+)x(\d+)b', lambda m: int(m.group(1)) * int(m.group(2))),  # 8x7b = 56b
        (r'2x(\d+)b', lambda m: int(m.group(1)) * 2),  # 2x32b = 64b
        # Decimal patterns
        (r'(\d+)\.(\d+)b', lambda m: int(float(m.group(1) + '.' + m.group(2)))),    # 1.5b, 7.5b
        # Simple patterns
        (r'(\d+)b', lambda m: int(m.group(1))),           # 7b, 13b, 70b, 87b
    ]
    
    for pattern, size_extractor in size_patterns:
        match = re.search(pattern, model_lower)
        if match:
            try:
                return size_extractor(match)
            except (ValueError, IndexError, AttributeError):
                continue
    
    return 0  # Unknown size


def calculate_timeout(model_name: str, default_timeout: int = 300) -> tuple:
    """
    Calculate appropriate timeout based on model size.
    Returns (timeout_seconds, model_size_billions, reasoning)
    """
    model_size = estimate_model_size(model_name)
    
    if model_size == 0:
        return (default_timeout, 0, "Unknown model size, using default timeout")
    
    # Timeout calculation based on empirical observations:
    # - Small models (< 10B): 180s (3 min)
    # - Medium models (10-20B): 300s (5 min)  
    # - Large models (20-40B): 600s (10 min)
    # - Very large models (40-70B): 900s (15 min)
    # - Huge models (70B+): 1200s (20 min)
    
    if model_size < 10:
        timeout = 180
        category = "small"
    elif model_size < 20:
        timeout = 300
        category = "medium"
    elif model_size < 40:
        timeout = 600
        category = "large"
    elif model_size < 70:
        timeout = 900
        category = "very large"
    else:
        timeout = 1200
        category = "huge"
    
    reasoning = f"{model_size}B model ({category}) - estimated {timeout}s timeout"
    return (timeout, model_size, reasoning)


def check_openwebui_endpoints(base_url: str, api_key: str = None) -> dict:
    """
    Check which OpenWebUI/Ollama endpoints are available.
    Returns dict with endpoint availability.
    """
    print(f"\n{'='*60}")
    print("Checking API Endpoint Availability")
    print(f"Base URL: {base_url}")
    print(f"{'='*60}")
    
    headers = {'Content-Type': 'application/json'}
    if api_key:
        headers['Authorization'] = f'Bearer {api_key}'
    
    endpoints_to_check = [
        ('/api/chat/completions', 'OpenAI Chat (primary)'),
        ('/v1/chat/completions', 'OpenAI Chat v1'),
        ('/ollama/v1/chat/completions', 'Ollama via OpenWebUI'),
        ('/ollama/api/chat', 'Ollama Chat Direct'),
        ('/ollama/api/generate', 'Ollama Generate Direct'),
        ('/api/generate', 'Ollama Generate'),
        ('/api/tags', 'Ollama Tags (for checking models)'),
    ]
    
    results = {}
    for endpoint, description in endpoints_to_check:
        try:
            # Use GET for /api/tags, POST for others
            if endpoint == '/api/tags':
                response = requests.get(
                    f'{base_url}{endpoint}',
                    headers=headers,
                    timeout=5
                )
            else:
                # Send minimal valid request
                response = requests.post(
                    f'{base_url}{endpoint}',
                    headers=headers,
                    json={'model': 'test'},  # Minimal payload
                    timeout=5
                )
            
            status = response.status_code
            available = status not in [404, 405, 501]  # Not found or not allowed
            
            results[endpoint] = {
                'available': available,
                'status': status,
                'description': description
            }
            
            status_symbol = '✓' if available else '✗'
            print(f"  {status_symbol} {endpoint:35s} HTTP {status:3d} - {description}")
            
        except requests.exceptions.Timeout:
            results[endpoint] = {'available': False, 'status': 'timeout', 'description': description}
            print(f"  ⚠ {endpoint:35s} TIMEOUT  - {description}")
        except requests.exceptions.ConnectionError:
            results[endpoint] = {'available': False, 'status': 'connection_error', 'description': description}
            print(f"  ✗ {endpoint:35s} CONN ERR - {description}")
        except Exception as e:
            results[endpoint] = {'available': False, 'status': str(e), 'description': description}
            print(f"  ✗ {endpoint:35s} ERROR    - {description}")
    
    # Summary
    available_endpoints = [k for k, v in results.items() if v['available']]
    print(f"\nSummary: {len(available_endpoints)}/{len(endpoints_to_check)} endpoints available")
    
    if available_endpoints:
        print(f"Recommended endpoint: {available_endpoints[0]}")
    else:
        print("⚠ WARNING: No endpoints available! Check:")
        print("  1. Is Open WebUI running?")
        print("  2. Is the base URL correct?")
        print("  3. Is authentication required?")
    
    print(f"{'='*60}\n")
    return results


def call_openwebui(prompt: str, model: str, base_url: str = "http://localhost:8080", 
                   api_key: str = None, temperature: float = 0.7, use_ollama_direct: bool = False,
                   timeout: int = None, max_retries: int = 2) -> str:
    """
    Calls Open WebUI API to generate code completion with improved error handling
    
    Args:
        timeout: Request timeout in seconds (auto-calculated if None)
        max_retries: Number of retry attempts on failure (default 2)
    """
    
    # Auto-calculate timeout based on model size if not provided
    if timeout is None:
        timeout, model_size, reasoning = calculate_timeout(model)
        print(f"  Auto-timeout: {reasoning}")
    
    for attempt in range(max_retries):
        try:
            headers = {
                'Content-Type': 'application/json',
            }
            
            # Add API key if provided
            if api_key:
                headers['Authorization'] = f'Bearer {api_key}'
            
            # Try Ollama direct API first if requested
            if use_ollama_direct:
                result = call_ollama_direct(prompt, model, base_url, headers, temperature, timeout)
                if result:
                    return result
            
            # Open WebUI uses OpenAI-compatible API
            endpoints_to_try = [
                '/api/chat/completions',
                '/v1/chat/completions',
                '/ollama/v1/chat/completions'
            ]
            
            last_error = None
            for endpoint in endpoints_to_try:
                try:
                    if attempt == 0:  # Only print on first attempt
                        print(f"  Trying {endpoint}...", end='', flush=True)
                    start_time = time.time()
                    
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
                        timeout=timeout
                    )
                    
                    elapsed = time.time() - start_time
                    
                    if response.status_code == 200:
                        result = response.json()
                        if 'choices' in result and len(result['choices']) > 0:
                            if attempt == 0:
                                print(f" ✓ ({elapsed:.1f}s)")
                            return result['choices'][0]['message']['content']
                        else:
                            if attempt == 0:
                                print(f" Invalid response")
                            last_error = f"{endpoint}: Invalid response format"
                    
                    elif response.status_code == 401:
                        if attempt == 0:
                            print(f" AUTH")
                        last_error = f"Authentication required at {endpoint}"
                        continue
                    
                    elif response.status_code == 404:
                        if attempt == 0:
                            print(f" 404")
                        last_error = f"{endpoint}: Not found"
                        continue
                    
                    else:
                        if attempt == 0:
                            print(f" {response.status_code}")
                        last_error = f"{endpoint}: HTTP {response.status_code}"
                        continue
                        
                except requests.exceptions.Timeout:
                    if attempt == 0:
                        print(f" TIMEOUT ({timeout}s)")
                    last_error = f"{endpoint}: Timeout after {timeout}s"
                    
                    # Check if we should increase timeout for next attempt
                    if attempt < max_retries - 1:
                        print(f"  Timeout may be too short for this model. Will retry with longer timeout.")
                    continue
                except requests.exceptions.ConnectionError as e:
                    if attempt == 0:
                        print(f" CONN ERR")
                    last_error = f"{endpoint}: Connection error"
                    continue
                except Exception as e:
                    if attempt == 0:
                        print(f" ERR: {str(e)[:30]}")
                    last_error = f"{endpoint}: {e}"
                    continue
            
            # If all OpenAI-style attempts failed, try Ollama direct API
            if attempt == 0:
                print(f"\n  OpenAI endpoints failed, trying Ollama API...")
            result = call_ollama_direct(prompt, model, base_url, headers, temperature, timeout)
            if result:
                return result
            
            # If this attempt failed and we have retries left
            if attempt < max_retries - 1:
                # Increase timeout by 50% for next attempt
                timeout = int(timeout * 1.5)
                wait_time = 5
                print(f"  Retry {attempt + 2}/{max_retries} with increased timeout ({timeout}s) in {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"  All attempts exhausted. Last error: {last_error}")
                
        except Exception as e:
            print(f"  Outer exception: {e}")
            if attempt < max_retries - 1:
                time.sleep(5)
            else:
                return ""
    
    return ""


def call_ollama_direct(prompt: str, model: str, base_url: str, headers: dict, 
                      temperature: float, timeout: int = 900) -> str:
    """
    Try calling Ollama's native API directly
    
    Args:
        timeout: Request timeout in seconds
    """
    # Try both generate and chat endpoints
    endpoints_config = [
        ('/ollama/api/chat', 'chat'),
        ('/api/chat', 'chat'),
        ('/ollama/api/generate', 'generate'),
        ('/api/generate', 'generate')
    ]
    
    for endpoint, api_type in endpoints_config:
        try:
            print(f"  Ollama {endpoint}...", end='', flush=True)
            start_time = time.time()
            
            # Determine request format based on API type
            if api_type == 'chat':
                payload = {
                    'model': model,
                    'messages': [{'role': 'user', 'content': prompt}],
                    'stream': False,
                    'options': {
                        'temperature': temperature,
                        'num_predict': 2048
                    }
                }
            else:  # generate
                payload = {
                    'model': model,
                    'prompt': prompt,
                    'stream': False,
                    'options': {
                        'temperature': temperature,
                        'num_predict': 2048
                    }
                }
            
            response = requests.post(
                f'{base_url}{endpoint}',
                headers=headers,
                json=payload,
                timeout=timeout
            )
            
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                # Handle both /generate and /chat response formats
                if 'response' in result:
                    print(f" ✓ ({elapsed:.1f}s)")
                    return result['response']
                elif 'message' in result and 'content' in result['message']:
                    print(f" ✓ ({elapsed:.1f}s)")
                    return result['message']['content']
                else:
                    print(f" Invalid format")
            elif response.status_code == 401:
                print(f" AUTH")
            elif response.status_code == 404:
                print(f" 404")
            elif response.status_code == 405:
                print(f" 405")
            elif response.status_code == 500:
                print(f" 500")
                # Print more details for 500 errors
                try:
                    error_data = response.json()
                    if 'error' in error_data:
                        error_msg = error_data['error']
                        if 'timeout' in error_msg.lower() or 'time out' in error_msg.lower():
                            print(f"    (Server-side timeout - model too large or slow)")
                        else:
                            print(f"    Error: {error_msg[:100]}")
                except:
                    pass
            else:
                print(f" {response.status_code}")
                
        except requests.exceptions.Timeout:
            print(f" TIMEOUT ({timeout}s)")
        except Exception as e:
            print(f" ERR")
            continue
    
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


def generate_solutions(benchmark_file: str, output_file: str = None, model: str = None, 
                      base_url: str = "http://localhost:8080", api_key: str = None,
                      model_family: str = None, check_endpoints: bool = False, output_dir: str = "results"):
    """
    Generate solutions for all problems in the benchmark using Open WebUI
    
    Args:
        output_file: Path to save solutions (auto-generated if None)
        model_family: Override auto-detection. Options: mistral, qwen, deepseek, codellama,
                     gpt, llama3, gemma, phi, generic-instruct, base
        check_endpoints: Check API endpoint availability before starting (default: False)
        output_dir: Directory for auto-generated output files (default: "results")
    """
    # Auto-generate output filename if not provided
    if output_file is None:
        os.makedirs(output_dir, exist_ok=True)
        model_safe = model.replace(':', '_').replace('/', '_')
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file = f"{output_dir}/{model_safe}_{timestamp}_solutions.json"
        print(f"Auto-generated output file: {output_file}\n")
    
    # Load benchmark
    with open(benchmark_file, 'r') as f:
        benchmark = json.load(f)
    
    # Check endpoint availability first if requested
    if check_endpoints:
        endpoint_results = check_openwebui_endpoints(base_url, api_key)
        available = any(v['available'] for v in endpoint_results.values())
        if not available:
            print("⚠ WARNING: No endpoints appear to be available!")
            print("Continuing anyway, but expect errors...")
            time.sleep(2)
    
    # Auto-detect or use specified family
    if model_family is None:
        model_family = detect_model_family(model)
        print(f"Auto-detected model family: {model_family}")
    else:
        print(f"Using specified model family: {model_family}")
    
    # Calculate recommended timeout for this model
    timeout, model_size, reasoning = calculate_timeout(model)
    print(f"Model size analysis: {reasoning}")
    
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
    parser.add_argument('--output', type=str, default=None,
                        help='Output file for generated solutions (auto-generated if not specified)')
    parser.add_argument('--output-dir', type=str, default='results',
                        help='Directory for auto-generated output files (default: results)')
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
    parser.add_argument('--check-endpoints', action='store_true', default=False,
                        help='Check API endpoint availability before starting')
    
    args = parser.parse_args()
    
    # Get API key from environment if not provided
    api_key = args.api_key or os.environ.get('OPENWEBUI_API_KEY')
    
    generate_solutions(args.benchmark, args.output, args.model, args.base_url, api_key, 
                      args.model_family, args.check_endpoints, args.output_dir)
