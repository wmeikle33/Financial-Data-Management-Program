import pandas as pd
from excel_checker_sample import example_validate_and_merge

def test_example_validate_and_merge():
    a = pd.DataFrame({"A":[1,2], "B":[3,4]})
    b = pd.DataFrame({"A":[5], "B":[6]})
    out = example_validate_and_merge([a,b], ["A","B"])
    assert list(out.columns) == ["A","B"]
    assert len(out) == 3
