# Module 1: Agent Foundations

## 🔒 Releases December 1, 2024 (Week 1)

Build your first AI agent from scratch—understand the core agent loop, tool calling, and structured logging.

---

## What You'll Learn

### Core Concepts
- **LLM call anatomy** - How prompts become tokens become completions
- **Agent loops** - Policy, tools, and stop conditions
- **Function calling** - JSON contracts for tool invocation
- **JSONL logging** - Structured observability for debugging

### Practical Skills
- Building a complete agent loop
- Implementing tool calling with OpenAI
- Creating JSON schemas for tools
- Setting up structured JSONL logging
- Understanding finish_reason states

### Key Insights
- Agent loops are surprisingly simple (just while loops!)
- finish_reason elegantly categorizes next actions
- Context grows with each iteration (leads to Module 2)
- LLMs pattern-match, they don't compute (why tools exist)

---

## Prerequisites

✅ **Complete setup** from `setup/` folder before starting this module

---

## What You'll Build

A weather agent that:
- Accepts user queries
- Calls tools when needed
- Logs every step to JSONL
- Demonstrates the fundamental agent loop pattern

**Example:**
```
User: "What's the weather in Seattle?"
→ Agent calls get_weather("Seattle")
→ Returns: "72°F and sunny"
```

Simple, but it teaches the pattern ALL agents use.

---

## Module Structure

When this module releases on **December 1**, you'll get:

- **CONCEPTS.md** - Theory: LLM anatomy, agent loops, JSON contracts
- **PROJECT.md** - Architecture and design decisions
- **SOLUTION/simple_agent.py** - Complete working agent
- **Seed questions** - Guided questions to ask Claude Code

---

## Learning Approach

This course uses a unique model:
1. Read the theory (CONCEPTS.md)
2. Study the architecture (PROJECT.md)
3. Examine working code (SOLUTION/)
4. Ask Claude Code questions
5. Experiment and modify

**You're not building from scratch** - you're studying proven solutions with AI assistance.

---

## Coming December 1, 2024

**This module releases in Week 1.** Until then:
- Complete the setup from `setup/` folder
- Read START_HERE.md to understand the course
- Get excited for your first agent!

---

## Next Module

**Module 2: Memory & Context** (Week 2 - December 8)
- Solve the context growth problem
- Learn embeddings and vector databases
- Implement RAG (Retrieval-Augmented Generation)

---

**Stay tuned!** Module 1 drops December 1st. Make sure you've completed setup first.
