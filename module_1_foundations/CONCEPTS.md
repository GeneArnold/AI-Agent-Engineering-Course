# Module 1: Core Concepts

Before building your first agent, you need to understand three foundational concepts. These aren't just theory - they're the building blocks of every agent you'll ever build.

---

## Concept 1: LLM Call Anatomy

### The Three-Stage Pipeline

Think of an LLM call as a pipeline with three distinct stages:

```
User Input → [Stage 1: Prompts] → [Stage 2: Tokens] → [Stage 3: Completion] → Output
```

### Stage 1: Prompts (What YOU send)

A prompt is structured input to the LLM. It has several parts:

**1. System Message** - Sets the role/behavior (the "policy")
```python
{
  "role": "system",
  "content": "You are a helpful weather assistant. Use the get_weather tool when asked about weather."
}
```

**2. User Message** - The actual request
```python
{
  "role": "user",
  "content": "What's the weather in Seattle?"
}
```

**3. Assistant Messages** - Previous responses (conversation history)
```python
{
  "role": "assistant",
  "content": "The weather in Seattle is sunny!"
}
```

### Stage 2: Tokens (How the LLM reads it)

The LLM doesn't "read" text - it reads **tokens** (chunks converted to numbers).

**Examples:**
- `"Hello world"` → `[9906, 1917]` (2 tokens)
- `"Hello, world!"` → `[9906, 11, 1917, 0]` (4 tokens)

**Why this matters:**
- **Cost:** You pay per token (input + output)
- **Limits:** Models have token limits (4K, 8K, 128K, etc.)
- **Performance:** More tokens = more $$ and slower responses

**Quick math:**
- 1 token ≈ 4 characters of English text
- 100 words ≈ 130 tokens
- A page of text ≈ 500 tokens

### Stage 3: Completion (What the LLM returns)

The model generates a response, measured in tokens.

**Two types of completions:**

**Type 1: Text completion** (Simple answer)
```json
{
  "content": "The weather in Seattle is 72°F and sunny!",
  "finish_reason": "stop"
}
```

**Type 2: Tool call** (Requesting to use a tool)
```json
{
  "tool_calls": [{
    "function": {
      "name": "get_weather",
      "arguments": "{\"city\": \"Seattle\"}"
    }
  }],
  "finish_reason": "tool_calls"
}
```

**Key insight:** The `finish_reason` tells you what the LLM wants to do next!
- `"stop"` = Done, final answer provided
- `"tool_calls"` = Needs to use a tool, loop continues

---

## Concept 2: Agent Loop Fundamentals

### The Core Insight: Agents are Just Loops!

A **single LLM call** is one question → one answer.

An **agent** is a *loop* that keeps calling the LLM until a task is complete.

```python
while not done:
    response = call_llm(messages, tools)

    if response.finish_reason == "tool_calls":
        # Execute tool, add result to messages, continue loop
        tool_result = execute_tool(response.tool_calls[0])
        messages.append(tool_result)
    else:
        # Final answer received, exit loop
        done = True
        return response.content
```

That's it. That's an agent. Everything else is details.

### The Three Components

#### 1. Policy (System Rules)

The "personality" and instructions that stay consistent:

```python
system_message = {
    "role": "system",
    "content": (
        "You are a weather assistant. "
        "When asked about weather, use the get_weather tool. "
        "When you have the answer, provide a friendly response."
    )
}
```

The policy defines:
- What the agent can do
- When to use tools
- How to respond

#### 2. Tools (Actions)

Functions the LLM can invoke to interact with the world:

```python
def get_weather(city: str, units: str = "fahrenheit") -> str:
    """Fetch current weather for a city."""
    # Call weather API
    return "72°F, Sunny"
```

**Critical:** The LLM doesn't *execute* tools - it just **requests** them. YOU execute the tool and feed the result back.

#### 3. Stop Condition (When to Exit)

The loop needs to know when it's done:

**Common patterns:**
- ✅ `finish_reason == "stop"` (LLM signals completion)
- ✅ Max iterations reached (safety: prevent infinite loops)
- ✅ Model returns special token like "FINISHED"

### How the Loop Works (Concrete Example)

**User:** "What's the weather in Seattle?"

```
ITERATION 1:
  Input:  system message + "What's the weather in Seattle?"
  LLM:    tool_call → get_weather("Seattle")
  Action: Execute tool → "72°F, Sunny"
  Output: Add tool result to conversation

ITERATION 2:
  Input:  Full conversation + "72°F, Sunny"
  LLM:    text → "The weather in Seattle is 72°F and sunny!"
  Action: finish_reason == "stop"
  Output: Return final answer, EXIT LOOP
```

**Total:** 2 iterations, task complete!

### Why This Matters

**Without an agent (single call):**
- User: "What's the weather?"
- LLM: "I don't have real-time weather data." ❌

**With an agent (loop):**
- User: "What's the weather?"
- LLM → Calls tool → Gets real data → Accurate answer ✅

---

## Concept 3: JSON Contracts & Function Calling

### What is a JSON Contract?

A **contract** is a formal description of a tool, written in JSON. It tells the LLM:
1. What the tool is called
2. When to use it
3. How to call it (parameters and types)

Think of it as a function signature for an AI.

### Anatomy of a Contract

```json
{
  "type": "function",
  "function": {
    "name": "get_weather",
    "description": "Get current weather for a city. Use when user asks about weather conditions.",
    "parameters": {
      "type": "object",
      "properties": {
        "city": {
          "type": "string",
          "description": "City name (e.g., 'Seattle', 'New York')"
        },
        "units": {
          "type": "string",
          "enum": ["fahrenheit", "celsius"],
          "description": "Temperature units"
        }
      },
      "required": ["city"]
    }
  }
}
```

**Breaking it down:**

**1. Name** - What it's called
```json
"name": "get_weather"
```

**2. Description** - When/why to use it (BE SPECIFIC!)
```json
"description": "Get current weather for a city. Use when user asks about weather conditions."
```

**3. Parameters** - What inputs it needs

- **Type:** Always `"object"` for function parameters
- **Properties:** Each parameter definition
- **Required:** Which params are mandatory

### How Function Calling Works

#### Step 1: You Define Tools

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            # ... rest of contract
        }
    }
]
```

#### Step 2: You Send Prompt + Tools to LLM

```python
response = openai.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Weather in Seattle?"}],
    tools=tools  # ← LLM now knows about these tools
)
```

#### Step 3: LLM Responds with Tool Call

```json
{
  "tool_calls": [{
    "id": "call_abc123",
    "function": {
      "name": "get_weather",
      "arguments": "{\"city\": \"Seattle\", \"units\": \"fahrenheit\"}"
    }
  }]
}
```

**The LLM generated valid JSON that matches your contract!**

#### Step 4: You Execute the Tool

```python
import json

# Parse arguments
args = json.loads(tool_call.function.arguments)
# {"city": "Seattle", "units": "fahrenheit"}

# Execute your actual Python function
result = get_weather(**args)
# "72°F, Sunny"
```

#### Step 5: Feed Result Back to LLM

```python
messages.append({
    "role": "tool",
    "tool_call_id": "call_abc123",
    "content": "72°F, Sunny"
})

# Call LLM again with tool result
final_response = openai.chat.completions.create(...)
```

#### Step 6: LLM Gives Final Answer

```json
{
  "content": "The weather in Seattle is 72°F and sunny!",
  "finish_reason": "stop"
}
```

### Why Deterministic Structure Matters

#### Temperature Setting

Controls randomness in responses:
- `temperature=0` → Deterministic, same input = same output
- `temperature=1` → Creative, varied responses

**For agent loops:** Use low temperature (0-0.3) so tool calls are predictable!

#### Schema Validation

The contract **enforces structure**:
- ✅ LLM can't call `get_weather("tomorrow")` if `city` is required
- ✅ LLM can't use `units="hot"` when only "fahrenheit"/"celsius" allowed
- ✅ Prevents garbage data from breaking your code

#### Type Safety

You know `city` will be a string, not a number or array!

```python
def get_weather(city: str, units: str = "fahrenheit"):
    # city is GUARANTEED to be a string!
    return fetch_weather_api(city.lower(), units)
```

Without contracts, you'd need tons of validation and error handling.

---

## Putting It All Together

Let's trace a complete agent execution:

### User Query: "What's the weather in Seattle?"

**ITERATION 1:**

1. **Prompts:** System + User messages sent to LLM
2. **Tokens:** Converted to numbers (117 tokens)
3. **Completion:** LLM requests `get_weather("Seattle")`
4. **Tool execution:** We run the function → "72°F, Sunny"
5. **Loop continues:** Add tool result to messages

**ITERATION 2:**

1. **Prompts:** Full conversation + tool result
2. **Tokens:** Now 143 tokens (history growing!)
3. **Completion:** LLM synthesizes final answer
4. **finish_reason:** "stop" → Loop exits
5. **Return:** "The weather in Seattle is 72°F and sunny!"

**Total:**
- 2 iterations
- 260 tokens (input + output)
- ~3 seconds latency
- Task complete ✅

---

## Key Takeaways

### 1. LLM Call Anatomy
- Prompts are structured (system/user/assistant)
- Tokens are how LLMs "see" text (and how you pay)
- Completions are either text or tool calls

### 2. Agent Loop
- Agents are just while loops with LLM calls
- `finish_reason` tells you: continue or stop
- Three components: policy, tools, stop condition

### 3. JSON Contracts
- Teach LLMs about tools with schemas
- Enable type-safe, validated function calls
- Low temperature = deterministic tool usage

---

## Mental Models to Remember

**🎯 The Agent Loop Mental Model:**
```
while not done:
    if LLM says "use a tool":
        execute it, add result, continue
    else:
        return final answer, stop
```

**🎯 The Tool Call Flow:**
```
Contract → LLM reads it → Requests tool → You execute → Feed back result → LLM uses it
```

**🎯 The Context Growth Problem:**
```
Iteration 1: 117 tokens
Iteration 2: 143 tokens (+tool result)
Iteration 3: 180 tokens (+another result)
...eventually: Hit token limit!
```
*(Module 2 solves this with vector memory!)*

---

## Common Misconceptions

❌ **"The LLM executes the tools"**
→ No! It only **requests** them. You execute and return results.

❌ **"Agents are super complex"**
→ No! At the core, they're just loops with tool calls.

❌ **"LLMs can do math"**
→ No! They pattern-match. That's why they need calculator tools.

❌ **"Temperature doesn't matter for tool calls"**
→ Wrong! High temperature = unpredictable JSON = broken tools.

---

## Ready to Build?

Now that you understand the concepts, you're ready to build `simple_agent.py`!

**Next:** Read [PROJECT.md](PROJECT.md) for detailed specifications →

**Questions?** Re-read sections that aren't clear. These concepts are foundational!
