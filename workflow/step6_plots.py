# workflow/step6_plots.py

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple, Union, Optional

import numpy as np

from workflow.step5_background import read_singleband_geotiff


def _connected_components_4(mask: np.ndarray) -> List[np.ndarray]:
    """Return connected components (4-connectivity) as arrays of (row, col) coords."""
    visited = np.zeros(mask.shape, dtype=bool)
    components: List[np.ndarray] = []

    rows, cols = mask.shape
    for r in range(rows):
        for c in range(cols):
            if not mask[r, c] or visited[r, c]:
                continue

            stack = [(r, c)]
            visited[r, c] = True
            coords = []

            while stack:
                rr, cc = stack.pop()
                coords.append((rr, cc))

                for nr, nc in ((rr - 1, cc), (rr + 1, cc), (rr, cc - 1), (rr, cc + 1)):
                    if 0 <= nr < rows and 0 <= nc < cols:
                        if mask[nr, nc] and not visited[nr, nc]:
                            visited[nr, nc] = True
                            stack.append((nr, nc))

            components.append(np.array(coords, dtype=np.int32))

    return components


def create_experimental_plots(
    ndvi_cleaned: np.ndarray,
    min_pixels: int = 200,
    threshold: float = 0.0,
) -> List[Dict]:
    """
    Step 6: Create experimental plots from a cleaned NDVI raster.

    Args:
        ndvi_cleaned: 2D NDVI array with background already removed (usually 0).
        min_pixels: minimum connected component size to count as a plot.
        threshold: pixels > threshold are treated as plot pixels.

    Returns:
        List of dicts with plot_id, pixel_count, bbox.
        bbox = (row_min, row_max, col_min, col_max) inclusive.
    """
    if ndvi_cleaned.ndim != 2:
        raise ValueError("ndvi_cleaned must be a 2D array (single band).")

    mask = np.isfinite(ndvi_cleaned) & (ndvi_cleaned > threshold)
    components = _connected_components_4(mask)

    plots: List[Dict] = []
    plot_idx = 1
    for coords in components:
        n = int(coords.shape[0])
        if n < min_pixels:
            continue

        rmin = int(coords[:, 0].min())
        rmax = int(coords[:, 0].max())
        cmin = int(coords[:, 1].min())
        cmax = int(coords[:, 1].max())

        plots.append(
            {
                "plot_id": f"plot_{plot_idx}",
                "pixel_count": n,
                "bbox": (rmin, rmax, cmin, cmax),
            }
        )
        plot_idx += 1

    return plots


def step6_create_plots(
    ndvi_cleaned_input: Union[np.ndarray, str, Path],
    min_pixels: int = 200,
    threshold: float = 0.0,
) -> List[Dict]:
    """
    Wrapper: accept cleaned NDVI as array OR GeoTIFF path.
    """
    if isinstance(ndvi_cleaned_input, (str, Path)):
        arr = read_singleband_geotiff(ndvi_cleaned_input)
    else:
        arr = ndvi_cleaned_input

    return create_experimental_plots(arr, min_pixels=min_pixels, threshold=threshold)
