# Module 1 Project: Simple Weather Agent

## How to Use This Document

You're reading the architecture guide for Module 1's solution. The working code is in `SOLUTION/simple_agent.py`.

**Your learning path:**
1. ✅ Read CONCEPTS.md (theory - LLM anatomy, agent loops, JSON contracts)
2. ➡️ Read this PROJECT.md (architecture - how it's designed)
3. ➡️ Study SOLUTION/simple_agent.py (the working code)
4. ➡️ Ask Claude Code the seed questions below
5. ➡️ Experiment and modify the code

---

## What This Agent Does

This agent demonstrates the **fundamental agent loop pattern** that all AI agents share.

**Capabilities:**
- Answers weather questions by calling a tool
- Implements complete agent loop with finish_reason logic
- Logs every event to JSONL for observability
- Demonstrates context growth (motivates Module 2)

**Example interaction:**
```
User: "What's the weather in Seattle?"

Iteration 1:
- LLM decides to call get_weather("Seattle")
- Tool executes → "72°F, Sunny"
- Result added to context

Iteration 2:
- LLM synthesizes final answer
- "The weather in Seattle is currently 72°F and sunny."
- finish_reason = "stop" → Loop exits

Total: 2 iterations, 292 tokens, ~3.8s
```

---

## Architecture Overview

### The Agent Loop Pattern

```
┌────────────────────────────────────────────────────┐
│                 Simple Agent                       │
│                                                    │
│  ┌──────────────┐                                 │
│  │  User Query  │                                 │
│  └──────┬───────┘                                 │
│         │                                         │
│         ▼                                         │
│  ┌──────────────────────────────┐                │
│  │   messages = [               │                │
│  │     system_message,          │                │
│  │     user_query               │                │
│  │   ]                          │                │
│  └──────┬───────────────────────┘                │
│         │                                         │
│         ▼                                         │
│  ┌──────────────────────────────┐                │
│  │   While iteration < max:     │◄───────┐       │
│  └──────┬───────────────────────┘        │       │
│         │                                 │       │
│         ▼                                 │       │
│  ┌──────────────────────────────┐        │       │
│  │   LLM Call                   │        │       │
│  │   (OpenAI GPT-4o-mini)       │        │       │
│  │   messages + tools           │        │       │
│  └──────┬───────────────────────┘        │       │
│         │                                 │       │
│         ▼                                 │       │
│  ┌──────────────────────────────┐        │       │
│  │   Check finish_reason        │        │       │
│  └──────┬───────────────────────┘        │       │
│         │                                 │       │
│    ┌────┴────┐                           │       │
│    │         │                           │       │
│    ▼         ▼                           │       │
│  "tool_calls"  "stop"                    │       │
│    │            │                        │       │
│    ▼            ▼                        │       │
│  Execute Tool  Return Answer             │       │
│    │                                     │       │
│    ▼                                     │       │
│  Add result to messages ─────────────────┘       │
│  (Continue loop)                                 │
└────────────────────────────────────────────────────┘
```

**Key insight:** The entire agent is just a while loop that checks `finish_reason` to decide what to do next.

---

## Tools & Technologies

### OpenAI GPT-4o-mini

**Model:** `gpt-4o-mini`

**Why we chose it:**
- Fast (~2s per call)
- Cheap ($0.15/$0.60 per million tokens)
- Reliable tool calling
- Good for learning fundamentals

**Alternatives:**
- GPT-4o: More capable, more expensive
- GPT-3.5-turbo: Cheaper, less capable tool calling
- Claude, Gemini: Different APIs (covered in future modules)

### Function Calling (Tool Calling)

**What it is:**
OpenAI's API feature that lets LLMs request function execution using JSON.

**How it works:**
1. Send tool definitions as JSON schemas
2. LLM analyzes user query
3. If tool needed: LLM returns `tool_calls` with arguments
4. You execute the function
5. Send result back to LLM
6. LLM uses result to answer user

**Key properties:**
- LLM generates valid JSON matching your schema
- finish_reason indicates whether tools are needed
- Tool execution happens in YOUR code (not by LLM)

### JSONL Logging

**Format:** JSON Lines (one JSON object per line)

**Why JSONL:**
- Each line is valid JSON (easy to parse)
- Append-only (no need to read/parse whole file)
- Human-readable with line-by-line viewing
- Standard format for ML logging

**What we log:**
```jsonl
{"timestamp": "...", "event_type": "llm_call", "tokens": 117, ...}
{"timestamp": "...", "event_type": "tool_execution", "tool": "get_weather", ...}
{"timestamp": "...", "event_type": "completion", "iterations": 2, ...}
```

---

## Component Breakdown

### Component 1: Configuration Section

**Purpose:** Central place for all settings

**What it contains:**
```python
# API client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Model settings
MODEL = "gpt-4o-mini"
TEMPERATURE = 0.1      # Low for deterministic tool calls
MAX_ITERATIONS = 10     # Safety limit

# Paths
LOG_FILE = "logs/simple_agent.jsonl"
```

**Design decision:**
- Low temperature (0.1) ensures reliable tool calling
- MAX_ITERATIONS prevents infinite loops
- Single source of truth for settings

### Component 2: Tool Definition (Python Function)

**Purpose:** Actual tool implementation

```python
def get_weather(city: str, units: str = "fahrenheit") -> str:
    """
    Get current weather for a city.

    Args:
        city: City name
        units: "fahrenheit" or "celsius"

    Returns:
        Weather description string
    """
    # Mock implementation for learning
    mock_weather = {
        "seattle": {"temp": 72, "condition": "Sunny"},
        ...
    }

    # Return formatted string
    return f"{temp}{unit_symbol}, {condition}"
```

**Key points:**
- Regular Python function (not special)
- Type hints help with schema generation
- Returns string (not JSON) - simpler for learning
- Mock data (no real API) - focus on agent pattern

### Component 3: Tool Contract (JSON Schema)

**Purpose:** Tell LLM how to call the tool

```python
WEATHER_TOOL = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current weather for a city. Use when user asks about weather.",
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

**Design decisions:**
- Clear description → LLM knows when to use tool
- Enum for units → Prevents invalid values
- Only city required → units has default
- Examples in descriptions → Helps LLM format correctly

### Component 4: Logging Utilities

**Purpose:** Structured event logging

```python
def log_event(event_type: str, data: dict):
    """Write structured event to JSONL log."""
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event_type": event_type,
        **data  # Spread operator for clean merging
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
```

**Event types:**
- `llm_call`: Every LLM request (tokens, latency, finish_reason)
- `tool_execution`: Every tool call (name, args, result)
- `completion`: Final result (total iterations, final answer)
- `error`: Any failures

**Why this matters:**
Complete observability → Can debug any issue by reading logs

### Component 5: Agent Loop

**Purpose:** Main agent logic

**The loop:**
```python
def run_agent(user_query: str) -> str:
    # Initialize messages
    messages = [
        {"role": "system", "content": "You are a helpful weather assistant..."},
        {"role": "user", "content": user_query}
    ]

    # Loop until done or max iterations
    iteration = 0
    while iteration < MAX_ITERATIONS:
        iteration += 1

        # Call LLM
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=[WEATHER_TOOL],
            temperature=TEMPERATURE
        )

        message = response.choices[0].message

        # Decision point: Check finish_reason
        if message.tool_calls:
            # Execute tool, add result, continue loop
            result = execute_tool(message.tool_calls[0])
            messages.append(message)  # LLM's tool request
            messages.append({"role": "tool", "content": result})  # Result
        else:
            # No tools needed - we're done!
            return message.content

    # Safety: Max iterations reached
    return "Agent stopped: max iterations reached"
```

**Key insights:**
1. Messages list grows with each iteration (context growth!)
2. finish_reason implicitly checked via `message.tool_calls`
3. Tool results fed back to LLM in next iteration
4. Safety limit prevents infinite loops

---

## Key Design Decisions

### Decision 1: Why One Tool Only?

**Chosen:** Single `get_weather` tool
**Alternative:** Multiple tools (weather, time, calculator, etc.)

**Reasoning:**
- Focus on the agent loop pattern, not tool complexity
- Easier to trace execution in logs
- Clearly shows finish_reason decision logic
- Multi-tool coordination is Module 3 topic

### Decision 2: Why Mock Data?

**Chosen:** Hardcoded weather data
**Alternative:** Real API calls (OpenWeatherMap, etc.)

**Reasoning:**
- No API key needed (simpler setup)
- Consistent results (easier to learn)
- Focus on agent pattern, not API integration
- Real APIs add latency and cost
- Module 3 covers real API integration

### Decision 3: Why Low Temperature (0.1)?

**Chosen:** TEMPERATURE = 0.1
**Alternative:** 0.7-1.0 (more creative)

**Reasoning:**
- Tool calling needs determinism
- Low temp → reliable JSON generation
- Low temp → consistent tool selection
- High temp risks malformed tool calls
- Students can experiment with this!

### Decision 4: Why MAX_ITERATIONS = 10?

**Chosen:** Safety limit of 10 iterations
**Alternative:** No limit, or 3, or 20

**Reasoning:**
- Prevents infinite loops (critical for learning)
- 10 is generous (most queries take 2-3)
- Easy to hit during experiments (teaches limits)
- Clear error message when hit

**When to adjust:**
- Lower (3): Force efficiency, catch issues faster
- Higher (20): Complex multi-step queries
- Remove: Only in production with other safeguards

### Decision 5: Why JSONL Over Other Formats?

**Chosen:** JSONL logging
**Alternatives:** CSV, plain text, database

**Reasoning:**
- JSON = structured, machine-parseable
- Lines = append-only, no file locks
- Human-readable with `cat logs/file.jsonl`
- Standard in ML/AI logging
- Easy to process with `jq`, Python, etc.

**Trade-offs:**
- Larger than CSV
- Not as compact as binary
- Perfect for learning and debugging

---

## File Structure

```
module_1_foundations/
├── CONCEPTS.md           # Theory you already read
├── PROJECT.md            # This file
├── README.md             # Module overview
├── SOLUTION/
│   └── simple_agent.py   # Complete working agent
└── logs/
    └── simple_agent.jsonl  # Execution logs (gitignored)
```

---

## Configuration

The agent uses these settings:

```python
# LLM settings
MODEL = "gpt-4o-mini"
TEMPERATURE = 0.1

# Safety
MAX_ITERATIONS = 10

# Logging
LOG_FILE = "logs/simple_agent.jsonl"
```

**Experiments to try:**
- Change temperature: 0.1 → 0.5 → 0.9
- Change max iterations: 10 → 3 → 20
- Change model: gpt-4o-mini → gpt-4o

---

## Testing & Verification

### Success Criteria

Your agent is working when:

1. ✅ **Tool calling works**
   - User asks about weather
   - Agent calls `get_weather(city)`
   - Result returned correctly

2. ✅ **Loop terminates correctly**
   - finish_reason = "stop" after synthesizing answer
   - No infinite loops

3. ✅ **Logging captures everything**
   - llm_call events with tokens and latency
   - tool_execution events with args and results
   - completion event with final answer

4. ✅ **Multiple iterations work**
   - Agent can handle multi-step queries
   - Context carries forward correctly

5. ✅ **Safety limit works**
   - MAX_ITERATIONS prevents infinite loops
   - Clear error message when limit hit

### Testing Checklist

- [ ] Agent runs without errors
- [ ] Weather query returns correct answer
- [ ] Tool is called with valid JSON
- [ ] Logs show all events (llm_call, tool_execution, completion)
- [ ] Token counts increase across iterations (context growth)
- [ ] Latency is measured and logged
- [ ] finish_reason is logged correctly
- [ ] Agent stops at right condition
- [ ] MAX_ITERATIONS safety works (try impossible query)

---

## Questions to Ask Your Professor (Claude Code)

### 🌱 Getting Started (Start Here!)

These questions will help you understand the basics:

1. **"Walk me through the agent loop in simple_agent.py - how does it work?"**
   - Understand the while loop and decision logic

2. **"Explain finish_reason - why is it important?"**
   - See how it elegantly categorizes next actions

3. **"Show me how the tool definition connects to the tool contract"**
   - Understand Python function → JSON schema mapping

4. **"Trace a single query through the code step-by-step"**
   - Follow execution from user input to final answer

5. **"Why is temperature set to 0.1 instead of 0.7?"**
   - Understand determinism for tool calling

6. **"What's happening to the messages list as iterations increase?"**
   - See context growth in action

7. **"Explain the JSONL logging - what events are captured?"**
   - Understand observability

### 🌿 Going Deeper (Once You Understand Basics)

8. **"What happens if I remove the MAX_ITERATIONS limit?"**
   - Understand safety mechanisms

9. **"Why does the tool return a string instead of JSON?"**
   - Design decision for simplicity

10. **"Show me in the logs: where does token count increase?"**
    - Measure context growth

11. **"What would happen if the LLM returns malformed JSON for tool args?"**
    - Understand error handling (or lack thereof!)

12. **"How would I add a second tool to this agent?"**
    - Extend to multi-tool scenario

13. **"Walk me through what happens when finish_reason is 'stop'"**
    - Understand termination logic

14. **"Why do we append both the tool call AND the result to messages?"**
    - Understand conversation context building

### 🌳 Advanced Understanding

15. **"How would this agent handle a query that requires multiple tool calls?"**
    - Think about iteration patterns

16. **"What's the relationship between temperature and tool calling reliability?"**
    - Experiment with different values

17. **"How would I add error handling for API failures?"**
    - Think about production readiness

18. **"Show me how to calculate cost from the logged token counts"**
    - Understand cost modeling

---

## Experiments to Try

### Experiment 1: Change Temperature
```python
# In simple_agent.py, try:
TEMPERATURE = 0.1  # Current (deterministic)
TEMPERATURE = 0.5  # Moderate
TEMPERATURE = 0.9  # Creative

# Observe:
# - Does tool calling become unreliable?
# - Do responses vary more?
# - Check logs for consistency
```

### Experiment 2: Add a Second Tool
```python
# Add to simple_agent.py:
def get_time(timezone: str = "UTC") -> str:
    """Get current time in timezone."""
    return datetime.now().strftime("%H:%M:%S %Z")

# Create tool contract (copy WEATHER_TOOL pattern)
# Add to TOOLS list
# Test: "What time is it and what's the weather in Seattle?"
```

### Experiment 3: Force Multiple Iterations
```python
# Try complex queries:
"Compare weather in Seattle and New York"
"Is it warmer in Seattle or London?"
"What should I wear in Tokyo today?"

# Check logs: How many iterations? Why?
```

### Experiment 4: Break the Safety Limit
```python
# Set MAX_ITERATIONS = 2
# Ask: "What's the weather in Seattle?"
# What happens? Why? Check logs.
```

### Experiment 5: Study Token Growth
```python
# Run agent with increasing query complexity
# Check logs for token counts
# Plot: iteration → tokens
# See the context growth problem!
```

---

## Going Further (Optional Enhancements)

### Enhancement 1: Real Weather API
```python
import requests

def get_weather(city: str, units: str = "fahrenheit") -> str:
    api_key = os.getenv("OPENWEATHER_API_KEY")
    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather",
        params={"q": city, "appid": api_key, "units": "imperial"}
    )
    data = response.json()
    return f"{data['main']['temp']}°F, {data['weather'][0]['description']}"
```

### Enhancement 2: Error Handling
```python
try:
    response = client.chat.completions.create(...)
except openai.RateLimitError:
    log_event("error", {"type": "rate_limit"})
    time.sleep(60)  # Retry after 1 minute
except openai.APIError as e:
    log_event("error", {"type": "api_error", "message": str(e)})
    return "Sorry, I'm having trouble connecting."
```

### Enhancement 3: Streaming Responses
```python
for chunk in client.chat.completions.create(
    model=MODEL,
    messages=messages,
    tools=TOOLS,
    stream=True  # Stream!
):
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

### Enhancement 4: Token Usage Tracking
```python
class TokenTracker:
    def __init__(self):
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0

    def add(self, usage):
        self.total_prompt_tokens += usage.prompt_tokens
        self.total_completion_tokens += usage.completion_tokens

    def cost(self):
        # GPT-4o-mini pricing
        prompt_cost = self.total_prompt_tokens * 0.15 / 1_000_000
        completion_cost = self.total_completion_tokens * 0.60 / 1_000_000
        return prompt_cost + completion_cost
```

---

## Key Takeaways

After studying this module, you should understand:

1. **Agent loops are simple** - Just while loops with finish_reason checks
2. **finish_reason is elegant** - Cleanly categorizes "tool_calls" vs "stop"
3. **Context grows linearly** - Each iteration adds to messages (problem for Module 2!)
4. **Tools enable capabilities** - LLMs can't compute, so tools are essential
5. **Logging is critical** - Complete observability makes debugging trivial

---

## What's Next?

After completing Module 1:

1. **Test thoroughly** - Run through testing checklist
2. **Study the logs** - Understand what happened at each step
3. **Experiment** - Try the suggested modifications
4. **Reflect** - Answer the reflection questions in README.md
5. **Measure context growth** - See tokens increase across iterations

**Then move to Module 2:** Solve the context growth problem with vector memory and RAG!

---

## Summary: The Foundation Pattern

**What you learned:**
```python
# This pattern powers ALL agents:

while not done:
    response = llm(messages, tools)

    if response.finish_reason == "tool_calls":
        result = execute_tool(response.tool_calls)
        messages.append(result)  # Continue
    elif response.finish_reason == "stop":
        return response.content  # Done!
```

**Why it matters:**
- ChatGPT uses this pattern
- Cursor uses this pattern
- All agent frameworks use this pattern
- You now understand the foundation!

---

**Ready to study the code?** Open `SOLUTION/simple_agent.py` and start asking Claude Code those seed questions!
