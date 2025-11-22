"""
Core agent loop and policy logic

This module will be implemented during Module 1.
It contains the fundamental agent control flow.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel


class AgentMessage(BaseModel):
    """Structured message in agent conversation"""
    role: str  # "system", "user", "assistant", "tool"
    content: str
    tool_calls: Optional[List[Dict[str, Any]]] = None
    tool_call_id: Optional[str] = None
    name: Optional[str] = None


class AgentState(BaseModel):
    """Agent execution state"""
    messages: List[AgentMessage] = []
    step_count: int = 0
    total_cost: float = 0.0
    done: bool = False
    result: Optional[Any] = None


# TODO: Implement in Module 1
# - AgentLoop class
# - run_step() method
# - termination logic
# - logging utilities
