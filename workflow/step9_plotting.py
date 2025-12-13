# workflow/step9_plotting.py

from __future__ import annotations

from pathlib import Path
from typing import Union

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def step9_plot_ndvi_vs_disease(
    features_csv: Union[str, Path],
    disease_csv: Union[str, Path],
    out_png: Union[str, Path],
    x_col: str = "ndvi_mean",
    y_col: str = "disease_severity",
) -> Path:
    """
    Step 9: Make a scatter plot (with regression line) of NDVI vs disease severity.

    Saves a PNG to out_png and returns the output path.
    """
    features_csv = Path(features_csv)
    disease_csv = Path(disease_csv)
    out_png = Path(out_png)

    feats = pd.read_csv(features_csv)
    dis = pd.read_csv(disease_csv)

    if "plot_id" not in feats.columns or "plot_id" not in dis.columns:
        raise ValueError("Both CSVs must contain a 'plot_id' column.")

    df = feats.merge(dis, on="plot_id", how="inner")

    if x_col not in df.columns:
        raise ValueError(f"x_col '{x_col}' not found in merged data.")
    if y_col not in df.columns:
        raise ValueError(f"y_col '{y_col}' not found in merged data.")

    x = df[x_col].astype(float)
    y = df[y_col].astype(float)

    mask = np.isfinite(x) & np.isfinite(y)
    x = x[mask]
    y = y[mask]

    if len(x) < 2:
        raise ValueError("Not enough paired data points to plot.")

    # Regression line
    coef = np.polyfit(x, y, 1)
    poly = np.poly1d(coef)

    plt.figure()
    plt.scatter(x, y)
    plt.plot(x, poly(x))

    plt.xlabel("Mean NDVI per plot" if x_col == "ndvi_mean" else x_col)
    plt.ylabel("Disease severity (%)" if y_col == "disease_severity" else y_col)
    plt.title("NDVI vs Disease Severity")

    out_png.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_png, dpi=300, bbox_inches="tight")
    plt.close()

    return out_png
