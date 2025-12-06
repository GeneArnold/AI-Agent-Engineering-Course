#!/usr/bin/env python3
"""
Module 3: Multi-Tool Agent with Dynamic Registry
=================================================
Demonstrates dynamic tool registration, Pydantic validation, and clean dispatch patterns.

Key Concepts Demonstrated:
- Pydantic schemas for type-safe tool definitions
- Dynamic tool registration with decorators
- Clean tool dispatch (no if/elif chains)
- Per-tool cost tracking and performance monitoring
- JSONL logging for observability

Author: AI Agent Engineering Course
"""

import os
import json
import time
from datetime import datetime, UTC
from typing import Optional, cast, Any
from pathlib import Path
from pydantic import BaseModel, Field
from openai import OpenAI
import requests

# ============================================================================
# CONFIGURATION
# ============================================================================

# Load API key from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Model configuration
MODEL = "gpt-4o-mini"
TEMPERATURE = 0.1
MAX_ITERATIONS = 10

# Logging configuration
LOG_FILE = "logs/tool_agent.jsonl"

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)


# ============================================================================
# PYDANTIC SCHEMAS - Type-Safe Tool Definitions
# ============================================================================
# 👉 MODULE 1 vs MODULE 3: In Module 1, you wrote JSON schemas by hand.
# Here, we define schemas as Python classes and let Pydantic generate the JSON.
# See comparison_simple_vs_pydantic.py for a side-by-side example!

class ReadFileInput(BaseModel):
    """Schema for read_file tool"""
    filepath: str = Field(description="Path to the file to read")


class WriteFileInput(BaseModel):
    """Schema for write_file tool"""
    filepath: str = Field(description="Path to the file to write")
    content: str = Field(description="Content to write to the file")


class FetchURLInput(BaseModel):
    """Schema for fetch_url tool"""
    url: str = Field(description="URL to fetch content from")


class CalculateInput(BaseModel):
    """Schema for calculate tool"""
    expression: str = Field(description="Mathematical expression to evaluate (e.g., '2 + 2', '10 * 5')")


# ============================================================================
# TOOL REGISTRY - Dynamic Registration & Dispatch
# ============================================================================
# 👉 MODULE 1 vs MODULE 3: In Module 1, you had a static AVAILABLE_TOOLS list
# and used if/elif to dispatch tools. This registry replaces BOTH of those!
# - Tools register themselves (no manual list)
# - Dictionary lookup replaces if/elif (O(1) instead of O(n))

class ToolRegistry:
    """
    Simple tool registry using decorator pattern.

    Handles:
    - Tool registration via @tool_registry.register
    - Schema generation for OpenAI
    - Tool execution with Pydantic validation
    """

    def __init__(self):
        self._tools = {}  # {name: {"func": callable, "schema": dict, "model": PydanticModel}}

    def register(self, name: str, schema_model: type[BaseModel]):
        """
        Decorator to register a tool.

        Usage:
            @tool_registry.register("tool_name", SchemaModel)
            def my_tool(param1: str, param2: int) -> str:
                return "result"

        👉 This ONE decorator replaces 3 manual steps from Module 1:
           1. Writing the JSON schema by hand
           2. Adding it to AVAILABLE_TOOLS list
           3. Adding an if/elif branch for dispatch
        """
        def decorator(func):
            # Generate OpenAI-compatible schema from Pydantic model
            # 👉 This is automatic! No manual JSON writing needed.
            properties = {}
            required = []

            for field_name, field_info in schema_model.model_fields.items():
                properties[field_name] = {
                    "type": "string",  # Simplified: all strings for this educational version
                    "description": field_info.description or ""
                }
                if field_info.is_required():
                    required.append(field_name)

            openai_schema = {
                "type": "function",
                "function": {
                    "name": name,
                    "description": func.__doc__ or "No description provided",
                    "parameters": {
                        "type": "object",
                        "properties": properties,
                        "required": required
                    }
                }
            }

            # Store tool - automatically added to registry!
            self._tools[name] = {
                "func": func,
                "schema": openai_schema,
                "model": schema_model
            }

            return func
        return decorator

    def get_schemas(self):
        """Return list of tool schemas for OpenAI API"""
        return [tool["schema"] for tool in self._tools.values()]

    def execute(self, tool_name: str, arguments: dict):
        """
        Execute a tool with Pydantic validation.

        Returns tuple: (success: bool, result: str, latency_ms: float)

        👉 MODULE 1 vs MODULE 3: In Module 1, you had if/elif chains like:
           if tool_name == "get_weather": result = get_weather(**args)
           elif tool_name == "get_stock": result = get_stock(**args)
           ...

           Here, we just look up the tool in a dictionary - one line for ALL tools!
        """
        if tool_name not in self._tools:
            return False, f"Tool '{tool_name}' not found", 0

        tool = self._tools[tool_name]  # 👈 O(1) lookup replaces if/elif chain
        start_time = time.time()

        try:
            # Validate arguments with Pydantic
            # 👉 This catches bad inputs BEFORE calling the function
            validated = tool["model"](**arguments)

            # Execute the tool function
            result = tool["func"](**validated.model_dump())

            latency_ms = (time.time() - start_time) * 1000
            return True, str(result), latency_ms

        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            return False, f"Error: {str(e)}", latency_ms


# Initialize global registry
tool_registry = ToolRegistry()


# ============================================================================
# TOOL IMPLEMENTATIONS - Decorated with @tool_registry.register
# ============================================================================
# 👉 SCALABILITY WIN: Notice how easy it is to add tools below.
# Each tool is just:
#   1. Define Pydantic schema (5 lines)
#   2. Add @register decorator (1 line)
#   3. Write function (10-20 lines)
#
# That's it! No manual JSON schema, no updating AVAILABLE_TOOLS, no if/elif.
# With 10 tools: Module 1 = ~500 lines | Module 3 = ~100 lines

@tool_registry.register("read_file", ReadFileInput)
def read_file(filepath: str) -> str:
    """Read the contents of a text file"""
    try:
        path = Path(filepath)
        if not path.exists():
            return f"Error: File '{filepath}' does not exist"

        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        return f"File content ({len(content)} chars):\n{content}"
    except Exception as e:
        return f"Error reading file: {str(e)}"


@tool_registry.register("write_file", WriteFileInput)
def write_file(filepath: str, content: str) -> str:
    """Write content to a text file"""
    try:
        path = Path(filepath)

        # Create parent directories if needed
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

        return f"Successfully wrote {len(content)} characters to '{filepath}'"
    except Exception as e:
        return f"Error writing file: {str(e)}"


@tool_registry.register("fetch_url", FetchURLInput)
def fetch_url(url: str) -> str:
    """Fetch content from a URL"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Limit response size for educational purposes
        content = response.text[:1000]

        return f"Fetched {len(response.text)} chars from {url}:\n{content}..."
    except Exception as e:
        return f"Error fetching URL: {str(e)}"


@tool_registry.register("calculate", CalculateInput)
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression safely"""
    try:
        # Simple safe evaluation (educational - not production-safe!)
        # Only allow numbers, operators, and parentheses
        allowed_chars = set("0123456789+-*/(). ")
        if not all(c in allowed_chars for c in expression):
            return "Error: Expression contains invalid characters"

        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error calculating: {str(e)}"


# ============================================================================
# LOGGING UTILITIES
# ============================================================================

def log_event(event_type: str, data: dict) -> None:
    """Log an event to JSONL file"""
    log_entry = {
        "timestamp": datetime.now(UTC).isoformat().replace('+00:00', 'Z'),
        "event_type": event_type,
        **data
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")


def calculate_cost(usage: dict) -> float:
    """
    Calculate cost in USD based on token usage.

    gpt-4o-mini pricing (as of 2024):
    - Input: $0.150 per 1M tokens
    - Output: $0.600 per 1M tokens
    """
    input_tokens = usage.get("prompt_tokens", 0)
    output_tokens = usage.get("completion_tokens", 0)

    input_cost = (input_tokens / 1_000_000) * 0.150
    output_cost = (output_tokens / 1_000_000) * 0.600

    return input_cost + output_cost


# ============================================================================
# AGENT LOOP
# ============================================================================

def run_agent(user_query: str, max_iterations: int = MAX_ITERATIONS):
    """
    Run the multi-tool agent with dynamic tool dispatch.

    Args:
        user_query: The user's question or request
        max_iterations: Maximum number of agent loop iterations
    """
    print(f"\n{'='*60}")
    print(f"USER: {user_query}")
    print(f"{'='*60}\n")

    # Initialize conversation history
    messages = [
        {"role": "system", "content": "You are a helpful assistant with access to tools. Use them when needed to answer user questions."},
        {"role": "user", "content": user_query}
    ]

    iteration = 0
    total_cost = 0.0

    while iteration < max_iterations:
        iteration += 1
        print(f"[Iteration {iteration}]")

        # Call OpenAI with available tools
        start_time = time.time()
        response = client.chat.completions.create(
            model=MODEL,
            messages=cast(Any, messages),  # Cast for type checker (educational code uses dicts)
            tools=tool_registry.get_schemas(),
            temperature=TEMPERATURE
        )
        llm_latency_ms = (time.time() - start_time) * 1000

        # Calculate cost for this call
        usage = response.usage.model_dump() if response.usage else {}
        call_cost = calculate_cost(usage)
        total_cost += call_cost

        # Log LLM call
        log_event("llm_call", {
            "iteration": iteration,
            "input_tokens": usage["prompt_tokens"],
            "output_tokens": usage["completion_tokens"],
            "latency_ms": round(llm_latency_ms, 2),
            "cost_usd": round(call_cost, 6)
        })

        message = response.choices[0].message

        # Check if assistant wants to use tools
        if message.tool_calls:
            print(f"  🔧 Agent wants to use {len(message.tool_calls)} tool(s)")

            # Add assistant message to history
            messages.append(cast(Any, {
                "role": "assistant",
                "content": message.content,
                "tool_calls": [tc.model_dump() for tc in message.tool_calls]
            }))

            # Execute each tool call
            for tool_call in message.tool_calls:
                # Safely access function attribute (type checker friendly)
                function = getattr(tool_call, 'function', None)
                if not function:
                    continue

                tool_name = function.name
                tool_args = json.loads(function.arguments)

                print(f"     → Calling {tool_name} with {tool_args}")

                # Execute tool via registry
                # 👉 This ONE line replaces the entire if/elif dispatch from Module 1!
                success, result, tool_latency_ms = tool_registry.execute(tool_name, tool_args)

                # Log tool execution
                log_event("tool_call", {
                    "iteration": iteration,
                    "tool_name": tool_name,
                    "arguments": tool_args,
                    "success": success,
                    "latency_ms": round(tool_latency_ms, 2),
                    "result_preview": result[:100]
                })

                print(f"     ✓ Result: {result[:100]}..." if len(result) > 100 else f"     ✓ Result: {result}")

                # Add tool result to messages
                messages.append(cast(Any, {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                }))

            # Continue loop to get final response
            continue

        # No tool calls - agent has final answer
        print(f"\n{'='*60}")
        print(f"ASSISTANT: {message.content}")
        print(f"{'='*60}")
        print(f"\n📊 Total cost: ${total_cost:.6f}")
        print(f"📊 Total iterations: {iteration}")

        # Log completion
        log_event("completion", {
            "iterations": iteration,
            "total_cost_usd": round(total_cost, 6),
            "final_response": message.content
        })

        break

    if iteration >= max_iterations:
        print(f"\n⚠️  Reached max iterations ({max_iterations})")


# ============================================================================
# MAIN - Example Usage
# ============================================================================

if __name__ == "__main__":
    # Example 1: Using calculator
    run_agent("What is 42 * 137?")

    print("\n" + "="*60 + "\n")

    # Example 2: File operations
    run_agent("Write 'Hello from Module 3!' to a file called test.txt, then read it back to verify")

    print("\n" + "="*60 + "\n")

    # Example 3: HTTP fetch (using a simple API)
    run_agent("Fetch the content from https://api.github.com/zen and tell me what it says")
