# Module 4: Multi-Agent Systems

**Released:** December 22, 2024 (Week 4)

Coordinate multiple specialized agents working together—learn the Planner → Worker → Critic pattern and scale beyond single-agent systems.

---

## What You'll Build

A complete multi-agent system that:
- **Plans** complex tasks using a Planner agent
- **Executes** plans using a Worker agent
- **Reviews** work using a Critic agent
- **Orchestrates** coordination with budget gates and escalation
- **Logs** everything for full observability

**Pattern:** Planner → Worker → Critic with intelligent escalation

---

## Learning Objectives

By the end of this module, you'll understand:

✅ When to use multi-agent systems vs single agents
✅ How the Planner → Worker → Critic pattern works
✅ Orchestration strategies (deterministic vs LLM-based)
✅ Budget gates and why they prevent infinite loops
✅ Escalation patterns (Worker retry → Planner re-plan → Give up)
✅ Shared state vs message passing trade-offs

---

## Your Learning Workflow

### Step 1: Read CONCEPTS.md (Theory)

**Start here!** Learn the theory before looking at code.

Key concepts you'll learn:
- When multi-agent beats single-agent
- The three agent roles (Planner, Worker, Critic)
- Why escalation matters
- Budget gates (tokens, not dollars!)
- Error handling strategies

**Time:** 30-40 minutes

### Step 2: Read PROJECT.md (Architecture)

Understand how the system is designed:
- Architecture diagram
- Component breakdown
- Data flow through shared_state
- Key design decisions and trade-offs

**Use the seed questions!** PROJECT.md includes 25 questions organized by difficulty.

**Time:** 20-30 minutes

### Step 3: Study SOLUTION/multi_agent_system.py

Now dive into the code with Claude Code as your guide.

**Start with these questions:**
- "Walk me through the orchestrator() function"
- "How does escalation work? Show me the code"
- "Explain the shared_state structure"

**The code is ~600 lines with extensive comments.**

**Time:** 45-60 minutes

### Step 4: Run the Code

#### Option A: Quick Test (No API Key)

Test the orchestration logic without API calls:

```bash
source venv/bin/activate
python SOLUTION/test_multi_agent_mock.py
```

You'll see three test cases:
1. Success after Worker revision
2. Success after escalation to Planner
3. Failure after max attempts

**Time:** 5 minutes

#### Option B: Full Test (Requires OpenAI API Key)

Run the real multi-agent system:

```bash
source venv/bin/activate
python SOLUTION/multi_agent_system.py
```

Watch Planner → Worker → Critic coordinate in real-time!

Check logs at: `logs/multi_agent_system.jsonl`

**Time:** 10 minutes

### Step 5: Ask Deep Questions

Now that you've seen it work, dive deeper:

**From PROJECT.md seed questions (🌿 Going Deeper):**
- "Compare our deterministic orchestrator to an LLM orchestrator. What are the trade-offs?"
- "Why do we track tokens instead of dollars for budget gates?"
- "How does format_history() prevent the Worker from repeating mistakes?"
- "What would happen if we removed the history tracking?"

**Time:** 30-45 minutes

### Step 6: Experiment

Modify the code and see what happens:

**Experiment 1:** Change budget gates
```python
MAX_ITERATIONS = 3  # Very restrictive
# Does it fail faster? How?
```

**Experiment 2:** Remove history tracking
```python
# Comment out history formatting in worker_agent()
# Does Worker repeat mistakes?
```

**Experiment 3:** Change escalation logic
```python
# Escalate immediately on first failure
# What changes?
```

**Time:** 30-60 minutes

### Step 7: Reflect

Answer these questions:

1. **What improved with role separation?** (Planner/Worker/Critic vs one agent)
2. **Where did orchestration add complexity?** Is it worth it?
3. **When is multi-agent overkill?** When is it necessary?
4. **How does shared state compare to message passing?** Trade-offs?
5. **What would you add for production?** Monitoring? Retries? Parallelism?

---

## Files in This Module

```
module_4_multi_agent/
├── README.md (this file)
├── CONCEPTS.md (theory - read first!)
├── PROJECT.md (architecture + seed questions)
├── SOLUTION/
│   ├── multi_agent_system.py (full implementation)
│   ├── test_multi_agent_mock.py (mock test - no API)
│   └── README_TESTING.md (testing guide)
└── logs/ (execution traces)
```

---

## Concepts Covered

- **Multi-agent patterns:** When to use vs single agents
- **Planner → Worker → Critic:** The most common quality-control pattern
- **Orchestration:** Deterministic (Python rules) vs adaptive (LLM)
- **Shared state:** Simple, visible, debuggable
- **Escalation:** Worker retry → Planner re-plan → Human
- **Budget gates:** Max iterations + max tokens (not dollars!)
- **History tracking:** Prevents LLMs from repeating mistakes
- **Error handling:** Simple retry for API, fail fast for validation
- **Observability:** JSONL logs for full execution trace

---

## Success Criteria

You'll know you've mastered this module when you can:

✅ Explain when to use multi-agent vs single agent
✅ Describe the Planner → Worker → Critic roles
✅ Trace the orchestration logic through the code
✅ Explain why budget gates prevent infinite loops
✅ Understand the escalation pattern
✅ Modify the code to add features or change behavior
✅ Compare shared state vs message passing
✅ Design a multi-agent system for a new problem

---

## Key Insights from Building This

### Design Decision 1: Deterministic Orchestrator

**What we built:** Python rules coordinate agents
**Why:** Predictable flow, easy to debug, won't get stuck in loops
**Trade-off:** Less adaptive than LLM orchestrator

### Design Decision 2: Escalation Pattern

**What we built:** Worker retry → Planner re-plan → Give up
**Why:** Recognizes sometimes the *plan* is wrong, not just execution
**Insight:** "I hired these agents to do their job - only pull me in when they need help"

### Design Decision 3: Token Budget (Not Dollars)

**What we built:** MAX_TOTAL_TOKENS = 50,000
**Why:** Industry standard - "expensive" = tokens/time, not money
**Insight:** "Nobody wants to wait. Token count covers time AND context limits."

### Design Decision 4: History Tracking

**What we built:** Store all attempts in shared_state["history"]
**Why:** Prevents LLMs from repeating the same failed approach
**Insight:** "If we don't give full history, the LLM could try the same thing twice and fail again"

### Design Decision 5: Simple Error Handling

**What we built:** Retry once for rate limits, fail fast for validation
**Why:** Good practices without production complexity
**Insight:** "We don't need production code, but we still want good code"

---

## Common Questions

**Q: Why three agents instead of one?**
A: Role separation improves quality (Planner, Worker, Critic each focus on what they do best), enables cost optimization (different models per agent), and provides better observability (can see exactly where things break).

**Q: When is multi-agent overkill?**
A: For simple tasks like "translate this text" or "summarize this paragraph." Use single agents for straightforward input/output operations.

**Q: Why deterministic orchestrator instead of LLM?**
A: Educational clarity and reliability. LLM orchestrators are more adaptive but can get stuck in loops, lose focus, or overcomplicate things. Our deterministic approach is predictable and easier to debug.

**Q: Why track tokens, not dollars?**
A: Industry reality - "expensive" means tokens (which equals time, context limits, throughput), not money. GPT-4o-mini is so cheap (~$0.001 per task) that dollars don't matter. Speed and context limits do.

**Q: What's missing for production?**
A: Message passing (for distributed systems), sophisticated retry logic (exponential backoff), monitoring/alerts, agent pools (parallelism), state persistence (database), human-in-the-loop workflows.

---

## What's Next?

### After This Module

You now understand multi-agent coordination! You can:
- Design role-based agent systems
- Implement orchestration logic
- Add budget gates and escalation
- Build for observability

### Module 5: LLM as Judge & Evaluation (Dec 29)

Learn to measure agent quality with:
- LLM-as-judge pattern
- Rubric design
- Multi-criteria scoring
- Quality metrics

### Keep Learning

**Practice:**
- Design a multi-agent system for code review
- Add a Researcher agent to this system
- Implement message passing instead of shared state
- Add human-in-the-loop approval

**Explore:**
- LangGraph multi-agent systems
- CrewAI framework
- AutoGen framework
- Compare approaches

---

## Feedback & Questions

As you work through this module:
- Use Claude Code as your professor
- Ask the seed questions in PROJECT.md
- Experiment with the code
- Read the logs to understand execution

**Remember:** The goal isn't to memorize code—it's to understand the *patterns* so you can design your own multi-agent systems!

---

**Happy Learning!** 🚀
