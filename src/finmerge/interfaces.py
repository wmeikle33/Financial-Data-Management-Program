from __future__ import annotations
from typing import Iterable, Dict, Any, Protocol, runtime_checkable

Record = Dict[str, Any]

@runtime_checkable
class Loader(Protocol):
    def load(self) -> Iterable[Record]: ...

@runtime_checkable
class Transformer(Protocol):
    def transform(self, rows: Iterable[Record]) -> Iterable[Record]: ...

@runtime_checkable
class Combiner(Protocol):
    def combine(self, rows: Iterable[Record]) -> Iterable[Record]: ...

@runtime_checkable
class Sink(Protocol):
    def write(self, rows: Iterable[Record]) -> None: ...
