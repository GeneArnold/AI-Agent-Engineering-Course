# Module 3: Tools & Registries

## Overview

Build a multi-tool agent with dynamic registration and type-safe schemas. Learn how to scale from one tool to many using Pydantic validation and decorator patterns. Solve the tool dispatch problem from Module 1.

---

## How to Use This Module

**Follow this learning path:**

1. **Read CONCEPTS.md** - Understand Pydantic, decorators, and dynamic registries
2. **Read PROJECT.md** - Learn the architecture and design decisions
3. **Study SOLUTION/tool_agent.py** - Examine the working implementation
4. **Ask Claude Code questions** - Use seed questions from PROJECT.md
5. **Experiment** - Add new tools and test modifications

**Remember:** Claude Code is your tutor. The solution exists - your goal is to understand it deeply and experiment with modifications.

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
- You should understand agent loops and tool calling (Module 1)
- Familiarity with JSONL logging
- Experience with memory systems and RAG (Module 2)

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

**Adding a new tool is now trivial:**
```python
@tool_registry.register
def calculate(expression: str) -> float:
    """Evaluate a mathematical expression"""
    return eval(expression)  # Note: Use safely in production!
```

---

## Files in This Module

```
module_3_tools/
├── README.md              ← You are here
├── CONCEPTS.md            ← Theory: Pydantic, decorators, registries
├── PROJECT.md             ← Architecture, design decisions, seed questions
└── SOLUTION/
    └── tool_agent.py      ← Complete working multi-tool agent
```

### What Each File Does

**CONCEPTS.md**
Theory and fundamentals:
- What is Pydantic and why use it for schemas?
- How do Python decorators work?
- What makes a registry "dynamic"?
- Error handling strategies for tools
- Cost tracking and performance monitoring

**PROJECT.md**
Architecture and tools:
- How the tool registry is designed
- Why we chose Pydantic over manual JSON
- Component breakdown (ToolRegistry, tool functions, agent loop)
- 18 seed questions to ask Claude Code
- Experiments to try (add new tools, test error handling)

**SOLUTION/tool_agent.py**
Complete working implementation:
- ToolRegistry class with decorator pattern
- 2-3 practical tools (file I/O, HTTP API, data transform)
- Pydantic schemas for type safety
- Cost tracking per tool
- JSONL logging for observability
- Error handling with graceful fallbacks

---

## Learning Workflow Example

**Typical session with this module:**

```
You: "I'm ready to start Module 3. What should I do first?"

Claude Code: "Great! Start with CONCEPTS.md to understand Pydantic
and decorators. Would you like me to explain the theory first, or
would you prefer to read it and then ask questions?"

You: [Read CONCEPTS.md]

You: "I read about Pydantic. How is it different from what we did in Module 1?"

Claude Code: "In Module 1, you manually wrote JSON schemas like this:
{
  'type': 'object',
  'properties': { 'city': {'type': 'string'} }
}

With Pydantic, you write Python classes and get validation automatically.
Let me show you the difference..."

You: "That makes sense! Now let me read PROJECT.md."

You: "Walk me through the ToolRegistry class - how does the decorator work?"

Claude Code: "Great question! Let's open SOLUTION/tool_agent.py and
I'll explain step by step..."

You: "Can I add a new tool for JSON parsing?"

Claude Code: "Absolutely! Here's how you'd add it using the decorator
pattern..."
```

---

## Key Features

**What the tool agent demonstrates:**
- **Type safety** - Pydantic validates all tool inputs
- **Scalability** - Add new tools without touching dispatch code
- **Observability** - Track performance per tool
- **Robustness** - Graceful error handling when tools fail
- **Cost awareness** - Know what each tool costs to run

---

## Success Criteria

You've mastered Module 3 when you can:

✅ Explain how Pydantic schemas improve safety vs raw JSON
✅ Understand how the decorator pattern works for registration
✅ Add a new tool without modifying the ToolRegistry class
✅ Track and interpret per-tool performance metrics
✅ Implement graceful error handling for tool failures
✅ Understand when to use static vs dynamic dispatch
✅ Explain the trade-offs of this architecture

---

## Testing Checklist

Run through these tests to verify your understanding:

1. [ ] Run `python SOLUTION/tool_agent.py` - agent works correctly
2. [ ] Add a new tool using `@tool_registry.register` decorator
3. [ ] Test with invalid inputs - Pydantic catches them
4. [ ] Force a tool to fail - agent handles error gracefully
5. [ ] Check logs/ - per-tool metrics are recorded
6. [ ] Remove a tool - agent still works (no dispatch code to change)
7. [ ] Ask all seed questions from PROJECT.md
8. [ ] Try experiments from PROJECT.md
9. [ ] Modify cost tracking - add new metrics

---

## Reflection Questions

After completing this module, answer:

1. How does Pydantic improve tool safety compared to raw JSON?
2. What makes the decorator pattern useful for tool registration?
3. Which tools were hardest to make robust?
4. How would you handle tool failures gracefully?
5. When would you need more than 3-5 tools in an agent?

---

## Common Experiments

Try these to deepen understanding:

1. **Add a calculator tool** - Mathematical expression evaluation
2. **Add a JSON parser tool** - Parse and query JSON data
3. **Break error handling** - Remove try/except, see what happens
4. **Add custom metrics** - Track success rate per tool
5. **Test Pydantic validation** - Pass invalid inputs, see errors

---

## Troubleshooting

**Tool not registering?**
- Check that you used `@tool_registry.register` decorator
- Verify the function is defined before the agent loop runs
- Look for syntax errors in the tool function

**Pydantic validation errors?**
- Check the schema matches the function signature
- Verify required fields are provided
- Ensure types match (str, int, float, etc.)

**Cost tracking seems wrong?**
- Verify you're using the correct API pricing
- Check that token counts are being captured
- Ensure timestamps are recorded correctly

---

## Pro Tips

1. **Start simple** - Understand the existing tools before adding new ones
2. **Test validation** - Intentionally pass bad inputs to see Pydantic at work
3. **Read the logs** - JSONL files show what happened at each step
4. **Compare to Module 1** - Notice how much cleaner the dispatch is
5. **Experiment freely** - The code is designed to be modified

---

## Next Module

**Module 4: Multi-Agent Systems** (December 22)
- Coordinate multiple agents working together
- Planner → Worker → Critic pattern
- Shared state management
- Evaluation and quality checks

---

## Getting Help

**From Claude Code:**
Ask specific questions about the code, concepts, or experiments.

**From the Code:**
Study the comments, follow the logic, trace execution.

**From the Logs:**
Check `logs/tool_agent.jsonl` to see what happened.

**From Experiments:**
Modify code, break things, fix things - that's learning!

---

## Quick Start

Ready to begin? Follow these steps:

1. Read CONCEPTS.md (theory first)
2. Read PROJECT.md (architecture second)
3. Study SOLUTION/tool_agent.py (implementation third)
4. Run the agent: `python SOLUTION/tool_agent.py`
5. Ask seed questions to Claude Code
6. Try experiments from PROJECT.md
7. Reflect on what you learned

**Remember:** You're studying working code, not building from scratch. Your goal is deep understanding and experimentation!
