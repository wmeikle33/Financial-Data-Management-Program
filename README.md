# FinMerge (Sample / Redacted)

During my time at SEMILeds, Finance received separate Excel exports for AP, AR, and inventory from different systems. Manually combining them was slow and error-prone. FinMerge automates merging these files into one unified dataset keyed by account & currency.

Public, redaction‑safe sample of a company tool that **combines multiple Excel/CSV files
with financial data** into a unified output. This repo demonstrates sample code — while keeping your **proprietary connectors
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
