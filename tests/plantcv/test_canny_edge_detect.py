import pytest
import numpy as np
from plantcv.plantcv import canny_edge_detect
from tests import synthetic


@pytest.mark.parametrize('color', ["white", "black"])
def test_canny_edge_detect(color, synthetic_rgb):
    """Test for PlantCV."""
    # The leaf edges fall inside the mask, and the small object and lower stem fall outside it,
    # so edges remain to be detected with either mask color
    mask = np.zeros(synthetic.PLANT_SHAPE, dtype=np.uint8)
    mask[20:75, 20:100] = 255
    edge_img = canny_edge_detect(img=synthetic_rgb, mask=mask, thickness=2, mask_color=color)
    # Assert that the output image has the dimensions of the input image and is binary
    assert synthetic_rgb.shape[:2] == edge_img.shape and np.array_equal(np.unique(edge_img), np.array([0, 255]))


def test_canny_edge_detect_grayscale(synthetic_mask):
    """Test for PlantCV."""
    edge_img = canny_edge_detect(img=synthetic_mask)
    # Assert that the output image has the dimensions of the input image and is binary
    assert synthetic_mask.shape == edge_img.shape and np.array_equal(np.unique(edge_img), np.array([0, 255]))


def test_canny_edge_detect_bad_input(synthetic_mask):
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _ = canny_edge_detect(img=synthetic_mask, mask=synthetic_mask, mask_color="gray")
