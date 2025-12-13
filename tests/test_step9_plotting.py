import pandas as pd
from workflow.step9_plotting import step9_plot_ndvi_vs_disease


def test_step9_creates_png(tmp_path):
    features_csv = tmp_path / "features.csv"
    disease_csv = tmp_path / "disease.csv"
    out_png = tmp_path / "plot.png"

    pd.DataFrame(
        {
            "plot_id": ["plot_1", "plot_2", "plot_3"],
            "ndvi_mean": [0.2, 0.5, 0.8],
        }
    ).to_csv(features_csv, index=False)

    pd.DataFrame(
        {
            "plot_id": ["plot_1", "plot_2", "plot_3"],
            "disease_severity": [80, 50, 20],
        }
    ).to_csv(disease_csv, index=False)

    p = step9_plot_ndvi_vs_disease(features_csv, disease_csv, out_png)

    assert p.exists()
    assert p.stat().st_size > 0
