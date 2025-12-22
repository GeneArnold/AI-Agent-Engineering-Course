# Module 4: Multi-Agent Systems - Project Architecture

**What We're Building:** A Planner → Worker → Critic multi-agent system with deterministic orchestration, escalation logic, and budget gates.

---

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture Diagram](#architecture-diagram)
3. [Component Breakdown](#component-breakdown)
4. [Data Flow](#data-flow)
5. [Key Design Decisions](#key-design-decisions)
6. [Code Structure](#code-structure)
7. [Seed Questions](#seed-questions)

---

## System Overview

### What Does It Do?

Given a complex task (like "Write a 300-word blog post about AI agents"), the system:

1. **Planner** breaks it into executable steps
2. **Worker** executes all steps and produces output
3. **Critic** reviews and provides feedback
4. **Orchestrator** decides: approve, revise, escalate, or give up

### Success Criteria

✅ Planner creates actionable plans
✅ Worker executes plans completely
✅ Critic provides objective, actionable feedback
✅ System escalates intelligently (Worker retry → Planner re-plan)
✅ Budget gates prevent infinite loops
✅ Full observability via JSONL logs

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR                         │
│  (Deterministic Python - coordinates everything)        │
│                                                          │
│  Budget Gates:                                          │
│  - MAX_ITERATIONS = 10                                  │
│  - MAX_TOTAL_TOKENS = 50,000                           │
│                                                          │
│  Escalation Logic:                                      │
│  - 1st rejection: Worker revises                       │
│  - 2nd rejection: Escalate to Planner                   │
│  - 3rd+ rejection: Give up                              │
└─────────────────────────────────────────────────────────┘
          ↓                  ↓                  ↓
    ┌─────────┐        ┌─────────┐        ┌─────────┐
    │ PLANNER │        │ WORKER  │        │ CRITIC  │
    │         │        │         │        │         │
    │ Breaks  │        │ Executes│        │ Reviews │
    │ down    │──plan──>│ plan   │─result─>│ and     │
    │ tasks   │        │ fully   │        │ provides│
    │         │        │         │        │ feedback│
    └─────────┘        └─────────┘        └─────────┘
         ↑                  ↑                  │
         │                  │                  │
         └──────re-plan─────┴──────feedback────┘
                     (if escalation needed)

           ALL AGENTS READ/WRITE TO:

         ┌───────────────────────────┐
         │     SHARED STATE          │
         │  (In-memory dictionary)   │
         │                           │
         │  - task                   │
         │  - plan                   │
         │  - result                 │
         │  - critic_approved        │
         │  - critic_feedback        │
         │  - history []             │
         │  - total_tokens           │
         └───────────────────────────┘

                     ↓

         ┌───────────────────────────┐
         │    JSONL LOGGING          │
         │  (Full execution trace)   │
         │                           │
         │  - planner_call events    │
         │  - worker_call events     │
         │  - critic_call events     │
         │  - orchestrator events    │
         └───────────────────────────┘
```

---

## Component Breakdown

### 1. Helper Functions

**`calculate_cost(usage)`**
- Calculates actual API cost from token usage
- Educational: Shows students costs are negligible
- Budget gates enforce tokens, not dollars

**`log_event(event_type, data)`**
- Logs every event to JSONL file
- Full observability: can replay execution
- Format: `{timestamp, event_type, ...data}`

**`format_history(history)`**
- Formats attempt history for LLM context
- **Critical:** Prevents LLMs from repeating mistakes
- Shows what was tried and what failed

**`call_llm_with_retry(messages, agent_name)`**
- Simple retry for rate limits (one attempt)
- Fails fast for unexpected errors
- Error handling philosophy: "Good code without production complexity"

### 2. Agent Implementations

#### Planner Agent

```python
def planner_agent(shared_state: Dict[str, Any]) -> int:
    """
    Breaks down complex tasks into executable plans.

    Reads:
    - task (original requirements)
    - history (if re-planning after failure)

    Writes:
    - plan (step-by-step execution plan)
    - plan_version (tracks re-planning)

    Returns: tokens used
    """
```

**Prompt Strategy:**
- System: "You are a Planner agent. Break down tasks into clear, executable steps."
- User: Task + history (if re-planning)
- Temperature: 0.7 (creative planning)

**Key Insight:** If re-planning (version > 1), includes history so Planner learns from failures!

#### Worker Agent

```python
def worker_agent(shared_state: Dict[str, Any]) -> int:
    """
    Executes the ENTIRE plan and produces results.

    Reads:
    - task (original requirements)
    - plan (from Planner)
    - history (previous attempts - prevents repeating mistakes!)
    - critic_feedback (if revising)

    Writes:
    - result (completed work)
    - worker_attempts (tracks retries)

    Returns: tokens used
    """
```

**Prompt Strategy:**
- System: "Execute all steps in the plan. Be thorough and complete."
- User: Task + plan + history + feedback (if revising)
- Temperature: 0.7 (balanced execution)

**Critical Feature:** History tracking prevents Worker from trying the same failed approach twice!

#### Critic Agent

```python
def critic_agent(shared_state: Dict[str, Any]) -> int:
    """
    Reviews work and provides actionable feedback.

    Reads:
    - task (original requirements)
    - result (Worker's output)

    Writes:
    - critic_approved (True/False)
    - critic_feedback (specific feedback)

    Returns: tokens used
    """
```

**Prompt Strategy:**
- System: "Review output against requirements. Be honest and constructive."
- User: Task + Worker's output
- Expected format:
  ```
  APPROVED: [YES or NO]
  FEEDBACK: [Specific, actionable feedback]
  ```

**Key Insight:** Critic is separate from Worker for objectivity (less biased than self-review).

### 3. Orchestrator

```python
def orchestrator(task: str, max_iterations=10, max_tokens=50_000):
    """
    Coordinates all agents with budget gates and escalation.

    Flow:
    1. Initial planning (Planner)
    2. Loop until success or budget exhausted:
       a. Worker executes
       b. Critic reviews
       c. Decision: approve, retry, escalate, or give up
    3. Return result or None
    """
```

**Orchestration Logic:**

```python
# Step 1: Initial plan
planner_agent(shared_state)

# Step 2: Main loop
while iteration < MAX_ITERATIONS and tokens < MAX_TOKENS:
    worker_agent(shared_state)
    critic_agent(shared_state)

    # SUCCESS GATE
    if critic_approved:
        return result

    # ESCALATION LOGIC
    if worker_attempts == 1:
        # First rejection: Worker revises
    elif worker_attempts == 2:
        # Second rejection: Escalate to Planner
        planner_agent(shared_state)
        worker_attempts = 0
    elif worker_attempts >= 3:
        # Third+ rejection: Give up
        return None
```

**Why Deterministic?**
- Predictable flow (students can trace logic)
- Easy to debug (clear decision points)
- Won't get stuck in loops (unlike LLM orchestrators can)

---

## Data Flow

### Shared State Structure

```python
shared_state = {
    # INPUT
    "task": "Write a 300-word blog post about AI agents",

    # PLANNER OUTPUT
    "plan": None,           # Step-by-step plan
    "plan_version": 0,      # Tracks re-planning

    # WORKER OUTPUT
    "result": None,         # Completed work
    "worker_attempts": 0,   # Tracks retries

    # CRITIC OUTPUT
    "critic_approved": False,     # True = success
    "critic_feedback": None,       # Specific feedback

    # HISTORY (prevents repeating mistakes!)
    "history": [
        {
            "agent": "planner",
            "version": 1,
            "plan": "1. Research...",
            "timestamp": "2024-12-20T10:00:00Z"
        },
        {
            "agent": "worker",
            "attempt": 1,
            "output": "Blog post draft...",
            "timestamp": "2024-12-20T10:01:00Z"
        },
        {
            "agent": "critic",
            "attempt": 1,
            "feedback": "Needs more examples...",
            "approved": False,
            "timestamp": "2024-12-20T10:02:00Z"
        }
    ],

    # METADATA
    "total_tokens": 3500,
    "iteration": 2,
    "status": "in_progress"  # or "completed" or "failed"
}
```

### Execution Flow Example

**Scenario:** Blog post task, Worker fails once, succeeds on revision

```
Iteration 0:
  Planner → Creates plan (500 tokens)
  State: plan="1. Research, 2. Write...", plan_version=1

Iteration 1:
  Worker → Executes plan poorly (800 tokens)
  State: result="Short blog post...", worker_attempts=1

  Critic → Rejects (600 tokens)
  State: critic_approved=False, feedback="Too short, needs examples..."

  Decision: Worker will revise (first rejection)

Iteration 2:
  Worker → Revises based on feedback (800 tokens)
  State: result="Improved blog post...", worker_attempts=2

  Critic → Approves (600 tokens)
  State: critic_approved=True

  Decision: SUCCESS! Return result.

Total: 3,300 tokens, ~$0.0007 cost
```

---

## Key Design Decisions

### Decision 1: Deterministic Orchestrator (Not LLM)

**Choice:** Python rules coordinate agents
**Rationale:** Predictable, educational, prevents infinite loops
**Trade-off:** Less adaptive than LLM orchestrator

**From Phase 1 Learning:**
> "Claude Code can get stuck in loops, lose focus, or get too complicated. We need something predictable for students."

### Decision 2: Shared State (Not Message Passing)

**Choice:** In-memory dictionary
**Rationale:** Simple, visible, easy to debug
**Trade-off:** Doesn't scale to distributed systems

**Why:** Educational clarity > production scalability

### Decision 3: Escalation Pattern

**Choice:** Worker retry → Planner re-plan → Give up
**Rationale:** Recognizes sometimes the plan is wrong, not just execution
**Trade-off:** More complex than simple retry, but more intelligent

**From Phase 1 Learning:**
> "I hired these agents to do their job - only pull me in when they need help. Give it another shot, escalate if needed."

### Decision 4: Token Budget (Not Dollar Budget)

**Choice:** MAX_TOTAL_TOKENS = 50,000
**Rationale:** Industry standard, meaningful constraint
**Trade-off:** None (this is the right choice)

**From Phase 1 Learning:**
> "Expensive is not just money but it's time. Token count covers both of these. Nobody wants to wait."

### Decision 5: History Tracking

**Choice:** Store all attempts in shared_state["history"]
**Rationale:** Prevents LLMs from repeating same mistakes
**Trade-off:** Slightly more complex, but critical for quality

**From Phase 1 Learning:**
> "If we do not give full history the LLM could try to do the same thing twice and fail again because it does not know what didn't already fail."

### Decision 6: Simple Error Handling

**Choice:** Retry once for rate limits, fail fast for validation
**Rationale:** Good practices without production complexity
**Trade-off:** Won't handle every edge case (acceptable for education)

**From Phase 1 Learning:**
> "We don't need production code, but we still want good code. We need to trap errors gracefully, but I don't want the script to just crash."

---

## Code Structure

```
module_4_multi_agent/
├── SOLUTION/
│   ├── multi_agent_system.py           # Full implementation
│   ├── test_multi_agent_mock.py         # Mock version (no API)
│   └── README_TESTING.md                # Testing instructions
├── logs/
│   ├── multi_agent_system.jsonl         # Real execution logs
│   └── multi_agent_test_mock.jsonl      # Mock test logs
├── CONCEPTS.md                           # Theory (you just read)
├── PROJECT.md                            # Architecture (this file)
└── README.md                             # Learning workflow

Total: ~600 lines of production code
       ~400 lines of test code
       Full observability via JSONL logs
```

---

## Seed Questions

Use these questions with Claude Code to deepen your understanding!

### 🌱 Getting Started (Basics)

1. **"Walk me through the shared_state structure. What does each field do?"**
   - Understand the data that flows between agents

2. **"Why do we have three separate agents instead of one?"**
   - Explore the value of role separation

3. **"What happens in a single iteration of the orchestrator loop?"**
   - Trace the execution flow

4. **"How does the Planner agent decide what steps to include in the plan?"**
   - Understand LLM prompting for planning tasks

5. **"Show me the escalation logic. When does it trigger re-planning?"**
   - See how intelligent retry works

6. **"What's in the history list? Why do we track it?"**
   - Learn about preventing repeated mistakes

7. **"Run the mock test. What do the three test cases demonstrate?"**
   - See success, escalation, and failure scenarios

### 🌿 Going Deeper (Intermediate)

8. **"Compare our deterministic orchestrator to an LLM orchestrator. What are the trade-offs?"**
   - Understand different coordination strategies

9. **"Why do we track tokens instead of dollars for budget gates?"**
   - Learn industry thinking about "expensive"

10. **"How does format_history() prevent the Worker from repeating mistakes?"**
    - See how we give LLMs memory

11. **"What would happen if we removed the history tracking?"**
    - Experiment by commenting out history code

12. **"Walk through the error handling in call_llm_with_retry(). Why is it simple?"**
    - Understand the "good code without production complexity" philosophy

13. **"What's the difference between worker_attempts and plan_version?"**
    - Understand revision vs re-planning

14. **"Trace a successful execution using the JSONL logs. What can you learn?"**
    - Practice log analysis

15. **"What happens if the Critic is too harsh and never approves anything?"**
    - Explore failure modes

### 🌳 Advanced Understanding (Deep Dive)

16. **"How would you add a fourth agent (like a Researcher) to this system?"**
    - Practice extending the pattern

17. **"Compare shared state vs message passing. When would you use each?"**
    - Understand architectural trade-offs

18. **"How would you modify this to process multiple tasks in parallel?"**
    - Think about scaling

19. **"What production features are missing from our implementation?"**
    - Learn what real systems need

20. **"How would you add a 'human-in-the-loop' approval step?"**
    - Design escalation to humans

21. **"Modify the budget gates to add a 'cost per task' limit. How would that work?"**
    - Practice extending constraints

22. **"How does this pattern compare to CrewAI or LangGraph multi-agent systems?"**
    - Understand the landscape

23. **"Design a different task (like code review). How would the prompts change?"**
    - Apply the pattern to new domains

24. **"What would you log differently for better observability?"**
    - Think about debugging and monitoring

25. **"How would you test this system thoroughly? What test cases matter?"**
    - Practice quality engineering

---

## Experiments to Try

### Experiment 1: Change Budget Gates

```python
# Current:
MAX_ITERATIONS = 10
MAX_TOTAL_TOKENS = 50_000

# Try:
MAX_ITERATIONS = 3  # Very restrictive
# What happens? Does it fail faster?
```

### Experiment 2: Remove History Tracking

```python
# In worker_agent(), comment out history formatting:
# user_prompt += f"PREVIOUS ATTEMPTS:\n{format_history(history)}"

# Run it. Does Worker repeat mistakes?
```

### Experiment 3: Add a Fourth Agent

```python
def researcher_agent(shared_state):
    """Gathers information before Worker executes."""
    # What would this do?
    # How would it fit in the flow?
```

### Experiment 4: Change Escalation Logic

```python
# Current: Escalate after 2 failures
# Try: Escalate immediately on first failure
# Or: Never escalate, just retry
# What changes?
```

### Experiment 5: Different Task

```python
# Current task: Blog post
# Try: "Analyze this code for bugs and suggest fixes"
# How do agent prompts change?
```

---

## What Makes This Implementation Educational?

✅ **Transparent:** Every decision point is visible Python code
✅ **Debuggable:** Print statements, JSONL logs, clear state
✅ **Minimal:** No unnecessary abstractions or frameworks
✅ **Extensible:** Easy to add agents or modify logic
✅ **Real:** Actual multi-agent pattern used in production (simplified)
✅ **Complete:** Handles success, failure, and edge cases

**Philosophy:**
> "Simple enough to understand in one sitting, complex enough to be useful, real enough to matter."

---

## Next Steps

1. **Read the code:** Start with `orchestrator()`, trace the flow
2. **Run the mock test:** See all three scenarios (success, escalation, failure)
3. **Ask Claude the seed questions:** Deepen understanding
4. **Modify and experiment:** Change parameters, add features
5. **Read the logs:** Understand what happened at each step
6. **Compare to production systems:** What would you add for production?

---

**Remember:** The goal isn't to memorize this code—it's to understand the *patterns* so you can design your own multi-agent systems for different problems!
