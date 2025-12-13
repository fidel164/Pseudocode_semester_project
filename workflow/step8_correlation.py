# workflow/step8_correlation.py

from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Sequence, Union

import numpy as np
import pandas as pd


def load_csv(path: Union[str, Path]) -> pd.DataFrame:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"CSV not found: {p}")
    return pd.read_csv(p)


def merge_features_and_disease(
    features_csv: Union[str, Path],
    disease_csv: Union[str, Path],
    on: str = "plot_id",
) -> pd.DataFrame:
    """
    Merge Step 7 features with disease ratings.

    Requirements:
      - both CSVs have a column named `on` (default: plot_id)
    """
    feats = load_csv(features_csv)
    dis = load_csv(disease_csv)

    if on not in feats.columns:
        raise ValueError(f"'{on}' not found in features columns: {list(feats.columns)}")
    if on not in dis.columns:
        raise ValueError(f"'{on}' not found in disease columns: {list(dis.columns)}")

    merged = feats.merge(dis, on=on, how="inner")
    return merged


def pearson_corr(
    df: pd.DataFrame,
    x_cols: Sequence[str],
    y_col: str,
) -> pd.DataFrame:
    """
    Compute Pearson correlation between each x in x_cols and y_col.
    Returns a table with r and n (pairwise non-NA sample size).
    """
    if y_col not in df.columns:
        raise ValueError(f"y_col '{y_col}' not in df columns")

    rows: List[dict] = []
    y = df[y_col]

    for xcol in x_cols:
        if xcol not in df.columns:
            continue
        x = df[xcol]
        mask = x.notna() & y.notna()
        n = int(mask.sum())
        if n < 3:
            r = np.nan
        else:
            r = float(np.corrcoef(x[mask], y[mask])[0, 1])
        rows.append({"x": xcol, "y": y_col, "r_pearson": r, "n": n})

    return pd.DataFrame(rows).sort_values(
        "r_pearson", ascending=False, na_position="last"
    )


def step8_run(
    features_csv: Union[str, Path],
    disease_csv: Union[str, Path],
    disease_col: str,
    x_cols: Optional[Sequence[str]] = None,
) -> pd.DataFrame:
    """
    Full Step 8:
      1) merge features + disease
      2) run correlations of selected feature columns vs disease_col
    """
    merged = merge_features_and_disease(features_csv, disease_csv, on="plot_id")

    if x_cols is None:
        # sensible defaults from Step 7
        x_cols = ["ndvi_mean", "ndvi_std", "ndvi_min", "ndvi_max", "pixel_count"]

    return pearson_corr(merged, x_cols=x_cols, y_col=disease_col)
