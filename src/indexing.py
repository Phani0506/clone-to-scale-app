from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

def build_index(collection_name, documents):
    """Builds an in-memory vector index from documents."""
    print(f"Building in-memory index for collection: {collection_name}...")
    
    db = chromadb.Client()
    chroma_collection = db.get_or_create_collection(collection_name)
    
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context
    )
    
    print(f"Successfully built in-memory index for '{collection_name}'.")
    return index
