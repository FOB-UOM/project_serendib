from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List


@dataclass
class TrainConfig:
    mode: str
    dataset: str | None
    corpus: str | None
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


def _iter_text_files(path: Path) -> Iterable[Path]:
    if path.is_file():
        yield path
        return
    for p in sorted(path.rglob("*.txt")):
        if p.is_file():
            yield p


def _load_corpus_texts(corpus_path: Path, max_docs: int | None) -> List[str]:
    texts: List[str] = []
    for p in _iter_text_files(corpus_path):
        if max_docs is not None and len(texts) >= max_docs:
            break
        try:
            txt = p.read_text(encoding="utf-8").strip()
        except UnicodeDecodeError:
            txt = p.read_text(encoding="utf-8", errors="ignore").strip()
        if txt:
            texts.append(txt)
    return texts


def train_qlora(cfg: TrainConfig) -> None:
    _ensure_unsloth_available()

    from datasets import Dataset, load_dataset  # type: ignore[import]
    from transformers import AutoTokenizer, TrainingArguments  # type: ignore[import]
    from trl import SFTTrainer  # type: ignore[import]
    from unsloth import FastLanguageModel  # type: ignore[import]

    if cfg.mode == "instruction":
        if not cfg.dataset:
            raise SystemExit("--dataset is required for --mode instruction")
        dataset_path = Path(cfg.dataset)
        raw_dataset = load_dataset("json", data_files={"train": str(dataset_path)}, split="train")
        if cfg.max_samples is not None:
            raw_dataset = raw_dataset.select(range(min(cfg.max_samples, len(raw_dataset))))

        tokenizer = AutoTokenizer.from_pretrained(cfg.base_model)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        def format_example(example: Dict[str, Any]) -> Dict[str, str]:
            messages = example["conversations"]
            text = tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=False,
            )
            return {"text": text}

        train_dataset = raw_dataset.map(format_example, remove_columns=raw_dataset.column_names)
    elif cfg.mode == "continued-pretrain":
        if not cfg.corpus:
            raise SystemExit("--corpus is required for --mode continued-pretrain")
        corpus_path = Path(cfg.corpus)
        if not corpus_path.exists():
            raise SystemExit(f"Corpus path not found: {corpus_path}")
        texts = _load_corpus_texts(corpus_path, max_docs=cfg.max_samples)
        if not texts:
            raise SystemExit(f"No .txt files found under: {corpus_path}")
        train_dataset = Dataset.from_dict({"text": texts})
        tokenizer = AutoTokenizer.from_pretrained(cfg.base_model)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
    else:
        raise SystemExit(f"Unknown mode: {cfg.mode}")

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

    run_meta = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "train_config": asdict(cfg),
        "num_samples": len(train_dataset),
        "base_model": cfg.base_model,
        "library": "unsloth_qlora",
    }
    (out_dir / "run.json").write_text(json.dumps(run_meta, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Unsloth QLoRA training for Serendib layers.")
    parser.add_argument(
        "--mode",
        type=str,
        default="instruction",
        choices=["instruction", "continued-pretrain"],
        help="Training mode: instruction fine-tune vs continued-pretrain on raw corpus text.",
    )
    parser.add_argument(
        "--dataset",
        type=str,
        default=None,
        help="Path to instruction JSONL (required for --mode instruction).",
    )
    parser.add_argument(
        "--corpus",
        type=str,
        default=None,
        help="Path to a .txt file or a folder of .txt files (required for --mode continued-pretrain).",
    )
    parser.add_argument(
        "--base-model",
        type=str,
        default="mistralai/Mistral-7B-Instruct-v0.3",
        help="HF model id for a 7B-class model (instruct or base).",
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
        mode=args.mode,
        dataset=args.dataset,
        corpus=args.corpus,
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

    if cfg.mode == "instruction":
        if not cfg.dataset:
            raise SystemExit("--dataset is required for --mode instruction")
        if not Path(cfg.dataset).exists():
            raise SystemExit(f"Dataset not found: {cfg.dataset}")
    if cfg.mode == "continued-pretrain":
        if not cfg.corpus:
            raise SystemExit("--corpus is required for --mode continued-pretrain")
        if not Path(cfg.corpus).exists():
            raise SystemExit(f"Corpus not found: {cfg.corpus}")

    train_qlora(cfg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

