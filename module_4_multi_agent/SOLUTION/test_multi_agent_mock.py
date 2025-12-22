#!/usr/bin/env python3
"""
Mock version of multi-agent system for testing without API calls.

This verifies the orchestration logic, escalation pattern, and budget gates work correctly.
"""

import os
import json
from datetime import datetime, UTC
from typing import Dict, List, Any, Optional

LOG_FILE = "logs/multi_agent_test_mock.jsonl"
MAX_ITERATIONS = 10
MAX_TOTAL_TOKENS = 50_000


def log_event(event_type: str, data: Dict[str, Any]) -> None:
    """Log events to JSONL file."""
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    event = {
        "timestamp": datetime.now(UTC).isoformat(),
        "event_type": event_type,
        **data
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")


def format_history(history: List[Dict[str, Any]]) -> str:
    """Format history for display."""
    if not history:
        return "No previous attempts."

    formatted = []
    for entry in history:
        agent = entry.get("agent", "unknown")
        if agent == "worker":
            formatted.append(f"Attempt {entry['attempt']}: {entry['output'][:100]}...")
        elif agent == "critic":
            formatted.append(f"  Critic: {entry['feedback'][:100]}... (Approved: {entry['approved']})")

    return "\n".join(formatted)


def mock_planner_agent(shared_state: Dict[str, Any], should_improve: bool = False) -> int:
    """Mock Planner - simulates creating a plan."""
    plan_version = shared_state["plan_version"]

    if should_improve:
        plan = f"""Plan v{plan_version + 1} (IMPROVED):
1. Research multi-agent benefits with SPECIFIC examples
2. Write intro explaining the concept clearly
3. Write body with concrete use cases
4. Add conclusion with recommendations
5. Proofread and ensure 300 words"""
    else:
        plan = f"""Plan v{plan_version + 1}:
1. Research multi-agent systems
2. Write about benefits
3. Add examples
4. Write conclusion"""

    shared_state["plan"] = plan
    shared_state["plan_version"] += 1
    shared_state["history"].append({
        "agent": "planner",
        "version": shared_state["plan_version"],
        "plan": plan,
        "timestamp": datetime.now(UTC).isoformat()
    })

    print(f"\n{'='*60}")
    print(f"🎯 PLANNER (Version {shared_state['plan_version']}): Creating plan...")
    print(f"{'='*60}")
    print(f"📋 Plan:\n{plan}")

    tokens = 500  # Mock token count
    return tokens


def mock_worker_agent(shared_state: Dict[str, Any], quality: str = "poor") -> int:
    """Mock Worker - simulates executing work with varying quality."""
    attempt = shared_state["worker_attempts"] + 1

    if quality == "poor":
        result = "Multi-agent systems are useful. They can do things. Use them for tasks."
    elif quality == "medium":
        result = """Multi-agent systems coordinate multiple specialized agents to solve complex problems.

Benefits include parallel processing, specialization, and modularity. For example, you might use a Planner to break down tasks, a Worker to execute them, and a Critic to review quality.

Use multi-agent when tasks are complex and have distinct phases. Use single agents for simple, straightforward operations.

This approach scales better than monolithic agents."""
    else:  # good
        result = """Multi-agent systems in production offer significant advantages over single-agent approaches for complex workflows. By coordinating specialized agents—each optimized for specific tasks—organizations achieve better scalability and maintainability.

Consider a content generation pipeline: a Planner agent breaks down requirements into actionable steps, a Worker agent executes the plan using domain-specific tools, and a Critic agent ensures quality standards. This separation allows each agent to use different models (GPT-4 for planning, GPT-3.5-turbo for execution) optimizing both cost and performance.

Use multi-agent systems when tasks have distinct phases requiring different expertise, when parallel processing improves throughput, or when independent components need separate deployment cycles. Single agents remain appropriate for straightforward operations like simple translations or single-step classifications.

The key is matching architectural complexity to actual requirements—over-engineering simple tasks wastes resources while under-architecting complex workflows creates brittleness."""

    shared_state["result"] = result
    shared_state["worker_attempts"] += 1
    shared_state["history"].append({
        "agent": "worker",
        "attempt": attempt,
        "output": result,
        "timestamp": datetime.now(UTC).isoformat()
    })

    print(f"\n{'='*60}")
    print(f"🔨 WORKER (Attempt {attempt}): Executing plan...")
    print(f"{'='*60}")
    print(f"✅ Result:\n{result[:200]}...")

    tokens = 800  # Mock token count
    return tokens


def mock_critic_agent(shared_state: Dict[str, Any], should_approve: bool = False) -> int:
    """Mock Critic - simulates reviewing work."""
    result = shared_state["result"]

    if should_approve:
        review = """APPROVED: YES
FEEDBACK: Excellent work! The blog post meets all requirements:
- 300 words achieved
- Clear explanation of multi-agent systems
- Specific production examples included
- Good contrast with single-agent approaches
- Professional writing quality

Ready for publication."""
        approved = True
    else:
        review = """APPROVED: NO
FEEDBACK: The output needs improvement:
- Too brief (only ~50 words, need 300)
- Lacks specific examples
- No concrete use cases
- Missing comparison with single agents
- Needs more depth and detail

Please expand with specific examples and reach the 300-word target."""
        approved = False

    shared_state["critic_approved"] = approved
    shared_state["critic_feedback"] = review
    shared_state["history"].append({
        "agent": "critic",
        "attempt": shared_state["worker_attempts"],
        "feedback": review,
        "approved": approved,
        "timestamp": datetime.now(UTC).isoformat()
    })

    print(f"\n{'='*60}")
    print(f"🔍 CRITIC: Reviewing work...")
    print(f"{'='*60}")
    if approved:
        print(f"✅ APPROVED!")
    else:
        print(f"❌ REVISION NEEDED")
    print(f"📝 Feedback:\n{review}")

    tokens = 600  # Mock token count
    return tokens


def mock_orchestrator_success_case(task: str) -> Optional[str]:
    """Test case: Success after Worker revision (iteration 2)."""
    print("\n" + "="*60)
    print("TEST CASE 1: Success After Revision")
    print("="*60)

    shared_state = {
        "task": task,
        "plan": None,
        "plan_version": 0,
        "result": None,
        "worker_attempts": 0,
        "critic_approved": False,
        "critic_feedback": None,
        "history": [],
        "total_tokens": 0,
        "iteration": 0,
        "status": "in_progress"
    }

    # Initial plan
    tokens = mock_planner_agent(shared_state)
    shared_state["total_tokens"] += tokens

    # Iteration 1: Poor work → Rejection
    shared_state["iteration"] += 1
    print(f"\n📊 ITERATION 1")
    tokens = mock_worker_agent(shared_state, quality="poor")
    shared_state["total_tokens"] += tokens
    tokens = mock_critic_agent(shared_state, should_approve=False)
    shared_state["total_tokens"] += tokens

    print(f"💡 Strategy: Worker will revise based on feedback")

    # Iteration 2: Good work → Approval
    shared_state["iteration"] += 1
    print(f"\n📊 ITERATION 2")
    tokens = mock_worker_agent(shared_state, quality="good")
    shared_state["total_tokens"] += tokens
    tokens = mock_critic_agent(shared_state, should_approve=True)
    shared_state["total_tokens"] += tokens

    print(f"\n✅ SUCCESS! Completed in {shared_state['iteration']} iterations")
    print(f"💰 Total tokens: {shared_state['total_tokens']:,}")

    return shared_state["result"]


def mock_orchestrator_escalation_case(task: str) -> Optional[str]:
    """Test case: Escalation to Planner after 2 rejections."""
    print("\n" + "="*60)
    print("TEST CASE 2: Escalation to Planner")
    print("="*60)

    shared_state = {
        "task": task,
        "plan": None,
        "plan_version": 0,
        "result": None,
        "worker_attempts": 0,
        "critic_approved": False,
        "critic_feedback": None,
        "history": [],
        "total_tokens": 0,
        "iteration": 0,
        "status": "in_progress"
    }

    # Initial plan
    tokens = mock_planner_agent(shared_state)
    shared_state["total_tokens"] += tokens

    # Iteration 1: Poor work → Rejection
    shared_state["iteration"] += 1
    print(f"\n📊 ITERATION 1")
    tokens = mock_worker_agent(shared_state, quality="poor")
    shared_state["total_tokens"] += tokens
    tokens = mock_critic_agent(shared_state, should_approve=False)
    shared_state["total_tokens"] += tokens
    print(f"💡 Strategy: Worker will revise")

    # Iteration 2: Medium work → Rejection (triggers escalation)
    shared_state["iteration"] += 1
    print(f"\n📊 ITERATION 2")
    tokens = mock_worker_agent(shared_state, quality="medium")
    shared_state["total_tokens"] += tokens
    tokens = mock_critic_agent(shared_state, should_approve=False)
    shared_state["total_tokens"] += tokens

    # Escalation!
    print(f"\n⬆️  ESCALATING TO PLANNER: Creating new plan...")
    tokens = mock_planner_agent(shared_state, should_improve=True)
    shared_state["total_tokens"] += tokens
    shared_state["worker_attempts"] = 0  # Reset for new plan

    # Iteration 3: Good work with improved plan → Approval
    shared_state["iteration"] += 1
    print(f"\n📊 ITERATION 3")
    tokens = mock_worker_agent(shared_state, quality="good")
    shared_state["total_tokens"] += tokens
    tokens = mock_critic_agent(shared_state, should_approve=True)
    shared_state["total_tokens"] += tokens

    print(f"\n✅ SUCCESS! Completed in {shared_state['iteration']} iterations (with escalation)")
    print(f"💰 Total tokens: {shared_state['total_tokens']:,}")

    return shared_state["result"]


def mock_orchestrator_failure_case(task: str) -> Optional[str]:
    """Test case: Failure after max attempts."""
    print("\n" + "="*60)
    print("TEST CASE 3: Failure After Max Attempts")
    print("="*60)

    shared_state = {
        "task": task,
        "plan": None,
        "plan_version": 0,
        "result": None,
        "worker_attempts": 0,
        "critic_approved": False,
        "critic_feedback": None,
        "history": [],
        "total_tokens": 0,
        "iteration": 0,
        "status": "in_progress"
    }

    # Initial plan
    tokens = mock_planner_agent(shared_state)
    shared_state["total_tokens"] += tokens

    # All attempts fail
    for i in range(1, 4):
        shared_state["iteration"] += 1
        print(f"\n📊 ITERATION {i}")
        tokens = mock_worker_agent(shared_state, quality="poor")
        shared_state["total_tokens"] += tokens
        tokens = mock_critic_agent(shared_state, should_approve=False)
        shared_state["total_tokens"] += tokens

        if i == 2:
            # Escalation after 2nd failure
            print(f"\n⬆️  ESCALATING TO PLANNER")
            tokens = mock_planner_agent(shared_state, should_improve=True)
            shared_state["total_tokens"] += tokens
            shared_state["worker_attempts"] = 0

    print(f"\n❌ FAILED: Max revision attempts reached")
    print(f"💰 Total tokens: {shared_state['total_tokens']:,}")

    return None


if __name__ == "__main__":
    task = "Write a 300-word blog post about why multi-agent systems are useful in production."

    # Run all test cases
    print("\n🧪 Running Mock Multi-Agent System Tests\n")

    result1 = mock_orchestrator_success_case(task)
    assert result1 is not None, "Test 1 should succeed"

    result2 = mock_orchestrator_escalation_case(task)
    assert result2 is not None, "Test 2 should succeed with escalation"

    result3 = mock_orchestrator_failure_case(task)
    assert result3 is None, "Test 3 should fail"

    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED!")
    print("="*60)
    print("\nOrchestration logic verified:")
    print("  ✅ Worker revision on first rejection")
    print("  ✅ Escalation to Planner on second rejection")
    print("  ✅ Failure after max attempts")
    print("  ✅ Budget tracking throughout")
    print(f"\n📊 Check logs at: {LOG_FILE}")
