import pytest
import cv2
import numpy as np
from plantcv.plantcv import y_axis_pseudolandmarks


def test_y_axis_pseudolandmarks(test_data):
    """Test for PlantCV."""
    img = cv2.imread(test_data.small_rgb_img)
    mask = cv2.imread(test_data.small_bin_img, -1)
    obj_contour = test_data.load_composed_contours(test_data.small_composed_contours_file)
    left, right, center_h = y_axis_pseudolandmarks(obj=obj_contour, mask=mask, img=img)
    assert all([left.shape == (20, 1, 2), right.shape == (20, 1, 2), center_h.shape == (20, 1, 2)])


@pytest.mark.parametrize("obj,mask,shape", [
    [np.array(([[0, 0]], [[10, 0]], [[10, 10]], [[0, 10]])), np.array(([[0, 0]], [[10, 0]], [[10, 10]], [[0, 10]])),
     (20, 1, 2)],
    [np.array(([[89, 222]], [[252, 39]], [[89, 207]])), np.array(([[42, 161]], [[2, 47]], [[211, 222]])), (20, 1, 2)],
    [np.array(([[21, 11]], [[159, 155]], [[237, 11]])), np.array(([[38, 54]], [[144, 169]], [[81, 137]])), (20, 1, 2)]
])
def test_y_axis_pseudolandmarks_small_obj(obj, mask, shape, test_data):
    """Test for PlantCV."""
    img = cv2.imread(test_data.small_rgb_img)
    left, right, center_h = y_axis_pseudolandmarks(obj=obj, mask=mask, img=img)
    assert all([np.shape(left) == shape, np.shape(right) == shape, np.shape(center_h) == shape])


def test_y_axis_pseudolandmarks_bad_input():
    """Test for PlantCV."""
    img = np.array([])
    mask = np.array([])
    obj_contour = np.array([])
    result = y_axis_pseudolandmarks(obj=obj_contour, mask=mask, img=img)
    assert np.array_equal(np.unique(result), np.array(["NA"]))


def test_y_axis_pseudolandmarks_bad_obj_input(test_data):
    """Test for PlantCV."""
    img = cv2.imread(test_data.small_rgb_img)
    with pytest.raises(RuntimeError):
        _ = y_axis_pseudolandmarks(obj=np.array([[-2, -2], [-2, -2]]), mask=np.array([[-2, -2], [-2, -2]]), img=img)
