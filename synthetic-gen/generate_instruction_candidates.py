from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


def _load_seed_prompts(path: Path) -> List[str]:
    if not path.exists():
        raise SystemExit(f"Seed file not found: {path}")
    prompts = [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    if not prompts:
        raise SystemExit(f"No prompts found in: {path}")
    return prompts


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate synthetic instruction candidates (Bonito/LLaMA-Factory style stub)."
    )
    parser.add_argument("--seeds", type=Path, required=True, help="Text file with one seed prompt per line")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("instruction/synthetic_candidates.sample.jsonl"),
        help="Where to write JSONL candidates",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="Qwen/Qwen2.5-7B-Instruct",
        help="HF model id (must be available locally / via HF).",
    )
    parser.add_argument("--max-new-tokens", type=int, default=256)
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--top-p", type=float, default=0.9)
    parser.add_argument("--limit", type=int, default=5, help="Max number of candidates to generate")
    parser.add_argument("--domain", type=str, default="education_ol_al")
    parser.add_argument("--language", type=str, default="si", choices=["si", "ta", "en", "mixed"])
    args = parser.parse_args()

    seeds = _load_seed_prompts(args.seeds)[: args.limit]

    try:
        from transformers import AutoModelForCausalLM, AutoTokenizer  # type: ignore[import]
        import torch  # type: ignore[import]
    except ImportError:
        raise SystemExit("Missing deps. Install: pip install transformers accelerate torch")

    tokenizer = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        torch_dtype=getattr(torch, "bfloat16", None) or None,
        device_map="auto",
    )

    out_lines: List[str] = []
    now = datetime.now(timezone.utc).isoformat()

    for i, seed in enumerate(seeds, start=1):
        prompt = (
            "You are helping build a Sri Lankan-local instruction dataset.\n"
            "Write a short multi-turn dialogue (user+assistant) in Sinhala where possible.\n"
            "Be safe. Avoid PII. If the domain is law/regs, avoid giving definitive legal advice.\n\n"
            f"Seed topic: {seed}\n\n"
            "Output ONLY the assistant reply for the last turn, in plain text."
        )
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        outputs = model.generate(
            **inputs,
            max_new_tokens=args.max_new_tokens,
            do_sample=True,
            temperature=args.temperature,
            top_p=args.top_p,
        )
        gen = tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Heuristic: keep the tail; this is a stub and will be improved.
        response = gen.split("Output ONLY")[-1].strip()

        record: Dict[str, Any] = {
            "id": f"synthetic_{now}_{i:04d}",
            "language": args.language,
            "domain": args.domain,
            "source": "synthetic",
            "provenance": {"model": args.model, "seed": seed, "created_at": now},
            "conversations": [
                {"role": "user", "content": seed},
                {"role": "assistant", "content": response or "(empty generation)"},
            ],
        }
        out_lines.append(json.dumps(record, ensure_ascii=False))

    _ensure_parent(args.output)
    args.output.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(out_lines)} synthetic candidate(s) to: {args.output}")
    print("Next step: run Argilla verification before merging into release packs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

