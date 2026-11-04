import numpy as np
from tests import synthetic
from plantcv.plantcv._globals import params
from plantcv.plantcv._helpers import _find_tips, _dilate


def test_helper_find_tips():
    """Test for PlantCV."""
    skel = synthetic.skeleton()
    mask = _dilate(synthetic.skeleton(), params.line_thickness, 1)
    tip_img1, tip_list1, _ = _find_tips(skel, mask)
    tip_img2, tip_list2, _ = _find_tips(skel)
    assert np.array_equal(tip_img1, tip_img2)
    assert tip_list1 == tip_list2
