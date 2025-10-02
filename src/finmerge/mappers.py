from __future__ import annotations
from typing import Iterable, Dict, Any, List
from .interfaces import Transformer, Record

_DEFAULT_SYNONYMS = {
    "date": ["date", "Date", "txn_date", "TxnDate"],
    "account": ["account", "Account", "acct", "Acct"],
    "amount": ["amount", "Amount", "value", "Value", "amt", "Amt"],
    "currency": ["currency", "Currency", "curr", "Curr"],
    "department": ["department", "Department", "dept", "Dept"],
}

class SchemaMapper(Transformer):
    def __init__(self, synonyms: Dict[str, List[str]] | None = None, keep_extra: bool = False) -> None:
        self.synonyms = synonyms or _DEFAULT_SYNONYMS
        self.keep_extra = keep_extra

    def transform(self, rows: Iterable[Record]) -> Iterable[Record]:
        for r in rows:
            out: Dict[str, Any] = {"__source_path": r.get("__source_path")}
            for canon, alts in self.synonyms.items():
                for key in alts:
                    if key in r and r[key] not in (None, ""):
                        out[canon] = r[key]
                        break
            if self.keep_extra:
                for k, v in r.items():
                    if k not in out:
                        out[k] = v
            yield out
