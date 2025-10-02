import os
from datetime import datetime
from .file_utils import save_json
from backend.config import REPORTS_DIR

def generate_report(run_id: str, test_results: list):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(REPORTS_DIR, f"{run_id}_{timestamp}.json")

    report_data = {
        "run_id": run_id,
        "timestamp": timestamp,
        "summary": {
            "total_tests": len(test_results),
            "passed": sum(1 for t in test_results if t["status"] == "passed"),
            "failed": sum(1 for t in test_results if t["status"] == "failed"),
        },
        "tests": test_results
    }

    save_json(report_path, report_data)
    return report_path
