from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_each_subpillar_has_minimum_100_records_in_dataset_v1() -> None:
    dataset_files = sorted(REPO_ROOT.glob("pillar-*/**/dataset.v1.jsonl"))
    assert dataset_files, "Expected dataset.v1.jsonl files in sub-pillar folders"

    for dataset_path in dataset_files:
        count = sum(
            1 for line in dataset_path.read_text(encoding="utf-8").splitlines() if line.strip()
        )
        assert count >= 100, f"{dataset_path} has only {count} records"
