# Project: Build `simple_agent.py`

## 🎯 Goal

Build a working AI agent that can answer weather questions by calling a tool and logging every step.

## 📋 Requirements

### Functional Requirements

**The agent must:**
1. Accept a user query as input
2. Call an LLM (OpenAI or Anthropic)
3. Use a `get_weather(city, units)` tool when appropriate
4. Loop until the task is complete
5. Return a friendly, accurate final answer
6. Log all events to a JSONL file

### Non-Functional Requirements

**Code quality:**
- Clear variable names
- Comments explaining key concepts
- Organized into logical sections
- Error handling for API failures

**Performance:**
- Complete simple queries in 2-3 iterations
- Stay under max_iterations safety limit (10)
- Use low temperature (0.1-0.3) for deterministic tool calls

## 🏗️ Architecture

### File Structure

```
simple_agent.py
├── Configuration (API keys, model, settings)
├── Tool Definitions (Python functions)
├── Tool Contracts (JSON schemas)
├── Logging Utilities (JSONL writer)
├── Agent Loop (main logic)
└── Main Entry Point (if __name__ == "__main__")
```

### Components

#### 1. Configuration Section

```python
# API client setup
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Model settings
MODEL = "gpt-4o-mini"  # Fast and cheap for learning
TEMPERATURE = 0.1  # Low for deterministic tool calls
MAX_ITERATIONS = 10  # Safety limit

# Logging
LOG_FILE = "logs/simple_agent.jsonl"
```

#### 2. Tool Definition

```python
def get_weather(city: str, units: str = "fahrenheit") -> str:
    """
    Get current weather for a city.

    In a real agent, this would call a weather API.
    For learning, we return mock data.
    """
    # Mock implementation (replace with real API in production)
    mock_weather = {
        "seattle": {"temp": 72, "condition": "Sunny"},
        # ... more cities
    }

    # Return formatted string
    return f"{temp}{unit_symbol}, {condition}"
```

#### 3. Tool Contract

```python
WEATHER_TOOL = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current weather for a city...",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", ...},
                "units": {"type": "string", "enum": [...], ...}
            },
            "required": ["city"]
        }
    }
}
```

#### 4. Logging Function

```python
def log_event(event_type: str, data: dict):
    """
    Write structured event to JSONL log.

    Each event includes:
    - timestamp (ISO 8601)
    - event_type (llm_call, tool_execution, completion, etc.)
    - event-specific data
    """
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event_type": event_type,
        **data
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
```

#### 5. Agent Loop

```python
def run_agent(user_query: str) -> str:
    """
    Main agent loop.

    Flow:
    1. Initialize messages with system + user
    2. Loop:
       a. Call LLM with messages + tools
       b. If tool_calls: execute, add result, continue
       c. If stop: return final answer
    3. Safety: exit after max_iterations
    """
    messages = [
        {"role": "system", "content": "You are a weather assistant..."},
        {"role": "user", "content": user_query}
    ]

    iteration = 0
    while iteration < MAX_ITERATIONS:
        iteration += 1

        # Call LLM
        response = client.chat.completions.create(...)

        # Log the call
        log_event("llm_call", {...})

        # Check finish_reason
        if message.tool_calls:
            # Execute tool
            # Add to messages
            # Continue loop
        else:
            # Return final answer
            return message.content

    # Max iterations reached
    return "Agent stopped: max iterations"
```

## 📊 Expected Behavior

### Test Case 1: Simple Weather Query

**Input:** `"What's the weather in Seattle?"`

**Expected Flow:**
```
Iteration 1:
  → LLM Call: system + user query
  → Response: tool_call(get_weather, {city: "Seattle"})
  → Execute: get_weather("Seattle") → "72°F, Sunny"
  → Log: llm_call + tool_execution events

Iteration 2:
  → LLM Call: messages + tool result
  → Response: "The weather in Seattle is 72°F and sunny!"
  → finish_reason: "stop"
  → Log: llm_call + completion events
  → Return: final answer
```

**Expected Output:**
```
🤖 AGENT STARTING
Query: What's the weather in Seattle?

--- Iteration 1 ---
🔧 Tool call: get_weather({'city': 'Seattle'})
📊 Result: 72°F, Sunny

--- Iteration 2 ---
✅ Final answer: The weather in Seattle is currently 72°F and sunny!

✅ AGENT COMPLETE (took 2 iterations)
```

**Expected Logs:** (in `logs/simple_agent.jsonl`)
```json
{"timestamp":"2025-11-22T10:00:00Z","event_type":"llm_call","iteration":1,"tokens":131,...}
{"timestamp":"2025-11-22T10:00:00Z","event_type":"tool_execution","tool":"get_weather",...}
{"timestamp":"2025-11-22T10:00:02Z","event_type":"llm_call","iteration":2,"tokens":161,...}
{"timestamp":"2025-11-22T10:00:02Z","event_type":"completion","result":"The weather...",...}
```

### Test Case 2: Multiple Cities

**Input:** `"How's the weather in Tokyo?"`

**Expected:** Same flow, different city

### Test Case 3: Non-Weather Query

**Input:** `"What is 2+2?"`

**Expected:**
- Iteration 1: LLM answers directly (no tool needed)
- finish_reason: "stop"
- Complete in 1 iteration

## ✅ Success Criteria

Your agent is complete when it:

1. **Runs without errors**
   - ✅ No Python exceptions
   - ✅ Handles API responses correctly
   - ✅ Creates log file successfully

2. **Completes weather queries correctly**
   - ✅ Calls `get_weather` tool when asked about weather
   - ✅ Returns friendly, accurate answers
   - ✅ Completes in 2-3 iterations

3. **Logs all events**
   - ✅ Creates `logs/simple_agent.jsonl`
   - ✅ Logs contain: timestamp, event_type, relevant data
   - ✅ Logs include: prompt_tokens, completion_tokens, latency

4. **Has safety limits**
   - ✅ max_iterations prevents infinite loops
   - ✅ Exits cleanly when limit reached

5. **Code is readable**
   - ✅ Comments explain key concepts
   - ✅ Clear function/variable names
   - ✅ Organized into sections

## 🎨 Code Template

Here's a skeleton to get you started:

```python
#!/usr/bin/env python3
"""
Module 1: Simple Agent
A minimal agent loop with one tool and structured logging.
"""

import os
import json
import time
from datetime import datetime
from openai import OpenAI

# ============================================================================
# CONFIGURATION
# ============================================================================

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-4o-mini"
TEMPERATURE = 0.1
MAX_ITERATIONS = 10
LOG_FILE = "logs/simple_agent.jsonl"

# ============================================================================
# TOOL DEFINITIONS
# ============================================================================

def get_weather(city: str, units: str = "fahrenheit") -> str:
    """Simulated weather tool."""
    # TODO: Implement mock weather data
    pass

# Tool contract (JSON schema)
WEATHER_TOOL = {
    # TODO: Define the contract
}

TOOLS = [WEATHER_TOOL]

# ============================================================================
# LOGGING
# ============================================================================

def log_event(event_type: str, data: dict):
    """Write event to JSONL log."""
    # TODO: Implement logging
    pass

# ============================================================================
# AGENT LOOP
# ============================================================================

def run_agent(user_query: str) -> str:
    """Main agent loop."""
    # TODO: Implement the loop
    pass

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    result = run_agent("What's the weather in Seattle?")
    print(f"\nResult: {result}")
```

## 💡 Implementation Tips

### Tip 1: Build Incrementally

Don't try to write everything at once! Build in stages:

1. **Stage 1:** Basic LLM call (no tools)
2. **Stage 2:** Add tool definition + contract
3. **Stage 3:** Implement tool calling in loop
4. **Stage 4:** Add logging
5. **Stage 5:** Test and refine

### Tip 2: Use Low Temperature

For tool calls, always use low temperature (0.1-0.3):

```python
response = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    tools=TOOLS,
    temperature=0.1  # ← Deterministic tool calls
)
```

### Tip 3: Handle Tool Arguments Safely

Always parse JSON tool arguments:

```python
if message.tool_calls:
    tool_call = message.tool_calls[0]
    args = json.loads(tool_call.function.arguments)  # Parse JSON
    result = get_weather(**args)  # Unpack as kwargs
```

### Tip 4: Log Early, Log Often

Add logging immediately. It's invaluable for debugging:

```python
# Log before LLM call
print(f"--- Iteration {iteration} ---")

# Log after tool execution
print(f"🔧 Tool: {function_name}({args})")
print(f"📊 Result: {result}")
```

### Tip 5: Test With Different Queries

Don't just test one query! Try:
- Different cities
- Celsius vs Fahrenheit
- Non-weather questions
- Edge cases

## 🐛 Common Bugs & Fixes

### Bug: `KeyError: 'tool_calls'`
**Cause:** Checking for key that might not exist
**Fix:** Use `hasattr()` or `getattr()`
```python
if hasattr(message, 'tool_calls') and message.tool_calls:
    # Handle tool calls
```

### Bug: `JSONDecodeError`
**Cause:** Malformed JSON from LLM
**Fix:** Use low temperature, add try/except
```python
try:
    args = json.loads(tool_call.function.arguments)
except json.JSONDecodeError:
    print("Invalid JSON from LLM")
    args = {}
```

### Bug: Agent loops forever
**Cause:** No stop condition
**Fix:** Add max_iterations check
```python
while iteration < MAX_ITERATIONS:
    # ...
```

### Bug: Logs not created
**Cause:** Directory doesn't exist
**Fix:** Create directory first
```python
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
```

## 🚀 Extension Challenges

After completing the basic agent, try:

1. **Add a second tool:** `calculate(expression)`
2. **Support multiple LLM providers:** OpenAI and Anthropic
3. **Add conversation memory:** Multi-turn conversations
4. **Calculate costs:** Track $ spent per query
5. **Real weather API:** Use actual weather service

## 📚 Reference

### OpenAI Function Calling
- [Official Guide](https://platform.openai.com/docs/guides/function-calling)
- [API Reference](https://platform.openai.com/docs/api-reference/chat/create)

### JSON Schema
- [Understanding JSON Schema](https://json-schema.org/understanding-json-schema)

---

**Ready to code?** Start building `simple_agent.py`!

**Stuck?** Review [CONCEPTS.md](CONCEPTS.md) or use Claude Code for guidance.

**Done?** Compare with `SOLUTION/` (released Week 1) to see how you did!
