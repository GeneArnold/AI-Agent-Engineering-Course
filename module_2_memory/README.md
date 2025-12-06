# Module 2: Memory & Context

## Overview

Give your agent long-term memory using vector databases and RAG (Retrieval-Augmented Generation). Build a memory-enabled agent that remembers conversations across sessions and solves the context growth problem from Module 1.

---

## How to Use This Module

**Follow this learning path:**

1. **Read CONCEPTS.md** - Understand embeddings, vector databases, and RAG
2. **Read PROJECT.md** - Learn the architecture and tools (ChromaDB, etc.)
3. **Study SOLUTION/memory_agent.py** - Examine the working implementation
4. **Ask Claude Code questions** - Use seed questions from PROJECT.md
5. **Experiment** - Modify the code and test changes

**Remember:** Claude Code is your tutor. The solution exists - your goal is to understand it deeply and experiment with modifications.

---

## What You'll Learn

### Core Concepts
- **Embeddings** - Text as semantic coordinates in vector space
- **Vector databases** - Storage and similarity search (ChromaDB)
- **RAG** - Retrieval-Augmented Generation pattern
- **Context management** - Token efficiency with memory
- **Cosine similarity** - Measuring semantic distance

### Practical Skills
- Setting up ChromaDB for persistent storage
- Implementing RAG in an agent loop
- Managing memory operations (store/retrieve)
- Logging memory events for observability
- Measuring cost savings vs naive approaches

### Key Insights
- How ChatGPT and Claude "remember" your conversations
- Why RAG is the standard pattern for agent memory
- How to build cost-effective, long-running agents
- When to use vector memory vs other strategies

---

## Prerequisites

✅ **Complete Module 1: Agent Foundations**
- You should understand agent loops and tool calling
- Familiarity with JSONL logging
- Understanding of context growth problem

---

## What This Module Solves

**Problem from Module 1:**
```
Iteration 1: 117 tokens
Iteration 2: 143 tokens (+26)
Iteration 3: 180 tokens (+37)
...
Iteration 20: 💥 Context limit exceeded
```

**Solution in Module 2:**
```
Conversation length: 10 messages → 200 tokens/query
Conversation length: 100 messages → 200 tokens/query ✅
Conversation length: 1000 messages → 200 tokens/query ✅

Token usage stays constant!
```

---

## Files in This Module

```
module_2_memory/
├── README.md              ← You are here
├── CONCEPTS.md            ← Theory: embeddings, vectors, RAG
├── PROJECT.md             ← Architecture, design decisions, seed questions
└── SOLUTION/
    └── memory_agent.py    ← Complete working agent with memory
```

### What Each File Does

**CONCEPTS.md**
Theory and fundamentals:
- What are embeddings and how do they work?
- How do vector databases enable similarity search?
- What is RAG and why does it matter?
- Context window management strategies

**PROJECT.md**
Architecture and tools:
- How the memory agent is designed
- Why ChromaDB, why OpenAI embeddings
- Component breakdown (MemoryManager, RAG loop)
- Key design decisions explained
- **18 seed questions** to ask Claude Code
- Experiments to try

**SOLUTION/memory_agent.py**
Working code with:
- MemoryManager class (ChromaDB wrapper)
- RAG-enabled agent loop
- Interactive chat interface
- JSONL logging for memory operations
- Extensive comments and documentation

---

## Learning Workflow Example

Here's a typical session with this module:

```
You: "I'm starting Module 2. What should I do first?"

Claude: "Great! Start by reading CONCEPTS.md to understand embeddings and RAG..."

[You read CONCEPTS.md]

You: "Okay, I read it. Can you explain embeddings using an analogy?"

Claude: "Think of embeddings as coordinates on a map of meaning..."

[Claude explains]

You: "That makes sense! Now I'm ready for PROJECT.md."

[You read PROJECT.md]

You: "Walk me through the MemoryManager class - how does it work?"

Claude: "Let's open SOLUTION/memory_agent.py. The MemoryManager class..."

[Claude explains the code step-by-step]

You: "Now I want to run it and see it work."

[You run: python module_2_memory/SOLUTION/memory_agent.py]

You: "Cool! What happens if I change top_k from 3 to 5?"

Claude: "Good experiment! Let's try it..."

[You experiment and observe the changes]
```

---

## Key Features of This Agent

**Long-term Memory:**
- Stores conversations in ChromaDB (vector database)
- Persists across sessions (restart agent, memory remains)
- Semantic search (finds meaning, not just keywords)

**RAG Integration:**
- Retrieves top-3 relevant facts before each response
- Includes only relevant context in prompts
- Token usage stays constant regardless of conversation length

**Interactive Mode:**
- Multi-turn conversations
- `stats` command shows memory information
- `exit` command to quit cleanly

**Complete Logging:**
- Memory storage events
- Memory retrieval events (with distance scores)
- LLM calls with token usage
- Cost comparison data

---

## Success Criteria

You'll know you've mastered Module 2 when you can:

✅ Explain how embeddings capture semantic meaning
✅ Describe the RAG pattern and why it's useful
✅ Walk through the memory_agent.py code confidently
✅ Modify the agent (change top_k, add features)
✅ Explain design decisions (why ChromaDB? why top_k=3?)
✅ Calculate and demonstrate cost savings vs Module 1

---

## Testing Checklist

Before moving to Module 3, verify:

- [ ] Agent starts and can have basic conversation
- [ ] Facts are stored in ChromaDB after each turn
- [ ] Relevant facts are retrieved for queries
- [ ] Memory persists after restarting the agent
- [ ] Semantic search works (similar meaning, different words)
- [ ] Token usage stays constant over long conversations
- [ ] JSONL logs capture all memory operations
- [ ] `stats` command shows accurate memory info
- [ ] Multiple sessions don't interfere with each other

---

## Reflection Questions

After completing this module, reflect on:

1. **How does RAG reduce token usage compared to Module 1?**
   - Calculate actual savings from your experiments

2. **Why is semantic search better than keyword search?**
   - Think about examples where meaning matters

3. **When would you skip RAG and use full context?**
   - Are there cases where RAG doesn't make sense?

4. **What did changing top_k teach you?**
   - How does retrieval count affect quality?

5. **What surprised you most about vector memory?**
   - What clicked? What was counterintuitive?

---

## Common Experiments

### Experiment 1: Test Semantic Search
```
Store: "My favorite color is blue"
Query: "What color do I like?"
Expected: Agent retrieves the fact even though words don't match exactly
```

### Experiment 2: Compare Token Usage
```
Run 10-turn conversation, check logs for token usage
Run 50-turn conversation, check logs again
Compare: Should be roughly the same!
```

### Experiment 3: Change top_k
```
Modify MEMORY_TOP_K = 3 to different values (1, 5, 10)
Observe: How does retrieval quality change?
```

### Experiment 4: Test Persistence
```
Have a conversation, then exit
Restart agent
Ask about previous conversation
Expected: Agent remembers!
```

---

## Troubleshooting

### "ChromaDB not found" Error
```bash
# Install ChromaDB:
pip install chromadb
```

### "No memories found" on Restart
- Check if `chroma_db/` folder exists in module directory
- Verify ChromaDB is using persistent storage (not in-memory)

### Retrieval Returns Irrelevant Facts
- Try adjusting top_k
- Check your query phrasing
- Look at distance scores in logs (higher = less relevant)

### Token Usage Still Growing
- Verify RAG retrieval is working (check logs)
- Ensure you're not including full message history
- Check that facts_used count is staying constant

---

## Pro Tips

**Tip 1: Study the Logs**
JSONL logs show exactly what's retrieved and why. Use them to understand retrieval patterns.

**Tip 2: Compare Distance Scores**
Low distance = high relevance. Watch how scores change with different queries.

**Tip 3: Break It Intentionally**
Comment out memory.store_fact() - what happens? Set top_k=0 - what breaks? Learn by breaking!

**Tip 4: Ask "Why" Questions**
Don't just learn HOW it works - understand WHY design decisions were made.

**Tip 5: Experiment Extensively**
The code works - now modify it! Change parameters, add features, test edge cases.

---

## Next Module

**Module 3: Tools & Local Models** (Coming December 15)

Build a multi-tool agent with support for local LLMs using Ollama. Learn about:
- Dynamic tool registries
- Multiple tool coordination
- Local model deployment
- Quantization and performance

---

## Getting Help

**From Claude Code (Your Professor):**
- Ask the seed questions in PROJECT.md
- Request explanations of specific code sections
- Get help experimenting with modifications

**From the Code:**
- Read the extensive comments
- Trace execution flow
- Study the logging output

**From the Logs:**
- See what facts were retrieved
- Understand distance scoring
- Track token usage patterns

---

## Quick Start

Ready to begin?

1. Open CONCEPTS.md and read about embeddings and RAG
2. Open PROJECT.md for architecture and design
3. Run the agent: `python module_2_memory/SOLUTION/memory_agent.py`
4. Ask Claude Code the seed questions
5. Experiment with modifications
6. Complete the testing checklist
7. Answer the reflection questions

**Happy learning!** 🚀

---

**Last Updated:** November 24, 2024
**Estimated Time:** 1 week for deep understanding
**Difficulty:** Intermediate (builds on Module 1)
