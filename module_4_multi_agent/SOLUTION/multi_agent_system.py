#!/usr/bin/env python3
"""
Multi-Agent System: Planner → Worker → Critic Pattern

This module demonstrates coordinating multiple specialized agents to complete
complex tasks through role separation and intelligent escalation.

Architecture:
- Planner: Breaks down tasks into executable plans
- Worker: Executes plans and produces results
- Critic: Reviews work and provides feedback
- Orchestrator: Coordinates agents with budget gates

Design Decisions (from Phase 1 learning conversation):
- Deterministic orchestrator (Python rules, not LLM)
- Escalation pattern (Worker retry → Planner re-plan → Human)
- Budget gates focus on tokens (not dollars) - industry standard
- Simple retry for API errors, fail fast for validation
- History tracking prevents LLMs from repeating mistakes
"""

import os
import json
import time
from datetime import datetime, UTC
from typing import Dict, List, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Configuration
MODEL = "gpt-4o-mini"
MAX_ITERATIONS = 10
MAX_TOTAL_TOKENS = 50_000
LOG_FILE = "logs/multi_agent_system.jsonl"


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def calculate_cost(usage) -> float:
    """
    Calculate actual API cost from token usage.

    Note: We track cost for educational purposes (shows it's cheap!),
    but budget gates enforce TOKEN limits, not dollar limits.
    Industry reality: "expensive" = tokens/time, not money.
    """
    if not usage:
        return 0.0

    # GPT-4o-mini pricing (as of 2024)
    input_cost = (usage.prompt_tokens / 1_000_000) * 0.15
    output_cost = (usage.completion_tokens / 1_000_000) * 0.60
    return input_cost + output_cost


def log_event(event_type: str, data: Dict[str, Any]) -> None:
    """Log events to JSONL file for full observability."""
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    event = {
        "timestamp": datetime.now(UTC).isoformat(),
        "event_type": event_type,
        **data
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")


def format_history(history: List[Dict[str, Any]]) -> str:
    """
    Format history for LLM context.

    Critical: Without history, LLMs repeat the same mistakes!
    This gives agents memory of what was tried and what failed.
    """
    if not history:
        return "No previous attempts."

    formatted = []
    for i, entry in enumerate(history, 1):
        agent = entry.get("agent", "unknown")

        if agent == "worker":
            formatted.append(f"Attempt {entry['attempt']}:")
            formatted.append(f"  Output: {entry['output'][:200]}...")
        elif agent == "critic":
            formatted.append(f"  Critic Feedback: {entry['feedback']}")
            formatted.append(f"  Approved: {entry['approved']}")
        elif agent == "planner":
            formatted.append(f"Plan Version {entry['version']}:")
            formatted.append(f"  {entry['plan'][:200]}...")

    return "\n".join(formatted)


def call_llm_with_retry(messages: List[Dict[str, str]],
                        agent_name: str) -> Dict[str, Any]:
    """
    Call LLM with simple retry for transient errors.

    Error handling strategy (from Phase 1):
    - Retry once for rate limits (common, transient)
    - Raise for unexpected errors (fail fast with clear message)
    - Don't hide bugs with overly complex retry logic
    """
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.7
        )
        return response

    except Exception as e:
        # Check if it's a rate limit (common, worth retrying)
        if "rate" in str(e).lower() or "limit" in str(e).lower():
            print(f"⚠️  {agent_name}: Rate limited. Waiting 2s and retrying once...")
            time.sleep(2)

            # One retry
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                temperature=0.7
            )
            return response
        else:
            # Unexpected error - fail fast
            print(f"❌ {agent_name}: API Error: {e}")
            raise


# ============================================================================
# AGENT IMPLEMENTATIONS
# ============================================================================

def planner_agent(shared_state: Dict[str, Any]) -> int:
    """
    Planner Agent: Breaks down complex tasks into executable plans.

    Responsibilities:
    - Analyze the task requirements
    - Create a step-by-step execution plan
    - Consider previous failures (if re-planning)

    Returns: tokens used
    """
    task = shared_state["task"]
    plan_version = shared_state["plan_version"]
    history = shared_state.get("history", [])

    # Build prompt with context
    system_prompt = """You are a Planner agent. Your job is to break down complex tasks into clear, executable step-by-step plans.

Create a detailed plan that a Worker agent can follow. Be specific about what needs to be done at each step.

Return ONLY the plan as a numbered list. Example:
1. First step description
2. Second step description
3. Third step description"""

    user_prompt = f"""TASK:
{task}

"""

    # If re-planning after failure, include context
    if plan_version > 0:
        user_prompt += f"""PREVIOUS PLAN FAILED. History:
{format_history(history)}

Create an IMPROVED plan that addresses the issues in previous attempts.

"""

    user_prompt += "Create the execution plan:"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    # Call LLM
    print(f"\n{'='*60}")
    print(f"🎯 PLANNER (Version {plan_version + 1}): Creating execution plan...")
    print(f"{'='*60}")

    response = call_llm_with_retry(messages, "Planner")
    plan = response.choices[0].message.content
    tokens_used = response.usage.total_tokens
    cost = calculate_cost(response.usage)

    # Update shared state
    shared_state["plan"] = plan
    shared_state["plan_version"] += 1

    # Add to history
    shared_state["history"].append({
        "agent": "planner",
        "version": shared_state["plan_version"],
        "plan": plan,
        "timestamp": datetime.now(UTC).isoformat()
    })

    # Log event
    log_event("planner_call", {
        "plan_version": shared_state["plan_version"],
        "plan": plan,
        "tokens": tokens_used,
        "cost": cost
    })

    print(f"\n📋 Plan Created:\n{plan}")
    print(f"\n💰 Tokens: {tokens_used} | Cost: ${cost:.6f}")

    return tokens_used


def worker_agent(shared_state: Dict[str, Any]) -> int:
    """
    Worker Agent: Executes the plan and produces results.

    Responsibilities:
    - Execute ALL steps in the plan
    - Review previous attempts to avoid repeating mistakes
    - Address feedback from Critic if revising

    Returns: tokens used
    """
    task = shared_state["task"]
    plan = shared_state["plan"]
    attempt = shared_state["worker_attempts"] + 1
    history = shared_state.get("history", [])
    critic_feedback = shared_state.get("critic_feedback")

    # Validate we have a plan
    if not plan:
        raise ValueError("Worker called without a plan! Planner must run first.")

    # Build prompt with context
    system_prompt = """You are a Worker agent. Your job is to execute the given plan and produce the requested output.

Execute ALL steps in the plan. Be thorough and complete. Produce the final deliverable.

If you're revising based on feedback, address ALL the issues mentioned."""

    user_prompt = f"""ORIGINAL TASK:
{task}

EXECUTION PLAN:
{plan}

"""

    # If this is a revision, include previous attempts and feedback
    if attempt > 1:
        user_prompt += f"""PREVIOUS ATTEMPTS AND FEEDBACK:
{format_history(history)}

LATEST CRITIC FEEDBACK:
{critic_feedback}

Create an IMPROVED version that addresses all feedback.

"""

    user_prompt += "Execute the plan and produce the complete result:"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    # Call LLM
    print(f"\n{'='*60}")
    print(f"🔨 WORKER (Attempt {attempt}): Executing plan...")
    print(f"{'='*60}")

    response = call_llm_with_retry(messages, "Worker")
    result = response.choices[0].message.content
    tokens_used = response.usage.total_tokens
    cost = calculate_cost(response.usage)

    # Update shared state
    shared_state["result"] = result
    shared_state["worker_attempts"] += 1

    # Add to history
    shared_state["history"].append({
        "agent": "worker",
        "attempt": attempt,
        "output": result,
        "timestamp": datetime.now(UTC).isoformat()
    })

    # Log event
    log_event("worker_call", {
        "attempt": attempt,
        "result_length": len(result),
        "tokens": tokens_used,
        "cost": cost
    })

    print(f"\n✅ Work Completed (Attempt {attempt})")
    print(f"📄 Result: {result[:200]}...")
    print(f"\n💰 Tokens: {tokens_used} | Cost: ${cost:.6f}")

    return tokens_used


def critic_agent(shared_state: Dict[str, Any]) -> int:
    """
    Critic Agent: Reviews work and provides actionable feedback.

    Responsibilities:
    - Compare result against original requirements
    - Provide specific, actionable feedback
    - Decide: approve or request revision

    Returns: tokens used
    """
    task = shared_state["task"]
    result = shared_state["result"]

    # Validate we have a result to review
    if not result:
        raise ValueError("Critic called without Worker output! Worker must run first.")

    # Build prompt
    system_prompt = """You are a Critic agent. Your job is to review the Worker's output against the original task requirements.

Provide honest, constructive feedback. Be specific about what needs improvement.

Return your review in this exact format:

APPROVED: [YES or NO]
FEEDBACK: [Specific feedback on what's good and what needs improvement]

If approving, explain why it meets requirements.
If rejecting, be specific about what needs to be fixed."""

    user_prompt = f"""ORIGINAL TASK:
{task}

WORKER'S OUTPUT:
{result}

Review the output and provide your assessment:"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    # Call LLM
    print(f"\n{'='*60}")
    print(f"🔍 CRITIC: Reviewing work...")
    print(f"{'='*60}")

    response = call_llm_with_retry(messages, "Critic")
    review = response.choices[0].message.content
    tokens_used = response.usage.total_tokens
    cost = calculate_cost(response.usage)

    # Parse approval
    approved = "APPROVED: YES" in review.upper()

    # Update shared state
    shared_state["critic_approved"] = approved
    shared_state["critic_feedback"] = review

    # Add to history
    shared_state["history"].append({
        "agent": "critic",
        "attempt": shared_state["worker_attempts"],
        "feedback": review,
        "approved": approved,
        "timestamp": datetime.now(UTC).isoformat()
    })

    # Log event
    log_event("critic_call", {
        "approved": approved,
        "feedback": review,
        "tokens": tokens_used,
        "cost": cost
    })

    if approved:
        print(f"\n✅ APPROVED!")
    else:
        print(f"\n❌ REVISION NEEDED")

    print(f"\n📝 Feedback:\n{review}")
    print(f"\n💰 Tokens: {tokens_used} | Cost: ${cost:.6f}")

    return tokens_used


# ============================================================================
# ORCHESTRATOR
# ============================================================================

def orchestrator(task: str, max_iterations: int = MAX_ITERATIONS,
                max_tokens: int = MAX_TOTAL_TOKENS) -> Optional[str]:
    """
    Orchestrator: Coordinates all agents with budget gates and escalation.

    Orchestration Strategy (from Phase 1 design):
    - Deterministic Python rules (not LLM) for predictable flow
    - Escalation pattern: Worker retry → Planner re-plan → Give up
    - Budget gates: max iterations AND max tokens
    - Success condition: Critic approves

    Returns: Final approved result, or None if failed
    """
    print("\n" + "="*60)
    print("🚀 MULTI-AGENT SYSTEM STARTING")
    print("="*60)
    print(f"Task: {task}")
    print(f"Budget Gates: {max_iterations} iterations, {max_tokens:,} tokens")
    print("="*60)

    # Initialize shared state
    shared_state = {
        # Input
        "task": task,

        # Planner output
        "plan": None,
        "plan_version": 0,

        # Worker output
        "result": None,
        "worker_attempts": 0,

        # Critic output
        "critic_approved": False,
        "critic_feedback": None,

        # History (prevents LLMs from repeating mistakes!)
        "history": [],

        # Metadata
        "total_tokens": 0,
        "iteration": 0,
        "status": "in_progress"
    }

    # Log start
    log_event("orchestrator_start", {
        "task": task,
        "max_iterations": max_iterations,
        "max_tokens": max_tokens
    })

    # Step 1: Initial planning
    tokens = planner_agent(shared_state)
    shared_state["total_tokens"] += tokens

    # Main orchestration loop
    while shared_state["iteration"] < max_iterations:
        shared_state["iteration"] += 1
        iteration = shared_state["iteration"]

        print(f"\n{'='*60}")
        print(f"📊 ITERATION {iteration}/{max_iterations}")
        print(f"💰 Tokens Used: {shared_state['total_tokens']:,}/{max_tokens:,}")
        print(f"{'='*60}")

        # Budget gate: Check token limit
        if shared_state["total_tokens"] >= max_tokens:
            print(f"\n❌ FAILED: Token budget exhausted ({shared_state['total_tokens']:,} tokens)")
            shared_state["status"] = "failed_budget"
            log_event("orchestrator_end", {
                "status": "failed_budget",
                "total_tokens": shared_state["total_tokens"],
                "iterations": iteration
            })
            return None

        # Token warning at 80%
        if shared_state["total_tokens"] >= max_tokens * 0.8:
            print(f"⚠️  WARNING: 80% of token budget used!")

        # Step 2: Worker executes
        tokens = worker_agent(shared_state)
        shared_state["total_tokens"] += tokens

        # Step 3: Critic reviews
        tokens = critic_agent(shared_state)
        shared_state["total_tokens"] += tokens

        # Step 4: Decision point - SUCCESS GATE
        if shared_state["critic_approved"]:
            print(f"\n{'='*60}")
            print(f"✅ SUCCESS!")
            print(f"{'='*60}")
            print(f"Completed in {iteration} iterations")
            print(f"Total tokens: {shared_state['total_tokens']:,}")
            print(f"Total cost: ${sum(calculate_cost(entry.get('usage')) for entry in shared_state.get('history', []) if 'usage' in entry):.4f}")

            shared_state["status"] = "completed"
            log_event("orchestrator_end", {
                "status": "completed",
                "total_tokens": shared_state["total_tokens"],
                "iterations": iteration
            })

            return shared_state["result"]

        # Step 5: Escalation logic
        worker_attempts = shared_state["worker_attempts"]

        if worker_attempts == 1:
            # First rejection: Let Worker revise
            print(f"\n💡 Strategy: Worker will revise based on feedback")

        elif worker_attempts == 2:
            # Second rejection: Escalate to Planner
            print(f"\n⬆️  ESCALATING TO PLANNER: Creating new plan...")
            tokens = planner_agent(shared_state)
            shared_state["total_tokens"] += tokens
            # Reset worker attempts for new plan
            shared_state["worker_attempts"] = 0

        elif worker_attempts >= 3:
            # Third+ rejection: Give up
            print(f"\n❌ FAILED: Max revision attempts reached")
            print(f"Even after re-planning, quality standards not met.")
            print(f"Human intervention recommended.")

            shared_state["status"] = "failed_quality"
            log_event("orchestrator_end", {
                "status": "failed_quality",
                "total_tokens": shared_state["total_tokens"],
                "iterations": iteration
            })
            return None

    # If we exit loop: hit max iterations
    print(f"\n❌ FAILED: Max iterations reached ({max_iterations})")
    shared_state["status"] = "failed_iterations"
    log_event("orchestrator_end", {
        "status": "failed_iterations",
        "total_tokens": shared_state["total_tokens"],
        "iterations": max_iterations
    })

    return None


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Example task
    task = "Write a 300-word blog post about why multi-agent systems are useful in production. Include specific examples of when to use them vs single agents."

    # Run the multi-agent system
    result = orchestrator(task)

    if result:
        print(f"\n{'='*60}")
        print("📄 FINAL APPROVED OUTPUT")
        print(f"{'='*60}")
        print(result)
        print(f"\n✅ Check logs at: {LOG_FILE}")
    else:
        print(f"\n❌ Task failed. Check logs at: {LOG_FILE}")
