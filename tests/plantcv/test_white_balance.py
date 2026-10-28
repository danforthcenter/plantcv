import pytest
import cv2
from plantcv.plantcv import white_balance


def test_white_balance_gray_16bit(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.fmax, -1)
    # Test with mode "hist"
    white_balanced = white_balance(img=img, mode='hist', roi=(5, 5, 80, 80))
    assert img.shape == white_balanced.shape


def test_white_balance_gray_8bit(synthetic_gray):
    """Test for PlantCV."""
    # Test with mode "max"
    white_balanced = white_balance(img=synthetic_gray, mode='max', roi=(5, 5, 80, 80))
    assert synthetic_gray.shape == white_balanced.shape


@pytest.mark.parametrize("mode", ["hist", "max"])
def test_white_balance_rgb(mode, synthetic_rgb):
    """Test for PlantCV."""
    # Test without an ROI
    white_balanced = white_balance(img=synthetic_rgb, mode=mode, roi=None)
    assert synthetic_rgb.shape == white_balanced.shape


@pytest.mark.parametrize("mode, roi", [['hist', (5, 5, 5, 5, 5)],  # too many points
                                       ['hist', (5., 5, 5, 5)],  # not all integers
                                       ['histogram', (5, 5, 80, 80)]])  # bad mode
def test_white_balance_bad_input(mode, roi, synthetic_mask):
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _ = white_balance(img=synthetic_mask, mode=mode, roi=roi)
