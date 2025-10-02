from finmerge.adapters_csv import CSVFolderLoader
from finmerge.mappers import SchemaMapper
from finmerge.combiners import SumAggregator
from finmerge.sinks import CSVSink
from finmerge.pipeline import run_pipeline
from pathlib import Path
import csv

def write_csv(path: Path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)

def test_sum_aggregator(tmp_path: Path):
    d = tmp_path
    write_csv(d / "a.csv", ["Date","Account","Amount","Currency","Department"], [
        ["2024-01-01","1000","10.0","USD","R&D"],
        ["2024-01-02","1000","5.0","USD","R&D"],
        ["2024-01-03","2000","7.5","USD","Sales"],
    ])
    write_csv(d / "b.csv", ["TxnDate","Acct","Value","Curr","Dept"], [
        ["2024-01-01","1000","2.0","USD","R&D"],
        ["2024-01-02","2000","3.0","USD","Sales"],
    ])

    loader = CSVFolderLoader(str(d))
    mapper = SchemaMapper()
    comb = SumAggregator(keys=["account","currency"])
    out_csv = d / "out.csv"
    sink = CSVSink(str(out_csv))

    run_pipeline([loader], mapper, comb, sink)

    rows = list(csv.DictReader(open(out_csv, newline="", encoding="utf-8")))
    totals = { (r["account"], r["currency"]): float(r["total_amount"]) for r in rows }
    assert totals[("1000","USD")] == 17.0
    assert totals[("2000","USD")] == 10.5
