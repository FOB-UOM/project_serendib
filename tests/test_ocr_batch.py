import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BATCH_PATH = REPO_ROOT / "shared" / "ocr-pipeline" / "batch.py"


sys.path.insert(0, str(BATCH_PATH.parent))
spec = importlib.util.spec_from_file_location("ocr_batch", BATCH_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("Unable to load OCR batch module")
ocr_batch = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = ocr_batch
spec.loader.exec_module(ocr_batch)


def test_ocr_batch_routes_uncertain_documents(tmp_path: Path):
    incoming = tmp_path / "incoming"
    incoming.mkdir()
    (incoming / "clean_doc.png").write_text("x", encoding="utf-8")
    (incoming / "handwritten_scan.png").write_text("x", encoding="utf-8")

    output = tmp_path / "batch-results.jsonl"
    uncertain = tmp_path / "ocr-uncertain.json"
    result = ocr_batch.run_batch(incoming, output, uncertain, threshold=0.7)

    assert result["processed"] == 2
    assert result["uncertain"] == 1
