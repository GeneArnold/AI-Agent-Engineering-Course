# 🎓 AI Agent Engineering Training — Local Agent Edition

**Author:** ChatGPT (co-instructor)  
**Owner:** Gene Arnold  
**Version:** 1.0 (2025‑11‑05)  
**Purpose of this file:** A single, portable document that captures the *why*, *what*, and *how* of your AI Agent training so you can move it to a **local agent** or any machine and keep going without context loss.

---

## 1) Why This Training Exists (Motivation & Problem Statement)

You’re highly capable with integration tools (n8n, Activepieces) but noticed a skill debt forming: **using abstractions without fully owning the wiring** (the agent loop, function tools, memory, quantization, pipelines). That led to a very healthy question:

> “If I can ship with n8n, should I even code? And if I stop coding, do I really understand agents, models, and tooling?”

**Answer:** You should do both—deliver with no‑code when it’s pragmatic, but also **reclaim the wiring** so you can debug, extend, and reason about trade‑offs (latency, cost, accuracy, privacy). This program is the hands‑on path to rebuild that foundation:
- Build a working agent loop from scratch.  
- Add memory (embeddings + vector store).  
- Wire real tools (files, APIs, Atlan/MCP).  
- Run local models and **feel** quantization trade‑offs.  
- Scale to **multi‑agent** patterns and lightweight evaluation.  
- Adopt **MCP** to standardize tools across clients and agents.

This restores confidence, avoids vendor lock‑in, and gives you the insight to use n8n/Activepieces **as accelerators**, not crutches.

---

## 2) What We’re Covering (Scope)

### Core Modules (4‑week arc, flexible pacing)
1. **Agent Foundations** — minimal loop, tool calls, structured outputs, logging.  
2. **Memory & Context** — embeddings, vector search (Chroma/FAISS), persistent recall.  
3. **Tools & Local Models** — Pydantic tool schemas, tool registry, Ollama/HF pipelines, **quantization** compare.  
4. **Multi‑Agent & Evaluation** — Planner→Worker→Critic, shared state, cost/latency logs, simple success checks.

### MCP Track (Add‑on spanning Modules 3–4)
- **Concepts:** Why MCP, local (stdio) vs remote (SSE), Docker MCP **Gateway**.  
- **Catalog Try‑outs:** Use a couple of prebuilt servers (e.g., Obsidian, DuckDuckGo, YouTube transcripts).  
- **Build One Safely:** Create a minimal custom MCP server (e.g., dice/utility or a harmless public API wrapper).  
- **Integrate:** Call MCP tools *from your own agent*; move toward MCP as your standard tool interface.  
- **Architecture:** Local vs remote deployments, secrets, and gateway patterns.

> 🔒 **Safety:** We deliberately exclude offensive security tooling. If you ever run security labs, do so legally on isolated, permissioned targets.

---

## 3) How We’ll Work Together (Operating Model)

- **Command‑driven lessons:** You say “Start Module 1 Lesson 1” (or “Review Module 2 Project”). I teach, pair‑code, quiz, and annotate.  
- **Artifacts over theory:** Every lesson produces runnable code, logs, and short notes.  
- **Reflection loop:** You jot 3–5 bullets per module (“what clicked”, “what broke”, “next question”), I coach and adjust.  
- **Progress tracking:** A simple journal table (see §8) captures each lesson/project with status ✅/🕓/🔁.

---

## 4) Detailed Curriculum (Concepts → Project → Reflection)

### Module 1 — Agent Foundations
**Concepts**
- LLM call anatomy: prompts → tokens → completion  
- Agent loop: *policy* (system rules) + *tool calls* + *stop condition*  
- JSON contracts, function calling, deterministic structure (temperature, schema)

**Project: `simple_agent.py`**
- Make one hosted or local model call.  
- Register **one** tool (e.g., `web_search` or `get_weather`).  
- Implement a loop that ends with `{"done": true, "result": ...}`.  
- Log every step to `.jsonl` (prompt, tool args, tool result, tokens, latency).

**Reflection**
- What surprised you about how *simple* the loop is?  
- Where did structure break (bad JSON, tool args), and how did logging help?

---

### Module 2 — Memory & Context
**Concepts**
- Embeddings (semantic vectors), cosine similarity, *context windows*  
- Vector stores (Chroma/FAISS), persistence, recall strategies (pre‑query/top‑k)  
- Cost/latency impact of retrieval vs prompt stuffing

**Project: `memory_agent.py`**
- Generate embeddings (e.g., `text-embedding-3-small` or local equivalent).  
- Save useful facts; on each turn, fetch top‑k and inject into the model context.  
- Show retrieved items in logs (ids, distance).

**Reflection**
- Did memory reduce repeat questions or token bloat?  
- What retrieval strategy worked best for your tasks?

---

### Module 3 — Tools & Local Models
**Concepts**
- Pydantic schemas for tool I/O, validation, and guardrails  
- Tool registry (discover & dispatch by name)  
- **Local inference** via Ollama or Hugging Face pipelines  
- **Quantization** (GGUF/awq/bnb): speed vs quality trade‑offs

**Project: `tool_agent.py`**
- Two or more tools (file I/O + a simple HTTP API).  
- Ability to switch **OpenAI vs Ollama** via config/env.  
- Quantize a 7B‑class model (e.g., `Q4_K_M`) and log speed/quality deltas.  
- Collect per‑step **latency, token counts, and dollar estimates**.

**Reflection**
- When would you pick local over hosted?  
- What did quantization *feel* like in code and outputs?

---

### Module 4 — Multi‑Agent & Evaluation
**Concepts**
- Planner→Worker→Critic roles, shared `state` dict (messages, tasks, scratch)  
- Termination criteria, retries/backoff, budget gates (steps/cost)  
- Observability: traces/logs, success checks, regression seeds

**Project: `multi_agent_system.py`**
- Three roles as small policies with clear responsibilities.  
- Message passing and final aggregation.  
- Simple evaluator that checks acceptance criteria and flags weak outputs.

**Reflection**
- What improved with role separation?  
- Where did it over‑orchestrate? How would you simplify?

---

## 5) MCP Add‑On (Standardized Tools for Agents)

### Lesson A — Concepts
- **Why MCP:** standard interface so agents/clients don’t need per‑API glue.  
- **Local (stdio) vs Remote (SSE/HTTPS):** low‑latency spawn‑on‑use vs network services.  
- **Docker MCP Gateway:** one connection → many tools, centralized secrets/caching.

### Lesson B — Catalog Try‑Out
**Project: `mcp_catalog_exploration.md`**
- Connect Claude Desktop / LM Studio / Cursor to gateway or native config.  
- Add at least **two** catalog servers (e.g., Obsidian, DuckDuckGo, YouTube transcripts).  
- Execute a small chained flow (search → summarize → append note).

### Lesson C — Build a Minimal MCP Server (Safe)
**Project: `mcp_dice_server/`**
- Tools: `roll_dice`, `flip_coin` (or another harmless utility).  
- Package with Dockerfile + requirements + server script + README.  
- Register through the gateway; verify discovery & invocation from a client.

### Lesson D — Use MCP Tools *Inside Your Agent*
**Project: update `tool_agent.py`**
- Add an MCP client adapter that can list tools and invoke by name with JSON.  
- Replace one bespoke tool with an MCP‑backed tool (e.g., note append).  
- Log: `tool`, `args`, `latency_ms`, `result_size`.

### Lesson E — Architecture & Secrets
**Project: `mcp_architecture_notes.md`**
- Diagram: Client(s) ↔ Gateway ↔ MCP Servers (catalog + custom).  
- Paragraph: your migration plan (which tools will become MCP first, how secrets are stored, local vs remote split).

> **Security & Ethics:** Keep servers and tools within lawful, permissioned use. Manage secrets via the gateway; never hard‑code.

---

## 6) Deliverables (What “Done” Looks Like)

- `simple_agent.py` — minimal loop + single tool + logs  
- `memory_agent.py` — vector recall + context injection + logs  
- `tool_agent.py` — multi‑tool registry + OpenAI/Ollama switch + quantization notes  
- `multi_agent_system.py` — planner/worker/critic + evaluator + cost/latency logs  
- `mcp_dice_server/` — minimal safe MCP server (Dockerized) + README  
- `mcp_catalog_exploration.md` — results of catalog servers trial  
- `mcp_architecture_notes.md` — diagram + migration paragraph  
- **Training Journal** — table rows for each lesson with status & reflections

---

## 7) Success Criteria (Acceptance Tests)

- ✅ Agent loop terminates with `{"done": true}` and logs are structured JSON.  
- ✅ Memory retrieval measurably reduces repeat prompting and/or token usage.  
- ✅ Local model runs; quantized vs non‑quantized comparison recorded (latency & quality).  
- ✅ Multi‑agent run completes with planner→worker→critic handoff and a basic evaluator pass.  
- ✅ An MCP tool was called by your agent; tool discovery & invocation are logged.  
- ✅ Architecture notes exist; you can explain local vs remote MCP, gateway role, and secrets flow.

---

## 8) Training Journal (Copy as a Table Header)

| Date | Module | Lesson/Project | What I Built | What Clicked | Next Question | Status (✅/🕓/🔁) |
|------|--------|----------------|--------------|--------------|---------------|------------------|

Add one row per lesson or project.

---

## 9) Setup Checklist (Minimal)

- Python **3.11+** and VS Code (Python extension)  
- `pip install openai pydantic chromadb fastapi`  
- **Ollama** or **Hugging Face** for local inference (optional but recommended)  
- Docker (for MCP gateway/servers)  
- API keys as needed (store in gateway secrets; **never** commit)  
- Git repo (optional, helps with history and review)

---

## 10) Operating Locally (Agent Handoff Tips)

- Keep `.env` or config YAML for **provider switch** (OpenAI ↔ Ollama).  
- Separate modules by concern: `agent_core.py`, `memory.py`, `tools.py`, `local_model.py`, `evaluator.py`.  
- Use **Pydantic** schemas for tool inputs/outputs; validate everything.  
- Log to `.jsonl`; include timestamps, tokens, latency, costs, tool names.  
- Add a `--max-steps` and `--budget` CLI flag to avoid runaway loops.  
- Write tiny **smoke tests** (e.g., `pytest -k agent_smoke`) for critical paths.

---

## 11) Roadmap After Completion

- Add **RAG** with your own docs (LangChain/LlamaIndex)  
- Containerize with **Docker Compose** (agent + vector store + UI)  
- Expose your standard tools via **MCP** and retire ad‑hoc glue code  
- Write a short blog/LinkedIn recap to reinforce mental models

---

## 12) Glossary (Quick Reference)

- **Agent Loop:** The control flow that decides to call tools and when to stop.  
- **Embeddings:** Vector representations of text for semantic search/retrieval.  
- **Vector Store:** Database for embeddings (e.g., Chroma, FAISS).  
- **Quantization:** Reduce numerical precision for faster inference at accuracy cost.  
- **MCP (Model Context Protocol):** Standard for exposing tools to LLMs (local stdio / remote SSE).  
- **Gateway:** A single MCP entry point that multiplexes many servers/tools and centralizes secrets.

---

### End of File
