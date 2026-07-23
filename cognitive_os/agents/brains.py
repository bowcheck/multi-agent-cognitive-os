class SlowBrain:
    def __init__(self, llm_provider, sentinel):
        self.llm = llm_provider
        self.evict = sentinel.should_evict_slow_brain()

    def derive_math(self, prompt):
        sys = "You are the Slow Brain. You do NOT write code. Your ONLY job is to derive the core mathematical logic and array boundary rules. Output ONLY the pure mathematical steps."
        return self.llm.generate(prompt, system=sys, use_gpu=not self.evict)
        
    def outline_book(self, prompt):
        sys = "You are the Slow Brain. Outline the requested book/essay. Slice it into distinct chapters separated by exactly '---CHUNK---'. Output nothing but the chunks."
        return self.llm.generate(prompt, system=sys, use_gpu=not self.evict)
        
    def chunk_logic(self, math_logic, limit=2500):
        sys = f"You are the Slow Brain. The hardware limit is {limit} characters. Slice your logic into dynamic VRAM-safe modules separated by '---CHUNK---'. Do not write code."
        prompt = f"Slice this math into dynamic VRAM-safe modules separated by '---CHUNK---':\n{math_logic}"
        return self.llm.generate(prompt, system=sys, use_gpu=not self.evict)

class FastBrain:
    def __init__(self, llm_provider):
        self.llm = llm_provider

    def translate_math_to_code(self, chunk):
        sys = "You are the Fast Brain. Translate this specific mathematical chunk into Python code. Output ONLY the python code."
        return self.llm.generate(chunk, system=sys)
        
    def write_chapter(self, outline_chunk):
        sys = "You are the Fast Brain. Write a highly detailed, engaging chapter based ONLY on this outline. Output only the story prose."
        return self.llm.generate(outline_chunk, system=sys)

    def extract_data(self, text):
        sys = "You are a Data Extractor. Extract the requested entities from the text into strict JSON format. Output ONLY raw JSON. No markdown."
        return self.llm.generate(text, system=sys)

    def translate_chunk(self, chunk):
        sys = "You are a Translator. Translate this chunk accurately. Output ONLY the translated text."
        return self.llm.generate(chunk, system=sys)
        
    def agentic_act(self, prompt):
        sys = "You are an Agent. You can execute local terminal commands. To run a command (like curl, grep, or python), output exactly '[COMMAND] <your bash command>'. Otherwise, output the final answer to the user."
        return self.llm.generate(prompt, system=sys)
        
    def chat(self, prompt):
        sys = "You are a helpful assistant. Keep it short and witty."
        return self.llm.generate(prompt, system=sys)
