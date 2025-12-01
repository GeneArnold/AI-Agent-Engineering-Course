# Module 1: Agent Foundations

## Overview

Build your first AI agent from scratch. Understand the core agent loop, tool calling, and structured logging. This module teaches the fundamental patterns that all agents share.

---

## How to Use This Module

**Follow this learning path:**

1. **Read CONCEPTS.md** - Understand LLM anatomy, agent loops, and JSON contracts
2. **Read PROJECT.md** - Learn the architecture and design patterns
3. **Study SOLUTION/simple_agent.py** - Examine the working implementation
4. **Ask Claude Code questions** - Use seed questions from PROJECT.md
5. **Experiment** - Modify the code and test changes

**Remember:** Claude Code is your tutor. The solution exists - your goal is to understand it deeply and experiment with modifications.

---

## What You'll Learn

### Core Concepts
- **LLM call anatomy** - Prompts → tokens → completion pipeline
- **Agent loops** - Policy, tools, and stop conditions
- **Function calling** - JSON contracts for tool invocation
- **JSONL logging** - Structured observability for debugging

### Practical Skills
- Building a complete agent loop from scratch
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

✅ **Setup complete** (from `setup/` folder)
- Python environment configured
- OpenAI API key set
- Dependencies installed
- Claude Code ready

---

## What This Module Teaches

**The Agent Loop Pattern:**
```python
while not done:
    response = llm(messages, tools)

    if response.finish_reason == "tool_calls":
        result = execute_tool(response.tool_calls)
        messages.append(result)  # Continue loop
    elif response.finish_reason == "stop":
        return response.content  # Done!
```

This simple pattern powers all AI agents.

---

## Files in This Module

```
module_1_foundations/
├── README.md                  ← You are here
├── CONCEPTS.md                ← Theory: LLM anatomy, loops, contracts
├── PROJECT.md                 ← Architecture, design, seed questions
└── SOLUTION/
    └── simple_agent.py        ← Complete working agent
```

### What Each File Does

**CONCEPTS.md**
Theory and fundamentals:
- How LLMs process requests (prompts → tokens → completion)
- What makes an agent loop work
- How JSON contracts enable function calling
- Why structured logging matters

**PROJECT.md**
Architecture and design:
- How simple_agent.py is structured
- Component breakdown (config, tools, logging, loop)
- Key design decisions explained
- **15 seed questions** to ask Claude Code
- Experiments to try

**SOLUTION/simple_agent.py**
Working code with:
- One tool: `get_weather(city, units)`
- Complete agent loop with max iterations safety
- JSONL logging for all events
- Extensive comments explaining every section

---

## Learning Workflow Example

Here's a typical session with this module:

```
You: "I'm starting Module 1. What should I do first?"

Claude: "Great! Start by reading CONCEPTS.md to understand agent loops..."

[You read CONCEPTS.md]

You: "Okay, I read it. Can you explain the agent loop in simpler terms?"

Claude: "Think of it like a conversation where the LLM can pause to use tools..."

[Claude explains]

You: "That makes sense! Now I'm ready for PROJECT.md."

[You read PROJECT.md]

You: "Walk me through the agent loop code step-by-step"

Claude: "Let's open SOLUTION/simple_agent.py. Starting at line 139..."

[Claude explains the code]

You: "Now I want to run it and see it work."

[You run: python module_1_foundations/SOLUTION/simple_agent.py]

You: "Cool! What happens if I change temperature from 0.1 to 0.9?"

Claude: "Good experiment! Higher temperature means..."

[You experiment and observe the changes]
```

---

## Key Features of This Agent

**Simple Weather Agent:**
- Answers weather questions using a mock `get_weather` tool
- Demonstrates complete agent loop with tool calling
- Shows finish_reason decision logic
- Logs every event to JSONL for complete observability

**What Makes It Educational:**
- Just ONE tool (focus on the pattern, not complexity)
- Clear separation of concerns (config, tools, logging, loop)
- Extensive comments explaining the "why"
- Shows context growth problem (leads to Module 2)

**Real Output:**
```
Query: "What's the weather in Seattle?"

Iteration 1: LLM calls get_weather("Seattle")
→ Result: "72°F, Sunny"

Iteration 2: LLM synthesizes answer
→ "The weather in Seattle is currently 72°F and sunny."

Total: 2 iterations, 292 tokens
```

---

## Success Criteria

You'll know you've mastered Module 1 when you can:

✅ Explain the three parts of an LLM call (prompts, tokens, completion)
✅ Describe how the agent loop works (while loop + finish_reason)
✅ Walk through simple_agent.py code confidently
✅ Modify the tool (change return format, add parameters)
✅ Explain why finish_reason is elegant ("tool_calls" vs "stop")
✅ Understand the context growth problem (leads to Module 2)

---

## Testing Checklist

Before moving to Module 2, verify:

- [ ] Agent runs successfully with weather query
- [ ] Tool is called with correct arguments
- [ ] finish_reason correctly categorizes states
- [ ] JSONL logs capture all events (llm_call, tool_execution, completion)
- [ ] Token usage is tracked and logged
- [ ] Multiple iterations work (try complex queries)
- [ ] Agent stops at correct finish condition
- [ ] Error handling works (try invalid input)
- [ ] You understand every line of code

---

## Reflection Questions

After completing this module, reflect on:

1. **What surprised you about the agent loop?**
   - Was it simpler or more complex than expected?

2. **Why is finish_reason elegant?**
   - How does it enable the decision logic?

3. **Where did you see context growth?**
   - Look at token counts in logs across iterations

4. **Why do agents need tools?**
   - What can LLMs not do on their own?

5. **What would you add to make this production-ready?**
   - Error handling? Retry logic? Rate limiting?

---

## Common Experiments

### Experiment 1: Change Temperature
```python
# In simple_agent.py, change:
TEMPERATURE = 0.1  # Try 0.5, 0.9, 1.0

# Run agent and observe:
# - Does tool calling become less reliable?
# - Does response creativity change?
```

### Experiment 2: Add a Second Tool
```python
# Add a new tool:
def get_time(timezone: str = "UTC") -> str:
    return datetime.now().strftime("%H:%M:%S")

# Register it and test multi-tool coordination
```

### Experiment 3: Change Max Iterations
```python
# Change:
MAX_ITERATIONS = 10  # Try 3, 20

# See what happens with complex queries
```

### Experiment 4: Break It Intentionally
```python
# What happens if you:
# - Remove the tool definition?
# - Set max iterations to 1?
# - Return invalid JSON from tool?

# Learn by breaking!
```

---

## Troubleshooting

### "OpenAI API key not found" Error
```bash
# Check .env file:
cat .env | grep OPENAI_API_KEY

# Should show: OPENAI_API_KEY=sk-...
```

### Tool Not Being Called
- Check temperature (should be low: 0.1-0.3)
- Verify tool description is clear
- Look at LLM response in logs

### Agent Never Stops
- Check max_iterations safety limit
- Look at finish_reason in logs
- Verify LLM is returning "stop" eventually

### JSONL Logs Empty
- Check logs/ directory exists
- Verify LOG_FILE path is correct
- Look for file permissions issues

---

## Pro Tips

**Tip 1: Study the Logs First**
Before asking questions, read the JSONL logs. They show exactly what happened at each step.

**Tip 2: One Change at a Time**
When experimenting, change ONE thing and observe. Don't change multiple things simultaneously.

**Tip 3: Temperature Matters**
Low temperature (0.1) for tool calling, higher (0.7+) for creative responses. Try both!

**Tip 4: Count Tokens**
Watch token growth across iterations in logs. This motivates Module 2's RAG solution.

**Tip 5: Ask "Why" Constantly**
- Why this temperature?
- Why finish_reason instead of boolean?
- Why JSONL instead of CSV?

---

## Next Module

**Module 2: Memory & Context** (Week 2)

Solve the context growth problem you discovered in Module 1. Learn about:
- Embeddings and vector databases
- RAG (Retrieval-Augmented Generation)
- Keeping token usage constant
- Persistent memory across sessions

---

## Getting Help

**From Claude Code (Your Professor):**
- Ask the seed questions in PROJECT.md
- Request line-by-line code explanations
- Get help experimenting with modifications

**From the Code:**
- Read the extensive comments
- Trace the agent loop flow
- Study the tool definition pattern

**From the Logs:**
- See what the LLM requested
- Check tool execution results
- Track token usage growth

---

## Quick Start

Ready to begin?

1. Open CONCEPTS.md and read about agent loops
2. Open PROJECT.md for architecture overview
3. Run the agent: `python module_1_foundations/SOLUTION/simple_agent.py`
4. Study the output and logs
5. Ask Claude Code the seed questions
6. Experiment with modifications
7. Complete the testing checklist
8. Answer the reflection questions

**Welcome to AI Agent Engineering!** 🚀

---

**Last Updated:** November 24, 2024
**Estimated Time:** 1 week for deep understanding
**Difficulty:** Beginner (foundational)
