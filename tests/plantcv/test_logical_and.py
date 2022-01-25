import numpy as np
from plantcv.plantcv import logical_and


def test_logical_and():
    """Test for PlantCV."""
    # Create test data
    img1 = np.zeros((20, 20), dtype=np.uint8)
    img1[0:10, 0:10] = 255
    img2 = np.zeros((20, 20), dtype=np.uint8)
    img2[9:19, 9:19] = 255
    and_img = logical_and(bin_img1=img1, bin_img2=img2)
    assert np.count_nonzero(and_img) == 1
