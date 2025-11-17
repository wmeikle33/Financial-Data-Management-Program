import pathlib
import pandas as pd
import pytest


@pytest.fixture(scope="session")
def project_root() -> pathlib.Path:
    # Assumes standard layout: repo root / src / finmerge / ...
    return pathlib.Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def sample_data_dir(project_root: pathlib.Path) -> pathlib.Path:
    # Assumes you have a "sample_data" folder at repo root.
    d = project_root / "sample_data"
    if not d.exists():
        pytest.skip("sample_data directory not found")
    return d


@pytest.fixture
def tmp_output_path(tmp_path: pathlib.Path) -> pathlib.Path:
    return tmp_path / "combined.csv"


# --- Simple DataFrames for core tests --- #

@pytest.fixture
def ap_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "account": ["1000", "1000"],
            "currency": ["USD", "USD"],
            "amount": [10.0, 5.0],
            "source": ["AP", "AP"],
        }
    )


@pytest.fixture
def ar_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "account": ["1000", "2000"],
            "currency": ["USD", "USD"],
            "amount": [7.0, 3.0],
            "source": ["AR", "AR"],
        }
    )


@pytest.fixture
def inventory_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "account": ["INV1", "INV2"],
            "currency": ["USD", "TWD"],
            "amount": [100.0, 200.0],
            "source": ["INV", "INV"],
        }
    )
