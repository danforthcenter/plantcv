import pytest
import cv2
from plantcv.plantcv.visualize import auto_threshold_methods


def test_auto_threshold_methods_bad_input(visualize_test_data):
    """Test for PlantCV."""
    img = cv2.imread(visualize_test_data.small_rgb_img)
    with pytest.raises(RuntimeError):
        _ = auto_threshold_methods(gray_img=img)


def test_auto_threshold_methods(visualize_test_data):
    """Test for PlantCV."""
    img = cv2.imread(visualize_test_data.small_gray_img, -1)
    labeled_imgs = auto_threshold_methods(gray_img=img)
    assert len(labeled_imgs) == 3
