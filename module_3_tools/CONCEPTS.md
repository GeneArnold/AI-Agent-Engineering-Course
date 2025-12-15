# Module 3: Tools & Registries - Core Concepts

This module teaches you how to build scalable multi-tool systems using type-safe schemas and dynamic registration patterns.

---

## The Problem We're Solving

In Module 1, you built an agent with ONE tool using a static approach:

```python
# Static tool definition
WEATHER_TOOL = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"]
        }
    }
}

# Static tool list
AVAILABLE_TOOLS = [WEATHER_TOOL]

# Manual dispatch
if tool_name == "get_weather":
    result = get_weather(**args)
```

**Problems with this approach:**
1. **Doesn't scale** - Adding 10 tools means 10 schema definitions + 10 if/elif branches
2. **Error-prone** - Easy to forget to add a tool to the list or dispatch code
3. **No type safety** - JSON schemas don't validate Python function calls
4. **Duplicate work** - Define the schema AND the function separately

**What happens at 10+ tools?**
Your dispatch code becomes unmaintainable:
```python
if tool_name == "get_weather": ...
elif tool_name == "get_stock": ...
elif tool_name == "send_email": ...
elif tool_name == "read_file": ...
elif tool_name == "write_file": ...
# ... 20 more lines ...
```

Module 3 solves this with **dynamic registration** and **type-safe schemas**.

---

## Concept 1: Type Safety with Pydantic

### What It Is

Pydantic is a Python library that lets you define data schemas using Python classes. It automatically:
- Validates data types
- Generates JSON schemas
- Provides helpful error messages
- Integrates with your IDE for autocomplete

### Why It Matters

**Without Pydantic (Module 1 approach):**
```python
# Manual JSON schema
TOOL_SCHEMA = {
    "type": "object",
    "properties": {
        "filepath": {"type": "string"},
        "content": {"type": "string"}
    }
}

# Separate function definition
def write_file(filepath: str, content: str) -> str:
    # No automatic validation!
    return "done"
```

Problems:
- Schema and function are separate (easy to get out of sync)
- No validation happens automatically
- IDE can't help you

**With Pydantic (Module 3 approach):**
```python
from pydantic import BaseModel, Field

class WriteFileInput(BaseModel):
    filepath: str = Field(description="Path to the file")
    content: str = Field(description="Content to write")

@tool_registry.register("write_file", WriteFileInput)
def write_file(filepath: str, content: str) -> str:
    # Pydantic validates automatically!
    return "done"
```

Benefits:
- ✅ Single source of truth
- ✅ Automatic validation
- ✅ IDE autocomplete works
- ✅ Better error messages
- ✅ Generate OpenAI schema from Python types

### How It Works

1. **Define your schema as a Python class:**
```python
class CalculateInput(BaseModel):
    expression: str = Field(description="Math expression like '2 + 2'")
```

2. **Pydantic validates data automatically:**
```python
# This works
validated = CalculateInput(expression="42 * 137")

# This fails with a helpful error
validated = CalculateInput(expression=12345)  # TypeError: str expected
```

3. **Schema is generated for you:**
```python
schema = CalculateInput.model_json_schema()
# Returns OpenAI-compatible JSON schema
```

### Key Properties

- **Type coercion**: Pydantic tries to convert types (`"123"` → `123` if needed)
- **Validation**: Checks types, required fields, formats
- **Serialization**: Converts to/from JSON easily
- **Documentation**: Field descriptions become tool descriptions for the LLM

---

## Concept 2: Dynamic Tool Registration

### What It Is

Dynamic registration means tools "register themselves" when defined. No manual lists, no manual dispatch.

**The pattern:**
```python
@tool_registry.register("tool_name", SchemaModel)
def my_tool(param: str) -> str:
    return "result"
```

The decorator automatically:
1. Adds the tool to the registry
2. Generates the OpenAI schema from Pydantic
3. Sets up validation
4. Makes it available for dispatch

### Why It Matters

**Scalability example:**

**Static (Module 1) - Adding a tool requires 3 changes:**
```python
# 1. Define schema
NEW_TOOL = {...}

# 2. Add to list
AVAILABLE_TOOLS = [WEATHER_TOOL, NEW_TOOL]  # Don't forget!

# 3. Add dispatch
if tool_name == "new_tool":  # Don't forget!
    result = new_tool(**args)
```

**Dynamic (Module 3) - Adding a tool requires 1 change:**
```python
@tool_registry.register("new_tool", NewToolInput)
def new_tool(param: str) -> str:
    return "result"
```

That's it! The registry, schemas, and dispatch all update automatically.

### How It Works (Decorators)

A decorator is a function that wraps another function:

```python
def register(name, schema):
    def decorator(func):
        # Store the tool
        tools[name] = {"func": func, "schema": schema}
        return func  # Return original function
    return decorator
```

When you write:
```python
@tool_registry.register("calculate", CalculateInput)
def calculate(expression: str) -> str:
    return eval(expression)
```

Python executes:
```python
calculate = tool_registry.register("calculate", CalculateInput)(calculate)
```

The decorator:
1. Receives the function
2. Stores it in the registry with its schema
3. Returns the original function (so it still works normally)

### Key Properties

- **Declarative**: Tool definition IS tool registration
- **No boilerplate**: No lists to maintain
- **Self-documenting**: Look at `@register` decorators to see all tools
- **Extensible**: Add tools without modifying core code

---

## Concept 3: Clean Tool Dispatch

### What It Is

The ToolRegistry provides a single `execute()` method that:
1. Looks up the tool by name
2. Validates arguments with Pydantic
3. Calls the tool function
4. Returns the result

**Usage:**
```python
success, result, latency = tool_registry.execute("calculate", {"expression": "2 + 2"})
```

### Why It Matters

**Compare dispatch code:**

**Module 1 (if/elif chain):**
```python
if tool_name == "get_weather":
    result = get_weather(**args)
elif tool_name == "get_stock":
    result = get_stock(**args)
elif tool_name == "send_email":
    result = send_email(**args)
# ... grows forever ...
```

**Module 3 (registry):**
```python
result = tool_registry.execute(tool_name, args)
```

One line handles ALL tools. Adding 10 more tools? Still one line.

### How It Works

The ToolRegistry stores tools in a dictionary:
```python
{
    "calculate": {
        "func": <function calculate>,
        "schema": {...},
        "model": CalculateInput
    },
    "read_file": {
        "func": <function read_file>,
        "schema": {...},
        "model": ReadFileInput
    }
}
```

Execution:
```python
def execute(self, tool_name, arguments):
    tool = self._tools[tool_name]  # Look up
    validated = tool["model"](**arguments)  # Validate with Pydantic
    result = tool["func"](**validated.model_dump())  # Call function
    return result
```

### Key Properties

- **O(1) lookup**: Dictionary lookup, not sequential if/elif
- **Automatic validation**: Pydantic catches bad inputs
- **Error handling**: Try/except in one place for all tools
- **Performance tracking**: Measure latency per tool easily

---

## Concept 4: Cost Tracking and Performance

### What It Is

Track the cost and performance of every operation:
- **Tokens used** (input + output)
- **Latency** (milliseconds per call)
- **Cost** (dollars per call)

### Why It Matters

In production, you need to know:
- Is this agent costing $0.01 per query or $1.00?
- Which tools are slow?
- Where are the bottlenecks?

**Example from our logs:**
```json
{
  "event_type": "tool_call",
  "tool_name": "fetch_url",
  "latency_ms": 162.5,
  "cost_usd": 0.000045
}
```

This tells you:
- URL fetch took 163ms
- Cost $0.000045 (very cheap!)

### How It Works

**Token tracking:**
```python
usage = response.usage
input_tokens = usage.prompt_tokens
output_tokens = usage.completion_tokens
```

**Cost calculation:**
```python
# gpt-4o-mini pricing (Dec 2024)
INPUT_PRICE = 0.150 / 1_000_000  # per token
OUTPUT_PRICE = 0.600 / 1_000_000  # per token

cost = (input_tokens * INPUT_PRICE) + (output_tokens * OUTPUT_PRICE)
```

**Latency tracking:**
```python
start = time.time()
result = tool_function()
latency_ms = (time.time() - start) * 1000
```

### Key Properties

- **Per-tool metrics**: See which tools are expensive/slow
- **Cumulative tracking**: Total cost per agent run
- **Logged to JSONL**: Analyze later with any tool
- **Real-time visibility**: Print costs as agent runs

---

## Putting It All Together

Here's how all concepts work together in Module 3:

### 1. Define Tool with Pydantic Schema
```python
class CalculateInput(BaseModel):
    expression: str = Field(description="Math expression")
```

### 2. Register Tool with Decorator
```python
@tool_registry.register("calculate", CalculateInput)
def calculate(expression: str) -> str:
    return f"{expression} = {eval(expression)}"
```

### 3. Tool is Available Automatically
```python
# Registry knows about it
schemas = tool_registry.get_schemas()  # Includes calculate

# Can execute it
result = tool_registry.execute("calculate", {"expression": "2 + 2"})
```

### 4. Agent Uses Tools Dynamically
```python
# Get tools from registry
response = client.chat.completions.create(
    model="gpt-4o-mini",
    tools=tool_registry.get_schemas()  # All registered tools
)

# Execute whatever tool LLM chose
for tool_call in response.tool_calls:
    result = tool_registry.execute(tool_call.name, tool_call.args)
```

### 5. Everything is Tracked
```json
{
  "tool_name": "calculate",
  "arguments": {"expression": "42 * 137"},
  "latency_ms": 0.15,
  "cost_usd": 0.000045,
  "result": "5754"
}
```

---

## What You Built

### Bridge Example: comparison_simple_vs_pydantic.py

**Start here if you're feeling lost!** This file shows Module 1 vs Module 3 side-by-side:
- Same weather tool, two different approaches
- Extensive comments showing what changed and why
- Scalability comparison (10 tools: 500 lines vs 100 lines)
- **Run this first** to see the direct correlation between modules

### Full Implementation: tool_agent.py

Once you understand the bridge example, study the full implementation:

1. **ToolRegistry class** - Manages tool registration and dispatch
2. **4 Pydantic schemas** - Type-safe tool definitions
3. **4 tool functions** - Registered with decorators:
   - `read_file` - Read text files
   - `write_file` - Write text files
   - `fetch_url` - HTTP GET requests
   - `calculate` - Math expressions
4. **Agent loop** - Uses tools dynamically based on user query
5. **Cost tracking** - Logs tokens, latency, and cost
6. **JSONL logging** - Complete observability

**Key achievement:** Adding a 5th tool is trivial:
```python
@tool_registry.register("json_parse", JSONParseInput)
def json_parse(json_string: str) -> str:
    return json.loads(json_string)
```

No changes to registry, no changes to dispatch, no changes to agent loop. It just works.

---

## Key Takeaways

1. **Pydantic provides type safety** - Define schemas once, get validation free
2. **Decorators enable dynamic registration** - Tools register themselves
3. **Registry pattern scales beautifully** - Add 100 tools, dispatch stays one line
4. **Cost tracking is essential** - Know what you're spending in production
5. **Simple beats complex** - Clean patterns > clever tricks

---

## Evolution from Module 1 to Module 3

**Module 1:**
- 1 tool (weather)
- Manual JSON schemas
- Static tool list
- if/elif dispatch
- ~200 lines

**Module 3:**
- 4 tools (files, HTTP, calc)
- Pydantic schemas
- Dynamic registry
- Dictionary dispatch
- ~400 lines

**But adding 10 more tools:**
- Module 1: +100 lines (schemas + dispatch)
- Module 3: +30 lines (just tool definitions)

That's the power of good patterns!

---

## What's Next?

**Module 4: Multi-Agent Systems**

You'll learn:
- Coordinating multiple agents (Planner, Worker, Critic)
- Shared state management
- Agent-to-agent communication
- Evaluation and quality checks

The tool patterns you learned here will be essential when multiple agents need to use the same tools!
