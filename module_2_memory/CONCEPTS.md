# Module 2: Memory & Context - Core Concepts

**Goal:** Understand how to give agents memory and solve the context growth problem from Module 1.

---

## The Problem We're Solving

In Module 1, you discovered that conversation history grows with every iteration:

```
Iteration 1: 117 tokens
Iteration 2: 143 tokens (+26)
Iteration 3: 180 tokens (+37)
Iteration 4: 225 tokens (+45)
...
Iteration 20: 💥 Context limit exceeded
```

**Why this happens:**
- LLMs are stateless - they need the full conversation every time
- Each tool call adds to the history (request + result)
- Complex tasks = many tool calls = massive context
- Cost scales linearly: More tokens = more money
- Performance degrades: Larger context = slower responses

**Real-world example:**
A customer support agent handling a 50-message conversation:
- Naive approach: 12,000 tokens per response = $0.60/query
- With memory: 800 tokens per response = $0.04/query
- **15x cost savings!**

---

## Concept 1: Embeddings - Text as Coordinates

### What Are Embeddings?

Embeddings convert text into numerical vectors (arrays of numbers) that capture **meaning**.

**Example:**
```
"The cat sat on the mat"  →  [0.23, -0.81, 0.45, ..., 0.12]  (1536 numbers)
"A feline rested on a rug" →  [0.25, -0.79, 0.47, ..., 0.14]  (1536 numbers)
"Pizza delivery is late"   →  [-0.65, 0.33, -0.12, ..., 0.88] (1536 numbers)
```

Notice: The first two are **similar** (close values), the third is **different**.

### Why This Matters

Embeddings let us measure **semantic similarity**:
- Similar meanings = vectors close together
- Different meanings = vectors far apart
- We can search by meaning, not just keywords!

**Visual Analogy:**
Think of meaning-space as a 3D map:
- "cat", "kitten", "feline" are clustered together
- "car", "vehicle", "automobile" are clustered elsewhere
- Distance between points = semantic difference

### How Embeddings Are Created

**Using OpenAI's embedding model:**
```python
from openai import OpenAI

client = OpenAI()
response = client.embeddings.create(
    model="text-embedding-3-small",
    input="The cat sat on the mat"
)
embedding = response.data[0].embedding  # [0.23, -0.81, ...]
```

**Common embedding models:**
- OpenAI `text-embedding-3-small` (1536 dimensions, cheap)
- OpenAI `text-embedding-3-large` (3072 dimensions, more accurate)
- Sentence Transformers (local, free, good quality)
- Cohere embeddings (specialized for search)

### Key Properties

1. **Dimensionality:** Usually 384-3072 numbers per embedding
2. **Consistency:** Same text always produces same embedding
3. **Semantic preservation:** Similar text = similar embeddings
4. **Not reversible:** Can't turn embedding back into original text

---

## Concept 2: Vector Databases - Memory Storage

### What Is a Vector Database?

A specialized database that stores embeddings and enables **similarity search**.

**Traditional database:**
```sql
SELECT * FROM facts WHERE text = 'exact match only';
```

**Vector database:**
```python
# Find facts SIMILAR to this question (not exact match!)
results = vector_db.search(
    query_embedding=embed("What did I say about Seattle?"),
    top_k=3  # Get 3 most similar facts
)
```

### How Vector Search Works

**1. Storage:**
```python
facts = [
    "Seattle weather is usually 72°F and sunny",
    "Paris temperature is 18°C and rainy",
    "Tokyo is experiencing 28°C and cloudy"
]

# Convert each fact to embedding and store
for fact in facts:
    embedding = embed(fact)
    vector_db.add(embedding, metadata={"text": fact})
```

**2. Search:**
```python
# User asks: "How's the weather in Seattle?"
query = "How's the weather in Seattle?"
query_embedding = embed(query)

# Find most similar facts
results = vector_db.search(query_embedding, top_k=1)
# Returns: "Seattle weather is usually 72°F and sunny"
```

**3. The Magic:**
- Database computes distance between query embedding and all stored embeddings
- Returns the closest matches
- Works even if exact words don't match!

### Distance Metrics

How do we measure "closeness" between embeddings?

**Cosine Similarity** (most common):
- Measures angle between vectors
- Range: -1 (opposite) to 1 (identical)
- 0 = unrelated

**Euclidean Distance:**
- Straight-line distance in n-dimensional space
- Lower = more similar

**Example:**
```python
# Query: "feline animal"
# Fact 1: "cat" → cosine similarity = 0.92 (very similar!)
# Fact 2: "dog" → cosine similarity = 0.71 (somewhat similar)
# Fact 3: "car" → cosine similarity = 0.12 (not similar)
```

### Popular Vector Databases

**ChromaDB** (recommended for learning):
- Easy setup (pip install chromadb)
- Runs locally, no server needed
- Good for small to medium datasets
- Simple API

**FAISS** (Facebook AI Similarity Search):
- Extremely fast
- Handles billions of vectors
- Requires more setup
- Good for production scale

**Pinecone** (managed cloud service):
- Fully managed (no infrastructure)
- Auto-scales
- Costs money
- Good for production without DevOps

**Qdrant** (production-grade open source):
- High performance with Rust implementation
- Runs locally or as managed cloud service
- Rich filtering capabilities with metadata
- Good API and Python client
- Scales well for production workloads
- Docker deployment support

**Weaviate, Milvus:**
- Production-grade open source alternatives
- More features, more complexity

### ChromaDB Example

```python
import chromadb

# Create a database
client = chromadb.Client()
collection = client.create_collection("agent_memory")

# Add facts
collection.add(
    documents=["Seattle is sunny", "Paris is rainy"],
    ids=["fact1", "fact2"]
)

# Search
results = collection.query(
    query_texts=["What's the weather in Seattle?"],
    n_results=1
)
print(results['documents'][0])  # "Seattle is sunny"
```

---

## Concept 3: RAG (Retrieval-Augmented Generation)

### What Is RAG?

**Retrieval-Augmented Generation** = Retrieve relevant facts, then generate response

**The Pattern:**
```
1. User asks a question
2. Convert question to embedding
3. Search vector DB for relevant facts
4. Include retrieved facts in LLM prompt
5. LLM generates answer using those facts
6. Return answer to user
```

### RAG vs Context Stuffing

**Context Stuffing (Module 1):**
```python
# Include EVERYTHING in every LLM call
prompt = system_message + all_previous_messages + user_query
# Result: Huge token usage, high cost, eventual failure
```

**RAG (Module 2):**
```python
# Include only RELEVANT facts
relevant_facts = vector_db.search(user_query, top_k=3)
prompt = system_message + relevant_facts + user_query
# Result: Lean prompts, low cost, infinite conversation length
```

### RAG Architecture

```
┌─────────────┐
│ User Query  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Embedding  │ (Convert to vector)
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  Vector Search  │ (Find similar facts)
└──────┬──────────┘
       │
       ▼
┌─────────────────────┐
│ Retrieved Facts     │ (Top 3-5 most relevant)
└──────┬──────────────┘
       │
       ▼
┌──────────────────────────┐
│ LLM Prompt:              │
│ System: "You are..."     │
│ Facts: [retrieved facts] │
│ User: [query]            │
└──────┬───────────────────┘
       │
       ▼
┌─────────────┐
│ LLM Answer  │
└─────────────┘
```

### When RAG Helps

**Good for:**
- Long conversations (customer support, tutoring)
- Large knowledge bases (documentation, research)
- Personal memory (remember user preferences)
- Fact-heavy queries (when context matters)

**Not needed for:**
- Single-turn queries (no memory needed)
- Small context (fits in prompt easily)
- Real-time data (use API calls instead)

### RAG Example

**Without RAG:**
```
Conversation history: 2,000 tokens
User: "What did I say about my favorite color?"
LLM: "I don't see that in our recent conversation" ❌
Cost: $0.10
```

**With RAG:**
```
Query: "What did I say about my favorite color?"
Vector search: Finds "My favorite color is blue" (from 20 messages ago)
Prompt tokens: 150 (just query + retrieved fact)
LLM: "You said your favorite color is blue" ✅
Cost: $0.01
```

---

## Concept 4: Context Window Management

### The Context Window

Every LLM has a maximum context size:
- GPT-3.5: 16K tokens
- GPT-4: 8K - 128K tokens (depending on version)
- Claude 3: 200K tokens
- Llama 3: 8K - 128K tokens

**What happens when you exceed it:**
- Request fails with error
- OR: Oldest messages get truncated (you lose history)

### Memory Strategies

**1. Sliding Window (simple, lossy):**
```python
# Keep only last N messages
if len(messages) > 20:
    messages = messages[-20:]  # Drop older messages
```
**Pros:** Simple
**Cons:** Lose important information

**2. Summarization (moderate complexity):**
```python
# Summarize old messages
if len(messages) > 20:
    old_summary = llm.summarize(messages[:10])
    messages = [old_summary] + messages[10:]
```
**Pros:** Retains some info
**Cons:** Summaries lose detail

**3. Vector Memory (RAG - best):**
```python
# Store everything, retrieve relevant
for message in all_messages:
    vector_db.add(embed(message))

# Only include relevant facts in prompt
relevant = vector_db.search(query, top_k=5)
prompt = system + relevant + query
```
**Pros:** Nothing lost, only relevant info used
**Cons:** Requires vector database

### Token Usage Comparison

**Scenario:** 50-message customer support conversation

| Strategy | Tokens/Query | Cost/Query | Info Retained |
|----------|--------------|------------|---------------|
| Naive (all messages) | 8,000 | $0.40 | 100% |
| Sliding window (20 msg) | 3,000 | $0.15 | 40% |
| Summarization | 1,500 | $0.08 | 60% |
| **RAG (vector memory)** | **600** | **$0.03** | **100%** |

---

## Concept 5: Embedding Metadata & Filtering

### Metadata: Context for Your Facts

When storing facts, you can include metadata for filtering:

```python
collection.add(
    documents=["Seattle is sunny"],
    metadatas=[{
        "date": "2024-11-22",
        "source": "conversation",
        "user_id": "user_123",
        "topic": "weather"
    }],
    ids=["fact1"]
)
```

### Why Metadata Matters

**Search with filters:**
```python
# Find weather facts from THIS week only
results = collection.query(
    query_texts=["weather"],
    where={"date": {"$gte": "2024-11-20"}},
    n_results=5
)
```

**Use cases:**
- User-specific memory: `where={"user_id": current_user}`
- Recency: `where={"date": {"$gte": one_week_ago}}`
- Topic filtering: `where={"topic": "technical"}`
- Source filtering: `where={"source": "documentation"}`

---

## Putting It All Together

### The Memory-Enabled Agent Flow

```
1. User sends message
2. Agent embeds message
3. Agent searches vector DB for relevant past facts
4. Agent constructs prompt:
   - System message
   - Retrieved facts (3-5 most relevant)
   - User message
5. Agent calls LLM
6. LLM generates response
7. Agent stores new facts in vector DB for future retrieval
8. Agent returns response
```

### Key Insights

**From Module 1:**
- Agents are loops
- Context grows with every iteration
- This becomes unsustainable

**From Module 2:**
- Embeddings capture meaning as numbers
- Vector databases enable similarity search
- RAG retrieves only relevant facts
- Context stays lean, cost stays low, memory is infinite

---

## What You'll Build

In this module, you'll build `memory_agent.py`:

- Integrates ChromaDB for vector storage
- Embeds every user message and agent response
- Retrieves relevant facts before each LLM call
- Demonstrates RAG in action
- Compares token usage: with/without memory
- Maintains conversation history across sessions

**By the end, you'll understand:**
- How ChatGPT and Claude "remember" your conversations
- Why RAG is the standard pattern for agent memory
- How to build cost-effective, long-running agents
- When to use vector memory vs other strategies

---

## Key Takeaways

1. **Embeddings are coordinates in meaning-space** - similar text = similar vectors
2. **Vector databases search by similarity** - not exact match
3. **RAG = Retrieve + Generate** - only use relevant facts in prompts
4. **Memory solves context growth** - infinite conversations, constant token usage
5. **This is how production agents work** - ChatGPT, Claude, all use RAG

---

**Ready to build?** Move on to [PROJECT.md](PROJECT.md) to see what we're creating!
