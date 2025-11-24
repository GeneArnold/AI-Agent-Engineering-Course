# Module 4: Multi-Agent & Evaluation

## 🔒 Releases December 22, 2024 (Week 4)

Coordinate multiple specialized agents and implement evaluation to measure quality—scale beyond single-agent systems.

## Learning Objectives
- Design role-based agent architectures
- Implement message passing and shared state
- Set budget gates and termination criteria
- Build simple evaluators for quality checks

## Concepts Covered
- Planner → Worker → Critic pattern
- Shared state management
- Orchestration and coordination
- Termination logic (steps, cost, success)
- Observability for multi-agent systems
- Success criteria and regression testing

## Project: `multi_agent_system.py`

### Requirements
- Three agent roles with distinct responsibilities:
  - **Planner**: Breaks down tasks, sets objectives
  - **Worker**: Executes actions, uses tools
  - **Critic**: Reviews outputs, flags issues
- Shared state dictionary (messages, tasks, scratch space)
- Message passing between agents
- Simple evaluator that checks acceptance criteria
- Budget gates: max steps, max cost

### Success Criteria
✅ Planner → Worker → Critic handoff completes successfully
✅ Shared state tracks all agent interactions
✅ Evaluator flags weak outputs with specific reasons
✅ System respects budget constraints
✅ Logs show full trace of agent coordination

## Files in This Module
- `multi_agent_system.py` - Orchestrated multi-agent system
- `logs/` - JSONL traces of agent interactions
- `evaluator.py` - Quality checking logic
- `reflections.md` - Your learning notes

## Reflection Questions
After completing this module, answer:
1. What improved with role separation?
2. Where did orchestration add unnecessary complexity?
3. How would you simplify the coordination?
4. What evaluation metrics matter most for your use cases?
5. When is multi-agent overkill vs necessary?

## Coming December 22, 2024

**This module releases in Week 4.** Until then:
- Complete Modules 1-3
- Master tool systems and local models
- Get ready for multi-agent orchestration!

---

## Next Step
MCP Add-On: Standardize your tools with the Model Context Protocol (Dec 29)
