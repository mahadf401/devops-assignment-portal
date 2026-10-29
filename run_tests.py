import subprocess
import json
import os
import datetime
import urllib.request
import sys

def main():
    res = subprocess.run(["pytest", "test_app.py", "--json-report", "--json-report-file=pytest_out.json"], capture_output=True, text=True)
    
    pytest_data = {}
    if os.path.exists("pytest_out.json"):
        with open("pytest_out.json") as f:
            pytest_data = json.load(f)
            
    repo_name = os.environ.get("GITHUB_REPOSITORY", "local/repo")
    branch_name = os.environ.get("GITHUB_REF_NAME", "main")
    commit_sha = os.environ.get("GITHUB_SHA", "local_sha")
    run_id = os.environ.get("GITHUB_RUN_ID", "1")
    receiver_url = os.environ.get("RECEIVER_URL", "")

    tests_summary = []
    total = pytest_data.get("summary", {}).get("total", 0)
    passed = pytest_data.get("summary", {}).get("passed", 0)
    failed = pytest_data.get("summary", {}).get("failed", 0)
    
    for t in pytest_data.get("tests", []):
        t_name = t.get("nodeid", "unknown_test")
        t_outcome = t.get("outcome", "failed")
        t_fail_msg = str(t.get("call", {}).get("longrepr", "")) if t_outcome != "passed" else ""
        tests_summary.append({
            "test_name": t_name,
            "result": t_outcome,
            "failure_message": t_fail_msg
        })

    overall_status = "passed" if res.returncode == 0 else "failed"

    report_payload = {
        "repository": repo_name,
        "branch": branch_name,
        "commit_sha": commit_sha,
        "pipeline_run_id": run_id,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "summary": {
            "total_tests": total,
            "passed_tests": passed,
            "failed_tests": failed,
            "overall_status": overall_status
        },
        "tests": tests_summary
    }

    if receiver_url:
        try:
            req = urllib.request.Request(
                receiver_url,
                data=json.dumps(report_payload).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req) as resp:
                print(f"[CI] Report transmitted to {receiver_url}. HTTP {resp.status}")
        except Exception as e:
            print(f"[CI ERROR] Transmission failed: {e}")

    sys.exit(res.returncode)

if __name__ == "__main__":
    main()