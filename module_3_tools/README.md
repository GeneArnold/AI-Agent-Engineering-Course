# Module 3: Tools & Registries

## 🔒 Releases December 15, 2024 (Week 3)

Build a robust multi-tool system with dynamic registration—learn type-safe tool schemas and clean dispatch patterns.

---

## What You'll Learn

### Core Concepts
- **Pydantic schemas** - Type-safe tool definitions with validation
- **Dynamic registries** - Tools register themselves with decorators
- **Tool dispatch** - Clean routing patterns without if/elif chains
- **Cost tracking** - Measure tokens, latency, and dollars per tool
- **Error handling** - Graceful degradation when tools fail

### Practical Skills
- Designing tool schemas with Pydantic
- Building a decorator-based tool registry
- Implementing multiple practical tools (file I/O + HTTP API)
- Per-tool performance logging
- Error recovery and fallback strategies

### Key Insights
- How to scale from 1 tool to 10+ tools cleanly
- Why type safety matters in production agents
- Trade-offs between static and dynamic dispatch
- When to add new tools vs extend existing ones

---

## Prerequisites

✅ **Complete Modules 1 & 2**
- Understand agent loops and tool calling (Module 1)
- Familiarity with JSONL logging
- Experience with memory systems (Module 2)

---

## What This Module Solves

**Problem from Module 1:**
```python
# Static tool registry - hard to scale
AVAILABLE_TOOLS = [WEATHER_TOOL]

# Manual dispatch - grows with each tool
if tool_name == "get_weather":
    result = get_weather(**args)
elif tool_name == "get_stock":
    result = get_stock(**args)
# ... becomes unmaintainable at 10+ tools
```

**Solution in Module 3:**
```python
# Dynamic registry with decorators
@tool_registry.register
def get_weather(city: str) -> str:
    """Get weather for a city"""
    return fetch_weather(city)

# Dispatch happens automatically
result = tool_registry.execute(tool_name, args)
```

---

## What You'll Build

A multi-tool agent that:
- Registers tools dynamically using decorators
- Validates inputs with Pydantic schemas
- Dispatches to the right tool automatically
- Tracks performance (tokens, latency, cost) per tool
- Handles errors gracefully with fallbacks

**Example tools:**
- File operations (read/write)
- HTTP API calls (fetch URLs)
- Data transformations (JSON parsing, calculations)

---

## Module Structure

When this module releases on **December 15**, you'll get:

- **CONCEPTS.md** - Theory: Pydantic, decorators, registries
- **PROJECT.md** - Architecture, design decisions, and seed questions
- **SOLUTION/tool_agent.py** - Complete working multi-tool agent
- **Seed questions** - 18 guided questions for Claude Code

---

## Coming December 15, 2024

**This module releases in Week 3.** Until then:
- Complete Module 1 (Dec 1) and Module 2 (Dec 8)
- Understand agent loops and memory patterns
- Get ready for multi-tool systems!

---

## Next Module

**Module 4: Multi-Agent Systems** (Week 4 - December 22)
- Planner → Worker → Critic pattern
- Multi-agent coordination
- Shared state management
- Evaluation and quality checks

---

**Stay tuned!** Module 3 drops December 15th. Complete Modules 1 & 2 first.
