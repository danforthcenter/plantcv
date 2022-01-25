import pytest
import cv2
import numpy as np
from skimage import img_as_ubyte
from plantcv.plantcv import image_fusion, Spectral_data


def test_image_fusion(test_data):
    """Test for PlantCV."""
    # Read in test data
    # 16-bit image
    img1 = cv2.imread(test_data.fmax, -1)
    img2 = cv2.imread(test_data.fmin)
    # 8-bit image
    img2 = img_as_ubyte(img2)
    fused_img = image_fusion(img1, img2, [480.0], [550.0, 640.0, 800.0])
    assert isinstance(fused_img, Spectral_data)


def test_image_fusion_size_diff(test_data):
    """Test for PlantCV."""
    img1 = cv2.imread(test_data.small_bin_img, 0)
    img2 = np.copy(img1)
    img2 = img2[0:10, 0:10]
    with pytest.raises(RuntimeError):
        _ = image_fusion(img1, img2, [480.0, 550.0, 670.0], [480.0, 550.0, 670.0])
