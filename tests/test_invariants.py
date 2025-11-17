import pandas as pd
import pytest

# TODO: adjust to match your actual high-level API
from finmerge.io import read_input_folder
from finmerge.core import merge_dataframes, aggregate_by_keys


def test_sum_of_amounts_preserved(sample_data_dir):
    """Sum of amounts across all inputs should equal sum in final combined output."""
    dfs = read_input_folder(sample_data_dir)
    assert dfs, "No input DataFrames returned from sample_data_dir"

    # Make sure all inputs have the 'amount' column
    total_input = 0.0
    for df in dfs:
        assert "amount" in df.columns
        total_input += df["amount"].astype(float).sum()

    merged = merge_dataframes(dfs)
    combined = aggregate_by_keys(merged, ["account", "currency"])

    total_output = combined["amount"].astype(float).sum()

    assert total_input == pytest.approx(
        total_output
    ), "Total amount changed between inputs and combined output"


def test_no_duplicate_keys_after_aggregation(sample_data_dir):
    """After aggregating by (account, currency), there should be no duplicate keys."""
    dfs = read_input_folder(sample_data_dir)
    merged = merge_dataframes(dfs)
    combined = aggregate_by_keys(merged, ["account", "currency"])

    dup_mask = combined.duplicated(subset=["account", "currency"])
    assert not dup_mask.any(), "Found duplicate (account, currency) after aggregation"


def test_expected_schema_after_merge(sample_data_dir):
    """Check that the combined output schema matches expectations."""
    dfs = read_input_folder(sample_data_dir)
    merged = merge_dataframes(dfs)
    combined = aggregate_by_keys(merged, ["account", "currency"])

    # Adjust list as needed
    expected_cols = {"account", "currency", "amount"}
    missing = expected_cols - set(combined.columns)
    assert not missing, f"Missing expected columns: {missing}"
