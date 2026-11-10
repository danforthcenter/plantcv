import pytest
import cv2
import numpy as np
from plantcv.plantcv import outputs
from plantcv.plantcv.homology.x_axis_pseudolandmark import x_axis_pseudolandmarks as x_axis


def test_x_axis_pseudolandmarks(synthetic_rgb, synthetic_mask):
    """Test for PlantCV."""
    top, bottom, center_v = x_axis(img=synthetic_rgb, mask=synthetic_mask)
    assert all([top.shape == (20, 1, 2), bottom.shape == (20, 1, 2), center_v.shape == (20, 1, 2)])


@pytest.mark.parametrize("obj,shape", [
    [np.array(([[0, 0]], [[10, 0]], [[10, 10]], [[0, 10]])), (20, 1, 2)],
    [np.array(([[89, 222]], [[252, 39]], [[89, 207]])), (20, 1, 2)],
    [np.array(([[21, 11]], [[159, 155]], [[237, 11]])), (20, 1, 2)],
    [np.array(([[0, 0]], [[100, 0]], [[100, 100]], [[0, 100]])), (20, 1, 2)]
])
def test_x_axis_pseudolandmarks_small_obj(obj, shape, synthetic_rgb):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    mask = np.zeros((250, 250), dtype=np.uint8)
    cv2.drawContours(mask, obj, -1, (255), thickness=-1)
    top, bottom, center_v = x_axis(img=synthetic_rgb, mask=mask)
    assert all([np.shape(top) == shape, np.shape(bottom) == shape, np.shape(center_v) == shape])


def test_x_axis_pseudolandmarks_bad_input():
    """Test for PlantCV."""
    img = np.array([], dtype=np.uint8)
    mask = np.array([], dtype=np.uint8)
    result = x_axis(img=img, mask=mask)
    assert np.array_equal(np.unique(result), np.array(["NA"]))
