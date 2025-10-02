from __future__ import annotations
import csv
from typing import Iterable, Dict, Any
from .interfaces import Sink, Record

class CSVSink(Sink):
    def __init__(self, path: str, encoding: str = "utf-8") -> None:
        self.path = path
        self.encoding = encoding

    def write(self, rows: Iterable[Record]) -> None:
        rows = list(rows)
        if not rows:
            open(self.path, "w", encoding=self.encoding).close()
            return
        fieldnames = sorted(set().union(*[r.keys() for r in rows]))
        with open(self.path, "w", newline="", encoding=self.encoding) as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            for r in rows:
                w.writerow(r)

class ExcelSink(Sink):
    def __init__(self, *args, **kwargs) -> None:
        raise NotImplementedError("ExcelSink is private; implement in your internal repo.")
