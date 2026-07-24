import json
import urllib.request
import time
import os

class LLMProvider:
    """Model-agnostic interface. Supports local Ollama, Google Gemini, OpenAI, etc."""
    def __init__(self, provider="ollama", model="qwen-tuned"):
        self.provider = provider
        self.model = model

    def generate(self, prompt, system="You are an AI.", use_gpu=True):
        start = time.time()
        
        if self.provider == "ollama":
            url = 'http://localhost:11434/api/generate'
            
            # If use_gpu is False, we explicitly force 0 layers to GPU to keep it clean.
            # If use_gpu is True, we OMIT the num_gpu parameter so Ollama dynamically offloads
            # exactly the maximum safe number of layers based on the user's actual VRAM!
            options = {'num_ctx': 16384}
            if not use_gpu:
                options['num_gpu'] = 0
                
            payload = {'model': self.model, 'system': system, 'prompt': prompt, 'stream': False, 'options': options}
            req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
            try:
                with urllib.request.urlopen(req, timeout=None) as response:
                    result = json.loads(response.read().decode('utf-8'))['response'].strip()
            except Exception as e:
                result = f"ERROR: {str(e)}"
                
        elif self.provider == "gemini":
            # Using Google Gemini API (the one we tested earlier!)
            api_key = os.environ.get("GEMINI_API_KEY", "DUMMY_KEY")
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={api_key}"
            payload = {"contents": [{"parts": [{"text": f"SYSTEM: {system}\n\nUSER: {prompt}"}]}]}
            req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
            try:
                with urllib.request.urlopen(req, timeout=600) as response:
                    res_json = json.loads(response.read().decode('utf-8'))
                    result = res_json['candidates'][0]['content']['parts'][0]['text']
            except Exception as e:
                result = f"ERROR: {str(e)}"
                
        elif self.provider == "mock":
            # Instantly simulates LLM generation to test OS architecture routing
            if "Universal Task Dispatcher" in system:
                result = "MATH_CODE"
                time.sleep(0.1)
            elif "You are the Slow Brain. You do NOT write code" in system:
                # Generate a MASSIVE math derivation to violently trigger the Sentinel Hardware Override!
                result = "Derivation of Navier Stokes...\n" + ("Heavy Math Calculus Formula...\n" * 2000)
                time.sleep(0.3)
            elif "VRAM-safe modules separated by '---CHUNK---'" in system:
                # Simulate the chunking process
                result = "Chunk 1: Advection\n---CHUNK---\nChunk 2: Diffusion\n---CHUNK---\nChunk 3: Pressure"
                time.sleep(0.2)
            elif "Translate this specific mathematical chunk into Python code" in system:
                # Simulate the Fast Brain Swarm
                result = f"def fluid_sim_{time.time()}():\n    # Translated: {prompt[:30]}\n    pass"
                time.sleep(0.1)
            else:
                result = f"[SIMULATED AI OUTPUT] Processed chunk: {prompt[:40]}..."
                time.sleep(0.1)
                
        else:
            result = f"ERROR: Unsupported provider {self.provider}"
            
        return result, time.time() - start
