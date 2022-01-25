import pytest
import cv2
from plantcv.plantcv import analyze_bound_vertical, outputs


@pytest.mark.parametrize('pos,exp', [[220, 13], [2454, 16], [1, 0]])
def test_analyze_bound_vertical(pos, exp, test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    mask = cv2.imread(test_data.small_bin_img, -1)
    object_contours = test_data.load_composed_contours(test_data.small_composed_contours_file)
    _ = analyze_bound_vertical(img=img, obj=object_contours, mask=mask, line_position=pos)
    assert outputs.observations['default']['width_left_reference']['value'] == exp


def test_analyze_bound_vertical_grayscale_image(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Read in test data
    img = cv2.imread(test_data.small_gray_img, -1)
    mask = cv2.imread(test_data.small_bin_img, -1)
    object_contours = test_data.load_composed_contours(test_data.small_composed_contours_file)
    _ = analyze_bound_vertical(img=img, obj=object_contours, mask=mask, line_position=225)
    assert outputs.observations['default']['width_left_reference']['value'] == 16
