import pytest
import numpy as np
from plantcv.plantcv import image_subtract


def test_image_subtract(synthetic_mask):
    """Test for PlantCV."""
    # read in images
    img1 = synthetic_mask
    img2 = np.copy(img1)
    new_img = image_subtract(img1, img2)
    assert np.count_nonzero(new_img) == 0


def test_image_subtract_fail(synthetic_rgb, synthetic_mask):
    """Test for PlantCV."""
    # read in images
    img1 = synthetic_mask
    img2 = synthetic_rgb
    # test
    with pytest.raises(RuntimeError):
        _ = image_subtract(gray_img1=img1, gray_img2=img2)
