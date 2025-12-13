from __future__ import annotations

from pathlib import Path
from typing import Optional, Union

import numpy as np

# Optional GDAL import (so docs/tests still import without GDAL installed)
try:
    import rasterio
except Exception:
    rasterio = None

try:
    from osgeo import gdal  # type: ignore
except Exception:
    gdal = None


def read_singleband_geotiff(path: Union[str, Path]) -> np.ndarray:
    """Read a single-band GeoTIFF into float32 using rasterio (preferred) or GDAL."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"NDVI file not found: {p}")

    if rasterio is not None:
        with rasterio.open(p) as src:
            arr = src.read(1).astype(np.float32)
        return arr

    if gdal is not None:
        ds = gdal.Open(str(p))
        if ds is None:
            raise ValueError(f"Could not open raster: {p}")
        band = ds.GetRasterBand(1)
        arr = band.ReadAsArray()
        if arr is None:
            raise ValueError(f"Could not read raster band from: {p}")
        return arr.astype(np.float32)

    raise ImportError(
        "Neither rasterio nor GDAL is installed. Install one to read GeoTIFF."
    )


def remove_background(
    ndvi: np.ndarray,
    threshold: float = 0.10,
    nodata: Optional[float] = None,
    background_value: float = 0.0,
) -> np.ndarray:
    """
    Remove background pixels from an NDVI raster.

    Rules:
      - NaN/inf are treated as background.
      - If nodata is provided, nodata pixels are background.
      - Pixels with NDVI < threshold are background.
      - Background pixels are set to `background_value`.

    Returns:
      A copy of NDVI with background pixels set to background_value.
    """
    if ndvi.ndim != 2:
        raise ValueError("NDVI must be a 2D array (single band).")

    cleaned = ndvi.astype(np.float32, copy=True)

    mask = np.isfinite(cleaned) & (cleaned >= threshold)
    if nodata is not None:
        mask &= cleaned != nodata

    cleaned[~mask] = background_value
    return cleaned


def step5_background_removal(
    ndvi_input: Union[np.ndarray, str, Path],
    threshold: float = 0.10,
    nodata: Optional[float] = None,
    background_value: float = 0.0,
) -> np.ndarray:
    """
    Step 5 wrapper:
      - Accepts NDVI as either a NumPy array (tests) OR a GeoTIFF path (real workflow).
      - Returns cleaned NDVI array.
    """
    if isinstance(ndvi_input, (str, Path)):
        ndvi = read_singleband_geotiff(ndvi_input)
    else:
        ndvi = ndvi_input

    return remove_background(
        ndvi,
        threshold=threshold,
        nodata=nodata,
        background_value=background_value,
    )


def write_singleband_geotiff(
    out_path: Union[str, Path],
    array: np.ndarray,
    reference_path: Union[str, Path],
) -> Path:
    out_path = Path(out_path)

    if rasterio is not None:
        with rasterio.open(reference_path) as ref:
            profile = ref.profile.copy()
            profile.update(count=1, dtype="float32")

        out_path.parent.mkdir(parents=True, exist_ok=True)
        with rasterio.open(out_path, "w", **profile) as dst:
            dst.write(array.astype(np.float32), 1)

        return out_path

    if gdal is not None:
        ref = gdal.Open(str(reference_path))
        if ref is None:
            raise ValueError(f"Could not open reference raster: {reference_path}")

        driver = gdal.GetDriverByName("GTiff")
        rows, cols = array.shape
        out_ds = driver.Create(str(out_path), cols, rows, 1, gdal.GDT_Float32)
        out_ds.SetGeoTransform(ref.GetGeoTransform())
        out_ds.SetProjection(ref.GetProjection())

        band = out_ds.GetRasterBand(1)
        band.WriteArray(array.astype(np.float32))
        band.FlushCache()

        out_ds = None
        ref = None
        return out_path

    raise ImportError(
        "Neither rasterio nor GDAL is installed. Install one to write GeoTIFF."
    )
