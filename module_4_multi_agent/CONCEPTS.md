# Module 4: Multi-Agent Systems - Concepts

**Learning Goal:** Understand when and how to coordinate multiple specialized agents to solve complex tasks through role separation, shared state, and intelligent escalation.

---

## Table of Contents
1. [What Are Multi-Agent Systems?](#what-are-multi-agent-systems)
2. [When to Use Multi-Agent vs Single Agent](#when-to-use-multi-agent-vs-single-agent)
3. [The Planner → Worker → Critic Pattern](#the-planner--worker--critic-pattern)
4. [Orchestration Strategies](#orchestration-strategies)
5. [Shared State vs Message Passing](#shared-state-vs-message-passing)
6. [Escalation and Revision Patterns](#escalation-and-revision-patterns)
7. [Budget Gates and Termination](#budget-gates-and-termination)
8. [Error Handling in Multi-Agent Systems](#error-handling-in-multi-agent-systems)
9. [Production Considerations](#production-considerations)

---

## What Are Multi-Agent Systems?

**Multi-agent systems** coordinate multiple specialized agents—each with distinct roles and responsibilities—to complete complex tasks that benefit from role separation.

### Core Idea

Instead of one "do-everything" agent:
```python
# Single agent doing everything
result = single_agent("Write a blog post, review it, and fix issues")
```

You have specialized agents working together:
```python
# Multiple specialized agents
plan = planner_agent("Create execution plan")
draft = worker_agent(plan)
feedback = critic_agent(draft)
final = worker_agent(plan, feedback)  # Revision
```

### Why This Matters

**Analogy:** Building a house

- **Single agent** = One person designs, builds, and inspects (slow, error-prone)
- **Multi-agent** = Architect designs → Construction crew builds → Inspector reviews (faster, specialized, higher quality)

---

## When to Use Multi-Agent vs Single Agent

### Decision Framework

**Use Multi-Agent when you have 2+ of these:**

✅ **Task Complexity** - 3+ distinct phases (plan, execute, review)
✅ **Different Skill Sets** - Different expertise needed at each stage
✅ **Objective Review** - Value in unbiased critique
✅ **Parallelism/Throughput** - Need to process multiple tasks simultaneously
✅ **Cost Optimization** - Can use different models per agent (GPT-4 for planning, GPT-3.5-turbo for execution)
✅ **Modularity** - Agents can be upgraded/replaced independently
✅ **Reusability** - Same agents used across different projects

**Use Single Agent when:**

✅ Simple task (single input/output)
✅ No clear phase separation
✅ Low volume
✅ Quick prototype
✅ Minimal complexity overhead desired

### Real-World Examples

**Scenario A: "Translate English to Spanish"**
→ **Single Agent** ✅
- Straightforward input/output
- No decomposition needed
- Single skill required

**Scenario B: "Analyze GitHub repo, find bugs, suggest improvements, generate report"**
→ **Multi-Agent** ✅
- Many distinct phases (analyze, find bugs, generate report)
- Different specialties (code analysis, bug detection, writing)
- Cost optimization (use cheaper models for routine analysis)

**Scenario C: "Monitor log file and alert on errors"**
→ **Depends!**
- Simple log parsing: Single agent
- Complex pattern detection with review: Multi-agent
- Context matters!

---

## The Planner → Worker → Critic Pattern

This is the most common multi-agent pattern for task execution with quality control.

### The Three Roles

#### 1. Planner Agent

**Job:** Break down complex tasks into executable step-by-step plans

**Input:**
- Original task description
- Previous failures (if re-planning)

**Output:**
- Detailed execution plan (ordered list of steps)

**Doesn't:**
- Execute anything
- Review quality

**Example:**
```
Task: "Write a blog post about AI agents"

Planner Output:
1. Research AI agents fundamentals
2. Research production use cases
3. Write introduction (100 words)
4. Write body with examples (400 words)
5. Write conclusion (100 words)
6. Proofread and ensure 600 words total
```

#### 2. Worker Agent

**Job:** Execute the ENTIRE plan and produce results

**Input:**
- Plan from Planner
- Feedback from Critic (if revising)
- History of previous attempts (prevents repeating mistakes!)

**Output:**
- Completed work (e.g., blog post, code, analysis)

**Key Insight:** ONE worker executes ALL steps—not separate workers per step!

**Example:**
```
Plan: [6 steps from Planner]

Worker:
- Does research (step 1-2)
- Writes intro (step 3)
- Writes body (step 4)
- Writes conclusion (step 5)
- Proofreads (step 6)
- Returns complete blog post
```

#### 3. Critic Agent

**Job:** Review work and provide actionable feedback

**Input:**
- Worker's output
- Original task requirements

**Output:**
- Approval decision (YES/NO)
- Specific, actionable feedback

**Doesn't:**
- Rewrite the work itself
- Execute the plan

**Example:**
```
Worker Output: [Blog post draft]

Critic Output:
APPROVED: NO
FEEDBACK: The post needs improvement:
- Only 400 words (need 600)
- Missing concrete examples in body
- Conclusion is too abrupt

Fix these issues.
```

### Why Role Separation Matters

**Separation of Concerns:** Each agent focuses on what it does best

- Planner isn't biased by execution constraints
- Worker isn't second-guessing the plan
- Critic provides objective review (less biased than self-review)

**Observability:** Can see exactly where things break

- Did planning fail? (Bad plan structure)
- Did execution fail? (Worker couldn't execute plan)
- Did review fail? (Critic too harsh/lenient)

**Cost Optimization:** Can use different models per role

```python
# Production pattern (not in our educational code):
planner_agent(model="gpt-4")         # Expensive, smart planning
worker_agent(model="gpt-3.5-turbo")  # Cheaper, good execution
critic_agent(model="gpt-4")          # Expensive, thorough review

# Our implementation uses same model for simplicity:
MODEL = "gpt-4o-mini"  # All agents use this
```

---

## Orchestration Strategies

The **orchestrator** coordinates all agents. Two main approaches:

### Approach A: Deterministic Orchestrator (What We Build)

**Python rules** coordinate agents:

```python
def orchestrator(task):
    plan = planner_agent(task)

    while not approved and iteration < max_iterations:
        result = worker_agent(plan)
        approved = critic_agent(result)

        if not approved and worker_attempts == 2:
            # Deterministic rule: Re-plan after 2 failures
            plan = planner_agent(task)
            worker_attempts = 0
```

**Pros:**
- ✅ Predictable flow (students can trace logic)
- ✅ Easy to debug (clear decision points)
- ✅ Budget gates visible (won't run forever)
- ✅ Educational clarity

**Cons:**
- ❌ Less adaptive than LLM orchestrator
- ❌ Can't reason about meta-decisions

### Approach B: LLM Orchestrator (Production Pattern)

**LLM decides** what to do next:

```python
def orchestrator(task):
    plan = planner_agent(task)
    result = worker_agent(plan)

    # LLM decides next action
    decision = llm_orchestrator_call(
        "Worker failed. Options: (1) retry, (2) re-plan, (3) give up. Decide:"
    )

    if decision == "re-plan":
        plan = planner_agent(task)  # Adaptive!
```

**Pros:**
- ✅ Adaptive ("this didn't work, trying new approach")
- ✅ Can reason about meta-decisions
- ✅ Handles unexpected situations

**Cons:**
- ❌ Can get stuck in loops
- ❌ Can lose focus or overcomplicate
- ❌ Harder to debug (Why did it decide X?)

**Real Example:** Claude Code uses this approach. It can:
- Try approach → Fail
- "This didn't work, trying new approach" (autonomous decision)
- Try again → Fail
- "We need to change the plan" (meta-reasoning)

**Problem:** Without budget gates, can loop indefinitely and lose focus!

**Solution:** Even LLM orchestrators need hard limits (covered in Budget Gates section).

---

## Shared State vs Message Passing

Agents need to communicate. Two main patterns:

### Pattern A: Shared State (What We Build)

All agents read/write to a shared dictionary:

```python
shared_state = {
    # Input
    "task": "Write blog post",

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

planner_agent(shared_state)  # Writes "plan", increments "plan_version"
worker_agent(shared_state)   # Reads "plan", writes "result", increments "worker_attempts"
critic_agent(shared_state)   # Reads "result", writes "critic_approved" and "critic_feedback"
```

**Pros:**
- ✅ Simple to understand (one source of truth)
- ✅ Easy to debug (print the dict)
- ✅ Full visibility (see all state at once)
- ✅ Natural for single-machine, sequential execution

**Cons:**
- ❌ Doesn't scale across machines
- ❌ No built-in validation
- ❌ Tight coupling (all agents know the schema)

**When to use:** Educational code, single-machine systems, rapid prototyping

### Pattern B: Message Passing (Production Pattern)

Agents communicate via messages:

```python
# Planner sends message to Worker
message_queue.send({
    "from": "planner",
    "to": "worker",
    "type": "plan",
    "content": "1. Research, 2. Write, 3. Review"
})

# Worker receives, processes, sends to Critic
worker_message = message_queue.receive()
result = execute_plan(worker_message["content"])

message_queue.send({
    "from": "worker",
    "to": "critic",
    "type": "result",
    "content": result
})
```

**Pros:**
- ✅ Scales across machines (distributed systems)
- ✅ Loose coupling (agents don't need to know each other)
- ✅ Built-in validation (message schemas)
- ✅ Can replay/audit messages
- ✅ Parallel processing (multiple workers)

**Cons:**
- ❌ More complex to implement
- ❌ Harder to debug (trace messages across systems)
- ❌ Overhead of message infrastructure

**When to use:** Production systems, distributed systems, high throughput requirements

---

## Escalation and Revision Patterns

When Critic rejects work, what happens next?

### Pattern A: Binary Accept/Reject

```python
if critic_approved:
    return result  # Done!
else:
    result = worker_agent(plan)  # Try again
```

**Problem:** All-or-nothing, no nuance, can loop forever

### Pattern B: Iterative Refinement

```python
while not critic_approved and attempts < max_attempts:
    result = worker_agent(plan, feedback)
    feedback = critic_agent(result)
```

**Problem:** Assumes the plan is good—what if the plan itself is flawed?

### Pattern C: Escalation (What We Build) ✅

Intelligent escalation recognizes that sometimes the **plan is wrong**, not just the execution.

**The actual implementation (simplified):**

```python
# Main loop with MAX_ITERATIONS as the master safety net
iteration = 0
MAX_ITERATIONS = 10

planner_agent(shared_state)  # Initial plan

while iteration < MAX_ITERATIONS:
    worker_agent(shared_state)
    critic_agent(shared_state)

    # SUCCESS: Exit early
    if shared_state["critic_approved"]:
        return shared_state["result"]

    # Escalation based on worker_attempts for THIS plan
    attempts = shared_state["worker_attempts"]

    if attempts == 1:
        # First rejection: Worker revises
        print("Worker will revise based on feedback")

    elif attempts == 2:
        # Second rejection: Escalate to Planner
        print("Escalating to Planner - maybe the plan is wrong!")
        planner_agent(shared_state)  # Re-plan!
        shared_state["worker_attempts"] = 0  # Reset for new plan

    elif attempts >= 3:
        # Third rejection on same plan: Give up
        # (Rarely reached - usually hit MAX_ITERATIONS first)
        print("Max attempts on this plan. Giving up.")
        return None

    iteration += 1

# Hit MAX_ITERATIONS - the REAL safety net
return None
```

**How This Works in Practice:**

**Scenario 1: Success after revision (2 iterations)**
```
Iter 1: Worker fails (attempts=1) → "revise"
Iter 2: Worker succeeds → APPROVED → Return result
```

**Scenario 2: Escalation then success (4 iterations)**
```
Iter 1: Worker fails (attempts=1) → "revise"
Iter 2: Worker fails (attempts=2) → ESCALATE → Planner re-plans, reset attempts=0
Iter 3: Worker tries new plan (attempts=1) → "revise"
Iter 4: Worker succeeds → APPROVED → Return result
```

**Scenario 3: Continuous failure (hits MAX_ITERATIONS=10)**
```
Iter 1-2: Fail → Escalate → Re-plan
Iter 3-4: Fail → Escalate → Re-plan
Iter 5-6: Fail → Escalate → Re-plan
Iter 7-8: Fail → Escalate → Re-plan
Iter 9-10: Fail → MAX_ITERATIONS reached → Give up
```

**Key Insight:**
- `worker_attempts` tracks failures **per plan** (resets after escalation)
- `iteration` is the **master budget gate** that prevents infinite loops
- The `attempts >= 3` check rarely triggers because we escalate at 2
- **MAX_ITERATIONS = 10** is the real safety net

**Why This Is Better:**

1. **Gives agents autonomy** - "I hired them to do their job, only pull me in when they need help"
2. **Recognizes plan quality matters** - Sometimes execution isn't the problem
3. **Intelligent escalation** - Worker retry → Planner re-plan → Continue trying
4. **Hard limit prevents infinite loops** - MAX_ITERATIONS ensures termination
5. **Matches real team dynamics** - How actual teams work

**Real-World Analogy:**

- **Worker fails once** → "Try again with feedback" (like a developer fixing bugs)
- **Worker fails twice** → "Maybe the spec is wrong?" (escalate to architect for new plan)
- **Keeps failing** → MAX_ITERATIONS reached → "We tried everything, need human help"

---

## Budget Gates and Termination

Budget gates are **circuit breakers** that prevent infinite loops and runaway costs.

### Gate 1: Max Iterations

Prevents infinite loops:

```python
MAX_ITERATIONS = 10

while iteration < MAX_ITERATIONS:
    # ... run agents ...
    iteration += 1

if iteration == MAX_ITERATIONS:
    print("Max iterations reached - stopping")
    return None
```

**Why 10?**
- Enough attempts to show escalation (Planner → Worker → Critic → retry → escalate)
- Not so many that tests run forever
- Configurable for different task complexities

### Gate 2: Max Tokens (Not Dollars!)

Industry reality: "Expensive" = tokens/time, not money

```python
MAX_TOTAL_TOKENS = 50_000

total_tokens = 0
while total_tokens < MAX_TOTAL_TOKENS:
    response = llm_call(...)
    total_tokens += response.usage.total_tokens

    if total_tokens >= MAX_TOTAL_TOKENS * 0.8:
        print("Warning: 80% of token budget used")

if total_tokens >= MAX_TOTAL_TOKENS:
    print("Token budget exhausted")
    return None
```

**Why Tokens, Not Dollars?**

1. **Tokens = Time/Latency**
   - 10,000 tokens takes longer than 1,000 tokens
   - Users care about speed

2. **Tokens = Context Limits**
   - Models have hard limits (128k for GPT-4o-mini)
   - Can't exceed this, period

3. **Tokens = Throughput/Rate Limits**
   - Rate limits measured in tokens/minute
   - Affects scalability

4. **Dollars Are Negligible**
   - GPT-4o-mini: $0.15 per 1M input tokens
   - Whole task costs ~$0.001 (a tenth of a penny)
   - Money is relative, but speed matters to everyone

**Note:** We still track cost for educational purposes (shows students it's cheap!), but budget gates enforce TOKEN limits.

### Gate 3: Success Condition (Most Important!)

The **happy path** - stop when job is done:

```python
while iteration < MAX_ITERATIONS and total_tokens < MAX_TOTAL_TOKENS:
    # ... run agents ...

    if critic_approved:
        print(f"Success in {iteration} iterations!")
        return result  # Exit early - don't waste budget!
```

This is critical! Without it, system burns budget even after success.

### Real Costs (for Reference)

**Successful task** (approved after 2 worker attempts):
- Planner + Worker + Critic + Worker + Critic = ~3,000 tokens
- Cost: ~$0.0006 (less than a tenth of a penny)

**Failed task** (hits max iterations):
- 10 iterations × ~600 tokens avg = ~6,000 tokens
- Cost: ~$0.0012 (about a tenth of a penny)

**Running all day testing:**
- 100 test runs = ~$0.10 (10 cents)

So it's cheap, but **budget gates prevent it from becoming expensive** if something goes wrong!

---

## Error Handling in Multi-Agent Systems

Errors are more complex with multiple agents - any agent can fail!

### Error Type 1: API Failures (Transient)

Most common: rate limits, temporary outages

**Strategy: Simple Retry**

```python
def call_llm_with_retry(messages, agent_name):
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
```

**Why simple?** "We don't need production code, but we still want good code. We need to trap errors somewhat gracefully, but I don't want the script to just crash."

### Error Type 2: Validation Failures (Logic Bugs)

Agent didn't produce expected output

**Strategy: Fail Fast with Clear Message**

```python
# In worker_agent():
if not plan:
    raise ValueError("Worker called without a plan! Planner must run first.")

# In critic_agent():
if not result:
    raise ValueError("Critic called without Worker output! Worker must run first.")

# Crashes immediately but student knows exactly what went wrong
```

**Why fail fast?** Don't hide bugs! Clear errors are educational.

### What We DON'T Build (Production Patterns)

For educational code, we skip:
- ❌ Exponential backoff retry logic
- ❌ Circuit breakers for repeated failures
- ❌ Fallback/degradation strategies
- ❌ Dead letter queues for failed tasks

**Rationale:** Good practices without production complexity. Students learn the concepts without getting lost in error handling code.

---

## Production Considerations

### What We Built (Educational)

✅ Deterministic orchestrator (Python rules)
✅ Shared state (in-memory dict)
✅ Simple retry (one attempt)
✅ Token budget gates
✅ Escalation pattern (Worker → Planner → Human)

### What Production Systems Add

**1. Message Passing** - Distributed agent communication
**2. LLM Orchestrator** - Adaptive decision-making
**3. Sophisticated Retry** - Exponential backoff, circuit breakers
**4. Monitoring** - Metrics, alerts, dashboards
**5. Agent Pools** - Multiple Workers for parallelism
**6. State Persistence** - Database instead of in-memory dict
**7. Human-in-the-Loop** - Approval workflows, escalation UIs

### When to Add Complexity

**Start simple** (like our implementation):
- Single machine
- Sequential execution
- Low volume
- Learning/prototyping

**Add complexity when you need**:
- Distributed systems (multiple machines)
- High throughput (parallel processing)
- Production reliability (SLAs, uptime)
- Scale (thousands of tasks/day)

---

## Multi-Agent Systems: Architecture Pattern vs Deployment

### The Conceptual Question

**"Wait... these 'agents' are just Python functions in one file. How is this different from regular modular programming?"**

This is an excellent question that highlights an important distinction!

### What Makes Something a "Multi-Agent System"?

It's **not** about:
- ❌ Separate processes or servers
- ❌ Different machines or containers
- ❌ Network communication
- ❌ Microservices architecture

It **is** about:
- ✅ **Specialized roles** - Each agent has distinct responsibilities
- ✅ **Autonomous decisions** - Each agent uses an LLM to make choices
- ✅ **Coordination pattern** - Orchestrator manages workflow with escalation
- ✅ **Shared context** - Agents communicate through state or messages

### Regular Functions vs Agents

**Regular modular programming (deterministic):**
```python
def validate_email(email):
    # Same input → same output, always
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)

def format_name(name):
    # Predictable string manipulation
    return name.strip().title()
```

**Multi-agent system (non-deterministic):**
```python
def planner_agent(task):
    # LLM makes creative decisions
    plan = llm(f"Break this into steps: {task}")
    return plan  # Different output each time!

def worker_agent(plan, history):
    # LLM learns from past attempts
    result = llm(f"Execute plan: {plan}. History: {history}")
    return result  # Adapts based on feedback

def critic_agent(result):
    # LLM makes subjective judgments
    approved = llm(f"Is this good quality? {result}")
    return approved  # Contextual evaluation
```

**Key difference:** LLMs make autonomous, context-aware decisions in each agent.

### Deployment Options: The Same Pattern, Different Scales

The **architecture pattern** (Planner → Worker → Critic with escalation) stays the same.
The **deployment** varies based on needs:

#### Option 1: Single File (What We Built)
```python
# multi_agent_system.py
def planner_agent(): ...
def worker_agent(): ...
def critic_agent(): ...
def orchestrator(): ...
```

**When to use:**
- Learning and prototyping
- Simple workflows on one machine
- All agents use same LLM provider
- Fast iteration during development

**Example:** Content generation tool for blog posts

---

#### Option 2: Separate Processes (Same Machine)
```bash
python planner_service.py &    # Port 5001
python worker_service.py &     # Port 5002
python critic_service.py &     # Port 5003
python orchestrator.py         # Coordinates via HTTP
```

**When to use:**
- Different resource needs (CPU vs GPU)
- Independent scaling of agents
- Fault isolation (one agent crash doesn't kill system)

**Example:** Video processing where Worker needs GPU, others need CPU

---

#### Option 3: Distributed Services (Different Machines)
```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│  Planner    │      │   Worker    │      │   Critic    │
│  Server 1   │      │   Server 2  │      │   Server 3  │
│  Claude API │      │  OpenAI API │      │  Local LLM  │
└─────────────┘      └─────────────┘      └─────────────┘
       ↑                    ↑                    ↑
       └────────────────────┴────────────────────┘
              Orchestrator (Server 4)
              Message Queue (RabbitMQ)
```

**When to use:**
- Different LLM providers for different agents
- Geographic distribution (data sovereignty)
- Different teams own different agents
- Scale to millions of requests

**Example:** Enterprise customer support across regions

---

#### Option 4: MCP Tools (Standardized Interface)
```python
orchestrator_tools = [
    {"type": "mcp_tool", "server": "planner-mcp", "tool": "create_plan"},
    {"type": "mcp_tool", "server": "worker-mcp", "tool": "execute"},
    {"type": "mcp_tool", "server": "critic-mcp", "tool": "review"}
]

# LLM-based orchestrator decides which tool to call
result = orchestrator_llm(task, tools=orchestrator_tools)
```

**When to use:**
- Want LLM to decide orchestration (not Python rules)
- Agents reused across different workflows
- Standardized tool interface needed

**Example:** Agentic platform with shared agent pool

---

### Why Did We Build It in One File?

**For learning!**

If we started with:
- Docker compose files
- API contracts
- Service discovery
- Message queues

You'd be learning **DevOps**, not **multi-agent patterns**.

The single-file version lets you focus on:
- ✅ When to escalate from Worker to Planner
- ✅ How to track history so LLMs don't repeat mistakes
- ✅ Why budget gates matter
- ✅ Python orchestration vs LLM orchestration

**Once you understand the pattern, deploy it however you want!**

### The Architecture Pattern is What Matters

Whether your agents are:
- Functions in one file
- Separate Python processes
- Distributed microservices
- MCP tool servers

**The logic stays the same:**
1. Planner breaks down task
2. Worker executes with full context
3. Critic evaluates quality
4. Orchestrator decides: retry → re-plan → give up
5. Budget gates prevent runaway costs
6. History prevents repeated mistakes

**The pattern scales from prototype to production without changing the core logic.**

---

## Key Takeaways

1. **Multi-agent systems** coordinate specialized agents for complex tasks
2. **Planner → Worker → Critic** is the most common quality-control pattern
3. **Escalation matters** - Worker retry → Planner re-plan → Human intervention
4. **Orchestration can be deterministic** (Python rules) or adaptive (LLM)
5. **Budget gates prevent runaway costs** - max iterations + max tokens
6. **"Expensive" = tokens/time**, not dollars (industry reality)
7. **Shared state vs message passing** - Simple vs scalable trade-off
8. **Error handling**: Simple retry for API, fail fast for validation
9. **Start simple, add complexity when needed** - Don't over-engineer

---

**Next:** Study PROJECT.md to see how these concepts are implemented in code!
