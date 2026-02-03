# LLM Evaluation Harness (Structured Document Reasoning)

A reproducible evaluation pipeline to benchmark LLM providers on document-grounded QA tasks.

## What this repo contains
- `data/docs/`: structured documents used for reasoning tasks
- `data/gold/qa_gold.jsonl`: gold-standard QA dataset with base/edge cases (and room for ambiguous cases)
- `src/`: evaluation runner, scoring, metrics, cost tracking, and reporting
- `results/results.csv`: per-question outputs (answer, correctness, latency, token estimates, cost)
- `reports/`: summary, manual audit, and failure modes

## Quickstart (Mock baseline)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m src.run_eval --config configs/mock.yaml
python -m src.make_manual_audit
python -m src.failure_modes
python -m src.analyze_manual_audit
