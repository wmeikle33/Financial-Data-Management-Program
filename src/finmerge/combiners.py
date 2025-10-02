from __future__ import annotations
from typing import Iterable, Dict, Any, List, Tuple
from collections import defaultdict
from .interfaces import Combiner, Record

class PassThrough(Combiner):
    def combine(self, rows: Iterable[Record]) -> Iterable[Record]:
        for r in rows:
            yield r

class SumAggregator(Combiner):
    def __init__(self, keys: List[str]) -> None:
        self.keys = keys

    def combine(self, rows: Iterable[Record]) -> Iterable[Record]:
        buckets: Dict[Tuple[Any, ...], float] = defaultdict(float)
        for r in rows:
            try:
                amt = float(r.get("amount", 0))
            except (TypeError, ValueError):
                amt = 0.0
            key = tuple(r.get(k) for k in self.keys)
            buckets[key] += amt
        for key, total in buckets.items():
            out = {k: v for k, v in zip(self.keys, key)}
            out["total_amount"] = f"{total:.2f}"
            yield out
