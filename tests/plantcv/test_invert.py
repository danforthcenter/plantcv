import numpy as np
from plantcv.plantcv import invert


def test_invert(synthetic_mask):
    """Test for PlantCV."""
    img = synthetic_mask
    inverted_img = invert(gray_img=img)
    total_px = img.shape[0] * img.shape[1]
    expected = total_px - np.count_nonzero(img)
    assert np.count_nonzero(inverted_img) == expected
