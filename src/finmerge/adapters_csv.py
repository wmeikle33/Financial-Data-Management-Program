from __future__ import annotations
import csv, pathlib
from typing import Iterable, Dict, Any
from .interfaces import Loader, Record

class CSVFolderLoader(Loader):
    def __init__(self, folder: str, encoding: str = "utf-8") -> None:
        self.folder = folder
        self.encoding = encoding

    def load(self) -> Iterable[Record]:
        root = pathlib.Path(self.folder)
        for p in sorted(root.glob("*.csv")):
            with open(p, newline="", encoding=self.encoding) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    r: Dict[str, Any] = dict(row)
                    r["__source_path"] = str(p)
                    yield r
