import pytest
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv.homology import acute
from tests import synthetic


@pytest.mark.parametrize("win,exp", [[0, 0], [20, 4]])
def test_acute(win, exp, synthetic_rgb, synthetic_mask):
    """Test for PlantCV."""
    params.debug = "plot"
    homology_pts, _, _, _, _, _ = acute(img=synthetic_rgb, mask=synthetic_mask, win=win, threshold=90, label="plant")
    params.debug = None
    # recorded value: with win=20 the small object corner (10, 13), left leaf tip (30, 40),
    # stem base (58, 89), and right leaf tip (89, 64)
    assert len(homology_pts) == exp


@pytest.mark.parametrize("obj,win,thresh,exp", [[np.array(([[213, 190]], [[83, 61]], [[149, 246]])),
                                                 84, 192, 1],
                                                [np.array(([[103, 154]], [[27, 227]], [[152, 83]])),
                                                 35, 0, 0]])
def test_acute_small_contours(obj, win, thresh, exp):
    """Test for PlantCV."""
    params.debug = "plot"
    # Blank canvas large enough to hold each triangle
    img = np.zeros((260, 260, 3), dtype=np.uint8)
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    cv2.drawContours(mask, [obj], -1, 255, -1)
    homology_pts, _, _, _, _, _ = acute(img=img, mask=mask, win=win, threshold=thresh)
    params.debug = None
    assert len(homology_pts) == exp


def test_acute_flipped_contour(synthetic_gray):
    """Test for PlantCV."""
    params.debug = None
    mask = np.zeros(synthetic_gray.shape, dtype=np.uint8)
    contours, _ = synthetic.find_contours(synthetic.plant_mask(small_object=False))
    # Reverse the point order and swap x and y, giving the plant transposed with reversed orientation
    cnt = np.flip(contours[0])
    cv2.drawContours(mask, [cnt], -1, 255, -1)
    homology_pts, _, _, _, _, _ = acute(img=synthetic_gray, mask=mask, win=5, threshold=60)
    # recorded value: (30, 58) and (89, 61), the transposed stem corners
    assert len(homology_pts) == 2
