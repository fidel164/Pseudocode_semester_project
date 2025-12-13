import numpy as np
from workflow.step6_plots import create_experimental_plots


def test_step6_finds_two_plots():
    ndvi = np.zeros((50, 60), dtype=np.float32)

    # plot 1 rectangle
    ndvi[5:20, 5:25] = 0.6

    # plot 2 rectangle
    ndvi[30:45, 30:55] = 0.7

    plots = create_experimental_plots(ndvi, min_pixels=50, threshold=0.0)

    assert len(plots) == 2

    bboxes = sorted([p["bbox"] for p in plots])
    assert bboxes[0] == (5, 19, 5, 24)
    assert bboxes[1] == (30, 44, 30, 54)
