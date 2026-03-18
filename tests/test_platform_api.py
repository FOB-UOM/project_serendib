import importlib.util
import sys
from pathlib import Path

from fastapi.testclient import TestClient

REPO_ROOT = Path(__file__).resolve().parents[1]
API_PATH = REPO_ROOT / "platform" / "api.py"
sys.path.insert(0, str(REPO_ROOT / "platform"))
COMMUNITY_EXPORT_PATH = (
    REPO_ROOT
    / "pillar-education-human-development"
    / "teacher-empowerment"
    / "community.approved.jsonl"
)


spec = importlib.util.spec_from_file_location("platform_api", API_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("Unable to load platform API module")
platform_api = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = platform_api
spec.loader.exec_module(platform_api)


def setup_function() -> None:
    platform_api._CONN.execute("DELETE FROM events")
    platform_api._CONN.execute("DELETE FROM users")
    platform_api._CONN.execute("DELETE FROM public_submissions")
    platform_api._CONN.commit()
    if COMMUNITY_EXPORT_PATH.exists():
        COMMUNITY_EXPORT_PATH.unlink()


def test_health_endpoint_ok():
    client = TestClient(platform_api.app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_user_and_event_flow():
    client = TestClient(platform_api.app)
    headers = {"x-api-key": "serendib-staff-local"}

    create_user = client.post(
        "/users",
        json={"username": "student1", "display_name": "Student One"},
        headers=headers,
    )
    assert create_user.status_code == 200

    create_event = client.post(
        "/events",
        json={"username": "student1", "event_type": "curate", "units": 2},
        headers=headers,
    )
    assert create_event.status_code == 200

    leaderboard = client.get("/leaderboard")
    assert leaderboard.status_code == 200
    assert leaderboard.json()[0]["username"] == "student1"
    assert leaderboard.json()[0]["points"] == 6


def test_public_task_and_submission_flow():
    client = TestClient(platform_api.app)
    headers = {"x-api-key": "serendib-staff-local"}
    maintainer_headers = {"x-api-key": "serendib-maintainer-local"}

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
    assert submission.json()["status"] == "pending"

    moderation_queue = client.get("/moderation/queue", headers=headers)
    assert moderation_queue.status_code == 200
    assert moderation_queue.json()
    submission_id = moderation_queue.json()[0]["id"]

    decision = client.post(
        "/moderation/review",
        json={"submission_id": submission_id, "decision": "approved", "note": "Looks good"},
        headers=headers,
    )
    assert decision.status_code == 200
    assert decision.json()["status"] == "approved"

    export = client.post("/moderation/export-approved", headers=maintainer_headers)
    assert export.status_code == 200
    assert export.json()["exported"] >= 1


def test_staff_endpoint_requires_api_key():
    client = TestClient(platform_api.app)
    response = client.get("/moderation/queue")
    assert response.status_code == 401


def test_operations_metrics_endpoint_for_staff():
    client = TestClient(platform_api.app)
    response = client.get("/operations/metrics", headers={"x-api-key": "serendib-staff-local"})
    assert response.status_code == 200
    payload = response.json()
    assert "throughput" in payload
    assert "pillar_growth" in payload
