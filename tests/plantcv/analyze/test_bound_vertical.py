import pytest
import cv2
from plantcv.plantcv import outputs
from plantcv.plantcv.analyze import bound_vertical as analyze_bound_vertical


@pytest.mark.parametrize('pos,exp', [[220, 13], [2454, 16], [1, 0]])
def test_bound_vertical(pos, exp, test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    mask = cv2.imread(test_data.small_bin_img, -1)
    _ = analyze_bound_vertical(img=img, labeled_mask=mask, n_labels=1, line_position=pos)
    assert outputs.observations['default1']['width_left_reference']['value'] == exp


def test_bound_vertical_grayscale_image(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Read in test data
    img = cv2.imread(test_data.small_gray_img, -1)
    mask = cv2.imread(test_data.small_bin_img, -1)
    _ = analyze_bound_vertical(img=img, labeled_mask=mask, n_labels=1, line_position=225)
    assert outputs.observations['default1']['width_left_reference']['value'] == 16
