from langchain_chroma import Chroma
from .embedder import get_openai_embeddings
from backend.config import KNOWLEDGE_BASE_DIR

def get_vector_store(persist_directory=KNOWLEDGE_BASE_DIR):
    embeddings = get_openai_embeddings()
    return Chroma(persist_directory=persist_directory, embedding_function=embeddings)
