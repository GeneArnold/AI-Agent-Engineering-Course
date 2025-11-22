"""
Configuration management for AI Agent Training

Handles environment variables, provider selection, and runtime settings.
"""

from pathlib import Path
from typing import Literal
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os


# Load environment variables
load_dotenv()


class ModelConfig(BaseModel):
    """Configuration for LLM providers"""
    provider: Literal["openai", "anthropic", "ollama", "huggingface"] = Field(
        default="openai",
        description="Which model provider to use"
    )

    # OpenAI settings
    openai_api_key: str = Field(default="", description="OpenAI API key")
    openai_model: str = Field(default="gpt-4o-mini", description="OpenAI model name")
    openai_org_id: str = Field(default="", description="OpenAI organization ID")

    # Anthropic/Claude settings
    anthropic_api_key: str = Field(default="", description="Anthropic API key")
    anthropic_model: str = Field(default="claude-3-5-sonnet-20241022", description="Anthropic model name")

    # Ollama settings
    ollama_base_url: str = Field(default="http://localhost:11434", description="Ollama API URL")
    ollama_model: str = Field(default="llama3.2:3b", description="Ollama model name")

    # General model settings
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Sampling temperature")
    max_tokens: int = Field(default=2000, description="Maximum tokens per response")


class AgentConfig(BaseModel):
    """Configuration for agent behavior"""
    max_steps: int = Field(default=10, description="Maximum agent loop iterations")
    max_cost_dollars: float = Field(default=1.0, description="Budget limit in USD")
    log_level: str = Field(default="INFO", description="Logging level")
    log_to_file: bool = Field(default=True, description="Write logs to file")
    log_dir: Path = Field(default=Path("./logs"), description="Log directory path")


class VectorStoreConfig(BaseModel):
    """Configuration for vector/memory storage"""
    chroma_persist_dir: Path = Field(
        default=Path("./module_2_memory/chroma_db"),
        description="ChromaDB persistence directory"
    )
    embedding_model: str = Field(
        default="text-embedding-3-small",
        description="Embedding model name"
    )
    top_k: int = Field(default=3, description="Number of results to retrieve")


def load_config() -> tuple[ModelConfig, AgentConfig, VectorStoreConfig]:
    """Load all configuration from environment"""
    model_config = ModelConfig(
        provider=os.getenv("MODEL_PROVIDER", "openai"),
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        openai_org_id=os.getenv("OPENAI_ORG_ID", ""),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY", ""),
        anthropic_model=os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022"),
        ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        ollama_model=os.getenv("OLLAMA_MODEL", "llama3.2:3b"),
        temperature=float(os.getenv("TEMPERATURE", "0.7")),
    )

    agent_config = AgentConfig(
        max_steps=int(os.getenv("MAX_AGENT_STEPS", "10")),
        max_cost_dollars=float(os.getenv("MAX_COST_DOLLARS", "1.0")),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        log_to_file=os.getenv("LOG_TO_FILE", "true").lower() == "true",
        log_dir=Path(os.getenv("LOG_DIR", "./logs")),
    )

    vector_config = VectorStoreConfig(
        chroma_persist_dir=Path(os.getenv("CHROMA_PERSIST_DIR", "./module_2_memory/chroma_db")),
        embedding_model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"),
    )

    return model_config, agent_config, vector_config
