#!/usr/bin/env python3
"""
Module 3: Comparison Example - Module 1 vs Module 3
====================================================
This file shows the SAME weather tool implemented TWO ways:
1. Module 1 way (manual JSON, static list, if/elif dispatch)
2. Module 3 way (Pydantic, dynamic registry, clean dispatch)

Purpose: Help you see exactly what changed and why it's better.

Run this file to see both approaches working side-by-side!
"""

import os
from typing import cast, Any
from openai import OpenAI
from pydantic import BaseModel, Field

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-4o-mini"

print("="*80)
print("COMPARISON: Module 1 vs Module 3 - Same Tool, Different Approaches")
print("="*80)

# ============================================================================
# MODULE 1 APPROACH (From simple_agent.py)
# ============================================================================

print("\n" + "="*80)
print("MODULE 1 APPROACH - Static, Manual JSON")
print("="*80 + "\n")

# STEP 1: Define the tool function (same in both modules)
def get_weather_v1(city: str, units: str = "fahrenheit") -> str:
    """
    Get weather for a city (mock data for learning).

    THIS IS EXACTLY THE SAME as Module 1!
    """
    mock_weather = {
        "seattle": {"temp": 72, "condition": "Sunny"},
        "new york": {"temp": 68, "condition": "Cloudy"},
    }

    weather = mock_weather.get(city.lower(), {"temp": 70, "condition": "Unknown"})
    temp = weather["temp"]

    if units == "celsius":
        temp = round((temp - 32) * 5/9)
        unit_symbol = "°C"
    else:
        unit_symbol = "°F"

    return f"{temp}{unit_symbol}, {weather['condition']}"


# STEP 2: Define the JSON schema MANUALLY (Module 1 way)
# 👉 This is what you did in Module 1 - you wrote JSON by hand
WEATHER_TOOL_V1 = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current weather for a city",
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

# STEP 3: Create a static tool list (Module 1 way)
# 👉 In Module 1, you manually added tools to this list
AVAILABLE_TOOLS_V1 = [WEATHER_TOOL_V1]

print("✓ Manual JSON schema defined")
print("✓ Added to static AVAILABLE_TOOLS list")
print("✓ Function defined separately\n")

# STEP 4: Call OpenAI with the tool (Module 1 way)
print("Calling OpenAI with: 'What's the weather in Seattle?'\n")

response_v1 = client.chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": "What's the weather in Seattle?"}],
    tools=cast(Any, AVAILABLE_TOOLS_V1)  # 👈 Pass our static list (cast for type checker)
)

# Get the tool call (we know it exists for this example)
tool_calls_v1 = response_v1.choices[0].message.tool_calls
if tool_calls_v1 and len(tool_calls_v1) > 0:  # Type checker safety
    tool_call = tool_calls_v1[0]
    # Use getattr to safely access function attribute (type checker friendly)
    function = getattr(tool_call, 'function', None)
    if function:
        tool_name = function.name
        tool_args_str = function.arguments
        print(f"OpenAI wants to call: {tool_name}")
        print(f"With arguments: {tool_args_str}\n")

        # STEP 5: Dispatch with if/elif (Module 1 way)
        # 👉 In Module 1, you had to write if/elif for each tool
        import json
        args = json.loads(tool_args_str)

        # This is how you dispatched in Module 1:
        if tool_name == "get_weather":
            result = get_weather_v1(**args)  # 👈 Manual dispatch
        # elif tool_name == "get_stock":  # If you added more tools
        #     result = get_stock(**args)
        # elif tool_name == "send_email":
        #     result = send_email(**args)
        # ... etc - this grows with every tool!
        print(f"Result: {result}\n")
    else:
        raise RuntimeError("Tool call missing function attribute")
else:
    raise RuntimeError("Expected tool call but got none")

print("📝 PROBLEMS WITH MODULE 1 APPROACH:")
print("  ❌ Wrote JSON schema by hand (error-prone)")
print("  ❌ Had to maintain TWO things: JSON schema + function")
print("  ❌ No validation (what if LLM sends wrong types?)")
print("  ❌ if/elif dispatch grows with every tool")
print("  ❌ Easy to forget to add tool to AVAILABLE_TOOLS list")


# ============================================================================
# MODULE 3 APPROACH (With Pydantic + Registry)
# ============================================================================

print("\n" + "="*80)
print("MODULE 3 APPROACH - Pydantic + Dynamic Registry")
print("="*80 + "\n")

# STEP 1: Define the Pydantic schema (replaces manual JSON)
# 👉 THIS IS NEW! Instead of writing JSON, we write a Python class
class WeatherInput(BaseModel):
    """
    Pydantic schema for weather tool.

    THIS REPLACES the manual JSON from Module 1!
    Pydantic will auto-generate the JSON schema for us.
    """
    city: str = Field(description="City name (e.g., 'Seattle', 'New York')")
    units: str = Field(default="fahrenheit", description="Temperature units")

print("✓ Pydantic schema defined (WeatherInput class)")
print("  👉 This REPLACES the manual JSON from Module 1")
print("  👉 Pydantic auto-generates the JSON schema\n")


# STEP 2: Create a simple ToolRegistry (Module 3 way)
# 👉 THIS IS NEW! The registry handles tool storage and dispatch
class SimpleToolRegistry:
    """
    Simple tool registry (simplified for this comparison).

    THIS REPLACES:
    - The AVAILABLE_TOOLS list from Module 1
    - The if/elif dispatch from Module 1

    How it works:
    - Tools register themselves with @register decorator
    - Registry generates schemas automatically from Pydantic
    - Registry dispatches by name (no if/elif needed!)
    """

    def __init__(self):
        self._tools = {}  # 👈 Store tools in a dictionary

    def register(self, name: str, schema_model: type[BaseModel]):
        """
        Decorator to register a tool.

        THIS REPLACES manually adding to AVAILABLE_TOOLS!
        """
        def decorator(func):
            # Generate OpenAI schema from Pydantic (automatic!)
            properties = {}
            required = []

            for field_name, field_info in schema_model.model_fields.items():
                properties[field_name] = {
                    "type": "string",
                    "description": field_info.description or ""
                }
                if field_info.is_required():
                    required.append(field_name)

            # 👉 This is the SAME JSON structure as Module 1,
            #    but we GENERATED it from Pydantic!
            openai_schema = {
                "type": "function",
                "function": {
                    "name": name,
                    "description": func.__doc__ or "No description",
                    "parameters": {
                        "type": "object",
                        "properties": properties,
                        "required": required
                    }
                }
            }

            # Store the tool
            self._tools[name] = {
                "func": func,
                "schema": openai_schema,
                "model": schema_model
            }

            return func
        return decorator

    def get_schemas(self):
        """
        Get all tool schemas for OpenAI.

        THIS REPLACES the AVAILABLE_TOOLS list from Module 1!
        """
        return [tool["schema"] for tool in self._tools.values()]

    def execute(self, tool_name: str, arguments: dict):
        """
        Execute a tool by name.

        THIS REPLACES the if/elif dispatch from Module 1!
        """
        # Look up the tool (no if/elif needed!)
        if tool_name not in self._tools:
            raise ValueError(f"Tool '{tool_name}' not found in registry")

        tool = self._tools[tool_name]

        # Validate with Pydantic (automatic type checking!)
        validated = tool["model"](**arguments)

        # Call the function
        result = tool["func"](**validated.model_dump())

        return result


# Create the registry
tool_registry = SimpleToolRegistry()

print("✓ ToolRegistry created")
print("  👉 This REPLACES AVAILABLE_TOOLS + if/elif dispatch\n")


# STEP 3: Register the tool with a decorator (Module 3 way)
# 👉 THIS IS NEW! The @decorator automatically registers the tool
@tool_registry.register("get_weather", WeatherInput)
def get_weather(city: str, units: str = "fahrenheit") -> str:
    """
    Get current weather for a city.

    NOTICE: This is the SAME function as Module 1!
    The only difference is the @decorator above it.

    The decorator does ALL this for you:
    1. Generates the JSON schema from WeatherInput
    2. Adds it to the registry (no AVAILABLE_TOOLS list!)
    3. Sets up validation
    4. Makes it available for dispatch
    """
    # Same implementation as Module 1
    mock_weather = {
        "seattle": {"temp": 72, "condition": "Sunny"},
        "new york": {"temp": 68, "condition": "Cloudy"},
    }

    weather = mock_weather.get(city.lower(), {"temp": 70, "condition": "Unknown"})
    temp = weather["temp"]

    if units == "celsius":
        temp = round((temp - 32) * 5/9)
        unit_symbol = "°C"
    else:
        unit_symbol = "°F"

    return f"{temp}{unit_symbol}, {weather['condition']}"

print("✓ Tool registered with @tool_registry.register decorator")
print("  👉 This ONE LINE replaces 3 manual steps from Module 1:")
print("     1. Writing JSON schema by hand")
print("     2. Adding to AVAILABLE_TOOLS list")
print("     3. Adding if/elif dispatch code\n")


# STEP 4: Call OpenAI (same as Module 1, but with registry)
print("Calling OpenAI with: 'What's the weather in Seattle?'\n")

response_v3 = client.chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": "What's the weather in Seattle?"}],
    tools=tool_registry.get_schemas()  # 👈 Get schemas from registry
)

# Get the tool call (we know it exists for this example)
tool_calls_v3 = response_v3.choices[0].message.tool_calls
if tool_calls_v3 and len(tool_calls_v3) > 0:  # Type checker safety
    tool_call_v3 = tool_calls_v3[0]
    # Use getattr to safely access function attribute (type checker friendly)
    function_v3 = getattr(tool_call_v3, 'function', None)
    if function_v3:
        tool_name_v3 = function_v3.name
        tool_args_str_v3 = function_v3.arguments
        print(f"OpenAI wants to call: {tool_name_v3}")
        print(f"With arguments: {tool_args_str_v3}\n")

        # STEP 5: Dispatch with registry (Module 3 way)
        # 👉 THIS IS DIFFERENT! No if/elif needed!
        args = json.loads(tool_args_str_v3)

        # This is how you dispatch in Module 3:
        result = tool_registry.execute(tool_name_v3, args)  # 👈 One line!

        print(f"Result: {result}\n")
    else:
        raise RuntimeError("Tool call missing function attribute")
else:
    raise RuntimeError("Expected tool call but got none")

print("✅ BENEFITS OF MODULE 3 APPROACH:")
print("  ✅ Pydantic auto-generates JSON schema (no typos!)")
print("  ✅ Single source of truth (define once)")
print("  ✅ Automatic validation (Pydantic checks types)")
print("  ✅ One-line dispatch (no if/elif!)")
print("  ✅ Impossible to forget to register a tool")


# ============================================================================
# SIDE-BY-SIDE COMPARISON
# ============================================================================

print("\n" + "="*80)
print("SIDE-BY-SIDE: What Changed?")
print("="*80 + "\n")

print("📋 TO ADD A NEW TOOL:\n")

print("MODULE 1 (3 manual steps):")
print("-" * 40)
print("""
# Step 1: Write JSON schema by hand
NEW_TOOL = {
    "type": "function",
    "function": {
        "name": "get_stock",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {"type": "string"}
            },
            "required": ["symbol"]
        }
    }
}

# Step 2: Add to AVAILABLE_TOOLS (don't forget!)
AVAILABLE_TOOLS = [WEATHER_TOOL, NEW_TOOL]

# Step 3: Add if/elif dispatch (don't forget!)
if tool_name == "get_weather":
    result = get_weather(**args)
elif tool_name == "get_stock":  # 👈 New dispatch
    result = get_stock(**args)
""")

print("\nMODULE 3 (1 step - just define it):")
print("-" * 40)
print("""
# That's it! Just define the schema + function:
class StockInput(BaseModel):
    symbol: str = Field(description="Stock symbol")

@tool_registry.register("get_stock", StockInput)
def get_stock(symbol: str) -> str:
    return f"Stock price for {symbol}"

# 👉 Schema generated automatically ✓
# 👉 Added to registry automatically ✓
# 👉 Dispatch works automatically ✓
""")

print("\n" + "="*80)
print("📊 SCALABILITY: What happens with 10 tools?")
print("="*80 + "\n")

print("MODULE 1:")
print("-" * 40)
print("  • 10 manual JSON schemas (40+ lines each)")
print("  • 10 entries in AVAILABLE_TOOLS list")
print("  • 10 if/elif branches in dispatch")
print("  • Total: ~500 lines of boilerplate")
print("  • Easy to make mistakes and forget steps\n")

print("MODULE 3:")
print("-" * 40)
print("  • 10 Pydantic classes (5-10 lines each)")
print("  • 10 @register decorators (automatic)")
print("  • 0 if/elif branches (registry handles it)")
print("  • Total: ~100 lines of actual tool code")
print("  • Impossible to forget registration\n")

print("="*80)
print("🎯 KEY INSIGHT:")
print("="*80)
print("""
Module 1 approach works fine for 1-2 tools.
Module 3 approach is ESSENTIAL for 5+ tools.

The patterns you learn in Module 3 will:
- Scale to 100+ tools without growing complexity
- Catch errors before runtime (Pydantic validation)
- Make your code cleaner and easier to maintain
- Prepare you for Module 4 (multi-agent systems)

That's why we introduced Pydantic and registries!
""")

print("="*80)
print("✨ Run this file to see both approaches work identically!")
print("="*80)
