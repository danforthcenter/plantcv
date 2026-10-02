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
    assert int(outputs.observations['default_1']['gray_median']['value']) == 117


def test_grayscale_16bit(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Read in test data
    img = cv2.imread(test_data.small_gray_img, -1)
    mask = cv2.imread(test_data.small_bin_img, -1)

    _ = analyze_grayscale(gray_img=np.uint16(img), labeled_mask=mask, n_labels=1, bins=256)
    assert int(outputs.observations['default_1']['gray_median']['value']) == 117


def test_grayscale_multiple_objects(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Read in test data
    img = cv2.imread(test_data.small_gray_img, -1)
    mask = cv2.imread(test_data.small_bin_img, -1)
    # Split the plant into two labeled objects (label 3 is absent)
    labeled_mask = np.zeros(mask.shape, dtype=np.int32)
    labeled_mask[:, :215][mask[:, :215] > 0] = 1
    labeled_mask[:, 215:][mask[:, 215:] > 0] = 2
    _ = analyze_grayscale(gray_img=img, labeled_mask=labeled_mask, n_labels=3, bins=256, label=["a", "b", "c"])
    assert list(outputs.observations.keys()) == ["a_1", "b_2"]
    for i, sample in enumerate(("a_1", "b_2"), start=1):
        assert sum(outputs.observations[sample]['gray_frequencies']['value']) == np.count_nonzero(labeled_mask == i)
