# workflow/step7_features.py

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Union

import numpy as np

from workflow.step5_background import read_singleband_geotiff


def extract_features(
    ndvi_cleaned: np.ndarray,
    plots: List[Dict],
    threshold: float = 0.0,
) -> List[Dict]:
    """
    Step 7: Feature extraction from cleaned NDVI per plot.

    Args:
        ndvi_cleaned: 2D NDVI array with background already removed (usually 0).
        plots: list of plot dicts from Step 6 with keys: plot_id, bbox, pixel_count.
        threshold: pixels > threshold are treated as vegetation pixels inside each bbox.

    Returns:
        List of dicts, one per plot, with NDVI stats.
    """
    if ndvi_cleaned.ndim != 2:
        raise ValueError("ndvi_cleaned must be a 2D array (single band).")

    features: List[Dict] = []

    for p in plots:
        plot_id = p["plot_id"]
        rmin, rmax, cmin, cmax = p["bbox"]

        # inclusive bbox -> slice needs +1 on end
        window = ndvi_cleaned[rmin : rmax + 1, cmin : cmax + 1]

        # keep only plot pixels (exclude background/NaNs)
        vals = window[np.isfinite(window) & (window > threshold)]

        if vals.size == 0:
            features.append(
                {
                    "plot_id": plot_id,
                    "pixel_count": p.get("pixel_count", 0),
                    "ndvi_mean": None,
                    "ndvi_std": None,
                    "ndvi_min": None,
                    "ndvi_max": None,
                }
            )
            continue

        features.append(
            {
                "plot_id": plot_id,
                "pixel_count": p.get("pixel_count", int(vals.size)),
                "ndvi_mean": float(np.mean(vals)),
                "ndvi_std": float(np.std(vals)),
                "ndvi_min": float(np.min(vals)),
                "ndvi_max": float(np.max(vals)),
            }
        )

    return features


def step7_extract_features(
    ndvi_cleaned_input: Union[np.ndarray, str, Path],
    plots: List[Dict],
    threshold: float = 0.0,
) -> List[Dict]:
    """Wrapper: accept cleaned NDVI as array OR GeoTIFF path."""
    if isinstance(ndvi_cleaned_input, (str, Path)):
        arr = read_singleband_geotiff(ndvi_cleaned_input)
    else:
        arr = ndvi_cleaned_input

    return extract_features(arr, plots, threshold=threshold)
