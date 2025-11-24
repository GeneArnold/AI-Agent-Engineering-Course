# Module 3: Tools & Local Models

## 🔒 Releases December 15, 2024 (Week 3)

Build a robust tool system and run models locally—understand quantization trade-offs and gain infrastructure independence.

## Learning Objectives
- Design tool schemas with Pydantic
- Build a tool registry (discovery & dispatch)
- Run local models via Ollama or Hugging Face
- Compare quantization levels (speed vs quality)

## Concepts Covered
- Pydantic validation and guardrails
- Dynamic tool registration and routing
- Local inference (Ollama, HF Pipelines)
- Quantization formats (GGUF, AWQ, BNB)
- Cost modeling (tokens, latency, dollars)

## Project: `tool_agent.py`

### Requirements
- Implement TWO or more tools (file I/O + HTTP API)
- Support provider switching (OpenAI ↔ Ollama) via config
- Quantize a 7B-class model (e.g., `llama3.2:3b-q4_K_M`)
- Log per-step: latency, tokens, cost estimates
- Compare quantized vs full-precision runs

### Success Criteria
✅ Tool registry dynamically discovers and invokes tools
✅ Agent works with both hosted and local models
✅ Quantization comparison documented (speed & quality)
✅ Logs show per-tool latency and cost breakdowns

## Files in This Module
- `tool_agent.py` - Multi-tool agent with provider switching
- `logs/` - JSONL logs with tool and model metrics
- `quantization_notes.md` - Your comparison findings
- `reflections.md` - Your learning notes

## Reflection Questions
After completing this module, answer:
1. When would you pick local over hosted?
2. What did quantization *feel* like in outputs?
3. Which tools were hardest to make robust?
4. How would you handle tool failures gracefully?

## Coming December 15, 2024

**This module releases in Week 3.** Until then:
- Complete Module 1 (Dec 1) and Module 2 (Dec 8)
- Understand agent loops and memory patterns
- Get ready for multi-tool systems!

---

## Next Module
Module 4: Multi-Agent & Evaluation - Coordinate multiple agents and measure success (Dec 22)
