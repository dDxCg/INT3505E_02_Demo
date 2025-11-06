from datetime import datetime
import subprocess
import json
import pytest
from pathlib import Path

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
RESULT_PATH = Path(f"tests/results/run_result_{timestamp}.json")
COLLECTION_PATH = Path("tests/collection/Library.postman_collection.json")

@pytest.fixture(scope="session", autouse=True)
def run_newman_collection():
    """Run the Postman collection via newman before pytest tests."""
    if RESULT_PATH.exists():
        RESULT_PATH.unlink()
    
    cmd = [
        "newman", "run", str(COLLECTION_PATH),
        "--reporters", "json",
        "--reporter-json-export", str(RESULT_PATH)
    ]
    print(f"🚀 Running Newman collection: {COLLECTION_PATH}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    print("=== NEWMAN STDOUT ===")
    print(result.stdout)
    print("=== NEWMAN STDERR ===")
    print(result.stderr)
    result.check_returncode()

    with open(RESULT_PATH) as f:
        return json.load(f)


def test_collection_execution(run_newman_collection):
    """Basic validation: no requests failed."""
    summary = run_newman_collection["run"]["stats"]

    total = summary["requests"]["total"]
    failed = summary["requests"]["failed"]
    error_rate = (failed / total) * 100 if total else 0

    print(f"\n📊 Total Requests: {total}")
    print(f"❌ Failed: {failed}")
    print(f"⚠️ Error Rate: {error_rate:.2f}%")

    # Expect < 5% error rate
    assert error_rate < 5, f"High error rate: {error_rate:.2f}%"


def test_status_codes(run_newman_collection):
    """Check that each request returned a 2xx or 3xx status."""
    failures = []
    for exec_item in run_newman_collection["run"]["executions"]:
        name = exec_item["item"]["name"]
        status = exec_item["response"][0]["code"]
        if not (200 <= status < 400):
            failures.append((name, status))
    
    if failures:
        print("🚫 Non-OK responses:")
        for name, status in failures:
            print(f" - {name}: {status}")
    
    assert not failures, "Some requests did not return 2xx/3xx status."


def test_response_times(run_newman_collection):
    """Ensure all requests complete within 500ms avg."""
    times = [r["response"][0]["responseTime"]
             for r in run_newman_collection["run"]["executions"]
             if "response" in r and r["response"]]
    
    avg_time = sum(times) / len(times)
    max_time = max(times)

    print(f"\n⚡ Avg Response: {avg_time:.2f} ms | Max: {max_time} ms")
    
    assert avg_time < 500, f"Average response time too high: {avg_time} ms"
    assert max_time < 1000, f"Some requests took too long: {max_time} ms"