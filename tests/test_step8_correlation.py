import pandas as pd
from workflow.step8_correlation import pearson_corr


def test_step8_pearson_corr_runs():
    df = pd.DataFrame(
        {
            "plot_id": ["p1", "p2", "p3", "p4"],
            "ndvi_mean": [0.2, 0.4, 0.6, 0.8],
            "disease": [80, 60, 40, 20],  # strong negative relationship
        }
    )

    out = pearson_corr(df, x_cols=["ndvi_mean"], y_col="disease")
    assert len(out) == 1
    assert out.iloc[0]["n"] == 4
    assert out.iloc[0]["r_pearson"] < 0
