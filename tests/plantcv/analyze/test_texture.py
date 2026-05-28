import cv2
import numpy as np
from plantcv.plantcv._globals import outputs
from plantcv.plantcv.analyze.texture import texture


def test_analyze_texture(test_data):
    """Test for PlantCV."""
    outputs.clear()
    gray = cv2.imread(test_data.small_gray_img, -1)
    mask = cv2.imread(test_data.small_bin_img, -1)
    _ = texture(gray, mask)
    assert isinstance(outputs.observations["default_1"]["contrast_1_0"]["value"], np.float64)


def test_analyze_texture_rgb(test_data):
    """Test for PlantCV."""
    outputs.clear()
    rgb_img = cv2.imread(test_data.small_rgb_img)
    mask = cv2.imread(test_data.small_bin_img, -1)
    _ = texture(rgb_img, mask)
    assert isinstance(outputs.observations["default_1"]["contrast_1_0"]["value"], np.float64)
