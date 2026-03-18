import importlib.util
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
RELEASE_ENGINE_PATH = REPO_ROOT / "shared" / "scripts" / "release_engine.py"

spec = importlib.util.spec_from_file_location("release_engine", RELEASE_ENGINE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("Unable to load release engine module")
release_engine = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = release_engine
spec.loader.exec_module(release_engine)


def test_release_engine_generates_quality_report(tmp_path: Path):
    (tmp_path / "pillar-education-human-development" / "teacher-empowerment").mkdir(parents=True)
    sample = (
        tmp_path
        / "pillar-education-human-development"
        / "teacher-empowerment"
        / "seed.sample.jsonl"
    )
    sample.write_text('{"record_id":"x"}\\n', encoding="utf-8")

    report_path = release_engine.generate_release(tmp_path, "v0.1-test")
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["release_tag"] == "v0.1-test"
    assert report["record_count"] == 1
