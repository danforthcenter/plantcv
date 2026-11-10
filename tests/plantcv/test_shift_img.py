import pytest
from plantcv.plantcv import shift_img


@pytest.mark.parametrize("side", ["top", "bottom", "left", "right"])
def test_shift_img(side, synthetic_rgb):
    """Test for PlantCV."""
    # Shift within the 100 x 120 image
    shifted = shift_img(img=synthetic_rgb, number=30, side=side)
    assert synthetic_rgb.shape == shifted.shape


def test_shift_img_grayscale(synthetic_gray):
    """Test for PlantCV."""
    shifted = shift_img(img=synthetic_gray, number=30, side="top")
    assert synthetic_gray.shape == shifted.shape


def test_shift_img_bad_input(synthetic_gray):
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _ = shift_img(img=synthetic_gray, number=-30, side="top")


def test_shift_img_bad_side_input(synthetic_gray):
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _ = shift_img(img=synthetic_gray, number=30, side="starboard")
