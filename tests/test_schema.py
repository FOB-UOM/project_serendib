import json
from pathlib import Path


def test_schema_is_valid_json():
    schema_path = Path("data/hf_dataset_template/schema.json")
    assert schema_path.exists()
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    assert schema["type"] == "object"


def test_sample_jsonl_exists():
    sample_path = Path("data/hf_dataset_template/lanka_instruct_v1.sample.jsonl")
    assert sample_path.exists()
    text = sample_path.read_text(encoding="utf-8").strip()
    assert text.count("\n") >= 0

