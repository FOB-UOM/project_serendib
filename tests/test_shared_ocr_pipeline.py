import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OCR_PIPELINE_DIR = REPO_ROOT / "shared" / "ocr-pipeline"
CLI_PATH = OCR_PIPELINE_DIR / "cli.py"


def test_hybrid_router_auto_mode_selects_qwen_for_difficult_names():
    sys.path.insert(0, str(OCR_PIPELINE_DIR))
    from hybrid_router import route_ocr

    assert route_ocr("handwritten_scan_page_01.jpg", "auto") == "qwen2_vl"


def test_cli_runs_and_prints_selected_engine():
    result = subprocess.run(
        [sys.executable, str(CLI_PATH), "clean_document.png", "--mode", "auto"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "Selected OCR engine: tesseract" in result.stdout
