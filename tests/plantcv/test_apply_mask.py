import pytest
import numpy as np
from plantcv.plantcv import apply_mask
from tests import synthetic


def test_apply_mask_white(synthetic_rgb, synthetic_mask):
    """Test for PlantCV."""
    masked_img = apply_mask(img=synthetic_rgb, mask=synthetic_mask, mask_color="white")
    assert np.unique(masked_img[np.where(synthetic_mask == 0)]) == 255


def test_apply_mask_black(synthetic_rgb, synthetic_mask):
    """Test for PlantCV."""
    masked_img = apply_mask(img=synthetic_rgb, mask=synthetic_mask, mask_color="black")
    assert np.unique(masked_img[np.where(synthetic_mask == 0)]) == 0


def test_apply_mask_hyperspectral():
    """Test for PlantCV."""
    hsi = synthetic.spectral_data()
    mask = synthetic.spectral_mask()
    masked_array = apply_mask(img=hsi.array_data, mask=mask, mask_color="black")
    # Every band is zero outside the mask and unchanged inside it
    assert np.all(masked_array[np.where(mask == 0)] == 0)
    assert np.array_equal(masked_array[np.where(mask > 0)], hsi.array_data[np.where(mask > 0)])


def test_apply_mask_bad_input(synthetic_rgb, synthetic_mask):
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _ = apply_mask(img=synthetic_rgb, mask=synthetic_mask, mask_color="wite")
