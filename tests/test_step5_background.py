import numpy as np
from workflow.step5_background import remove_background


def test_background_removal_threshold():
    ndvi = np.array(
        [
            [-0.2, 0.05, 0.2],
            [np.nan, 0.3, 0.09],
        ],
        dtype=np.float32,
    )

    cleaned = remove_background(ndvi, threshold=0.10, background_value=0.0)

    # Background pixels -> 0
    assert cleaned[0, 0] == 0.0
    assert cleaned[0, 1] == 0.0
    assert cleaned[1, 0] == 0.0
    assert cleaned[1, 2] == 0.0

    # Vegetation pixels stay
    assert cleaned[0, 2] == 0.2
    assert cleaned[1, 1] == 0.3


import numpy as np
from workflow.step5_background import remove_background


def test_background_removal_threshold():
    ndvi = np.array(
        [
            [-0.2, 0.05, 0.2],
            [np.nan, 0.3, 0.09],
        ],
        dtype=np.float32,
    )

    cleaned = remove_background(ndvi, threshold=0.10, background_value=0.0)

    # Background pixels -> 0
    assert cleaned[0, 0] == 0.0
    assert cleaned[0, 1] == 0.0
    assert cleaned[1, 0] == 0.0
    assert cleaned[1, 2] == 0.0

    # Vegetation pixels stay
    assert cleaned[0, 2] == 0.2
    assert cleaned[1, 1] == 0.3


def test_background_removal_nodata():
    ndvi = np.array(
        [
            [0.5, -9999.0],
            [0.2, 0.05],
        ],
        dtype=np.float32,
    )

    cleaned = remove_background(
        ndvi,
        threshold=0.10,
        nodata=-9999.0,
        background_value=0.0,
    )

    assert cleaned[0, 0] == 0.5  # valid vegetation
    assert cleaned[0, 1] == 0.0  # nodata removed
    assert cleaned[1, 0] == 0.2  # valid vegetation
    assert cleaned[1, 1] == 0.0  # below threshold removed
