import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "shared" / "scripts"))
sys.path.insert(0, str(REPO_ROOT / "platform"))
ARGILLA_PIPELINE_PATH = REPO_ROOT / "shared" / "scripts" / "argilla_pipeline.py"

spec = importlib.util.spec_from_file_location("argilla_pipeline", ARGILLA_PIPELINE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("Unable to load argilla pipeline module")
argilla_pipeline = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = argilla_pipeline
spec.loader.exec_module(argilla_pipeline)


def setup_function() -> None:
    argilla_pipeline.DB_CONN.execute("DELETE FROM public_submissions")
    argilla_pipeline.DB_CONN.commit()
    argilla_pipeline.MODERATION_QUEUE_PATH.write_text("[]\n", encoding="utf-8")


def test_build_queue_and_export_flow_creates_approved_record(tmp_path: Path):
    submitted_at = datetime.now(timezone.utc).isoformat()
    argilla_pipeline.DB_CONN.execute(
        """
        INSERT INTO public_submissions
        (task_id, response_text, contributor_name, self_rating, submitted_at, status, exported)
        VALUES (?, ?, ?, ?, ?, 'pending', 0)
        """,
        ("env-001", "Community sustainability input", "Pilot User", 4, submitted_at),
    )
    argilla_pipeline.DB_CONN.commit()

    queue = argilla_pipeline.build_moderation_queue()
    assert queue
    submission_id = queue[0]["submission_id"]

    updated = argilla_pipeline.moderate_item(submission_id, "approved", "reviewer-1")
    assert updated["status"] == "approved"

    exported = argilla_pipeline.export_approved_to_pillar(root=tmp_path)
    assert exported >= 1

    target = (
        tmp_path
        / "pillar-society-environment"
        / "sustainability-climate"
        / "community.approved.jsonl"
    )
    assert target.exists()
    last_line = target.read_text(encoding="utf-8").strip().splitlines()[-1]
    payload = json.loads(last_line)
    assert payload["review_status"] == "approved"
