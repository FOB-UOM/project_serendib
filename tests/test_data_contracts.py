import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "shared" / "scripts" / "validate_pillar_records.py"


def test_pillar_data_contract_validation_passes_for_seed_samples():
    result = subprocess.run(
        [sys.executable, str(VALIDATOR_PATH), "--root", str(REPO_ROOT)],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "invalid=0" in result.stdout
