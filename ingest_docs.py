# backend/rag/ingest_docs.py

from .loader import ingest_documents

def ingest_documents_wrapper(urls: list[str] = None) -> int:
    """
    Ingest PDFs, text files, and optionally URLs into the vector store.

    Args:
        urls (list[str], optional): List of URLs to scrape and ingest. Defaults to None.

    Returns:
        int: Number of documents ingested.
    """
    docs_count = ingest_documents(urls)
    return docs_count
