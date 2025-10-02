from __future__ import annotations
from .interfaces import Loader, Record
from typing import Iterable

class ExcelFolderLoader(Loader):
    def __init__(self, *args, **kwargs) -> None:
        raise NotImplementedError("ExcelFolderLoader is private; implement in your internal repo.")
