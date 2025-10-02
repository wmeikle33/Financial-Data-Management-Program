import pandas as pd
import numpy as np
from typing import Iterable, List, Dict, Any, Optional

def ColIdxToXlName(idx):
    if idx < 1:
        raise ValueError("Index is too small")
    result = ""
    while True:
        if idx > 26:
            idx, r = divmod(idx - 1, 26)
            result = chr(r + ord('A')) + result
        else:
            return chr(idx + ord('A') - 1) + result

def example_validate_and_merge(frames: List[pd.DataFrame], required_cols: List[str]) -> pd.DataFrame:
    """
    Example helper illustrating how validation + concatenate could be structured.
    - Ensures required columns exist.
    - Concatenates frames with aligned columns and returns a single DataFrame.
    """
    checked = []
    for i, df in enumerate(frames):
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            raise ValueError(f"DataFrame {i} missing required columns: {missing}")
        # Ensure consistent column order
        checked.append(df[required_cols].copy())
    out = pd.concat(checked, ignore_index=True)
    return out
