# Module 1: Agent Foundations

**Week 1 - Estimated time: 2-3 hours**

## 🎯 Learning Objectives

By the end of this module, you will:
- ✅ Understand how LLM calls work (prompts → tokens → completion)
- ✅ Build a complete agent loop from scratch
- ✅ Implement tool calling with JSON contracts
- ✅ Add structured logging for observability
- ✅ Recognize the context growth problem (preview of Module 2)

## 📖 What You'll Build

**Project:** `simple_agent.py`

A working weather agent that:
- Accepts user queries ("What's the weather in Seattle?")
- Calls an LLM (OpenAI or Anthropic)
- Uses a `get_weather` tool when needed
- Logs every step to JSONL format
- Returns a friendly answer

**Example interaction:**
```
User: "What's the weather in Seattle?"

Iteration 1:
  → LLM requests: get_weather("Seattle")
  → Tool returns: "72°F, Sunny"

Iteration 2:
  → LLM synthesizes: "The weather in Seattle is 72°F and sunny!"
  → Loop exits (done=true)
```

## 🧠 Prerequisites

- Completed [Module 0: Setup](../setup/README.md)
- Python basics (functions, loops, dictionaries)
- Curiosity about how agents work!

## 📚 Learning Path

### Step 1: Learn the Concepts

Read [CONCEPTS.md](CONCEPTS.md) to understand:
1. LLM Call Anatomy
2. Agent Loop Fundamentals
3. JSON Contracts & Function Calling

**Estimated time:** 30 minutes

### Step 2: Review the Project Spec

Read [PROJECT.md](PROJECT.md) for:
- Detailed requirements
- Code structure guidance
- Success criteria

**Estimated time:** 15 minutes

### Step 3: Build It Yourself!

**Try building `simple_agent.py` on your own first!**

This is the best way to learn. Get stuck? That's good - it means you're learning!

**Estimated time:** 1-2 hours (with experimentation)

### Step 4: Compare with Solution

After you've attempted it, check `SOLUTION/` (released Week 1) to see a reference implementation.

**Things to compare:**
- Did you handle the loop the same way?
- How does your logging compare?
- What did you do differently?

### Step 5: Reflect

Answer these questions (mentally or in writing):
- What surprised you about how simple/complex the loop is?
- What clicked for you conceptually?
- Where did structure break (bad JSON, tool args)?
- How did logging help debug issues?

## 🎓 How to Use This Module

### With Claude Code (Recommended)

```bash
cd AI-Agent-Engineering-Course
claude-code
```

Then say:
```
"Start Module 1"
```

Claude Code will:
1. Teach you the concepts interactively
2. Guide you through building the agent
3. Help you debug and understand
4. Commit your completed work

### Without Claude Code

1. Read [CONCEPTS.md](CONCEPTS.md) carefully
2. Read [PROJECT.md](PROJECT.md) for specs
3. Create `simple_agent.py` yourself
4. Test it with different queries
5. Compare with `SOLUTION/` when released
6. Reflect on what you learned

## 🧪 Testing Your Agent

Once built, test with these queries:

```bash
python module_1_foundations/simple_agent.py
```

**Test cases:**
- "What's the weather in Seattle?"
- "How's the weather in Tokyo?"
- "Is it raining in London?"

**What to verify:**
- ✅ Agent completes in 2 iterations
- ✅ Tool is called with correct arguments
- ✅ Final answer is friendly and accurate
- ✅ JSONL logs are created in `logs/`
- ✅ Logs show tokens, latency, tool calls

## 📊 Expected Results

**Successful run:**
```
🤖 AGENT STARTING
Query: What's the weather in Seattle?

--- Iteration 1 ---
🔧 Tool call: get_weather({'city': 'Seattle'})
📊 Result: 72°F, Sunny

--- Iteration 2 ---
✅ Final answer: The weather in Seattle is currently 72°F and sunny!

✅ AGENT COMPLETE (took 2 iterations)
```

**Log file** (`logs/simple_agent.jsonl`):
```json
{"timestamp": "...", "event_type": "llm_call", "tokens": 131, ...}
{"timestamp": "...", "event_type": "tool_execution", "tool": "get_weather", ...}
{"timestamp": "...", "event_type": "llm_call", "tokens": 161, ...}
{"timestamp": "...", "event_type": "completion", "result": "..."}
```

## 🎯 Success Criteria

You've completed Module 1 when:
- ✅ Your agent runs end-to-end without errors
- ✅ It successfully calls the weather tool
- ✅ It completes in 2-3 iterations for simple queries
- ✅ JSONL logs are structured and complete
- ✅ You can explain how the agent loop works
- ✅ You understand why LLMs need tools

## 💡 Common Issues & Tips

### Issue: Agent loops forever
**Cause:** No stop condition or max iterations
**Fix:** Add `max_iterations` safety limit

### Issue: Tool not being called
**Cause:** Tool description unclear or missing from LLM call
**Fix:** Review the JSON contract, make description specific

### Issue: JSON parsing errors
**Cause:** LLM returns malformed JSON
**Fix:** Use low temperature (0.1-0.3) for deterministic tool calls

### Issue: Logs not being created
**Cause:** Directory doesn't exist
**Fix:** Use `os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)`

## 🚀 Going Further (Optional)

After completing the basics, try:

**Challenge 1: Add a second tool**
- Create `calculate(expression)` tool
- Test: "What's the weather in Seattle and what's 15 + 27?"

**Challenge 2: Better error handling**
- Handle API failures gracefully
- Retry logic for transient errors

**Challenge 3: Multi-turn conversations**
- Accept user input in a loop
- Maintain conversation history

**Challenge 4: Cost tracking**
- Calculate total cost from token usage
- Log cost per query

## 📝 Reflection Questions

After completing Module 1, consider:

1. **What surprised you?**
   - Was the agent loop simpler or more complex than expected?
   - What was the biggest "aha" moment?

2. **Context growth observation:**
   - How do tokens grow with each iteration?
   - What happens with 5+ tool calls?
   - How would you solve this? (Preview: Module 2!)

3. **Design decisions:**
   - Why use JSONL instead of regular logs?
   - Why is temperature important for tool calls?
   - When would you use higher max_iterations?

## 📚 Additional Resources

- [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)
- [Anthropic Tool Use](https://docs.anthropic.com/claude/docs/tool-use)
- [JSON Schema Reference](https://json-schema.org/understanding-json-schema)

## ➡️ Next Module

Once you've completed Module 1, you're ready for:

**[Module 2: Memory & Context](../module_2_memory/README.md)** (Released Week 1)

This module solves the context growth problem you discovered in Module 1!

---

**Questions?** [Open an issue](https://github.com/GeneArnold/AI-Agent-Engineering-Course/issues)

**Ready to start?** Read [CONCEPTS.md](CONCEPTS.md) →
