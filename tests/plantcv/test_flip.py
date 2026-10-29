import pytest
from plantcv.plantcv import flip


def test_flip(synthetic_rgb):
    """Test for PlantCV."""
    img = synthetic_rgb
    flipped_img = flip(img=img, direction="horizontal")
    assert img.shape == flipped_img.shape


def test_flip_grayscale(synthetic_gray):
    """Test for PlantCV."""
    gray_img = synthetic_gray
    flipped_img = flip(img=gray_img, direction="vertical")
    assert gray_img.shape == flipped_img.shape


def test_flip_bad_input(synthetic_rgb):
    """Test for PlantCV."""
    img = synthetic_rgb
    with pytest.raises(RuntimeError):
        _ = flip(img=img, direction="vert")
