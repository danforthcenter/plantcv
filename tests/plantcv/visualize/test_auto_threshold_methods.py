import pytest
from plantcv.plantcv.visualize import auto_threshold_methods


def test_auto_threshold_methods_bad_input(synthetic_rgb):
    """Test for PlantCV."""
    img = synthetic_rgb
    with pytest.raises(RuntimeError):
        _ = auto_threshold_methods(gray_img=img)


def test_auto_threshold_methods(synthetic_gray):
    """Test for PlantCV."""
    img = synthetic_gray
    labeled_imgs = auto_threshold_methods(gray_img=img)
    assert len(labeled_imgs) == 3
