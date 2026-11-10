import numpy as np
from plantcv.plantcv.roi import roi2mask, multi_rect
from plantcv.plantcv import Objects
from tests import synthetic


def test_roi2mask(synthetic_rgb, synthetic_mask):
    """Test for PlantCV."""
    roi_cnt, roi_h = synthetic.find_contours(synthetic_mask)
    roi = Objects(contours=[roi_cnt], hierarchy=[roi_h])
    mask = roi2mask(img=synthetic_rgb, roi=roi)
    assert np.shape(mask)[0:2] == np.shape(synthetic_rgb)[0:2] and np.array_equal(np.unique(mask), np.array([0, 255]))


def test_roi2labeledmask(synthetic_rgb):
    """Test for PlantCV."""
    roi_objects = multi_rect(img=synthetic_rgb, coord=(25, 25), h=5, w=5,
                             spacing=(10, 10), nrows=2, ncols=2)
    m = roi2mask(synthetic_rgb, roi_objects)
    assert np.array_equal(np.unique(m), np.array([0, 1, 2, 3, 4]))
