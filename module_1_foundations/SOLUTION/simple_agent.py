#!/usr/bin/env python3
"""
Module 1: Simple Agent
======================
A minimal agent loop with one tool and structured logging.

Key Concepts Demonstrated:
- LLM call anatomy (prompts → tokens → completion)
- Agent loop (policy + tools + stop condition)
- JSON contracts for function calling
- JSONL logging for observability
"""

import os
import json
import time
from datetime import datetime
from openai import OpenAI

# ============================================================================
# CONFIGURATION
# ============================================================================

# Load API key from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Model configuration
MODEL = "gpt-4o-mini"  # Fast and cheap for learning
TEMPERATURE = 0.1  # Low temperature for deterministic tool calls
MAX_ITERATIONS = 10  # Safety limit to prevent infinite loops

# Logging configuration
LOG_FILE = "logs/simple_agent.jsonl"


# ============================================================================
# TOOL DEFINITIONS
# ============================================================================

def get_weather(city: str, units: str = "fahrenheit") -> str:
    """
    Simulated weather tool (no real API calls in this learning module).

    In a real agent, this would call an actual weather API.
    For learning, we'll return mock data so we can focus on the agent loop.

    Args:
        city: City name (e.g., "Seattle")
        units: Temperature units ("fahrenheit" or "celsius")

    Returns:
        Weather description string
    """
    # Mock weather data (in Module 3 we'll wire real APIs)
    mock_weather = {
        "seattle": {"temp": 72, "condition": "Sunny"},
        "new york": {"temp": 68, "condition": "Cloudy"},
        "london": {"temp": 55, "condition": "Rainy"},
        "tokyo": {"temp": 75, "condition": "Clear"}
    }

    city_lower = city.lower()
    weather = mock_weather.get(city_lower, {"temp": 70, "condition": "Unknown"})

    temp = weather["temp"]
    if units == "celsius":
        temp = round((temp - 32) * 5/9)
        unit_symbol = "°C"
    else:
        unit_symbol = "°F"

    return f"{temp}{unit_symbol}, {weather['condition']}"


# JSON Contract (Tool Schema)
# This is what we send to the LLM so it knows how to call the tool
WEATHER_TOOL = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current weather for a city. Use this when the user asks about weather conditions.",
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
                    "description": "Temperature units (default: fahrenheit)"
                }
            },
            "required": ["city"]
        }
    }
}

# Tool registry (in Module 3 we'll make this dynamic)
TOOLS = [WEATHER_TOOL]


# ============================================================================
# LOGGING UTILITIES
# ============================================================================

def log_event(event_type: str, data: dict):
    """
    Write a structured event to JSONL log file.

    Each line is a complete JSON object with:
    - timestamp: ISO 8601 format
    - event_type: What happened (llm_call, tool_call, completion, etc.)
    - data: Event-specific information

    Args:
        event_type: Type of event (e.g., "llm_call", "tool_execution")
        data: Event data dictionary
    """
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event_type": event_type,
        **data
    }

    # Ensure log directory exists
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    # Append to JSONL file (one JSON object per line)
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")


# ============================================================================
# AGENT LOOP
# ============================================================================

def run_agent(user_query: str) -> str:
    """
    Main agent loop: Keep calling LLM until task is complete.

    Flow:
    1. Send user query + tool definitions to LLM
    2. LLM responds with either:
       - Tool call → Execute tool → Feed result back (continue loop)
       - Text response → Task complete (exit loop)
    3. Repeat until done or max iterations reached

    Args:
        user_query: User's question/request

    Returns:
        Final response string
    """
    print(f"\n{'='*70}")
    print(f"🤖 AGENT STARTING")
    print(f"{'='*70}")
    print(f"Query: {user_query}\n")

    # Initialize conversation with system policy + user query
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful weather assistant. "
                "When asked about weather, use the get_weather tool. "
                "Provide clear, friendly responses."
            )
        },
        {
            "role": "user",
            "content": user_query
        }
    ]

    # Agent loop
    iteration = 0
    while iteration < MAX_ITERATIONS:
        iteration += 1
        print(f"--- Iteration {iteration} ---")

        # Call LLM
        start_time = time.time()
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            temperature=TEMPERATURE
        )
        latency = time.time() - start_time

        message = response.choices[0].message

        # Log LLM call
        log_event("llm_call", {
            "iteration": iteration,
            "model": MODEL,
            "temperature": TEMPERATURE,
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
            "latency_ms": round(latency * 1000, 2),
            "finish_reason": response.choices[0].finish_reason
        })

        # Check if LLM wants to call a tool
        if message.tool_calls:
            # LLM requested tool execution
            tool_call = message.tool_calls[0]
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            print(f"🔧 Tool call: {function_name}({function_args})")

            # Execute the tool
            if function_name == "get_weather":
                result = get_weather(**function_args)
            else:
                result = f"Error: Unknown tool '{function_name}'"

            print(f"📊 Result: {result}")

            # Log tool execution
            log_event("tool_execution", {
                "iteration": iteration,
                "tool_name": function_name,
                "arguments": function_args,
                "result": result
            })

            # Add assistant's tool call to conversation
            messages.append(message)

            # Add tool result to conversation
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

            # Continue loop - LLM will process the tool result

        else:
            # LLM provided final answer (no tool calls)
            final_answer = message.content
            print(f"✅ Final answer: {final_answer}")

            # Log completion
            log_event("completion", {
                "iteration": iteration,
                "result": final_answer,
                "total_iterations": iteration
            })

            print(f"\n{'='*70}")
            print(f"✅ AGENT COMPLETE (took {iteration} iterations)")
            print(f"{'='*70}\n")

            return final_answer

    # Max iterations reached (safety cutoff)
    error_msg = f"Agent stopped: reached max iterations ({MAX_ITERATIONS})"
    print(f"⚠️  {error_msg}")

    log_event("error", {
        "reason": "max_iterations",
        "max_iterations": MAX_ITERATIONS
    })

    return error_msg


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # Example queries to test the agent
    test_queries = [
        "What's the weather in Seattle?",
        "How's the weather in Tokyo?",
        "Is it raining in London?"
    ]

    # Run the agent with the first query
    print("\n🎓 MODULE 1: SIMPLE AGENT")
    print("=" * 70)

    result = run_agent(test_queries[0])

    print("\n📝 Log file created:", LOG_FILE)
    print("💡 Try running with different queries or inspect the logs!")
