import pytest
import numpy as np
from plantcv.plantcv.transform import rescale


def test_rescale(synthetic_gray):
    """Test for PlantCV."""
    gray_img = synthetic_gray
    rescaled_img = rescale(gray_img=gray_img, min_value=0, max_value=100)
    assert max(np.unique(rescaled_img)) == 100


def test_rescale_inf(synthetic_gray):
    """Test for PlantCV."""
    gray_img = synthetic_gray.astype(np.float32)
    gray_img[0,0] = np.inf
    rescaled_img = rescale(gray_img=gray_img, min_value=0, max_value=100)
    assert max(np.unique(rescaled_img)) == 100


def test_rescale_bad_input(synthetic_rgb):
    """Test for PlantCV."""
    rgb_img = synthetic_rgb
    with pytest.raises(RuntimeError):
        _ = rescale(gray_img=rgb_img)
