from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


@dataclass
class TrainConfig:
    dataset: str
    base_model: str
    output_dir: str
    max_samples: int | None
    num_epochs: int
    batch_size: int
    learning_rate: float
    lora_r: int
    lora_alpha: int
    lora_dropout: float
    seed: int


def _ensure_unsloth_available() -> None:
    try:
        import unsloth  # noqa: F401  # type: ignore[import-not-found]
    except ImportError as e:  # noqa: F841
        message = (
            "Unsloth is not installed.\n"
            "Install GPU training deps first, for example:\n"
            "  pip install \"unsloth[cu121]\" bitsandbytes torch --extra-index-url "
            "https://download.pytorch.org/whl/cu121\n"
        )
        raise SystemExit(message)


def train_qlora_7b(cfg: TrainConfig) -> None:
    """
    Minimal Unsloth QLoRA fine-tuning loop for a 7B-class instruct model.

    This is intentionally simple and opinionated:
    - Uses `datasets` to read our JSONL format.
    - Uses the base model's chat template to serialize multi-turn conversations.
    - Runs supervised fine-tuning with QLoRA adapters using TRL.
    """

    _ensure_unsloth_available()

    from datasets import load_dataset  # type: ignore[import]
    from transformers import AutoTokenizer, TrainingArguments  # type: ignore[import]
    from unsloth import FastLanguageModel  # type: ignore[import]
    from trl import SFTTrainer  # type: ignore[import]

    dataset_path = Path(cfg.dataset)
    data_files: Dict[str, str] = {"train": str(dataset_path)}

    raw_dataset = load_dataset("json", data_files=data_files, split="train")
    if cfg.max_samples is not None:
        raw_dataset = raw_dataset.select(range(min(cfg.max_samples, len(raw_dataset))))

    tokenizer = AutoTokenizer.from_pretrained(cfg.base_model)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    def format_example(example: Dict[str, Any]) -> Dict[str, str]:
        # example["conversations"] is a list of {role, content}
        messages = example["conversations"]
        # For instruct-style chat template, we let tokenizer format it.
        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=False,
        )
        return {"text": text}

    train_dataset = raw_dataset.map(format_example, remove_columns=raw_dataset.column_names)

    max_seq_length = 2048
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=cfg.base_model,
        max_seq_length=max_seq_length,
        load_in_4bit=True,
    )

    model = FastLanguageModel.get_peft_model(
        model,
        r=cfg.lora_r,
        lora_alpha=cfg.lora_alpha,
        lora_dropout=cfg.lora_dropout,
        target_modules="all-linear",
    )

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=train_dataset,
        dataset_text_field="text",
        max_seq_length=max_seq_length,
        packing=True,
        args=TrainingArguments(
            per_device_train_batch_size=cfg.batch_size,
            num_train_epochs=cfg.num_epochs,
            learning_rate=cfg.learning_rate,
            logging_steps=10,
            output_dir=cfg.output_dir,
            seed=cfg.seed,
            report_to=[],
        ),
    )

    trainer.train()

    out_dir = Path(cfg.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    trainer.save_model(str(out_dir))

    # Save a tiny run metadata file for reproducibility.
    run_meta = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "train_config": asdict(cfg),
        "num_samples": len(train_dataset),
        "base_model": cfg.base_model,
        "library": "unsloth_qlora",
    }
    (out_dir / "run.json").write_text(json.dumps(run_meta, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Unsloth QLoRA fine-tuning for a 7B-class instruct model."
    )
    parser.add_argument(
        "--dataset",
        type=str,
        required=True,
        help="Path to Lanka-Instruct-v1 JSONL (see data/hf_dataset_template/).",
    )
    parser.add_argument(
        "--base-model",
        type=str,
        default="mistralai/Mistral-7B-Instruct-v0.3",
        help="HF model id for a 7B-class instruct model.",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="outputs/qlora_7b",
        help="Directory to store adapter and run metadata.",
    )
    parser.add_argument(
        "--max-samples",
        type=int,
        default=None,
        help="Optional cap on training samples (for quick experiments).",
    )
    parser.add_argument("--num-epochs", type=int, default=1)
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--learning-rate", type=float, default=2e-4)
    parser.add_argument("--lora-r", type=int, default=16)
    parser.add_argument("--lora-alpha", type=int, default=16)
    parser.add_argument("--lora-dropout", type=float, default=0.05)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    cfg = TrainConfig(
        dataset=args.dataset,
        base_model=args.base_model,
        output_dir=args.output_dir,
        max_samples=args.max_samples,
        num_epochs=args.num_epochs,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        lora_r=args.lora_r,
        lora_alpha=args.lora_alpha,
        lora_dropout=args.lora_dropout,
        seed=args.seed,
    )

    if not Path(cfg.dataset).exists():
        raise SystemExit(f"Dataset not found: {cfg.dataset}")

    train_qlora_7b(cfg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

