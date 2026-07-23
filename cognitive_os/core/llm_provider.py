import json
import urllib.request
import time
import os

class LLMProvider:
    """Model-agnostic interface. Supports local Ollama, Google Gemini, OpenAI, etc."""
    def __init__(self, provider="ollama", model="qwen-tuned"):
        self.provider = provider
        self.model = model

    def generate(self, prompt, system="You are an AI."):
        start = time.time()
        
        if self.provider == "ollama":
            url = 'http://localhost:11434/api/generate'
            payload = {'model': self.model, 'system': system, 'prompt': prompt, 'stream': False, 'options': {'num_ctx': 16384}}
            req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
            try:
                with urllib.request.urlopen(req, timeout=600) as response:
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
            result = f"[SIMULATED AI OUTPUT] Processed chunk: {prompt[:40]}..."
            time.sleep(0.5) # Simulate slight generation delay
                
        else:
            result = f"ERROR: Unsupported provider {self.provider}"
            
        return result, time.time() - start
