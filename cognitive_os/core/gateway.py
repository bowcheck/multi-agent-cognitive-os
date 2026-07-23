class GatewayDispatcher:
    def __init__(self, llm_provider):
        self.llm = llm_provider
        self.gateway_sys = """You are a Universal Task Dispatcher. Analyze the user request and categorize it into EXACTLY ONE of these seven tags:
        1. 'MATH_CODE' (Requires complex mathematics, algorithms, or physics to code)
        2. 'LONG_TEXT_GEN' (User asks you to WRITE a book, long essay, or large document)
        3. 'LONG_TEXT_SUM' (User asks you to SUMMARIZE or analyze a massive block of text)
        4. 'DATA_EXTRACTION' (User wants specific facts, entities, or JSON extracted from messy text)
        5. 'TRANSLATION' (User wants to translate text from one language to another)
        6. 'AGENTIC_TOOL' (User wants you to take an action: search the web, read a local file, run a script)
        7. 'QUICK_CHAT' (Simple question, joke, or conversational answer)
        Output NOTHING ELSE but the exact tag."""

    def route_request(self, prompt):
        # Brain Stem operates on CPU/NPU to reserve 100% of GPU VRAM for the Motor Cortex (Fast Brain Swarm)
        res, t = self.llm.generate(prompt, system=self.gateway_sys, use_gpu=False)
        return res, t
