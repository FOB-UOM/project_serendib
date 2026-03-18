import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_PATH = REPO_ROOT / "shared" / "ocr-pipeline" / "cli.py"


def test_cli_auto_mode_selects_qwen_for_handwritten_documents():
    result = subprocess.run(
        [sys.executable, str(CLI_PATH), "handwritten_scan_page_01.jpg", "--mode", "auto"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "Selected OCR engine: qwen2_vl" in result.stdout


def test_cli_runs_and_prints_selected_engine():
    result = subprocess.run(
        [sys.executable, str(CLI_PATH), "clean_document.png", "--mode", "auto"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "Selected OCR engine: tesseract" in result.stdout


def test_cli_rejects_unsupported_mode():
    result = subprocess.run(
        [sys.executable, str(CLI_PATH), "clean_document.png", "--mode", "invalid_mode"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0
    assert "invalid choice" in result.stderr
