import pytest
import cv2
from plantcv.plantcv import analyze_bound_horizontal, outputs


@pytest.mark.parametrize('pos,exp', [[200, 58], [-1, 0], [100, 0], [150, 11]])
def test_analyze_bound_horizontal(pos, exp, test_data):
    # Clear previous outputs
    outputs.clear()
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    # img_above_bound_only = cv2.imread(os.path.join(TEST_DATA, TEST_MASK_SMALL_PLANT))
    mask = cv2.imread(test_data.small_bin_img, -1)
    object_contours = test_data.load_composed_contours(test_data.small_composed_contours_file)
    # _ = pcv.analyze_bound_horizontal(img=img, obj=object_contours, mask=mask, line_position=300)
    # _ = pcv.analyze_bound_horizontal(img=img, obj=object_contours, mask=mask, line_position=100)
    # _ = pcv.analyze_bound_horizontal(img=img_above_bound_only, obj=object_contours, mask=mask, line_position=1756)
    # _ = pcv.analyze_bound_horizontal(img=img, obj=object_contours, mask=mask, line_position=1756)
    _ = analyze_bound_horizontal(img=img, obj=object_contours, mask=mask, line_position=pos)
    assert outputs.observations["default"]["height_above_reference"]["value"] == exp


def test_analyze_bound_horizontal_grayscale_image(test_data):
    # Read in test data
    img = cv2.imread(test_data.small_gray_img, -1)
    mask = cv2.imread(test_data.small_bin_img, -1)
    object_contours = test_data.load_composed_contours(test_data.small_composed_contours_file)
    boundary_img = analyze_bound_horizontal(img=img, obj=object_contours, mask=mask, line_position=200)
    assert len(boundary_img.shape) == 3
