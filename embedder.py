from langchain_openai import OpenAIEmbeddings
from backend.config import OPENAI_API_KEY

def get_openai_embeddings():
    return OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
