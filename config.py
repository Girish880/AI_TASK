import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
DEFAULT_MODEL = "gpt-4"
TEMPERATURE = 0.7

ARTIFACTS_DIR = os.path.join(os.getcwd(), "artifacts")
REPORTS_DIR = os.path.join(os.getcwd(), "reports")
KNOWLEDGE_BASE_DIR = os.path.join(os.getcwd(), "knowledge_base")
