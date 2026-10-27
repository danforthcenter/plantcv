import numpy as np
from plantcv.plantcv import create_labels, Objects, params
from tests import synthetic


def test_create_labels(synthetic_mask):
    """Test for PlantCV."""
    # ROI traced around the plant only
    cnt, cnt_str = synthetic.find_contours(synthetic.plant_mask(small_object=False))
    cnt_Obj = Objects(contours=[cnt], hierarchy=[cnt_str])
    masks, num = create_labels(mask=synthetic_mask, rois=cnt_Obj, roi_type="partial")
    assert np.unique(masks).size == (num + 1)
    # One ROI; only the 800 px plant overlaps it, so the small object is not labeled
    assert num == 1
    assert np.count_nonzero(masks) == 800


def test_create_labels_multi():
    """Test for PlantCV."""
    mask = synthetic.two_plants_mask()
    # ROI traced around both plants
    cnt, cnt_str = synthetic.find_contours(mask)
    cnt_Obj = Objects(contours=[cnt], hierarchy=[cnt_str])
    mask, num = create_labels(mask=mask, rois=cnt_Obj, roi_type="partial")
    assert np.unique(mask).size == (num + 1)
    # One ROI overlapping both 441 px disks
    assert num == 1
    assert np.count_nonzero(mask) == 2 * 441


def test_create_labels_no_roi(synthetic_mask):
    """Test for PlantCV."""
    _, num = create_labels(mask=synthetic_mask)
    # Plant and small object
    assert num == 2


def test_create_labels_debug(synthetic_mask):
    """Test for PlantCV."""
    params.debug = "plot"
    _, num = create_labels(mask=synthetic_mask)
    params.debug = None
    # Plant and small object
    assert num == 2
