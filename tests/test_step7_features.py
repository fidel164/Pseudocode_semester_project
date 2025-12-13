import numpy as np
from workflow.step7_features import extract_features


def test_step7_extract_features_two_plots():
    ndvi = np.zeros((10, 10), dtype=np.float32)

    # plot 1 bbox: rows 1-2, cols 1-3
    ndvi[1:3, 1:4] = 0.6

    # plot 2 bbox: rows 6-7, cols 6-8
    ndvi[6:8, 6:9] = 0.8

    plots = [
        {"plot_id": "plot_1", "pixel_count": 6, "bbox": (1, 2, 1, 3)},
        {"plot_id": "plot_2", "pixel_count": 6, "bbox": (6, 6, 6, 8)},
    ]

    feats = extract_features(ndvi, plots, threshold=0.0)

    assert len(feats) == 2

    f1 = next(x for x in feats if x["plot_id"] == "plot_1")
    f2 = next(x for x in feats if x["plot_id"] == "plot_2")

    assert abs(f1["ndvi_mean"] - 0.6) < 1e-6
    assert abs(f2["ndvi_mean"] - 0.8) < 1e-6
