# Testing Multi-Agent System

## Option A: Quick Test (No API Key Required) ⭐ RECOMMENDED

Run the mock version to verify orchestration logic:

```bash
cd module_4_multi_agent
source ../venv/bin/activate
python SOLUTION/test_multi_agent_mock.py
```

This tests:
- ✅ Worker revision on first rejection
- ✅ Escalation to Planner on second rejection
- ✅ Failure handling after max attempts
- ✅ Budget tracking throughout
- ✅ All orchestration logic verified

**Advantage:** Tests all the multi-agent patterns without needing an API key!

## Option B: Full Test (Requires OpenAI API Key)

**Prerequisites:**
1. Valid OpenAI API key with available credits
2. `.env` file in project root with `OPENAI_API_KEY=your-key-here`

**Note:** If you get a 403 error, your API key may be:
- Expired or invalid
- Missing required permissions
- From a free tier account that has expired

**Solution:** Use Option A (mock test) instead - it verifies all the same logic!

**To run full test:**

```bash
cd module_4_multi_agent
source ../venv/bin/activate
python SOLUTION/multi_agent_system.py
```

## What You'll See

The system will:
1. **Planner** creates execution plan
2. **Worker** attempts to execute
3. **Critic** reviews and provides feedback
4. **Orchestrator** decides: retry, escalate, or succeed
5. **Logs** saved to `logs/multi_agent_system.jsonl`

## Expected Output

Success case (2-3 iterations):
```
✅ SUCCESS!
Completed in 2 iterations
Total tokens: ~3,000-5,000
```

Check the logs for full execution trace!
