import pytest
import cv2
import numpy as np
from plantcv.plantcv import acute


@pytest.mark.parametrize("win", [0, 5])
def test_acute(win, test_data):
    """Test for PlantCV."""
    # Read in test data
    mask = cv2.imread(test_data.small_bin_img, -1)
    cnt = test_data.load_composed_contours(test_data.small_composed_contours_file)
    homology_pts = acute(obj=cnt, win=win, thresh=15, mask=mask)
    assert all([i == j] for i, j in zip(np.shape(homology_pts), (29, 1, 2)))


def test_acute_flipped_contour(test_data):
    """Test for PlantCV."""
    # Read in test data
    mask = cv2.imread(test_data.small_bin_img, -1)
    cnt = test_data.load_composed_contours(test_data.small_composed_contours_file)
    cnt = np.flip(cnt)
    homology_pts = acute(obj=cnt, win=5, thresh=15, mask=mask)
    assert all([i == j] for i, j in zip(np.shape(homology_pts), (29, 1, 2)))


@pytest.mark.parametrize("obj,win,thresh", [[np.array(([[213, 190]], [[83, 61]], [[149, 246]])), 84, 192],
                                            [np.array(([[103, 154]], [[27, 227]], [[152, 83]])), 35, 0]])
def test_acute_small_contours(obj, win, thresh, test_data):
    """Test for PlantCV."""
    # Read in test data
    mask = cv2.imread(test_data.small_bin_img, -1)
    homology_pts = acute(obj=obj, win=win, thresh=thresh, mask=mask)
    assert all([i == j] for i, j in zip(np.shape(homology_pts), (29, 1, 2)))
