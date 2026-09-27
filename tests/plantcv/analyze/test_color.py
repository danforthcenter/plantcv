import pytest
import cv2
import numpy as np
from plantcv.plantcv import outputs
from plantcv.plantcv.analyze import color as analyze_color


@pytest.mark.parametrize("colorspace", ["all", "lab", "hsv", "rgb"])
def test_color(colorspace, test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    mask = cv2.imread(test_data.small_bin_img, -1)
    _ = analyze_color(rgb_img=img, labeled_mask=mask, n_labels=1, colorspaces=colorspace)
    assert outputs.observations['default_1']['hue_median']['value'] == 80.0


def test_color_multiple_objects(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    mask = cv2.imread(test_data.small_bin_img, -1)
    # Split the plant into two labeled objects
    labeled_mask = np.zeros(mask.shape, dtype=np.int32)
    labeled_mask[:, :215][mask[:, :215] > 0] = 1
    labeled_mask[:, 215:][mask[:, 215:] > 0] = 2
    _ = analyze_color(rgb_img=img, labeled_mask=labeled_mask, n_labels=2, colorspaces="all", label=["a", "b"])
    assert list(outputs.observations.keys()) == ["a_1", "b_2"]
    for sample in ("a_1", "b_2"):
        assert sum(outputs.observations[sample]['blue_frequencies']['value']) == pytest.approx(100)


def test_color_bad_imgtype(test_data):
    """Test for PlantCV."""
    img_binary = cv2.imread(test_data.small_bin_img, -1)
    mask = cv2.imread(test_data.small_bin_img, -1)
    with pytest.raises(RuntimeError):
        _ = analyze_color(rgb_img=img_binary, labeled_mask=mask, n_labels=1)


def test_color_bad_hist_type(test_data):
    """Test for PlantCV."""
    img = cv2.imread(test_data.small_rgb_img)
    mask = cv2.imread(test_data.small_bin_img, -1)
    with pytest.raises(RuntimeError):
        _ = analyze_color(rgb_img=img, labeled_mask=mask, n_labels=1, colorspaces='bgr')
