import os
import json
import re
import logging
from playwright.sync_api import sync_playwright
from backend.config import ARTIFACTS_DIR

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ExecutorAgent")

class ExecutorAgent:
    """
    ExecutorAgent to run test cases synchronously (Windows-safe)
    """

    def execute_tests_sync(self, test_cases, run_id):
        # Split batch string into individual test case dicts if needed
        test_cases = self._split_batch_test_cases(test_cases)

        results = []
        os.makedirs(ARTIFACTS_DIR, exist_ok=True)

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)  # headless=False for debugging
                for case in test_cases:
                    page = browser.new_page()
                    artifacts = {}
                    status = "failed"
                    try:
                        url = case.get("url", "https://play.ezygamers.com")
                        logger.info(f"[{run_id}] Navigating to {url} for test case '{case.get('test_case')}'")
                        page.goto(url, timeout=15000)  # 15 sec timeout

                        # Take screenshot
                        safe_name = "".join(c if c.isalnum() else "_" for c in case.get("test_case", "")[:15])
                        screenshot_path = os.path.join(ARTIFACTS_DIR, f"{run_id}_{safe_name}.png")
                        page.screenshot(path=screenshot_path)
                        artifacts["screenshot"] = screenshot_path
                        status = "passed"

                    except Exception as e:
                        artifacts["error"] = str(e)
                        logger.error(f"[{run_id}] Test case '{case.get('test_case')}' failed: {e}")
                    finally:
                        page.close()

                    results.append({
                        "test_case": case.get("test_case", "Unnamed"),
                        "priority": case.get("priority", "medium"),
                        "status": status,
                        "artifacts": artifacts
                    })

                browser.close()

        except Exception as e:
            logger.error(f"[{run_id}] Browser launch failed: {e}")
            for case in test_cases:
                results.append({
                    "test_case": case.get("test_case", "Unnamed"),
                    "priority": case.get("priority", "medium"),
                    "status": "failed",
                    "artifacts": {"error": f"Browser launch failed: {e}"}
                })

        return results

    def _split_batch_test_cases(self, test_cases):
        """
        Convert a single batch string of numbered test cases into individual dicts
        """
        if len(test_cases) == 1 and isinstance(test_cases[0], str):
            raw = test_cases[0]
            split_cases = []

            matches = re.findall(r'\d+\.\s*({.*?})', raw, re.DOTALL)
            for match in matches:
                try:
                    case_dict = json.loads(match)
                    split_cases.append(case_dict)
                except json.JSONDecodeError:
                    split_cases.append({"test_case": match, "priority": "medium"})
            return split_cases
        else:
            return test_cases
