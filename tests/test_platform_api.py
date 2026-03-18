import importlib.util
import sys
from pathlib import Path

from fastapi.testclient import TestClient

REPO_ROOT = Path(__file__).resolve().parents[1]
API_PATH = REPO_ROOT / "platform" / "api.py"
STATE_PATH = REPO_ROOT / "shared" / "argilla" / "infra" / "state.json"
SUBMISSIONS_PATH = REPO_ROOT / "shared" / "argilla" / "infra" / "public_submissions.json"


spec = importlib.util.spec_from_file_location("platform_api", API_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("Unable to load platform API module")
platform_api = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = platform_api
spec.loader.exec_module(platform_api)


def setup_function() -> None:
    STATE_PATH.write_text('{"users": [], "events": []}\n', encoding="utf-8")
    SUBMISSIONS_PATH.write_text("[]\n", encoding="utf-8")


def test_health_endpoint_ok():
    client = TestClient(platform_api.app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_user_and_event_flow():
    client = TestClient(platform_api.app)

    create_user = client.post(
        "/users", json={"username": "student1", "display_name": "Student One"}
    )
    assert create_user.status_code == 200

    create_event = client.post(
        "/events", json={"username": "student1", "event_type": "curate", "units": 2}
    )
    assert create_event.status_code == 200

    leaderboard = client.get("/leaderboard")
    assert leaderboard.status_code == 200
    assert leaderboard.json()[0]["username"] == "student1"
    assert leaderboard.json()[0]["points"] == 6


def test_public_task_and_submission_flow():
    client = TestClient(platform_api.app)

    tasks = client.get("/public/tasks")
    assert tasks.status_code == 200
    assert tasks.json()
    task_id = tasks.json()[0]["task_id"]

    submission = client.post(
        "/public/submissions",
        json={
            "task_id": task_id,
            "response_text": "Sample community contribution",
            "contributor_name": "Public User",
            "self_rating": 4,
        },
    )
    assert submission.status_code == 200
    assert submission.json()["task_id"] == task_id
