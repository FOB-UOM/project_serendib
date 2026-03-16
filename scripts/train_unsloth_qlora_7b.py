from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    """
    Training stub for Unsloth QLoRA fine-tuning.

    This script is intentionally lightweight and beginner-friendly:
    - It documents the expected dataset shape (JSONL, multi-turn dialogues)
    - It sketches the Unsloth training flow without forcing GPU-only deps

    To implement fully:
    - add unsloth + bitsandbytes (GPU-specific) dependencies
    - load JSONL with `datasets`
    - map conversations to a chat template for the chosen base model
    - run SFT with QLoRA adapters, then export adapter + merged model
    """

    parser = argparse.ArgumentParser(description="Unsloth QLoRA training stub for a 7B base model.")
    parser.add_argument(
        "--dataset",
        type=Path,
        required=True,
        help="Path to Lanka-Instruct-v1 JSONL (see data/hf_dataset_template/)",
    )
    parser.add_argument(
        "--base-model",
        type=str,
        default="meta-llama/Llama-2-7b-hf",
        help="HF model id for a 7B base model (example default)",
    )
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/qlora_7b"))
    args = parser.parse_args()

    if not args.dataset.exists():
        raise SystemExit(f"Dataset not found: {args.dataset}")

    print("This is a stub.")
    print(f"Dataset: {args.dataset}")
    print(f"Base model: {args.base_model}")
    print(f"Output dir: {args.output_dir}")
    print("")
    print("Next steps to fully implement:")
    print("- Install GPU deps: unsloth, bitsandbytes, torch (CUDA), etc.")
    print("- Load dataset with `datasets.load_dataset('json', data_files=...)`")
    print("- Convert multi-turn `conversations` into model chat format")
    print("- Train with QLoRA (LoRA rank, target modules, 4-bit quantization)")
    print("- Save adapter + training logs; optionally merge for inference")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

