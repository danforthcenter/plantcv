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


def test_white_balance_gray_8bit(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_gray_img, -1)
    # Test with mode "max"
    white_balanced = white_balance(img=img, mode='max', roi=(5, 5, 80, 80))
    assert img.shape == white_balanced.shape


@pytest.mark.parametrize("mode", ["hist", "max"])
def test_white_balance_rgb(mode, test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    # Test without an ROI
    white_balanced = white_balance(img=img, mode=mode, roi=None)
    assert img.shape == white_balanced.shape


@pytest.mark.parametrize("mode, roi", [['hist', (5, 5, 5, 5, 5)],  # too many points
                                       ['hist', (5., 5, 5, 5)],  # not all integers
                                       ['histogram', (5, 5, 80, 80)]])  # bad mode
def test_white_balance_bad_input(mode, roi, test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_bin_img, -1)
    with pytest.raises(RuntimeError):
        _ = white_balance(img=img, mode=mode, roi=roi)
