import pandas as pd
import pytest

# TODO: adjust these to match your actual core API
from finmerge.core import (
    merge_dataframes,      # e.g. merge_dataframes([ap, ar, inv]) -> df
    aggregate_by_keys,     # e.g. aggregate_by_keys(df, ["account", "currency"])
    normalize_dataframe,   # e.g. normalize_dataframe(df) -> df with canonical columns/types
)


def assert_frame_equal_unordered(a: pd.DataFrame, b: pd.DataFrame, sort_by=None):
    """Helper to compare DataFrames without worrying about row order."""
    if sort_by is None:
        sort_by = list(b.columns)
    a_sorted = a.sort_values(by=sort_by).reset_index(drop=True)
    b_sorted = b.sort_values(by=sort_by).reset_index(drop=True)
    pd.testing.assert_frame_equal(a_sorted, b_sorted, check_dtype=False)


def test_merge_simple(ap_df, ar_df):
    """AP + AR should merge into combined rows with correct total amounts."""
    combined = merge_dataframes([ap_df, ar_df])

    expected = pd.DataFrame(
        {
            "account": ["1000", "2000"],
            "currency": ["USD", "USD"],
            "amount": [22.0, 3.0],  # 10 + 5 + 7 for 1000, 3 for 2000
        }
    )

    # allow extra columns in 'combined', just check required ones
    actual = combined[["account", "currency", "amount"]]
    assert_frame_equal_unordered(actual, expected, sort_by=["account", "currency"])


def test_aggregate_by_multiple_keys(ap_df, ar_df):
    """Aggregate by (account, currency) should remove duplicates and sum amounts."""
    merged = merge_dataframes([ap_df, ar_df])

    agg = aggregate_by_keys(merged, ["account", "currency"])

    # No duplicate keys
    dup_mask = agg.duplicated(subset=["account", "currency"])
    assert not dup_mask.any()

    # Check sums by key
    key = ("1000", "USD")
    total_1000 = agg.loc[
        (agg["account"] == key[0]) & (agg["currency"] == key[1]), "amount"
    ].iloc[0]
    assert total_1000 == pytest.approx(22.0)


def test_normalize_dataframe_column_names():
    """Normalization should standardize column names and types."""
    raw = pd.DataFrame(
        {
            "Account": ["1000"],
            "CURR": ["USD"],
            "Amount": ["10.00"],  # as string
        }
    )

    norm = normalize_dataframe(raw)

    for col in ("account", "currency", "amount"):
        assert col in norm.columns

    assert norm["amount"].dtype != object  # not string
    assert norm["amount"].iloc[0] == pytest.approx(10.0)


def test_missing_required_column_raises():
    """Missing required columns should produce a clear error."""
    raw = pd.DataFrame(
        {
            "account": ["1000"],
            # "currency" missing
            "amount": [10],
        }
    )

    with pytest.raises(ValueError):
        normalize_dataframe(raw)
