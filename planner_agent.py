from langchain_openai import ChatOpenAI
from backend.config import OPENAI_API_KEY, DEFAULT_MODEL, TEMPERATURE
from backend.agents.retriever_agent import RetrieverAgent
import json
import re

class PlannerAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name=DEFAULT_MODEL,
            temperature=TEMPERATURE,
            openai_api_key=OPENAI_API_KEY
        )
        self.retriever = RetrieverAgent()

    def generate_test_cases(self, description: str, num_cases: int = 10):
        context_docs = self.retriever.query(description)
        context_text = "\n".join(context_docs) if context_docs else "No additional context."

        prompt = f"""
You are an AI QA tester for a web game. Generate {num_cases} test cases based on this game description and reference material.
Reference:
{context_text}

Game Description:
{description}

Output JSON list with objects:
{{"test_case": "...", "priority": "high|medium|low"}}

Prioritize critical test cases:
- Game is playable
- Sum calculations are correct
- Multi-resolution UI
"""

        response = self.llm.predict(prompt)

        # Attempt to extract JSON array
        try:
            # Clean response: remove numbered list if present
            response_clean = re.sub(r'^\d+\.\s*', '', response, flags=re.MULTILINE)
            test_cases = json.loads(response_clean)
            if isinstance(test_cases, list) and len(test_cases) == num_cases:
                return test_cases
            else:
                # If response is string with multiple numbered JSONs, split and parse
                items = re.findall(r'\{.*?\}', response_clean, flags=re.DOTALL)
                return [json.loads(item) for item in items][:num_cases]
        except Exception as e:
            # Fallback: return single item repeated to match num_cases
            return [{"test_case": response.strip(), "priority": "high"} for _ in range(num_cases)]
