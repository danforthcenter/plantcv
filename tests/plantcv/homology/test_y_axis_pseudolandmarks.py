import pytest
import cv2
import numpy as np
from plantcv.plantcv.homology import y_axis_pseudolandmarks


def test_y_axis_pseudolandmarks(synthetic_rgb, synthetic_mask):
    """Test for PlantCV."""
    left, right, center_h = y_axis_pseudolandmarks(mask=synthetic_mask, img=synthetic_rgb)
    assert all([left.shape == (20, 1, 2), right.shape == (20, 1, 2), center_h.shape == (20, 1, 2)])


@pytest.mark.parametrize("obj,shape", [
    [np.array(([[0, 0]], [[10, 0]], [[10, 10]], [[0, 10]])), (20, 1, 2)],
    [np.array(([[89, 222]], [[252, 39]], [[89, 207]])), (20, 1, 2)],
    [np.array(([[21, 11]], [[159, 155]], [[237, 11]])), (20, 1, 2)],
    [np.array(([[0, 0]], [[100, 0]], [[100, 100]], [[0, 100]])), (20, 1, 2)]
])
def test_y_axis_pseudolandmarks_small_obj(obj, shape, synthetic_rgb):
    """Test for PlantCV."""
    mask = np.zeros((250, 250), dtype=np.uint8)
    cv2.drawContours(mask, obj, -1, (255), thickness=-1)
    left, right, center_h = y_axis_pseudolandmarks(mask=mask, img=synthetic_rgb)
    assert all([np.shape(left) == shape, np.shape(right) == shape, np.shape(center_h) == shape])


def test_y_axis_pseudolandmarks_bad_input():
    """Test for PlantCV."""
    img = np.array([], dtype=np.uint8)
    mask = np.array([], dtype=np.uint8)
    result = y_axis_pseudolandmarks(mask=mask, img=img)
    assert np.array_equal(np.unique(result), np.array(["NA"]))
