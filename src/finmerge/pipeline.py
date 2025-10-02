from __future__ import annotations
from typing import Iterable, List
from itertools import chain
from .interfaces import Loader, Transformer, Combiner, Sink, Record

def run_pipeline(loaders: List[Loader], transformer: Transformer, combiner: Combiner, sink: Sink) -> None:
    raw: Iterable[Record] = chain.from_iterable(loader.load() for loader in loaders)
    norm: Iterable[Record] = transformer.transform(raw)
    out: Iterable[Record] = combiner.combine(norm)
    sink.write(out)
