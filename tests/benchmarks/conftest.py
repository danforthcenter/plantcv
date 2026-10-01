"""Fixtures for pytest-benchmark runs: image-size axis and object-count axis."""
import cv2
import numpy as np
import pytest
from plantcv import plantcv as pcv


SIZES = {"small": (400, 400), "medium": (1000, 1000), "large": (4000, 3000)}
OBJECT_COUNTS = [1, 10, 100, 1000]
MASK_SHAPE = (2000, 2000)  # fixed size so only the object count varies


@pytest.fixture(scope="session", params=list(SIZES), ids=list(SIZES))
def sized_rgb(request, test_data):
    """The same real plant image resampled to each size on the size axis."""
    img = cv2.imread(test_data.small_rgb_img)
    return cv2.resize(img, SIZES[request.param], interpolation=cv2.INTER_LINEAR)


@pytest.fixture(scope="session", params=OBJECT_COUNTS, ids=lambda n: f"{n}obj")
def labeled_blobs(request):
    """Labeled mask with N non-overlapping circles on a fixed-size canvas.

    Returns (labeled_mask, binary_mask, n_labels). Circles sit on a regular
    grid, so the output is deterministic with no random seed to manage.
    """
    n = request.param
    h, w = MASK_SHAPE
    per_row = int(np.ceil(np.sqrt(n)))
    cell = min(h, w) // per_row
    radius = max(2, cell // 3)
    labeled = np.zeros(MASK_SHAPE, dtype=np.int32)
    for i in range(n):
        cy = (i // per_row) * cell + cell // 2
        cx = (i % per_row) * cell + cell // 2
        cv2.circle(labeled, (cx, cy), radius, i + 1, -1)
    binary = np.where(labeled > 0, 255, 0).astype(np.uint8)
    return labeled, binary, n


@pytest.fixture(autouse=True)
def _quiet_pcv():
    """No debug images, and clear Outputs so results don't pile up across rounds."""
    pcv.params.debug = None
    yield
    pcv.outputs.clear()
