import pandas as pd
import pytest

# TODO: adjust these to match your actual IO API
from finmerge.io import (
    read_input_folder,   # e.g. read_input_folder(path) -> list[pd.DataFrame]
    write_output_file,   # e.g. write_output_file(df, path)
)


def test_read_input_folder(sample_data_dir):
    """Read all supported files from sample_data and return some DataFrames."""
    dfs = read_input_folder(sample_data_dir)

    assert isinstance(dfs, list)
    assert dfs, "Expected at least one DataFrame from sample_data"

    for df in dfs:
        assert isinstance(df, pd.DataFrame)


def test_read_input_folder_ignores_unsupported(tmp_path):
    """Unsupported extensions (like .txt) should be ignored or raise a clean error."""
    # create a bogus text file
    f = tmp_path / "random.txt"
    f.write_text("not a spreadsheet")

    # Depending on your design, either:
    # - ignore unsupported files, OR
    # - raise a clear exception.
    try:
        dfs = read_input_folder(tmp_path)
    except ValueError:
        # acceptable behavior: explicit error
        return

    # Or: if your function silently ignores unsupported files, ensure it doesn't crash
    assert isinstance(dfs, list)


def test_write_output_file_roundtrip(tmp_path):
    """Writing a CSV and reading it back should preserve the data."""
    df = pd.DataFrame(
        {
            "account": ["1000", "2000"],
            "currency": ["USD", "USD"],
            "amount": [10.0, 20.0],
        }
    )

    out_path = tmp_path / "combined.csv"
    write_output_file(df, out_path)

    assert out_path.exists()

    roundtrip = pd.read_csv(out_path)
    pd.testing.assert_frame_equal(
        roundtrip.sort_values("account").reset_index(drop=True),
        df.sort_values("account").reset_index(drop=True),
        check_dtype=False,
    )
