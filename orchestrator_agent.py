import asyncio
from .executor_agent import ExecutorAgent

class OrchestratorAgent:
    def __init__(self, concurrency: int = 3):
        self.executor = ExecutorAgent()
        self.semaphore = asyncio.Semaphore(concurrency)

    async def run_tests(self, test_cases: list, run_id: str):
        results = []

        async def run_case(case):
            async with self.semaphore:
                res = await asyncio.to_thread(self.executor.execute_tests_sync, [case], run_id)
                results.extend(res)

        await asyncio.gather(*[run_case(tc) for tc in test_cases])
        return results
