#!/usr/bin/env python3
"""
Module 2: Memory-Enabled Agent
================================
Demonstrates long-term memory using RAG (Retrieval-Augmented Generation)
with ChromaDB vector database.

Key Concepts Demonstrated:
- Vector storage for infinite memory
- Semantic retrieval (embeddings + similarity search)
- RAG pattern (retrieve relevant facts, then generate)
- Constant token usage regardless of conversation length
- JSONL logging for observability

Author: AI Agent Engineering Course
"""

import os
import json
import chromadb
from datetime import datetime, UTC
from openai import OpenAI
from dotenv import load_dotenv
import uuid

# Load environment variables
load_dotenv()

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Unset any organization environment variables to avoid conflicts
# The OpenAI client auto-picks these up, which can cause mismatches
if "OPENAI_ORG_ID" in os.environ:
    del os.environ["OPENAI_ORG_ID"]
if "OPENAI_ORGANIZATION" in os.environ:
    del os.environ["OPENAI_ORGANIZATION"]

# Initialize OpenAI client (no organization header)
client = OpenAI(api_key=OPENAI_API_KEY)

# Constants
MODEL = "gpt-4o-mini"
COLLECTION_NAME = "agent_memory"
LOG_FILE = "logs/memory_agent.jsonl"
TOP_K_FACTS = 3  # Number of facts to retrieve

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Session ID (unique per run)
SESSION_ID = str(uuid.uuid4())[:8]


# ============================================================================
# LOGGING UTILITIES
# ============================================================================

def log_event(event_type: str, data: dict) -> None:
    """
    Log an event to JSONL file for observability.

    Args:
        event_type: Type of event (memory_store, memory_retrieval, llm_call)
        data: Event-specific data
    """
    log_entry = {
        "timestamp": datetime.now(UTC).isoformat().replace('+00:00', 'Z'),
        "event_type": event_type,
        "session_id": SESSION_ID,
        **data
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")


# ============================================================================
# MEMORY MANAGER - Vector Database Operations
# ============================================================================

class MemoryManager:
    """
    Handles all vector database operations using ChromaDB.

    Responsibilities:
    - Initialize ChromaDB collection
    - Store facts with automatic embeddings
    - Retrieve semantically similar facts
    - Provide memory statistics
    """

    def __init__(self, collection_name: str):
        """
        Initialize ChromaDB client and collection.

        Args:
            collection_name: Name of the collection to use
        """
        # Initialize ChromaDB client (persistent storage)
        self.client = chromadb.PersistentClient(path="./chroma_db")

        # Get or create collection
        # ChromaDB will auto-generate embeddings for us
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "Agent conversation memory"}
        )

        print(f"✓ MemoryManager initialized (collection: {collection_name})")

    def store_fact(self, text: str, metadata: dict) -> None:
        """
        Store a fact in the vector database.

        ChromaDB automatically:
        1. Generates embedding from text
        2. Stores vector in collection
        3. Associates metadata with the vector

        Args:
            text: The fact to store (will be embedded)
            metadata: Additional context (role, timestamp, session_id)
        """
        # Generate unique ID for this fact
        fact_id = str(uuid.uuid4())

        # Store in ChromaDB (auto-embeds the text)
        self.collection.add(
            documents=[text],
            metadatas=[metadata],
            ids=[fact_id]
        )

        # Log storage event
        log_event("memory_store", {
            "text": text,
            "metadata": metadata,
            "fact_id": fact_id,
            "collection": self.collection.name
        })

    def retrieve_relevant(self, query: str, top_k: int = 3) -> list[dict]:
        """
        Search for relevant facts using semantic similarity.

        ChromaDB automatically:
        1. Embeds the query
        2. Computes cosine similarity with stored embeddings
        3. Returns top-k most similar facts

        Args:
            query: Search query (will be embedded)
            top_k: Number of facts to retrieve (default: 3)

        Returns:
            List of dicts with {text, metadata, distance}
            Sorted by relevance (most relevant first)
        """
        start_time = datetime.now(UTC)

        # Query ChromaDB (auto-embeds query and searches)
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )

        # Calculate retrieval time
        retrieval_time_ms = (datetime.now(UTC) - start_time).total_seconds() * 1000

        # Format results
        facts = []
        if results["documents"][0]:  # Check if results exist
            for i, doc in enumerate(results["documents"][0]):
                facts.append({
                    "text": doc,
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i]
                })

        # Log retrieval event
        log_event("memory_retrieval", {
            "query": query,
            "top_k": top_k,
            "results_count": len(facts),
            "results": [{"text": f["text"], "distance": f["distance"]} for f in facts],
            "retrieval_time_ms": round(retrieval_time_ms, 2)
        })

        return facts

    def get_stats(self) -> dict:
        """
        Get memory statistics.

        Returns:
            Dict with collection stats (total facts, etc.)
        """
        count = self.collection.count()
        return {
            "collection_name": self.collection.name,
            "total_facts": count,
            "session_id": SESSION_ID
        }

    def clear_memory(self) -> int:
        """
        Clear all facts from memory.

        Returns:
            Number of facts deleted
        """
        # Get current count before clearing
        count = self.collection.count()

        # Delete the collection and recreate it
        self.client.delete_collection(name=self.collection.name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection.name,
            metadata={"description": "Agent conversation memory"}
        )

        # Log the reset
        log_event("memory_reset", {
            "facts_deleted": count,
            "collection": self.collection.name
        })

        return count


# ============================================================================
# AGENT LOOP - RAG Pattern
# ============================================================================

def agent_loop(memory: MemoryManager, user_query: str) -> str:
    """
    Main agent logic implementing RAG (Retrieval-Augmented Generation).

    Flow:
    1. Retrieve relevant facts from memory
    2. Construct prompt with retrieved facts
    3. Call LLM with lean prompt
    4. Store new conversation turn in memory
    5. Return response

    Args:
        memory: MemoryManager instance
        user_query: User's question or message

    Returns:
        Agent's response
    """
    # Step 1: Retrieve relevant facts from memory
    relevant_facts = memory.retrieve_relevant(user_query, top_k=TOP_K_FACTS)

    # Step 2: Construct prompt with retrieved facts
    if relevant_facts:
        context = "\n".join([f"- {fact['text']}" for fact in relevant_facts])
        system_message = f"""You are a helpful assistant with memory of past conversations.

Relevant facts from previous interactions:
{context}

Use these facts when answering the user's question. If they're not relevant, ignore them."""
    else:
        system_message = "You are a helpful assistant."

    # Step 3: Call LLM with lean prompt (only relevant context)
    start_time = datetime.now(UTC)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_query}
        ],
        temperature=0.7
    )

    # Extract response
    assistant_message = response.choices[0].message.content

    # Calculate metrics
    latency_ms = (datetime.now(UTC) - start_time).total_seconds() * 1000
    prompt_tokens = response.usage.prompt_tokens
    completion_tokens = response.usage.completion_tokens
    total_tokens = response.usage.total_tokens

    # Calculate cost (gpt-4o-mini pricing: $0.150/1M input, $0.600/1M output)
    cost_usd = (prompt_tokens * 0.150 / 1_000_000) + (completion_tokens * 0.600 / 1_000_000)

    # Log LLM call
    log_event("llm_call", {
        "model": MODEL,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
        "facts_used": len(relevant_facts),
        "latency_ms": round(latency_ms, 2),
        "cost_usd": round(cost_usd, 6)
    })

    # Step 4: Store new conversation turn in memory
    timestamp = datetime.now(UTC).isoformat().replace('+00:00', 'Z')

    memory.store_fact(
        text=f"User said: {user_query}",
        metadata={
            "role": "user",
            "timestamp": timestamp,
            "session_id": SESSION_ID
        }
    )

    memory.store_fact(
        text=f"Assistant responded: {assistant_message}",
        metadata={
            "role": "assistant",
            "timestamp": timestamp,
            "session_id": SESSION_ID
        }
    )

    # Step 5: Return response
    return assistant_message


# ============================================================================
# INTERACTIVE CHAT INTERFACE
# ============================================================================

def show_stats(memory: MemoryManager) -> None:
    """Display memory statistics."""
    stats = memory.get_stats()
    print("\n" + "="*60)
    print(f"Memory Statistics:")
    print(f"  Collection: {stats['collection_name']}")
    print(f"  Total Facts: {stats['total_facts']}")
    print(f"  Session ID: {stats['session_id']}")
    print("="*60 + "\n")


def chat():
    """
    Interactive chat interface with memory.

    Commands:
    - '/exit': Quit the agent
    - '/stats': Show memory statistics
    - '/reset': Clear all memory (with confirmation)
    - Any other text: Process as user query
    """
    print("\n" + "="*60)
    print("Memory-Enabled Agent (Module 2)")
    print("="*60)
    print("This agent remembers past conversations using RAG.")
    print("\nCommands:")
    print("  - Type '/exit' to quit")
    print("  - Type '/stats' to see memory info")
    print("  - Type '/reset' to clear all memory")
    print("  - Type anything else to chat")
    print("="*60 + "\n")

    # Initialize memory
    memory = MemoryManager(COLLECTION_NAME)

    # Show initial stats
    show_stats(memory)

    # Chat loop
    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            # Handle slash commands
            if user_input.lower() == "/exit":
                print("\nGoodbye! Your memory is saved and will persist across sessions.")
                break

            elif user_input.lower() == "/stats":
                show_stats(memory)
                continue

            elif user_input.lower() == "/reset":
                # Confirm before clearing
                stats = memory.get_stats()
                if stats['total_facts'] == 0:
                    print("\nMemory is already empty. Nothing to reset.\n")
                    continue

                confirm = input(f"\n⚠️  Warning: This will delete all {stats['total_facts']} facts from memory.\nType 'yes' to confirm: ").strip().lower()

                if confirm == "yes":
                    deleted = memory.clear_memory()
                    print(f"\n✓ Memory cleared! Deleted {deleted} facts.\n")
                else:
                    print("\nReset cancelled.\n")
                continue

            # Process as normal query
            response = agent_loop(memory, user_input)
            print(f"\nAgent: {response}\n")

        except KeyboardInterrupt:
            print("\n\nGoodbye! Your memory is saved.")
            break
        except Exception as e:
            print(f"\nError: {e}\n")
            continue


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    print(f"\nSession ID: {SESSION_ID}")
    print(f"Logs: {LOG_FILE}\n")

    chat()
