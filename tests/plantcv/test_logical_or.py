import numpy as np
from plantcv.plantcv import logical_or


def test_logical_or():
    """Test for PlantCV."""
    # Create test data
    img1 = np.zeros((20, 20), dtype=np.uint8)
    img1[0:10, 0:10] = 255
    img2 = np.zeros((20, 20), dtype=np.uint8)
    img2[9:19, 9:19] = 255
    or_img = logical_or(bin_img1=img1, bin_img2=img2)
    assert np.count_nonzero(or_img) == 199
