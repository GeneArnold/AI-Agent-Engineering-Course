# Module 2 Project: Memory-Enabled Agent

## How to Use This Document

You're reading the architecture guide for Module 2's solution. The working code is in `SOLUTION/memory_agent.py`.

**Your learning path:**
1. ✅ Read CONCEPTS.md (theory - embeddings, RAG, vector databases)
2. ➡️ Read this PROJECT.md (architecture - how it's designed)
3. ➡️ Study SOLUTION/memory_agent.py (the working code)
4. ➡️ Ask Claude Code the seed questions below
5. ➡️ Experiment and modify the code

---

## What This Agent Does

This agent demonstrates **long-term memory** using vector storage and RAG (Retrieval-Augmented Generation).

**Capabilities:**
- Stores every conversation in a vector database (ChromaDB)
- Retrieves relevant past facts before responding
- Maintains memory across multiple sessions (persistent storage)
- Keeps token usage constant regardless of conversation length
- Logs all memory operations for observability

**Example interaction:**
```
Session 1:
User: "My name is Gene and I love Python"
Agent: "Nice to meet you, Gene! Python is a great language."
[Stores: "User's name is Gene", "User loves Python"]

Session 2 (next day):
User: "What's my name?"
Agent: "Your name is Gene!"
[Retrieved from memory: "User's name is Gene"]

User: "What programming language do I like?"
Agent: "You love Python!"
[Retrieved from memory: "User loves Python"]
```

---

## Architecture Overview

### The RAG Pattern

This agent implements the classic RAG (Retrieval-Augmented Generation) pattern:

```
┌──────────────────────────────────────────────────────────┐
│                    Memory Agent                          │
│                                                          │
│  ┌────────────┐                    ┌─────────────────┐  │
│  │ User Query │─────────┐          │  ChromaDB       │  │
│  └────────────┘         │          │  (Vector Store) │  │
│                         ▼          └────────┬────────┘  │
│                  ┌──────────────┐           │           │
│                  │   Embedding  │───────────┘           │
│                  └──────┬───────┘      ▲                │
│                         │              │                │
│                         ▼              │ Store          │
│                  ┌──────────────┐     │                │
│                  │Vector Search │─────┘                │
│                  └──────┬───────┘                       │
│                         │                               │
│                         ▼                               │
│                  ┌──────────────┐                       │
│                  │Retrieved     │                       │
│                  │Facts (top 3) │                       │
│                  └──────┬───────┘                       │
│                         │                               │
│                         ▼                               │
│            ┌────────────────────────┐                   │
│            │  LLM Call with Facts   │                   │
│            │  (OpenAI GPT-4o-mini)  │                   │
│            └──────────┬─────────────┘                   │
│                       │                                 │
│                       ▼                                 │
│            ┌────────────────────┐                       │
│            │  Response          │                       │
│            └────────────────────┘                       │
└──────────────────────────────────────────────────────────┘
```

**Flow:**
1. User asks a question
2. Convert question to embedding (vector)
3. Search vector database for similar past facts
4. Retrieve top 3-5 most relevant facts
5. Include retrieved facts in LLM prompt
6. LLM generates answer using those facts
7. Store new conversation turn in vector DB
8. Return answer to user

---

## Tools & Technologies

### ChromaDB - Vector Database

**What it is:**
- Lightweight vector database that runs locally
- No server setup required (embedded mode)
- Handles embeddings automatically
- Persistent storage across restarts

**Why we chose it:**
- Easy setup: `pip install chromadb`
- Perfect for learning (simple API)
- Good performance for small-medium datasets
- Built-in embedding support

**Alternatives:**
- FAISS: Faster, but more complex setup
- Pinecone: Cloud-hosted, costs money
- Weaviate/Qdrant: Production-grade, more features

**About Embedded Mode:**
This agent uses ChromaDB in embedded mode (single-process). Memory persists to disk and survives restarts, which is perfect for personal agents. Note: If you run multiple agent sessions simultaneously, they won't see each other's changes until restarted (each loads the database state at startup). For multi-user or production scenarios, use ChromaDB in server mode instead.

### OpenAI Embeddings

**Model:** `text-embedding-3-small`

**What it does:**
- Converts text to 1536-dimensional vectors
- Captures semantic meaning as numbers
- Same text always produces same embedding

**Why we use it:**
- High quality embeddings
- Fast (< 200ms per embedding)
- Cheap ($0.00002 per 1K tokens)
- Consistent and reliable

**Alternatives:**
- `text-embedding-3-large`: More accurate, larger, more expensive
- Sentence Transformers: Local, free, good quality
- Cohere: Specialized for search tasks

### RAG (Retrieval-Augmented Generation)

**What it solves:**
- Context growth problem from Module 1
- Token costs scaling with conversation length
- Context window limits

**How it works:**
- Store everything in vector DB (infinite memory)
- Retrieve only relevant facts (top-k)
- Include only relevant context in prompts (lean prompts)
- Token usage stays constant

**Cost comparison:**
| Approach | 50-message conversation | Tokens/query |
|----------|------------------------|--------------|
| Naive (all history) | 8,000 tokens | $0.40 |
| RAG (top-3 facts) | 600 tokens | $0.03 |
| **Savings** | **13x cheaper** | **93% reduction** |

---

## Component Breakdown

### Component 1: MemoryManager Class

**Purpose:** Handle all vector database operations

**Responsibilities:**
- Initialize ChromaDB collection
- Store facts with embeddings
- Search for similar facts
- Provide memory statistics
- Clear all memory when needed

**Key methods:**
```python
class MemoryManager:
    def __init__(self, collection_name: str)
        # Initialize ChromaDB client and collection

    def store_fact(self, text: str, metadata: dict) -> None
        # Store a fact in vector DB
        # ChromaDB handles embedding automatically

    def retrieve_relevant(self, query: str, top_k: int = 3) -> list[dict]
        # Search for relevant facts
        # Returns list of {text, metadata, distance} dicts

    def get_stats(self) -> dict
        # Return memory statistics (total facts, etc.)

    def clear_memory(self) -> int
        # Delete all facts from memory
        # Returns number of facts deleted
```

**Design decisions:**
- ChromaDB auto-generates embeddings (we don't need to call OpenAI separately)
- Metadata stores: timestamp, role (user/agent), session_id
- top_k=3 balances context vs relevance (experiments show 3-5 is optimal)
- Persistent storage: survives agent restarts

### Component 2: Agent Loop with RAG

**Purpose:** Main agent logic integrating memory retrieval

**Flow:**
```python
def agent_loop(user_query: str) -> str:
    # 1. Retrieve relevant facts from memory
    relevant_facts = memory.retrieve_relevant(user_query, top_k=3)

    # 2. Construct prompt with retrieved facts
    context = "\n".join([f"- {fact['text']}" for fact in relevant_facts])
    system_message = f"""You are a helpful assistant with memory.

Relevant facts from past conversations:
{context}

Use these facts when relevant to answer the user's question."""

    # 3. Call LLM with lean prompt
    response = llm_call(system_message, user_query)

    # 4. Store new facts in memory for future retrieval
    memory.store_fact(
        text=f"User said: {user_query}",
        metadata={"role": "user", "timestamp": now(), "session_id": session_id}
    )
    memory.store_fact(
        text=f"Agent responded: {response}",
        metadata={"role": "agent", "timestamp": now(), "session_id": session_id}
    )

    # 5. Return response
    return response
```

**Key insights:**
- No message history array (unlike Module 1)
- Only relevant facts go into prompt
- Token usage stays constant
- Memory grows infinitely without cost increase

### Component 3: Interactive Chat Interface

**Purpose:** User-friendly conversation loop

**Features:**
```python
def chat():
    print("Memory Agent - Use slash commands: /exit, /stats, /reset")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "/exit":
            break
        elif user_input.lower() == "/stats":
            show_memory_stats()
            continue
        elif user_input.lower() == "/reset":
            # Confirm before clearing memory
            confirm = input("Type 'yes' to confirm: ")
            if confirm.lower() == "yes":
                memory.clear_memory()
            continue

        response = agent_loop(user_input)
        print(f"Agent: {response}")
```

**Commands (slash-prefixed to avoid confusion with conversation):**
- `/exit`: Quit the agent
- `/stats`: Show memory statistics (total facts, collection size)
- `/reset`: Clear all memory (requires confirmation)
- Any other text: Process as user query

**Why slash commands?** Prevents accidental command triggers - users can naturally say "I need to rest" or "Can you give me stats?" without triggering commands.

### Component 4: JSONL Logging

**Purpose:** Complete observability of memory operations

**Log events:**

**Event 1: Memory Storage**
```json
{
  "timestamp": "2024-11-24T10:15:30Z",
  "event_type": "memory_store",
  "text": "User said: My name is Gene",
  "metadata": {"role": "user", "session_id": "abc123"},
  "collection": "agent_memory"
}
```

**Event 2: Memory Retrieval**
```json
{
  "timestamp": "2024-11-24T10:16:45Z",
  "event_type": "memory_retrieval",
  "query": "What's my name?",
  "results": [
    {"text": "User said: My name is Gene", "distance": 0.15},
    {"text": "User loves Python", "distance": 0.82}
  ],
  "top_k": 3,
  "retrieval_time_ms": 45
}
```

**Event 3: LLM Call**
```json
{
  "timestamp": "2024-11-24T10:16:46Z",
  "event_type": "llm_call",
  "model": "gpt-4o-mini",
  "prompt_tokens": 150,
  "completion_tokens": 25,
  "facts_used": 2,
  "latency_ms": 850,
  "cost_usd": 0.002
}
```

**Event 4: Memory Reset**
```json
{
  "timestamp": "2024-11-24T10:20:00Z",
  "event_type": "memory_reset",
  "facts_deleted": 12,
  "collection": "agent_memory"
}
```

**Why logging matters:**
- See exactly what facts were retrieved
- Measure retrieval performance
- Calculate cost savings
- Debug relevance issues
- Understand agent behavior
- Track when memory is cleared

---

## Key Design Decisions

### Decision 1: Why ChromaDB?

**Chosen:** ChromaDB
**Alternatives:** FAISS, Pinecone, Weaviate

**Reasoning:**
- No server setup (embedded mode)
- Auto-handles embeddings
- Good performance for learning
- Persistent storage built-in
- Simple API

**Trade-offs:**
- Not fastest for massive scale (FAISS is faster)
- Not cloud-hosted (Pinecone is easier for production)
- Perfect for learning and prototypes

### Decision 2: Why top_k=3?

**Chosen:** Retrieve top 3 most relevant facts
**Alternatives:** 1, 5, 10, or threshold-based

**Reasoning:**
- Experiments show 3-5 facts is sweet spot
- More than 5: diminishing returns (less relevant facts)
- Less than 3: might miss important context
- 3 provides good balance

**When to adjust:**
- top_k=1: Simple questions, single fact needed
- top_k=5: Complex questions, more context helps
- threshold: Filter by distance score (advanced)

### Decision 3: Why Store Both User and Agent Messages?

**Chosen:** Store both sides of conversation
**Alternative:** Only store user messages

**Reasoning:**
- Agent responses contain synthesized information
- Future queries might relate to agent's answers
- Richer memory = better retrieval
- Minimal extra cost

**Example:**
```
User: "What's the capital of France?"
Agent: "Paris is the capital of France, with 2.1M population."

Later query: "Tell me about that city with 2M people"
→ Retrieves agent's response (has population info)
```

### Decision 4: Why Auto-Embedding?

**Chosen:** Let ChromaDB generate embeddings
**Alternative:** Call OpenAI embedding API ourselves

**Reasoning:**
- Simpler code (ChromaDB handles it)
- Consistent embedding model
- One less API call to manage
- ChromaDB caches embeddings

**Trade-off:**
- Less control over embedding model
- For learning, simplicity > control

---

## File Structure

```
module_2_memory/
├── CONCEPTS.md           # Theory you already read
├── PROJECT.md            # This file
├── README.md             # Module overview
├── SOLUTION/
│   └── memory_agent.py   # Complete working agent
└── data/
    └── chroma_db/        # Persistent vector storage (created at runtime)
```

---

## Configuration

The agent uses these key settings:

```python
# ChromaDB collection name
CHROMA_COLLECTION_NAME = "agent_memory"

# Number of facts to retrieve
MEMORY_TOP_K = 3

# LLM model
MODEL = "gpt-4o-mini"

# Log file location
LOG_FILE = "../logs/memory_agent.jsonl"
```

You can experiment with these values (especially MEMORY_TOP_K) to see how it affects performance.

---

## Testing & Verification

### Success Criteria

Your agent is working when:

1. ✅ **Memory persists across sessions**
   - Stop agent, restart it, ask about previous conversation
   - Agent correctly recalls past facts

2. ✅ **Semantic retrieval works**
   - User: "My favorite color is blue"
   - Later: "What color do I like?"
   - Agent: "You like blue" (retrieved semantically, not keyword match)

3. ✅ **Token usage stays constant**
   - 10-message conversation: ~200 tokens/query
   - 100-message conversation: Still ~200 tokens/query
   - Without RAG: Would be 2000+ tokens/query

4. ✅ **Logs show memory operations**
   - Storage events logged
   - Retrieval events logged with distances
   - Cost savings calculable from logs

5. ✅ **Interactive mode works smoothly**
   - Multi-turn conversations
   - `stats` command shows memory info
   - `exit` command works cleanly

### Testing Checklist

Before considering Module 2 complete:

- [ ] Fresh start: Agent with no memory can have basic conversation
- [ ] Memory storage: Facts are stored after each message
- [ ] Memory retrieval: Relevant facts are found for queries
- [ ] Session persistence: Restart agent, memory still available
- [ ] Semantic search: Similar meaning queries find right facts
- [ ] Token efficiency: Prompt size doesn't grow with conversation length
- [ ] Logs complete: All memory operations logged
- [ ] Stats command: Shows accurate memory information
- [ ] Multi-session: Multiple conversations don't interfere

---

## Questions to Ask Your Professor (Claude Code)

### 🌱 Getting Started (Start Here!)

These questions will help you understand the basics:

1. **"Walk me through the MemoryManager class - how does it interact with ChromaDB?"**
   - Understand initialization, storage, and retrieval

2. **"Explain the RAG flow step-by-step using the actual code"**
   - Trace a query from user input to final response

3. **"Why do we use ChromaDB instead of FAISS or Pinecone?"**
   - Understand tool selection reasoning

4. **"Show me where embeddings are generated and how they're used"**
   - See the embedding process in action

5. **"How does this agent loop differ from Module 1's simple_agent?"**
   - Compare and contrast the approaches

6. **"What's the significance of the 'distance' score in retrieval results?"**
   - Understand relevance ranking

7. **"Walk me through what happens when I type '/stats'"**
   - Trace the slash command execution

### 🌿 Going Deeper (Once You Understand Basics)

8. **"Why top_k=3? What happens if I change it to 5 or 1?"**
   - Experiment with retrieval parameters

9. **"Explain the metadata we're storing and why it matters"**
   - Understand role, timestamp, session_id

10. **"How does token usage stay constant even with long conversations?"**
    - See the cost savings in action

11. **"What would happen if I removed the metadata from storage?"**
    - Understand the purpose of each component

12. **"Show me in the logs: where are the cost savings compared to Module 1?"**
    - Analyze the JSONL logs for evidence

13. **"How does ChromaDB know to embed text automatically?"**
    - Understand the auto-embedding feature

14. **"What's the difference between storing user messages vs agent responses?"**
    - See why we store both sides

### 🌳 Advanced Understanding

15. **"How would I add timestamp filtering to only retrieve recent memories?"**
    - Learn about metadata filtering

16. **"What are the trade-offs between RAG and just using a large context window?"**
    - Compare approaches and when each is appropriate

17. **"Walk me through what happens during a cold start (no prior memories)"**
    - Understand edge cases

18. **"How would this agent handle multiple users? What would need to change?"**
    - Think about scaling and multi-tenancy

---

## Experiments to Try

### Experiment 1: Change top_k
```python
# In memory_agent.py, change:
MEMORY_TOP_K = 3  # Try 1, 5, 10

# Run agent and observe:
# - Does retrieval quality change?
# - Do you get irrelevant facts with high top_k?
# - Do you miss context with low top_k?
```

### Experiment 2: Add Metadata Filtering
```python
# Modify retrieve_relevant() to filter by timestamp:
results = collection.query(
    query_texts=[query],
    n_results=top_k,
    where={"timestamp": {"$gte": one_week_ago}}  # Only recent
)
```

### Experiment 3: Compare Embedding Models
```python
# Try different embedding models:
# - text-embedding-3-small (default)
# - text-embedding-3-large (more accurate)
# - sentence-transformers (local)

# Compare: retrieval quality, cost, speed
```

### Experiment 4: Break It Intentionally
```python
# What happens if you:
# - Comment out the memory.store_fact() calls?
# - Set top_k=0?
# - Delete the chroma_db/ folder while agent is running?

# Learn by breaking!
```

### Experiment 5: Add Conversation Summarization
```python
# When conversation gets long, summarize old facts:
if len(memory.get_all()) > 100:
    old_facts = memory.get_oldest(50)
    summary = llm.summarize(old_facts)
    memory.store_fact(summary, metadata={"type": "summary"})
    memory.delete(old_facts)
```

---

## Going Further (Optional Enhancements)

If you want to extend this agent:

### Enhancement 1: Multi-User Support
```python
# Filter memories by user_id
memory.retrieve_relevant(
    query,
    where={"user_id": current_user}
)
```

### Enhancement 2: Importance Scoring
```python
# Weight facts by importance
memory.store_fact(
    text,
    metadata={"importance": 0.9}  # High importance
)
```

### Enhancement 3: Memory Decay
```python
# Older memories retrieved less frequently
# Adjust distance scores by age
distance_adjusted = distance * (1 + age_in_days * 0.1)
```

### Enhancement 4: Semantic Search UI
```python
# Add a search command:
if user_input.startswith("/search "):
    query = user_input[8:]
    results = memory.retrieve_relevant(query, top_k=10)
    print_search_results(results)
```

---

## Key Takeaways

After studying this module, you should understand:

1. **RAG is simple** - Just retrieve + include in prompt
2. **Vector search is powerful** - Finds meaning, not just keywords
3. **Memory changes everything** - Agents become truly conversational
4. **Cost savings are real** - 10-15x cheaper for long conversations
5. **This is how production works** - ChatGPT, Claude, Copilot all use RAG

---

## What's Next?

After completing Module 2:

1. **Test thoroughly** - Run through testing checklist
2. **Analyze logs** - Understand retrieval patterns
3. **Compare costs** - Calculate real savings vs Module 1
4. **Reflect** - Answer the reflection questions in README.md
5. **Update your learning journal** - What clicked? What surprised you?

**Then move to Module 3:** Multi-tool agents and local models!

---

## Summary: From Module 1 to Module 2

**Module 1 Problem:**
- Context grows linearly with conversation
- Token costs increase per turn
- Eventually hit context limits

**Module 2 Solution:**
- Store everything in vector DB (infinite memory)
- Retrieve only relevant facts (constant token usage)
- Semantic search finds meaning (not just keywords)

**The Evolution:**
```
Module 1: messages = [] → Keep growing → 💥 Boom
Module 2: vector_db.store() → Retrieve relevant → ✅ Scales forever
```

---

**Ready to study the code?** Open `SOLUTION/memory_agent.py` and start asking Claude Code those seed questions!
