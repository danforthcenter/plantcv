import numpy as np
from plantcv.plantcv import logical_xor


def test_logical_xor():
    """Test for PlantCV."""
    # Create test data
    img1 = np.zeros((20, 20), dtype=np.uint8)
    img1[0:10, 0:10] = 255
    img2 = np.zeros((20, 20), dtype=np.uint8)
    img2[9:19, 9:19] = 255
    xor_img = logical_xor(bin_img1=img1, bin_img2=img2)
    assert np.count_nonzero(xor_img) == 198
