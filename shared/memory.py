"""
Memory and vector store utilities

This module will be implemented during Module 2.
It provides semantic memory via embeddings and vector search.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class MemoryItem(BaseModel):
    """A stored memory with metadata"""
    id: str
    content: str
    embedding: Optional[List[float]] = None
    metadata: Dict[str, Any] = {}
    timestamp: Optional[str] = None


class SearchResult(BaseModel):
    """Result from vector similarity search"""
    item: MemoryItem
    distance: float
    score: float


# TODO: Implement in Module 2
# - VectorStore class (wrapping ChromaDB or FAISS)
# - add_memory() method
# - search() method with top-k
# - Embedding generation (OpenAI or local)
# - Persistence and loading
