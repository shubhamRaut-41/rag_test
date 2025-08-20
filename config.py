import os
from typing import List

class Config:
    """Configuration settings for the application."""
    
    CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
    CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8000"))
    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "my_docs")
    PERSIST_DIRECTORY = os.getenv("PERSIST_DIRECTORY", "chroma_db")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    ALLOWED_FILE_TYPES = List[str] = os.getenv("ALLOWED_FILE_TYPES", ".pdf,.txt").split(",")    