# Module 4: Multi-Agent Systems

## 🔒 Releases December 22, 2024 (Week 4)

Coordinate multiple specialized agents working together—learn the Planner → Worker → Critic pattern and scale beyond single-agent systems.

## Learning Objectives
- Design role-based agent architectures
- Implement message passing and shared state
- Build orchestration logic for agent coordination
- Set budget gates and termination criteria

## Concepts Covered
- Planner → Worker → Critic pattern
- Shared state management
- Message passing between agents
- Orchestration and coordination
- Termination logic (max steps, max cost, task completion)
- Observability for multi-agent systems

## Project: `multi_agent_system.py`

### Requirements
- Three agent roles with distinct responsibilities:
  - **Planner**: Breaks down tasks, sets objectives, creates execution plan
  - **Worker**: Executes actions, uses tools, reports results
  - **Critic**: Reviews outputs, provides feedback, suggests improvements
- Shared state dictionary (messages, tasks, execution history)
- Message passing protocol between agents
- Orchestration loop that coordinates agent handoffs
- Budget gates: max iterations, max cost, completion criteria

### Success Criteria
✅ Planner → Worker → Critic handoff completes successfully
✅ Shared state tracks all agent interactions and messages
✅ Each agent fulfills its role (planning, execution, critique)
✅ System respects budget constraints (stops at limits)
✅ Logs show full trace of agent coordination and decisions

## Files in This Module
- `SOLUTION/multi_agent_system.py` - Orchestrated multi-agent system
- `logs/` - JSONL traces of agent interactions
- `CONCEPTS.md` - Theory: Multi-agent patterns, coordination, roles
- `PROJECT.md` - Architecture: Design decisions, seed questions
- `README.md` - This file - Module overview

## Reflection Questions
After completing this module, answer:
1. What improved with role separation (Planner/Worker/Critic)?
2. Where did orchestration add unnecessary complexity?
3. How would you simplify the coordination?
4. When is multi-agent overkill vs necessary?
5. How does shared state compare to message passing?

## Coming December 22, 2024

**This module releases in Week 4.** Until then:
- Complete Modules 1-3
- Master agent loops, memory, and tool systems
- Get ready for multi-agent orchestration!

---

## Next Step
**Module 5: LLM as Judge & Evaluation** (Dec 29)
Learn to measure agent quality with evaluation systems and the LLM-as-judge pattern.
