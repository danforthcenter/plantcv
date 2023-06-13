import pytest
import cv2
import numpy as np
from plantcv.plantcv.homology import y_axis_pseudolandmarks


def test_y_axis_pseudolandmarks(test_data):
    """Test for PlantCV."""
    img = cv2.imread(test_data.small_rgb_img)
    mask = cv2.imread(test_data.small_bin_img, -1)
    left, right, center_h = y_axis_pseudolandmarks(mask=mask, img=img)
    assert all([left.shape == (20, 1, 2), right.shape == (20, 1, 2), center_h.shape == (20, 1, 2)])


@pytest.mark.parametrize("mask,shape", [
    [np.array(([[0, 0]], [[10, 0]], [[10, 10]], [[0, 10]]), dtype=np.uint32),
     (20, 1, 2)],
    [np.array(([[42, 161]], [[2, 47]], [[211, 222]]), dtype=np.uint32), (20, 1, 2)],
    [np.array(([[38, 54]], [[144, 169]], [[81, 137]]), dtype=np.uint32), (20, 1, 2)]
])
def test_y_axis_pseudolandmarks_small_obj(mask, shape, test_data):
    """Test for PlantCV."""
    img = cv2.imread(test_data.small_rgb_img)
    left, right, center_h = y_axis_pseudolandmarks(mask=mask, img=img)
    assert all([np.shape(left) == shape, np.shape(right) == shape, np.shape(center_h) == shape])


def test_y_axis_pseudolandmarks_bad_input():
    """Test for PlantCV."""
    img = np.array([])
    mask = np.array([])
    result = y_axis_pseudolandmarks(mask=mask, img=img)
    assert np.array_equal(np.unique(result), np.array(["NA"]))


# def test_y_axis_pseudolandmarks_bad_obj_input(test_data):
#     """Test for PlantCV."""
#     img = cv2.imread(test_data.small_rgb_img)
#     with pytest.raises(RuntimeError):
#         _ = y_axis_pseudolandmarks(mask=np.array([[-2, -2], [-2, -2]]), img=img)
