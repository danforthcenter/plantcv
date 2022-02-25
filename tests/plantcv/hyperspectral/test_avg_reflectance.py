import cv2
from plantcv.plantcv.hyperspectral import _avg_reflectance


def test_avg_reflectance(hyperspectral_test_data):
    """Test for PlantCV."""
    mask = cv2.imread(hyperspectral_test_data.hsi_mask_file, -1)
    avg_reflect = _avg_reflectance(hyperspectral_test_data.load_hsi(hyperspectral_test_data.hsi_file), mask=mask)
    assert len(avg_reflect) == 978
