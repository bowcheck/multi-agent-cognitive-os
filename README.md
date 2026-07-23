# Multi-Agent Cognitive OS 🧠⚡

**Author:** bowcheck  
**Version:** 1.0  
**Status:** Public Prior Art  

An intelligent, hardware-aware Operating System for Large Language Models. This OS acts as a Just-In-Time (JIT) compiler, actively monitoring GPU VRAM limits and dynamically altering AI context windows to prevent crashes during massive code generation tasks.

## 🫀 The Biological Philosophy
This OS abandons traditional sequential AI loops in favor of strict biological asynchronous processing. 
> *"If every time I breathe, my brain says thank you to my lungs, and my lungs wait for that, I will die. The heart can't breathe and the lungs can't pump blood."* — bowcheck

The Slow Brain (RAM) and Fast Brain (GPU) operate completely independently, acting purely on event-driven triggers. There is zero handshake latency.

## 🚀 The Core Problem Solved
When asking a local LLM to generate complex mathematics or dense codebases, the model's **KV Cache** rapidly fills up. On consumer hardware (like an 8GB GPU), this causes immediate memory overflow, leading to truncated output or system crashes. 

## ⚙️ The Architecture
To bypass hardware constraints, the OS acts as a memory sentinel and network router:

1. **The Gateway Dispatcher:** Instantly categorizes the user's prompt into 1 of 7 execution pipelines (e.g., Code Gen, Data Extraction, Book Writing).
2. **The Slow Brain:** Runs on system RAM to derive the core logic/outline without using token-heavy code syntax.
3. **The OS Sentinel:** Measures the logic. If it exceeds safe GPU limits (e.g., >2500 characters), it triggers a defense override.
4. **Parallel Map-Reduce:** The OS forces the Slow Brain to slice its logic into independent chronological chunks. The OS then spawns a swarm of **Fast Brains** on the GPU to translate every chunk in parallel.
5. **The TCP Code Stitcher:** Instead of using an LLM to merge the parallel chunks (which causes hallucinations), the OS uses strict programmatic indexing to mathematically reorder and stitch the flawless code together.

## 🛠️ The 7 Supported Pipelines
The Gateway automatically detects your intent and routes to:
1. `MATH_CODE` - Parallel multi-agent software architecture.
2. `LONG_TEXT_GEN` - Parallel chapter-by-chapter book writing.
3. `LONG_TEXT_SUM` - Parallel massive document summarization.
4. `DATA_EXTRACTION` - Strict JSON extraction from messy text.
5. `TRANSLATION` - High-speed parallel translation of large files.
6. `AGENTIC_TOOL` - Local OS command execution and web search.
7. `QUICK_CHAT` - Instant conversational bypass.

## 💻 How to Run
1. Ensure you have `ollama` running locally with the target model (default: `qwen-tuned`).
2. Open `fast_brain_coder_router.py`.
3. Change the `test_prompt` variable to your desired request.
4. Run the script:
```bash
python3 fast_brain_coder_router.py
```
The Gateway will automatically analyze your prompt, choose the correct pipeline, chunk the logic if necessary, and output the perfectly TCP-stitched final result.

---
*See `patent_disclosure_draft.md` for full architectural IP claims.*
