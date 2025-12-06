# Module 3 Project: Multi-Tool Agent with Dynamic Registry

This document describes the architecture of `tool_agent.py` - a multi-tool agent with Pydantic validation and dynamic registration.

---

## How to Use This Document

**Learning path:**
1. Read CONCEPTS.md first (understand theory)
2. Read this PROJECT.md (understand architecture)
3. **NEW STUDENTS:** Run SOLUTION/comparison_simple_vs_pydantic.py first!
   - This shows Module 1 vs Module 3 side-by-side
   - Helps you see the direct correlation between approaches
   - If you're confused by Pydantic, start here
4. Study SOLUTION/tool_agent.py (full implementation)
5. Ask Claude Code the seed questions below
6. Try the experiments at the end

---

## What This Agent Does

The tool agent can interact with files, fetch web content, and perform calculations based on user requests.

**Example interaction:**
```
USER: Write "Hello World" to hello.txt, then read it back to verify

AGENT:
  → Calls write_file("hello.txt", "Hello World")
  → Calls read_file("hello.txt")
  → Responds: "I wrote 'Hello World' to hello.txt and verified it contains:
     Hello World"
```

The agent automatically:
- Chooses which tools to use
- Validates all inputs with Pydantic
- Tracks cost and latency per tool
- Logs everything to JSONL

---

## Architecture Overview

```
┌─────────────┐
│    User     │
│    Query    │
└──────┬──────┘
       │
       v
┌──────────────────────────────────────┐
│         Agent Loop                   │
│  (run_agent function)                │
│                                      │
│  1. Send query + tool schemas       │
│  2. Get tool calls from OpenAI      │
│  3. Execute tools via registry       │
│  4. Feed results back to OpenAI     │
│  5. Return final answer              │
└───────┬──────────────┬───────────────┘
        │              │
        v              v
┌───────────────┐  ┌──────────────────┐
│  ToolRegistry │  │  OpenAI API      │
│               │  │  (gpt-4o-mini)   │
│  • get_schemas│  └──────────────────┘
│  • execute    │
└───┬───────────┘
    │
    │ Registered tools:
    ├── read_file    (ReadFileInput)
    ├── write_file   (WriteFileInput)
    ├── fetch_url    (FetchURLInput)
    └── calculate    (CalculateInput)
```

**Flow:**
1. User provides query
2. Agent calls OpenAI with all registered tool schemas
3. OpenAI decides which tools (if any) to use
4. ToolRegistry executes each tool with Pydantic validation
5. Results fed back to OpenAI for final answer
6. Everything logged (tokens, latency, cost)

---

## Tools & Technologies

### Pydantic

**What it is:** Data validation library using Python type annotations

**Why we chose it:**
- Automatic validation of tool inputs
- Generate OpenAI schemas from Python classes
- Better error messages than manual validation
- IDE support (autocomplete, type checking)

**Alternatives considered:**
- Manual JSON validation - too error-prone, no IDE support
- TypedDict - no runtime validation
- attrs/dataclasses - no validation by default

**Trade-offs:**
- ✅ Pro: Type safety, validation, schema generation
- ✅ Pro: Single source of truth (one definition)
- ❌ Con: Extra dependency (but very common)

### OpenAI API (gpt-4o-mini)

**What it is:** Cloud-based LLM API

**Why we chose it:**
- Fast and cheap ($0.15 per 1M input tokens)
- Function calling support
- Consistent with Modules 1 & 2

**Configuration:**
```python
MODEL = "gpt-4o-mini"
TEMPERATURE = 0.1  # Low for deterministic tool use
```

### requests

**What it is:** HTTP library for Python

**Why we chose it:** Simple, standard library for HTTP requests

**Usage:** `fetch_url` tool uses it to GET web content

---

## Component Breakdown

### Component 1: ToolRegistry Class

**Purpose:** Manage tool registration and dispatch

**Location:** Lines 68-125 in tool_agent.py

**Key methods:**

1. **`__init__()`**
   - Initializes empty `_tools` dictionary
   - Stores tools as: `{name: {"func": callable, "schema": dict, "model": PydanticModel}}`

2. **`register(name, schema_model)`** - Decorator for registration
   - Takes tool name and Pydantic model
   - Returns decorator that wraps the tool function
   - Generates OpenAI schema from Pydantic model
   - Stores in `_tools` dictionary
   - Returns original function (so it still works normally)

3. **`get_schemas()`** - Get all tool schemas
   - Returns list of OpenAI-compatible schemas
   - Used when calling OpenAI API
   - Automatically includes all registered tools

4. **`execute(tool_name, arguments)`** - Execute a tool
   - Looks up tool by name
   - Validates arguments with Pydantic
   - Calls the tool function
   - Returns (success, result, latency_ms)
   - Handles errors gracefully

**Design decisions:**
- Dictionary storage for O(1) lookup
- Decorator pattern for clean registration
- Pydantic validation in execute() for safety
- Return tuple (success, result, latency) for caller flexibility

### Component 2: Pydantic Schemas

**Purpose:** Define type-safe tool inputs

**Location:** Lines 32-50 in tool_agent.py

**The 4 schemas:**

1. **ReadFileInput**
```python
class ReadFileInput(BaseModel):
    filepath: str = Field(description="Path to the file to read")
```

2. **WriteFileInput**
```python
class WriteFileInput(BaseModel):
    filepath: str = Field(description="Path to the file to write")
    content: str = Field(description="Content to write to the file")
```

3. **FetchURLInput**
```python
class FetchURLInput(BaseModel):
    url: str = Field(description="URL to fetch content from")
```

4. **CalculateInput**
```python
class CalculateInput(BaseModel):
    expression: str = Field(description="Mathematical expression to evaluate")
```

**Why one class per tool?**
- Clear separation of concerns
- Easy to add fields to individual tools
- Better error messages (knows which tool failed)

**Field descriptions:**
- Become the `description` in OpenAI schema
- LLM reads these to understand how to use the tool
- Make them clear and specific!

### Component 3: Tool Functions

**Purpose:** Actual tool implementations

**Location:** Lines 131-212 in tool_agent.py

**All tools follow this pattern:**
```python
@tool_registry.register("tool_name", SchemaModel)
def tool_function(param1: type1, param2: type2) -> str:
    """Docstring becomes tool description"""
    try:
        # Do the work
        result = some_operation()
        return f"Success: {result}"
    except Exception as e:
        return f"Error: {str(e)}"
```

**Key design decisions:**

1. **Always return strings**
   - Easy for LLM to parse
   - Include success/error in result message
   - Actual status tracked separately by registry

2. **Try/except in every tool**
   - Graceful error handling
   - Return error message instead of crashing
   - Registry can continue even if one tool fails

3. **Clear success messages**
   - Tell user what happened
   - Include metrics (chars written, URL fetched, etc.)
   - Help LLM compose final response

**Tool 1: read_file**
- Reads text file content
- Returns file size + content
- Handles missing files gracefully

**Tool 2: write_file**
- Writes text to file
- Creates parent directories if needed
- Returns bytes written

**Tool 3: fetch_url**
- HTTP GET request
- 10 second timeout
- Truncates response to 1000 chars (educational limit)

**Tool 4: calculate**
- Evaluates math expressions
- Simple character whitelist for safety
- Returns expression + result

### Component 4: Logging Utilities

**Purpose:** Track everything for observability

**Location:** Lines 217-241 in tool_agent.py

**Functions:**

1. **`log_event(event_type, data)`**
   - Writes JSON line to logs/tool_agent.jsonl
   - Adds timestamp to every event
   - Appends (doesn't overwrite)

2. **`calculate_cost(usage)`**
   - Converts tokens → dollars
   - Uses current gpt-4o-mini pricing
   - Returns total cost in USD

**What gets logged:**

**LLM calls:**
```json
{
  "timestamp": "2024-12-04T12:34:56Z",
  "event_type": "llm_call",
  "iteration": 1,
  "input_tokens": 120,
  "output_tokens": 45,
  "latency_ms": 850.2,
  "cost_usd": 0.000034
}
```

**Tool calls:**
```json
{
  "timestamp": "2024-12-04T12:34:57Z",
  "event_type": "tool_call",
  "iteration": 1,
  "tool_name": "calculate",
  "arguments": {"expression": "42 * 137"},
  "success": true,
  "latency_ms": 0.15,
  "result_preview": "42 * 137 = 5754"
}
```

**Completion:**
```json
{
  "timestamp": "2024-12-04T12:34:58Z",
  "event_type": "completion",
  "iterations": 2,
  "total_cost_usd": 0.000086,
  "final_response": "The result is 5754."
}
```

### Component 5: Agent Loop

**Purpose:** Orchestrate LLM + tools

**Location:** Lines 246-348 in tool_agent.py

**Flow:**
```python
def run_agent(user_query, max_iterations=10):
    messages = [system_prompt, user_query]

    for iteration in range(max_iterations):
        # 1. Call OpenAI with tools
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tool_registry.get_schemas()  # All tools available
        )

        # 2. Check if tool calls requested
        if response.tool_calls:
            # 3. Execute each tool
            for tool_call in response.tool_calls:
                result = tool_registry.execute(
                    tool_call.name,
                    tool_call.arguments
                )
                messages.append(result)  # Feed back to LLM

            continue  # Loop again for final response

        # 4. No tool calls = final answer
        print(response.content)
        break
```

**Why iteration limit?**
- Prevent infinite loops
- Catch bugs (agent stuck calling same tool)
- Cost control (max 10 × API calls)

**Message history:**
- Keeps all messages in context
- LLM sees: user query, tool results, previous responses
- OpenAI manages this automatically with tool_call_id

---

## Key Design Decisions

### Decision 1: Why Pydantic over Manual JSON?

**Chosen approach:** Pydantic BaseModel classes

**Alternatives considered:**
- Manual JSON schema dictionaries (Module 1 approach)
- Python dataclasses with manual validation
- No validation (trust LLM output)

**Reasoning:**
- Pydantic auto-generates OpenAI schemas
- Single source of truth (define once)
- Runtime validation catches bugs
- Better IDE support

**Trade-offs:**
- ✅ Much cleaner code
- ✅ Fewer bugs from typos
- ❌ Extra dependency (but very common)
- ❌ Slight learning curve

### Decision 2: Why Decorator Pattern for Registration?

**Chosen approach:** `@tool_registry.register()` decorator

**Alternatives considered:**
- Manual registration: `tool_registry.add("name", func, schema)`
- Class-based tools (inherit from Tool base class)
- Config file with tool definitions

**Reasoning:**
- Registration happens at definition (can't forget)
- Clean, declarative syntax
- Tool definition = registration
- Easy to see all tools (search for @register)

**Trade-offs:**
- ✅ Impossible to forget to register a tool
- ✅ Very Pythonic (follows common patterns)
- ❌ Decorator syntax can be confusing to beginners
- ❌ Less explicit than manual registration

### Decision 3: Why Return Tuples from execute()?

**Chosen approach:** `(success, result, latency_ms)`

**Alternatives considered:**
- Raise exceptions on error
- Return just the result
- Return a dataclass/dict

**Reasoning:**
- Caller needs to know if tool succeeded
- Latency useful for logging/debugging
- Tuple unpacking is clean: `success, result, latency = ...`

**Trade-offs:**
- ✅ Explicit success/failure
- ✅ No exception handling needed in caller
- ❌ Could use named tuple or dataclass for clarity
- ❌ Caller must handle all 3 values

### Decision 4: Why JSONL over SQLite?

**Chosen approach:** Append-only JSONL file

**Alternatives considered:**
- SQLite database
- CSV file
- No logging

**Reasoning:**
- Simple (no database setup)
- Human readable (JSON)
- Easy to analyze with jq, grep, Python
- Append-only (fast, no locking)

**Trade-offs:**
- ✅ Zero setup, just works
- ✅ Easy to parse and analyze
- ❌ No queries (must scan whole file)
- ❌ Can grow large (need log rotation in production)

---

## Questions to Ask Your Professor (Claude Code)

### 🌱 Getting Started (Basic Understanding)

1. "I'm confused about Pydantic - can you explain comparison_simple_vs_pydantic.py line by line?"

2. "Walk me through the ToolRegistry class - how does it store and retrieve tools?"

3. "Show me how the @tool_registry.register decorator works line by line"

4. "What happens when I call tool_registry.execute('calculate', {'expression': '2+2'})?"

5. "How does Pydantic validate the tool arguments before execution?"

6. "Why do we need Field() in the Pydantic models? What does description do?"

7. "Show me the flow from user query to tool execution to final response"

8. "How does the agent know when to use tools vs answer directly?"

### 🌿 Going Deeper (Architecture & Design)

9. "Why do we generate OpenAI schemas from Pydantic instead of writing them manually?"

10. "What would break if I forgot to add a tool to the registry but called it anyway?"

11. "How does the message history work when tools are called multiple times?"

12. "Walk through the cost calculation - how do tokens become dollars?"

13. "Why do all tools return strings instead of different types?"

14. "How would you add a new tool that takes multiple parameters?"

15. "What's the difference between tool_call.id and tool_call.function.name?"

### 🌳 Advanced Understanding (Trade-offs & Alternatives)

16. "What are the trade-offs of using decorators vs manual registration?"

17. "When would you NOT want to use Pydantic for tool schemas?"

18. "How would you implement rate limiting or retries for the fetch_url tool?"

19. "What would it take to make this work with Anthropic's API instead of OpenAI?"

20. "How could you make the registry thread-safe for multiple agents?"

21. "What's missing for production use? (auth, retries, monitoring, etc.)"

---

## Experiments to Try

### Experiment 1: Add a JSON Parser Tool

Add a tool that parses JSON strings:

```python
class JSONParseInput(BaseModel):
    json_string: str = Field(description="JSON string to parse")

@tool_registry.register("json_parse", JSONParseInput)
def json_parse(json_string: str) -> str:
    """Parse a JSON string and return formatted output"""
    try:
        data = json.loads(json_string)
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"Error parsing JSON: {e}"
```

Test: "Parse this JSON: {\"name\": \"Alice\", \"age\": 30}"

### Experiment 2: Break Pydantic Validation

Call a tool with wrong types:

```python
# Manually test validation
try:
    result = tool_registry.execute("calculate", {"expression": 12345})
except Exception as e:
    print(f"Caught: {e}")
```

What error do you get? How is it helpful?

### Experiment 3: Add Cost Limits

Modify the agent loop to stop if cost exceeds a threshold:

```python
COST_LIMIT = 0.001  # $0.001 max

if total_cost > COST_LIMIT:
    print(f"Cost limit exceeded: ${total_cost:.6f}")
    break
```

Test with expensive queries. Does it stop?

### Experiment 4: Tool Performance Analysis

Read the JSONL logs and analyze:
- Which tool is slowest?
- Which tool is called most?
- What's the average latency per tool?

```python
import json

with open("logs/tool_agent.jsonl") as f:
    tool_calls = [json.loads(line) for line in f if '"tool_call"' in line]

for tc in tool_calls:
    print(f"{tc['tool_name']}: {tc['latency_ms']:.2f}ms")
```

### Experiment 5: Error Handling

Make a tool fail and see what happens:

```python
run_agent("Read a file that doesn't exist: /fake/path.txt")
```

Does the agent recover gracefully? How does it tell the user?

### Experiment 6: Multi-Tool Queries

Test queries that need multiple tools:

```python
run_agent("Fetch https://api.github.com/zen, write it to zen.txt, then calculate the length of the text")
```

Count the iterations. How many tool calls happened?

### Experiment 7: Remove Error Handling

Comment out try/except in one tool:

```python
@tool_registry.register("calculate", CalculateInput)
def calculate(expression: str) -> str:
    # try:  # <-- Comment this out
    return f"{expression} = {eval(expression)}"
    # except Exception as e:  # <-- And this
    #     return f"Error: {e}"
```

Test with bad input. What happens?

### Experiment 8: Custom Tool with External API

Add a tool that uses a real API (e.g., weather, stocks):

```python
@tool_registry.register("get_weather", WeatherInput)
def get_weather(city: str) -> str:
    api_key = os.getenv("WEATHER_API_KEY")
    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}")
    data = response.json()
    return f"Weather in {city}: {data['weather'][0]['description']}"
```

### Experiment 9: Schema Introspection

Examine the generated schemas:

```python
schemas = tool_registry.get_schemas()
for schema in schemas:
    print(json.dumps(schema, indent=2))
```

Compare to your Pydantic definitions. Do they match?

### Experiment 10: Benchmark Cost

Run the same query 10 times and track costs:

```python
total = 0
for i in range(10):
    # Run agent, track cost
    # Add to total
print(f"10 queries cost: ${total:.6f}")
print(f"Per query average: ${total/10:.6f}")
```

---

## Testing & Verification

**Success criteria:**

✅ All 4 tools work (file, HTTP, calculator)
✅ Pydantic validates inputs before execution
✅ Registry dispatches to correct tool by name
✅ Logs show per-tool latency and cost
✅ Adding a 5th tool requires only @register decorator
✅ Agent handles tool errors gracefully
✅ Cost tracking is accurate

**Testing checklist:**

1. [ ] Run agent with calculator query
2. [ ] Run agent with file write + read
3. [ ] Run agent with HTTP fetch
4. [ ] Check logs/tool_agent.jsonl for all events
5. [ ] Verify cost calculations match token counts
6. [ ] Add a new tool (e.g., JSON parser)
7. [ ] Test tool with invalid inputs
8. [ ] Run multi-tool query (uses 2+ tools)
9. [ ] Check iteration count < max_iterations

---

## Going Further

**Production enhancements:**

1. **Authentication** - Add API keys to tools that need them
2. **Rate limiting** - Prevent tool abuse
3. **Retries** - Handle transient failures
4. **Timeouts** - Per-tool timeout limits
5. **Caching** - Cache repeated tool results
6. **Async** - Use asyncio for parallel tool calls
7. **Monitoring** - Send metrics to observability platform
8. **Tool versioning** - Support multiple versions of same tool

**Advanced patterns:**

1. **Conditional tools** - Only offer certain tools based on user role
2. **Tool chaining** - One tool's output becomes another's input
3. **Tool fallbacks** - If primary tool fails, try backup
4. **Dynamic schemas** - Generate tool schemas from config files
5. **Tool namespaces** - Group related tools (file.read, file.write)

---

## Key Takeaways

1. **Pydantic makes schemas type-safe** - Single source of truth, automatic validation
2. **Decorators enable clean registration** - Tool definition = registration
3. **Registry pattern scales** - 1 tool or 100 tools, dispatch is one line
4. **Cost tracking is essential** - Know what you're spending
5. **JSONL logging provides visibility** - Debug and analyze easily

---

## What's Next?

**Module 4: Multi-Agent Systems** (December 22)

You'll learn:
- Coordinating multiple agents (Planner, Worker, Critic)
- Shared state management between agents
- Message passing patterns
- Evaluation and quality checks

**The tool registry you built here will be reused** - multiple agents will share the same tool registry, demonstrating the value of clean abstractions!
