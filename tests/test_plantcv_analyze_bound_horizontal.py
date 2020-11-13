import pytest
import cv2
from plantcv.plantcv import analyze_bound_horizontal, params, outputs


@pytest.mark.parametrize("debug,pos", [("print", 300), ("print", 100), ("plot", 1756), (None, 1756)])
def test_plantcv_analyze_bound_horizontal(test_data, tmpdir, debug, pos):
    # Test cache directory
    tmp_dir = tmpdir.mkdir("sub")
    # Set the output directory
    params.debug_outdir = str(tmp_dir)
    params.debug = debug
    # Read in test data
    img = cv2.imread(test_data["input_color_img"])
    mask = cv2.imread(test_data["input_binary_img"], -1)
    object_contours = test_data["input_object_contours"]
    # Run PlantCV function
    _ = analyze_bound_horizontal(img=img, obj=object_contours, mask=mask, line_position=pos)
    results = outputs.observations
    outputs.clear()
    assert len(results) == 7


def test_plantcv_analyze_bound_horizontal_small_image(test_data, tmpdir):
    # Test cache directory
    tmp_dir = tmpdir.mkdir("sub")
    # Set the output directory
    params.debug_outdir = str(tmp_dir)
    params.debug = "print"
    # Read in test data
    img = cv2.imread(test_data["setaria_small_plant_mask"])
    mask = cv2.imread(test_data["input_binary_img"], -1)
    object_contours = test_data["input_object_contours"]
    # Run PlantCV function
    _ = analyze_bound_horizontal(img=img, obj=object_contours, mask=mask, line_position=1756)
    results = outputs.observations
    outputs.clear()
    assert len(results) == 7


def test_plantcv_analyze_bound_horizontal_grayscale_image(test_data):
    # Read in test data
    img = cv2.imread(test_data["input_gray_img"], -1)
    mask = cv2.imread(test_data["input_binary_img"], -1)
    object_contours = test_data["input_object_contours"]
    # Test with a grayscale reference image and debug="plot"
    params.debug = "plot"
    boundary_img1 = analyze_bound_horizontal(img=img, obj=object_contours, mask=mask, line_position=1756)
    assert len(boundary_img1.shape) == 3


@pytest.mark.parametrize("pos,expected", [(-1000, 0), (0, 0), (2056, 713)])
def test_plantcv_analyze_bound_horizontal_neg_y(test_data, pos, expected):
    # Read in test data
    img = cv2.imread(test_data["input_color_img"])
    mask = cv2.imread(test_data["input_binary_img"], -1)
    object_contours = test_data["input_object_contours"]
    # Test with debug=None, line position that will trigger -y
    params.debug = "plot"
    _ = analyze_bound_horizontal(img=img, obj=object_contours, mask=mask, line_position=pos)
    result = outputs.observations['height_above_reference']['value']
    outputs.clear()
    assert result == expected
