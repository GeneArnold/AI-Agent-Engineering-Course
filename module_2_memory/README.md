# Module 2: Memory & Context

## 🔒 Releases December 8, 2024 (Week 2)

Give your agent long-term memory using vector databases and RAG. Solve the context growth problem from Module 1.

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
- How ChatGPT and Claude "remember" conversations
- Why RAG is the standard pattern for agent memory
- How to build cost-effective, long-running agents
- When to use vector memory vs other strategies

---

## Prerequisites

✅ **Complete Module 1: Agent Foundations**
- Understand agent loops and tool calling
- Familiarity with JSONL logging
- Awareness of context growth problem

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
10 messages:   200 tokens/query
100 messages:  200 tokens/query ✅
1000 messages: 200 tokens/query ✅

Token usage stays constant!
```

---

## What You'll Build

A memory-enabled agent that:
- Stores conversations in ChromaDB (vector database)
- Retrieves relevant facts before responding
- Persists memory across sessions
- Keeps token usage constant
- Demonstrates RAG in action

**Example:**
```
Session 1:
User: "My name is Gene"
[Stored in vector DB]

Session 2 (next day):
User: "What's my name?"
Agent: "Your name is Gene!"
[Retrieved from memory semantically]
```

---

## Module Structure

When this module releases on **December 8**, you'll get:

- **CONCEPTS.md** - Theory: embeddings, vectors, RAG
- **PROJECT.md** - Architecture, design decisions, and seed questions
- **SOLUTION/memory_agent.py** - Complete working memory agent
- **Seed questions** - 18 guided questions for Claude Code

---

## Coming December 8, 2024

**This module releases in Week 2.** Until then:
- Complete Module 1 (releases December 1)
- Understand the context growth problem
- Get ready to build scalable agents!

---

## Next Module

**Module 3: Tools & Local Models** (Week 3 - December 15)
- Dynamic tool registries
- Multiple tool coordination
- Local LLM deployment with Ollama
- Quantization and performance

---

**Stay tuned!** Module 2 drops December 8th. Complete Module 1 first.
