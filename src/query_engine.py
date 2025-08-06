from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

def create_query_engine_from_index(index, system_prompt):
    """Creates a query engine directly from an in-memory index object."""
    query_engine = index.as_query_engine()
    
    if system_prompt:
        print(f"Applying system prompt: '{system_prompt[:50]}...'")
    
    return query_engine
