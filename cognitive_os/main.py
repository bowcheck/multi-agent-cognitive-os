import sys
import concurrent.futures
import subprocess
from core.llm_provider import LLMProvider
from core.gateway import GatewayDispatcher
from core.sentinel import VRAMSentinel, TCPStitcher
from agents.brains import SlowBrain, FastBrain

def main():
    print("=========================================================")
    print("  MULTI-AGENT COGNITIVE OS (JIT Compiler Edition)        ")
    print("=========================================================")
    
    # Change this to "gemini", "openai", or "mock" (for testing)
    PROVIDER = "ollama" 
    MODEL = "qwen-tuned" 
    
    test_prompt = "Derive the exact mathematical logic for a 2D Incompressible Fluid Dynamics simulation using the Navier-Stokes equations via Chorin's Projection Method."
    print(f"User Request: {test_prompt}\n")

    # 1. Initialize OS Core
    llm = LLMProvider(provider=PROVIDER, model=MODEL)
    gateway = GatewayDispatcher(llm)
    sentinel = VRAMSentinel()
    stitcher = TCPStitcher()
    
    # 2. Initialize Swarm
    slow_brain = SlowBrain(llm, sentinel)
    fast_brain = FastBrain(llm)

    # 3. Input Validation
    is_safe, reason = sentinel.check_input_safety(len(test_prompt))
    if not is_safe:
        print(f"[!] OS OVERRIDE: {reason}. Bypassing Gateway. Forcing Chunking.")
        gate_output = "LONG_TEXT_SUM"
    else:
        print("[*] OS Sensor Check: CPU, RAM, and GPU are SAFE.")
        gate_output, t = gateway.route_request(test_prompt)
        print(f"[*] Gateway routed to pipeline: {gate_output} (in {t:.2f}s)")

    # 4. Pipeline Execution
    if "QUICK_CHAT" in gate_output:
        res, _ = fast_brain.chat(test_prompt)
        print(f"\nRESPONSE:\n{res}")

    elif "DATA_EXTRACTION" in gate_output:
        res, _ = fast_brain.extract_data(test_prompt)
        print(f"\nRESPONSE:\n{res}")
        
    elif "AGENTIC_TOOL" in gate_output:
        print("[*] OS Triggered: AGENTIC_TOOL Pipeline. Initiating live bash proxy...")
        res, _ = fast_brain.agentic_act(test_prompt)
        if "[COMMAND]" in res:
            cmd = res.split("[COMMAND]")[1].strip()
            print(f"[*] OS Executing Sandbox Command: {cmd}")
            try:
                out = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.STDOUT)
            except Exception as e:
                out = str(e)
            print("[*] Command Finished. Feeding back to Fast Brain...")
            final_res, _ = fast_brain.agentic_act(f"Command Output:\n{out}\n\nNow give the final user answer.")
            print(f"\nFINAL RESPONSE:\n{final_res}")
        else:
            print(f"\nFINAL RESPONSE:\n{res}")

    elif "LONG_TEXT_SUM" in gate_output:
        profile = sentinel.dynamic_allocation_profile()
        chunk_size = profile["chunk_size"]
        swarm_size = profile["fast_brain_swarm_size"]
        
        chunks = [test_prompt[i:i+chunk_size] for i in range(0, len(test_prompt), chunk_size)]
        print(f"[*] OS dynamically chunked document into {len(chunks)} pieces (Limit: {chunk_size} tokens).")
        def summarize_chunk(chunk_data):
            i, text = chunk_data
            res, _ = fast_brain.chat(f"Summarize: {text}")
            return i, f"Chunk {i+1}:\n{res}"
        with concurrent.futures.ThreadPoolExecutor(max_workers=swarm_size) as executor:
            print(f"[*] OS spawned {swarm_size} Fast Brains in parallel based on Memory limits.")
            results = list(executor.map(summarize_chunk, enumerate(chunks)))
        final_output = stitcher.stitch(results) # PURE TCP STITCH. NO LLM.
        print(f"\nFINAL TCP-STITCHED SUMMARIES:\n{final_output}")
        
    elif "TRANSLATION" in gate_output:
        chunks = [test_prompt[i:i+2000] for i in range(0, len(test_prompt), 2000)]
        def translate_chunk(chunk_data):
            i, text = chunk_data
            res, _ = fast_brain.translate_chunk(text)
            return i, res
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(translate_chunk, enumerate(chunks)))
        print(f"\nFINAL TCP-STITCHED TRANSLATION:\n{stitcher.stitch(results)}")
        
    elif "LONG_TEXT_GEN" in gate_output:
        print("[*] SLOW BRAIN (RAM) writing Outline...")
        outline, _ = slow_brain.outline_book(test_prompt)
        chunks = [c for c in outline.split('---CHUNK---') if c.strip()]
        def write_chapter(chunk_data):
            i, text = chunk_data
            res, _ = fast_brain.write_chapter(text)
            return i, f"Chapter {i+1}:\n{res}"
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(write_chapter, enumerate(chunks)))
        print(f"\nFINAL TCP-STITCHED BOOK:\n{stitcher.stitch(results)}")

    elif "MATH_CODE" in gate_output:
        print("[*] SLOW BRAIN (RAM) deriving math...")
        math_logic, _ = slow_brain.derive_math(test_prompt)
        
        is_safe, reason = sentinel.check_input_safety(len(math_logic))
        
        if not is_safe:
            profile = sentinel.dynamic_allocation_profile()
            print(f"[!] SENTINEL OVERRIDE: {reason}. Dynamic Reallocation Triggered.")
            
            chunked_logic, _ = slow_brain.chunk_logic(math_logic, limit=profile["chunk_size"])
            chunks = [c for c in chunked_logic.split('---CHUNK---') if c.strip()]
            def code_chunk(chunk_data):
                i, text = chunk_data
                res, _ = fast_brain.translate_math_to_code(text)
                return i, f"# --- CHUNK {i+1} ---\n{res}"
            with concurrent.futures.ThreadPoolExecutor(max_workers=profile["fast_brain_swarm_size"]) as executor:
                print(f"[*] Swarm dynamically resized to {profile['fast_brain_swarm_size']} parallel workers.")
                results = list(executor.map(code_chunk, enumerate(chunks)))
            print(f"\nFINAL TCP-STITCHED CODE:\n{stitcher.stitch(results)}")
        else:
            res, _ = fast_brain.translate_math_to_code(math_logic)
            print(f"\nFINAL CODE:\n{res}")

    else:
        print("[!] ERROR or Unimplemented Pipeline.")

if __name__ == "__main__":
    main()
