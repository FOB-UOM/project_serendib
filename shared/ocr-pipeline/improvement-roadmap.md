# Sinhala OCR Improvement Roadmap

## Goal
Create a durable OCR improvement loop that supports all pillars with high-quality Sinhala text extraction.

## Hybrid Strategy
- Baseline OCR: Tesseract for fast first-pass extraction
- Assisted OCR: Qwen2-VL for difficult/handwritten/low-quality pages
- Routing: lightweight heuristic router chooses fast vs assisted path

## Iteration Loop
1. Ingest pages to `incoming/`
2. Run `cli.py` with selected mode (`auto`, `tesseract`, `qwen2_vl`)
3. Store extracted outputs and review flags
4. Send uncertain samples to Argilla for human correction
5. Feed corrected results back into quality reports

## Immediate Priorities
- Add confidence-aware routing thresholds
- Add per-document quality summary output
- Add batch processing hooks for GitHub Actions (`ocr-batch.yml`)
