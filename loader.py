# backend/rag/loader.py

import os
import asyncio
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain.schema import Document
from .vector_store import get_vector_store
from playwright.async_api import async_playwright


async def load_url_with_playwright(url: str) -> list[Document]:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        content = await page.content()
        await browser.close()
    return [Document(page_content=content, metadata={"source": url})]


def ingest_documents(urls: list[str] = None) -> int:
    """
    Ingest PDFs, text/markdown files, and optionally URLs into the vector store.

    Args:
        urls (list[str], optional): List of URLs to scrape and ingest.

    Returns:
        int: Number of documents ingested.
    """
    docs: list[Document] = []
    kb_dir = os.path.join(os.getcwd(), "knowledge_base")

    if not os.path.exists(kb_dir):
        print(f"⚠️ Knowledge base directory not found: {kb_dir}")
        return 0

    # PDFs
    pdf_loader = DirectoryLoader(kb_dir, glob="*.pdf", loader_cls=PyPDFLoader)
    docs.extend(pdf_loader.load())

    # Text/Markdown
    txt_loader = DirectoryLoader(kb_dir, glob="*.txt", loader_cls=TextLoader)
    md_loader = DirectoryLoader(kb_dir, glob="*.md", loader_cls=TextLoader)
    docs.extend(txt_loader.load())
    docs.extend(md_loader.load())

    # URLs
    if urls:
        for url in urls:
            try:
                url_docs = asyncio.run(load_url_with_playwright(url))
                docs.extend(url_docs)
            except Exception as e:
                print(f"❌ Failed to load {url}: {e}")

    if not docs:
        print("⚠️ No documents found to ingest.")
        return 0

    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(docs)

    # Store embeddings
    vectordb = get_vector_store()
    vectordb.add_documents(docs)
    vectordb.persist()

    print(f"✅ Ingested {len(docs)} documents into vector store.")
    return len(docs)
