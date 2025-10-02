import uuid
import shutil
import os
import sys
import asyncio
from typing import List, Optional
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Windows asyncio fix
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# Import Agents
from backend.agents.planner_agent import PlannerAgent
from backend.agents.ranker_agent import RankerAgent
from backend.agents.orchestrator_agent import OrchestratorAgent
from backend.agents.analyzer_agent import AnalyzerAgent
from backend.agents.retriever_agent import RetrieverAgent
from backend.agents.executor_agent import ExecutorAgent
from backend.rag.loader import ingest_documents
from backend.config import KNOWLEDGE_BASE_DIR, REPORTS_DIR, ARTIFACTS_DIR

# Ensure dirs
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(ARTIFACTS_DIR, exist_ok=True)
os.makedirs(KNOWLEDGE_BASE_DIR, exist_ok=True)

# Pydantic models
class RankRequest(BaseModel):
    test_cases: List[dict]
    top_k: Optional[int] = 3

class ExecuteRequest(BaseModel):
    test_cases: List[dict]

class AnalyzeRequest(BaseModel):
    run_id: str
    test_results: List[dict]

# App
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

planner = PlannerAgent()
ranker = RankerAgent()
orchestrator = OrchestratorAgent()
analyzer = AnalyzerAgent()
retriever = RetrieverAgent()
executor = ExecutorAgent()

# Endpoints
@app.post("/plan")
def plan(description: str):
    test_cases = planner.generate_test_cases(description, num_cases=10)
    return {"test_cases": test_cases}

@app.post("/rank")
def rank(request: RankRequest):
    ranked = ranker.rank_test_cases(request.test_cases, request.top_k)
    return {"ranked_test_cases": ranked}

@app.post("/execute")
def execute(request: ExecuteRequest):
    run_id = str(uuid.uuid4())
    results = executor.execute_tests_sync(request.test_cases, run_id)
    report_path = analyzer.analyze_results(run_id, results)
    return {"run_id": run_id, "results": results, "report_path": report_path}

@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    report_path = analyzer.analyze_results(request.run_id, request.test_results)
    return {"report_path": report_path}

@app.get("/report/{run_id}")
def get_report(run_id: str):
    from backend.utils.file_utils import load_json
    reports = [f for f in os.listdir(REPORTS_DIR) if f.startswith(run_id)]
    if not reports:
        return {"error": "Report not found"}
    return load_json(os.path.join(REPORTS_DIR, reports[0]))

@app.post("/upload_doc")
def upload_doc(file: UploadFile = File(...)):
    dest_path = os.path.join(KNOWLEDGE_BASE_DIR, file.filename)
    with open(dest_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        ingest_documents()
    except Exception as e:
        return {"error": f"Ingestion failed: {e}"}

    return {"message": f"{file.filename} uploaded and ingested successfully."}

@app.post("/ingest_url")
def ingest_url(url: str = Form(...)):
    from backend.rag.vector_store import get_vector_store
    from backend.rag.embedder import get_openai_embeddings
    from langchain.schema import Document
    from playwright.sync_api import sync_playwright

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=60000)
            text = page.inner_text("body")
            browser.close()

        embeddings = get_openai_embeddings()
        vectordb = get_vector_store(embeddings)
        vectordb.add_documents([Document(page_content=text, metadata={"source": url})])
        vectordb.persist()
    except Exception as e:
        return {"error": f"URL ingestion failed: {e}"}

    return {"message": f"URL {url} ingested successfully."}
