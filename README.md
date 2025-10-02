# FinMerge (Sample / Redacted)

Public, redaction‑safe sample of a company tool that **combines multiple Excel/CSV files
with financial data** into a unified output. This repo demonstrates **architecture,
interfaces, tests, CLI, and CI** — while keeping your **proprietary connectors
and rules private**.

> ✅ Safe to share publicly. Proprietary logic (ERP connectors, mapping rules, conversions) is *not* included.

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
pip install -r requirements-dev.txt
python -m finmerge.cli --input sample_data --out sample_data/combined.csv --aggregate account currency
pytest -q
```
