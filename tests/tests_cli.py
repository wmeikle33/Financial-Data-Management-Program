import subprocess
import sys

import pandas as pd
import pytest


def run_cli(args, cwd):
    """Helper to run `python -m finmerge.cli ...`."""
    cmd = [sys.executable, "-m", "finmerge.cli"] + args
    return subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
    )


def test_cli_help(project_root):
    """`--help` should print usage info and exit 0."""
    result = run_cli(["--help"], cwd=project_root)
    assert result.returncode == 0
    assert "usage" in result.stdout.lower() or "help" in result.stdout.lower()


def test_cli_happy_path(project_root, sample_data_dir, tmp_output_path):
    """Run CLI on sample_data and produce a combined.csv output."""
    rel_input = sample_data_dir.name
    rel_out = tmp_output_path.name

    # Use paths relative to project_root for simplicity
    result = run_cli(
        [
            "--input",
            rel_input,
            "--out",
            rel_out,
            "--aggregate",
            "account",
            "currency",
        ],
        cwd=project_root,
    )

    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

    assert result.returncode == 0

    # Combined file should exist in tmp_output_path's directory (tmp_path)
    # But since we passed rel_out in project_root, adjust accordingly:
    out_path = project_root / rel_out
    assert out_path.exists()

    df = pd.read_csv(out_path)
    assert not df.empty
    for col in ("account", "currency", "amount"):
        assert col in df.columns


def test_cli_invalid_input_folder(project_root):
    """Nonexistent input folder should fail with a clear error."""
    result = run_cli(
        [
            "--input",
            "does_not_exist",
            "--out",
            "combined.csv",
        ],
        cwd=project_root,
    )

    assert result.returncode != 0
    assert "not found" in (result.stderr.lower() + result.stdout.lower())
