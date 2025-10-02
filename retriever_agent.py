from backend.rag.vector_store import get_vector_store

class RetrieverAgent:
    def __init__(self):
        self.vectordb = get_vector_store()

    def query(self, query_text: str, top_k: int = 7):
        results = self.vectordb.similarity_search(query_text, k=top_k)
        return [r.page_content for r in results]
