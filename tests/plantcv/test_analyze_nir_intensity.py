import cv2
import numpy as np
from plantcv.plantcv import analyze_nir_intensity, outputs


def test_analyze_nir(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Read in test data
    img = cv2.imread(test_data.small_gray_img, -1)
    mask = cv2.imread(test_data.small_bin_img, -1)

    _ = analyze_nir_intensity(gray_img=img, mask=mask, bins=256, histplot=True)
    assert int(outputs.observations['default']['nir_median']['value']) == 117


def test_analyze_nir_16bit(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Read in test data
    img = cv2.imread(test_data.small_gray_img, -1)
    mask = cv2.imread(test_data.small_bin_img, -1)

    _ = analyze_nir_intensity(gray_img=np.uint16(img), mask=mask, bins=256, histplot=True)
    assert int(outputs.observations['default']['nir_median']['value']) == 117
