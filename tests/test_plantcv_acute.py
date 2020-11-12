import pytest
import cv2
import numpy as np
from plantcv.plantcv import acute


# Parameterize the test with win=0 and win=5
@pytest.mark.parametrize("win", [0, 5])
def test_plantcv_acute(test_data, win):
    # Read in test data
    mask = cv2.imread(test_data["setaria_small_mask"], -1)
    obj_contour = test_data['setaria_small_mask_contours']
    homology_pts = acute(obj=obj_contour, win=win, thresh=15, mask=mask)
    assert all([i == j] for i, j in zip(np.shape(homology_pts), (29, 1, 2)))


# Parameterize the test with various small contours, window sizes and thresholds
acute_paraemters = [
    (np.array(([[213, 190]], [[83, 61]], [[149, 246]])), 84, 192),
    (np.array(([[3, 29]], [[31, 102]], [[161, 63]])), 148, 56),
    (np.array(([[103, 154]], [[27, 227]], [[152, 83]])), 35, 0),
    (np.array(([[103, 154]], [[27, 227]], [[152, 83]])), 35, 0)
]


@pytest.mark.parametrize("obj,win,thresh", acute_paraemters)
def test_plantcv_acute_small_contours(test_data, obj, win, thresh):
    # Read in test data
    mask = cv2.imread(test_data["setaria_small_mask"], -1)
    homology_pts = acute(obj=obj, win=win, thresh=thresh, mask=mask)
    assert all([i == j] for i, j in zip(np.shape(homology_pts), (29, 1, 2)))
