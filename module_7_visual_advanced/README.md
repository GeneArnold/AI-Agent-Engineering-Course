# Module 7: Visual Recognition (Part 2) - Hybrid Architecture

## 🔒 Releases January 12, 2026 (Week 7)

Build production-ready hybrid architecture—combine vector databases and relational databases for scalable, real-world systems.

## Learning Objectives
- Understand when to use vector DB vs relational DB
- Apply the "3-10-100" decision rule for architecture choices
- Design hybrid systems (Vector DB for similarity + SQLite for rich data)
- Implement foreign key relationships between databases
- Query complex metadata efficiently with SQL
- Build production-ready face recognition that scales

## Concepts Covered
- Hybrid architecture patterns
- Vector DB vs relational DB strengths/weaknesses
- The "3-10-100 Rule" (when to use which database)
- Foreign key relationships across databases
- One-to-many relationships (person → interests, interactions)
- SQL for complex metadata queries
- Production scalability considerations

## Project: `hybrid_recognition_agent.py`

### Requirements
- ChromaDB for face embeddings (similarity search only)
- SQLite for rich relational data (people, interests, interactions)
- Foreign key relationships (person_id links both databases)
- Complex metadata queries (JOINs, aggregations, filters)
- One-to-many relationships (one person, many interests/interactions)
- Migration from Module 6's simple metadata to hybrid architecture
- Optional: Simple Streamlit UI for visualization (bonus, not required)

### Success Criteria
✅ Vector DB stores only embeddings + minimal filter fields
✅ SQLite stores all rich metadata with proper schema
✅ Foreign keys correctly link ChromaDB person_id to SQLite tables
✅ System can query: "Show me all interactions with Sarah"
✅ Agent retrieves person data efficiently from both databases
✅ One-to-many relationships work (person → multiple interests)
✅ Performance is noticeably better than storing everything in vector DB

## Files in This Module
- `SOLUTION/hybrid_recognition_agent.py` - Hybrid system implementation
- `SOLUTION/schema.sql` - SQLite database schema
- `SOLUTION/faces_db/` - ChromaDB storage (embeddings only)
- `SOLUTION/metadata.db` - SQLite database (rich data)
- `logs/` - System interactions and query performance
- `CONCEPTS.md` - Theory: Hybrid architectures, database trade-offs
- `PROJECT.md` - Architecture: Design decisions, seed questions
- `README.md` - This file - Module overview

## The "3-10-100" Decision Rule

**Use Vector DB Only When:**
- **< 3 metadata fields** per record (person_id, name, timestamp)
- **< 10 total fields** you care about
- **< 100K records** in dataset
- **Minimal relationships** between entities (flat data)

**Move to Hybrid When:**
- **> 5 metadata fields** per record
- **> 10 total fields** you want to query
- **> 100K records** (performance matters)
- **Any relationships** (one-to-many, many-to-many)
  - One person → multiple interests
  - One person → many interactions over time
  - Family trees, organizational hierarchies
- **Frequent metadata updates** (last_seen changes constantly)
- **Complex queries** (JOINs, aggregations, GROUP BY)

## Hybrid Architecture Pattern

**How it works:**

```
1. Camera captures face
   ↓
2. Generate face embedding (512D vector)
   ↓
3. Search ChromaDB for similar faces
   ↓
   Returns: person_id = "uuid-123"
   ↓
4. Query SQLite with person_id
   ↓
   Returns: Full profile (name, interests, interactions, etc.)
   ↓
5. Agent generates rich, personalized greeting
```

**Key insight:** Use each database for what it's good at!
- **ChromaDB:** Similarity search (vectors)
- **SQLite:** Rich metadata queries (SQL)

## Database Comparison

| Feature | Vector DB (ChromaDB) | Relational DB (SQLite) |
|---------|---------------------|------------------------|
| **Best for** | Similarity search | Complex queries, relationships |
| **Strengths** | Fast vector search, semantic matching | JOINs, ACID, aggregations, indexes |
| **Weaknesses** | Slow metadata filtering | No semantic similarity search |
| **Store here** | Embeddings + person_id | Everything else! |
| **Query speed** | Fast for vectors, slow for metadata | Slow for vectors, fast for metadata |

## SQLite Schema Example

```sql
-- Core identity
CREATE TABLE people (
    id TEXT PRIMARY KEY,  -- Same as ChromaDB person_id
    name TEXT NOT NULL,
    relationship TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- One-to-many: interests
CREATE TABLE interests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id TEXT NOT NULL,
    interest TEXT NOT NULL,
    proficiency TEXT,  -- beginner, intermediate, expert
    FOREIGN KEY (person_id) REFERENCES people(id) ON DELETE CASCADE
);

-- One-to-many: interactions over time
CREATE TABLE interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id TEXT NOT NULL,
    interaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    location TEXT,
    notes TEXT,
    FOREIGN KEY (person_id) REFERENCES people(id) ON DELETE CASCADE
);

-- Indexes for performance
CREATE INDEX idx_interests_person ON interests(person_id);
CREATE INDEX idx_interactions_person ON interactions(person_id);
CREATE INDEX idx_interactions_date ON interactions(interaction_date DESC);
```

## Real-World Example

**Module 6 (Simple - Vector DB only):**
```python
# Limited metadata stored in ChromaDB
metadata = {
    "person_id": "uuid-123",
    "name": "Sarah",
    "timestamp": "2024-11-22T10:30:00Z"
}
# Greeting: "Hi Sarah!"
```

**Module 7 (Hybrid - Vector DB + SQLite):**
```python
# ChromaDB: Only embedding + person_id
chromadb_metadata = {
    "person_id": "uuid-123"
}

# SQLite: Rich relational data
person = db.query("SELECT * FROM people WHERE id = ?", person_id)
interests = db.query("SELECT interest FROM interests WHERE person_id = ?", person_id)
last_interaction = db.query(
    "SELECT * FROM interactions WHERE person_id = ? ORDER BY interaction_date DESC LIMIT 1",
    person_id
)

# Rich greeting:
# "Hi Sarah! Gene's daughter who loves coding, AI, and music.
#  Last saw you 2 days ago when you helped debug the agent loop."
```

## Key Features

**What the hybrid agent demonstrates:**
- **Architectural decision-making** - When to use which database
- **Foreign key relationships** - Link data across systems
- **Complex SQL queries** - JOINs, aggregations, filters
- **One-to-many relationships** - Model real-world data
- **Production scalability** - Handle growing datasets efficiently
- **Performance optimization** - Use each database's strengths

## Reflection Questions
After completing this module, answer:
1. When would you choose hybrid architecture vs vector DB only?
2. How do foreign keys link ChromaDB and SQLite?
3. What queries are faster in SQLite vs ChromaDB?
4. When is the "3-10-100 Rule" guideline helpful?
5. How would you migrate from Module 6 to Module 7 architecture?

## Migration Path (Module 6 → Module 7)

**Step 1:** Design SQLite schema
**Step 2:** Create foreign key (person_id in both databases)
**Step 3:** Migrate metadata from ChromaDB to SQLite
**Step 4:** Keep only person_id in ChromaDB
**Step 5:** Update queries to fetch from both databases
**Step 6:** Test performance improvement

## Optional: Streamlit UI

**Bonus enhancement (not required):**
- Visualize face database
- Show person profiles with photos
- Display interaction history
- Add new people with form input

**Note:** UI is optional - core learning is hybrid architecture, not frontend.

## Coming January 12, 2026

**This module releases in Week 7.** Until then:
- Complete Modules 1-6
- Master all core agent patterns
- Complete simple face recognition (Module 6)
- Get ready for production architecture!

---

## Course Complete! 🎉

**Congratulations!** After completing Module 7, you've finished the AI Agent Engineering course.

**You've learned:**
- ✅ Agent loops and tool calling (Module 1)
- ✅ Memory and RAG patterns (Module 2)
- ✅ Multi-tool systems (Module 3)
- ✅ Multi-agent coordination (Module 4)
- ✅ Evaluation and quality measurement (Module 5)
- ✅ Multi-modal RAG (Module 6)
- ✅ Production hybrid architectures (Module 7)

**Next steps:**
- Build your own agent projects
- Explore advanced topics (MCP, local models)
- Share what you've built!
- Join the community and help others learn
