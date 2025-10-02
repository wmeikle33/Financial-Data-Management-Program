from __future__ import annotations
import argparse
from .adapters_csv import CSVFolderLoader
from .mappers import SchemaMapper
from .combiners import PassThrough, SumAggregator
from .sinks import CSVSink
from .pipeline import run_pipeline

def main() -> None:
    p = argparse.ArgumentParser(description="Public sample: combine financial files.")
    p.add_argument("--input", "-i", required=True, help="Folder with CSV files (public demo).")
    p.add_argument("--out", "-o", required=True, help="Output file path (.csv)")
    p.add_argument("--aggregate", nargs="*", help="Group-by keys for summing 'amount' (e.g., account currency).")
    p.add_argument("--keep-extra", action="store_true", help="Keep non-canonical columns in output.")
    args = p.parse_args()

    loader = CSVFolderLoader(args.input)
    mapper = SchemaMapper(keep_extra=args.keep_extra)
    combiner = SumAggregator(args.aggregate) if args.aggregate else PassThrough()
    sink = CSVSink(args.out)

    run_pipeline([loader], mapper, combiner, sink)

if __name__ == "__main__":
    main()
