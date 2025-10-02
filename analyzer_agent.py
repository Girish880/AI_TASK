import os
import json
from backend.config import REPORTS_DIR

class AnalyzerAgent:
    """
    AnalyzerAgent stores results in JSON reports
    """

    def analyze_results(self, run_id: str, results: list):
        os.makedirs(REPORTS_DIR, exist_ok=True)

        summary = {
            "total_tests": len(results),
            "passed": sum(1 for r in results if r["status"] == "passed"),
            "failed": sum(1 for r in results if r["status"] != "passed"),
        }
        summary["pass_rate"] = f"{(summary['passed']/summary['total_tests'])*100:.1f}%" if summary['total_tests'] > 0 else "0%"

        report = {
            "run_id": run_id,
            "summary": summary,
            "results": results
        }

        report_path = os.path.join(REPORTS_DIR, f"{run_id}_report.json")
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)

        return report_path
