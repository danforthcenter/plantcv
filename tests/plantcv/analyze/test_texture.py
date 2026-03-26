import cv2
import numpy as np
from plantcv.plantcv._globals import outputs
from plantcv.plantcv.analyze.texture import texture, _default_levels


def test_analyze_texture_default_levels(test_data):
    """Test for PlantCV."""
    img = cv2.imread(test_data.small_rgb_img)
    lvls = _default_levels(img, 10)
    assert lvls == 10


def test_analyze_texture_default_levels_uint8(test_data):
    """Test for PlantCV."""
    img = cv2.imread(test_data.small_rgb_img)
    lvls = _default_levels(img, None)
    assert lvls == 256


def test_analyze_texture_default_levels_uint16(test_data):
    """Test for PlantCV."""
    img = np.zeros((50, 50), dtype=np.uint16)
    img[0,0] = 1000
    lvls = _default_levels(img, None)
    assert lvls == 1001


def test_analyze_texture(test_data):
    """Test for PlantCV."""
    gray = cv2.imread(test_data.small_gray_img, -1)
    mask = cv2.imread(test_data.small_bin_img, -1)
    _ = texture(gray, mask)
    assert isinstance(outputs.observations["default_1"]["contrast"]["value"], np.float64)


def test_analyze_texture_rgb(test_data):
    """Test for PlantCV."""
    rgb_img = cv2.imread(test_data.small_rgb_img)
    mask = cv2.imread(test_data.small_bin_img, -1)
    _ = texture(rgb_img, mask)
    assert isinstance(outputs.observations["default_1"]["contrast"]["value"], np.float64)
