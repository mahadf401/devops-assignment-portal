import pytest
import json
import os
import requests
from datetime import datetime

class TestReportCollector:
    def __init__(self):
        self.tests = []

    def pytest_runtest_logreport(self, report):
        if report.when == 'call':
            failure_msg = str(report.longrepr) if report.failed else ""
            self.tests.append({
                "name": report.nodeid,
                "result": report.outcome,  # 'passed' or 'failed'
                "failure_message": failure_msg
            })

def main():
    collector = TestReportCollector()
    # Execute pytest tests programmatically
    exit_code = pytest.main(["-v"], plugins=[collector])

    total = len(collector.tests)
    passed = sum(1 for t in collector.tests if t["result"] == "passed")
    failed = sum(1 for t in collector.tests if t["result"] == "failed")
    overall_status = "passed" if exit_code == 0 else "failed"

    # Construct the JSON schema explicitly required by Task 4 rubric
    report_data = {
        "repository": os.environ.get("GITHUB_REPOSITORY", "mahadf401/devops-assignment-portal"),
        "branch": os.environ.get("GITHUB_REF_NAME", "main"),
        "commit_sha": os.environ.get("GITHUB_SHA", "local-commit"),
        "run_id": os.environ.get("GITHUB_RUN_ID", "local-run"),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "overall_status": overall_status,
        "summary": {
            "total": total,
            "passed": passed,
            "failed": failed
        },
        "tests": collector.tests
    }

    # Transmit payload to RECEIVER_URL secret via SSH Tunnel
    receiver_url = os.environ.get("RECEIVER_URL")
    if receiver_url:
        try:
            res = requests.post(receiver_url, json=report_data, timeout=10)
            print(f"[+] Webhook posted to {receiver_url}. HTTP Status: {res.status_code}")
        except Exception as e:
            print(f"[-] Failed to deliver report webhook: {e}")
    else:
        print("[-] RECEIVER_URL environment variable not set.")

    # Enforce CI failure if tests failed
    raise SystemExit(exit_code)

if __name__ == "__main__":
    main()