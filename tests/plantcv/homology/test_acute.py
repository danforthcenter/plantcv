import pytest
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv.homology import acute


@pytest.mark.parametrize("win,exp", [[0, 0], [5, 2]])
def test_acute(win, exp, homology_test_data):
    """Test for PlantCV."""
    params.debug = "plot"
    # Read in test data
    img = cv2.imread(homology_test_data.small_rgb_img)
    mask = cv2.imread(homology_test_data.small_bin_img, -1)
    homology_pts, _, _, _, _, _ = acute(img=img, mask=mask, win=win, threshold=15, label="plant")
    params.debug = None
    assert len(homology_pts) == exp


@pytest.mark.parametrize("obj,win,thresh,exp", [[np.array(([[213, 190]], [[83, 61]], [[149, 246]])),
                                                 84, 192, 1],
                                                [np.array(([[103, 154]], [[27, 227]], [[152, 83]])),
                                                 35, 0, 0]])
def test_acute_small_contours(obj, win, thresh, exp, homology_test_data):
    """Test for PlantCV."""
    params.debug = "plot"
    # Read in test data
    img = cv2.imread(homology_test_data.small_rgb_img)
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    cv2.drawContours(mask, [obj], -1, 255, -1)
    homology_pts, _, _, _, _, _ = acute(img=img, mask=mask, win=win, threshold=thresh)
    params.debug = None
    assert len(homology_pts) == exp


def test_acute_flipped_contour(homology_test_data):
    """Test for PlantCV."""
    params.debug = None
    # Read in test data
    img = cv2.imread(homology_test_data.small_gray_img, -1)
    mask = np.zeros(img.shape, dtype=np.uint8)
    cnt = homology_test_data.load_composed_contours(homology_test_data.small_composed_contours_file)
    cnt = np.flip(cnt)
    cv2.drawContours(mask, [cnt], -1, 255, -1)
    homology_pts, _, _, _, _, _ = acute(img=img, mask=mask, win=5, threshold=15)
    assert len(homology_pts) == 2


def test_acute_ptvals_do_not_wrap_on_uint8_masks(homology_test_data):
    """Landmark window means are computed in float, so a uint8 mask cannot wrap."""
    params.debug = None
    img = cv2.imread(homology_test_data.small_rgb_img)
    mask = cv2.imread(homology_test_data.small_bin_img, -1)
    _, _, _, ptvals, _, _ = acute(img=img, mask=mask, win=50, threshold=15)
    # The window lies inside the plant, so every mask pixel in it is 255
    assert ptvals == [255.0]
