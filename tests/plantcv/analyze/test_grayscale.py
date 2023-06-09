import cv2
import numpy as np
from plantcv.plantcv import outputs
from plantcv.plantcv.analyze import grayscale as analyze_grayscale


def test_grayscale(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Read in test data
    img = cv2.imread(test_data.small_gray_img, -1)
    mask = cv2.imread(test_data.small_bin_img, -1)

    _ = analyze_grayscale(gray_img=img, labeled_mask=mask, n_labels=1, bins=256)
    assert int(outputs.observations['default1']['gray_median']['value']) == 117


def test_grayscale_16bit(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Read in test data
    img = cv2.imread(test_data.small_gray_img, -1)
    mask = cv2.imread(test_data.small_bin_img, -1)

    _ = analyze_grayscale(gray_img=np.uint16(img), labeled_mask=mask, n_labels=1, bins=256)
    assert int(outputs.observations['default1']['gray_median']['value']) == 117
