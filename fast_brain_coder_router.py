# =========================================================
# Copyright (c) 2026 bowcheck. All Rights Reserved.
# Multi-Agent Cognitive OS - Dynamic Hardware-Aware Router
# =========================================================

import json
import urllib.request
import time
import re

OLLAMA_URL = 'http://localhost:11434/api/generate'
MODEL = 'qwen-tuned'

def call_ollama(prompt, system="You are an AI."):
    payload = {
        'model': MODEL,
        'system': system,
        'prompt': prompt,
        'stream': False,
        'options': {'temperature': 0.1, 'num_predict': -1, 'num_ctx': 16384}
    }
    req = urllib.request.Request(OLLAMA_URL, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=600) as response:
            result = json.loads(response.read().decode('utf-8'))['response'].strip()
    except Exception as e:
        result = f"ERROR: {str(e)}"
    return result, time.time() - start

test_prompt = """Derive the exact mathematical logic for a 2D Incompressible Fluid Dynamics simulation using the Navier-Stokes equations via Chorin's Projection Method. Include the advection, diffusion, pressure Poisson equation, and velocity correction steps."""

print("=========================================================")
print("  THE FINAL ARCHITECTURE (Fast Brain as Coder & Router)  ")
print("=========================================================")
print(f"User Request: {test_prompt}\n")

# 0. OS INPUT FILTER (Nervous System)
print("[*] 0. OS is checking physical input size to protect the GPU...")
input_length = len(test_prompt)

if input_length > 2500:
    print(f"    -> [OS detected massive {input_length} character input. Bypassing Fast Brain Gateway.]")
    print("[!] OS OVERRIDE: Input is too dense for 8GB VRAM. Automatically classifying as LONG_TEXT.")
    gate_output = "LONG_TEXT"
    gate_time = 0.0
else:
    print(f"    -> [Input is {input_length} characters. Safe for GPU.]")
    
    # 0.5 GATEWAY BRAIN (Input Validation & Task Dispatcher)
    print("[*] 0.5 GATEWAY BRAIN is analyzing the request to route it correctly...")
    gateway_sys = """You are a Universal Task Dispatcher. Analyze the user request and categorize it into EXACTLY ONE of these three tags:
    1. 'MATH_CODE' (If the request requires complex mathematics, algorithms, or physics to code)
    2. 'LONG_TEXT' (If the request asks for a book, long essay, or large document)
    3. 'QUICK_CHAT' (If the request is a simple question, joke, or short conversational answer)
    Output NOTHING ELSE but the exact tag."""

    def call_gateway(prompt):
        payload = {
            'model': MODEL,
            'system': gateway_sys,
            'prompt': prompt,
            'stream': False,
            'options': {'temperature': 0.0, 'num_predict': 10, 'num_ctx': 1024}
        }
        req = urllib.request.Request(OLLAMA_URL, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
        start = time.time()
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode('utf-8'))['response'].strip(), time.time() - start
        except:
            return "ERROR", 0.0

    gate_output, gate_time = call_gateway(test_prompt)

if "QUICK_CHAT" in gate_output:
    print(f"    -> [Gateway identified QUICK_CHAT in {gate_time:.2f} seconds]")
    print("[*] ROUTING DIRECTLY TO FAST BRAIN for instant response...\n")
    chat_code, _ = call_ollama(test_prompt, system="You are a helpful assistant. Keep it short and witty.")
    print(f"RESPONSE:\n{chat_code}")
    exit()

elif "LONG_TEXT" in gate_output:
    print(f"    -> [Gateway identified LONG_TEXT in {gate_time:.2f} seconds]")
    print("[*] ROUTING TO CREATIVE PIPELINE (Will use Slow Brain to outline, and Fast Brain to write chapters...)")
    print("[Implementation for Book-Writer OS goes here]")
    exit()

elif "MATH_CODE" in gate_output:
    print(f"    -> [Gateway identified MATH_CODE in {gate_time:.2f} seconds]")
    print("[*] ROUTING TO MATH-MAP-REDUCE PIPELINE...\n")
    
    # 1. SLOW BRAIN (The Mathematician)
print("[*] 1. SLOW BRAIN is deriving the math formula...")
slow_sys = """You are the Slow Brain. You do NOT write code. 
Your ONLY job is to derive the core mathematical logic and array boundary rules. 
Output ONLY the pure mathematical steps."""

formula_output, slow_time = call_ollama(test_prompt, system=slow_sys)
print(f"    -> [Slow Brain generated the logic in {slow_time:.2f} seconds]")
print(f"    -> PREVIEW: {formula_output[:150]}...\n") 

# 2. THIRD BRAIN (The Broker - VRAM Sentinel)
print("[*] 2. THIRD BRAIN is analyzing token density to protect the GPU...")
math_length = len(formula_output)
print(f"    -> [Third Brain detected {math_length} characters of raw math]\n")

if math_length > 2500:
    print("[!] THIRD BRAIN OVERRIDE: Math is too dense for 8GB VRAM. Forcing Map-Reduce Chunking.")
    fast_output = "ESCALATE"
    fast_time = 0.0
else:
    # 3. FAST BRAIN (The Coder & Decision Maker - GPU Bound)
    print("[*] 3. FAST BRAIN is evaluating the token density and its VRAM limits...")
    fast_sys = """You are the Fast Brain. You operate on a GPU with limited VRAM.
    You have been given mathematical logic by the Slow Brain.
    Evaluate if this logic is simple enough to be translated into strict Python code within your limited memory.
    If simple: Output exactly 'DECISION: PYTHON' on the first line, then output the Python code inside ```python ``` blocks.
    If too complex or dense: You will crash if you try to code this. Output exactly 'DECISION: ESCALATE' and NOTHING ELSE."""
    
    fast_prompt = f"User Request: {test_prompt}\n\nCore Math from Slow Brain:\n{formula_output}\n\nMake your format decision."
    fast_output, fast_time = call_ollama(fast_prompt, system=fast_sys)

if "ESCALATE" in fast_output or len(fast_output) == 0:
    print(f"    -> [Fast Brain generated the escalation decision in {fast_time:.2f} seconds]")
    print("[!] FAST BRAIN DETECTED VRAM OVERFLOW RISK. INITIATING MAP-REDUCE CHUNKING...")
    
    # 4. SLOW BRAIN CHUNKING (RAM Bound)
    chunker_sys = f"""You are the Slow Brain. The Fast Brain's GPU VRAM is too small to process your math at once.
    The OS has determined your math is {math_length} characters long. The absolute hardware limit is 2500 characters per chunk.
    Slice your mathematical logic into as many independent, chronological modules as necessary to ensure NO chunk exceeds 2500 characters. 
    Separate each module with EXACTLY the string '---CHUNK---'. Do not write any code."""
    
    print("[*] 4. SLOW BRAIN is slicing the logic into dynamic VRAM-safe chunks...")
    chunk_prompt = f"Slice this math into dynamic VRAM-safe modules separated by '---CHUNK---':\n{formula_output}"
    chunked_output, chunk_time = call_ollama(chunk_prompt, system=chunker_sys)
    print(f"    -> [Slow Brain chunked the logic in {chunk_time:.2f} seconds]")
    
    chunks = chunked_output.split('---CHUNK---')
    final_python_code = ""
    
    # 5. FAST BRAIN SEQUENTIAL CODING
    print("[*] 5. FAST BRAIN is translating chunks sequentially to bypass VRAM limits...")
    coder_sys = "You are the Fast Brain. Translate this specific mathematical chunk into Python code. Output ONLY the python code."
    
    for i, chunk in enumerate(chunks):
        if not chunk.strip(): continue
        print(f"    -> Translating Chunk {i+1}...")
        chunk_code, t_time = call_ollama(chunk.strip(), system=coder_sys)
        final_python_code += f"\n# --- CHUNK {i+1} ---\n{chunk_code}\n"
        print(f"       [Done in {t_time:.2f}s]")
        
    final_output = f"Decision: MAP_REDUCE_CHUNKING\n\n{final_python_code}"
else:
    final_output = fast_output
    print(f"    -> [Fast Brain generated the final deliverable in {fast_time:.2f} seconds]\n")

print("=========================================================")
print("  FINAL DELIVERABLE (Ready for User)                     ")
print("=========================================================")
print(final_output)
print("=========================================================")
