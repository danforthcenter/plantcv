import pytest
import cv2
import numpy as np
from skimage import img_as_ubyte
from plantcv.plantcv import image_fusion, Spectral_data
from tests import synthetic


def test_image_fusion():
    """Test for PlantCV."""
    # 16-bit image
    img1 = synthetic.fluor_image()
    # 8-bit, 3-channel image
    img2 = cv2.cvtColor(img_as_ubyte(img1), cv2.COLOR_GRAY2BGR)
    fused_img = image_fusion(img1, img2, [480.0], [550.0, 640.0, 800.0])
    assert isinstance(fused_img, Spectral_data)
    assert fused_img.array_data.shape == (140, 160, 4)
    assert fused_img.wavelength_dict == {480.0: 0.0, 550.0: 1.0, 640.0: 2.0, 800.0: 3.0}
    # Both images become 8-bit (each 16-bit value divided by 256), then every band is scaled by 255
    expected = np.pad(synthetic.plant_gray(), 20, constant_values=synthetic.BACKGROUND_GRAY) / 255
    assert np.allclose(fused_img.array_data, expected[..., None])


def test_image_fusion_size_diff(synthetic_mask):
    """Test for PlantCV."""
    img1 = synthetic_mask
    img2 = np.copy(img1)
    img2 = img2[0:10, 0:10]
    with pytest.raises(RuntimeError):
        _ = image_fusion(img1, img2, [480.0, 550.0, 670.0], [480.0, 550.0, 670.0])
