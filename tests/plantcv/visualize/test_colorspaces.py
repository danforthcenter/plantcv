import pytest
import cv2
from plantcv.plantcv.visualize import colorspaces


def test_colorspaces(visualize_test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(visualize_test_data.small_rgb_img)
    vis_img = colorspaces(rgb_img=img)
    assert vis_img.shape == (335, 1000, 3)


def test_colorspaces_bad_input(visualize_test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(visualize_test_data.small_gray_img, -1)
    with pytest.raises(RuntimeError):
        _ = colorspaces(rgb_img=img)
