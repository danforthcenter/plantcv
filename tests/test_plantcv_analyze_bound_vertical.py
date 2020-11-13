import pytest
import cv2
from plantcv.plantcv import analyze_bound_vertical, params, outputs


@pytest.mark.parametrize("debug", ["print", "plot", None])
def test_plantcv_analyze_bound_vertical(test_data, tmpdir, debug):
    # Test cache directory
    tmp_dir = tmpdir.mkdir("sub")
    # Set the output directory
    params.debug_outdir = str(tmp_dir)
    params.debug = debug
    # Read in test data
    img = cv2.imread(test_data["input_color_img"])
    mask = cv2.imread(test_data["input_binary_img"], -1)
    object_contours = test_data["input_object_contours"]
    _ = analyze_bound_vertical(img=img, obj=object_contours, mask=mask, line_position=1000)
    result = outputs.observations['width_left_reference']['value']
    outputs.clear()
    assert result == 94


def test_plantcv_analyze_bound_vertical_grayscale_image(test_data):
    # Read in test data
    img = cv2.imread(test_data["input_gray_img"], -1)
    mask = cv2.imread(test_data["input_binary_img"], -1)
    object_contours = test_data["input_object_contours"]
    # Test with a grayscale reference image and debug="plot"
    params.debug = "plot"
    _ = analyze_bound_vertical(img=img, obj=object_contours, mask=mask, line_position=1000)
    result = outputs.observations['width_left_reference']['value']
    outputs.clear()
    assert result == 94


@pytest.mark.parametrize("pos,expected", [(2454, 441), (1, 0)])
def test_plantcv_analyze_bound_vertical_outlier_x(test_data, pos, expected):
    # Read in test data
    img = cv2.imread(test_data["input_color_img"])
    mask = cv2.imread(test_data["input_binary_img"], -1)
    object_contours = test_data["input_object_contours"]
    # Test with debug="plot", line position that will trigger -x
    params.debug = "plot"
    _ = analyze_bound_vertical(img=img, obj=object_contours, mask=mask, line_position=pos)
    result = outputs.observations['width_left_reference']['value']
    outputs.clear()
    assert result == expected
