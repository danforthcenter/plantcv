import cv2
import numpy as np
from plantcv.plantcv import analyze_object, outputs


def test_analyze_object(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    mask = cv2.imread(test_data.small_bin_img, -1)
    obj_contour = test_data.load_composed_contours(test_data.small_composed_contours_file)
    _ = analyze_object(img=img, obj=obj_contour, mask=mask)
    assert int(outputs.observations["default"]["area"]["value"]) == 221


def test_analyze_object_grayscale_input(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Read in test data
    img = cv2.imread(test_data.small_gray_img, -1)
    mask = cv2.imread(test_data.small_bin_img, -1)
    obj_contour = test_data.load_composed_contours(test_data.small_composed_contours_file)
    _ = analyze_object(img=img, obj=obj_contour, mask=mask)
    assert int(outputs.observations["default"]["area"]["value"]) == 221


def test_analyze_object_zero_slope(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Create a test image
    img = np.zeros((50, 50, 3), dtype=np.uint8)
    img[10:11, 10:40, 0] = 255
    mask = img[:, :, 0]
    obj_contour = np.array([[[10, 10]], [[11, 10]], [[12, 10]], [[13, 10]], [[14, 10]], [[15, 10]], [[16, 10]],
                            [[17, 10]], [[18, 10]], [[19, 10]], [[20, 10]], [[21, 10]], [[22, 10]], [[23, 10]],
                            [[24, 10]], [[25, 10]], [[26, 10]], [[27, 10]], [[28, 10]], [[29, 10]], [[30, 10]],
                            [[31, 10]], [[32, 10]], [[33, 10]], [[34, 10]], [[35, 10]], [[36, 10]], [[37, 10]],
                            [[38, 10]], [[39, 10]], [[38, 10]], [[37, 10]], [[36, 10]], [[35, 10]], [[34, 10]],
                            [[33, 10]], [[32, 10]], [[31, 10]], [[30, 10]], [[29, 10]], [[28, 10]], [[27, 10]],
                            [[26, 10]], [[25, 10]], [[24, 10]], [[23, 10]], [[22, 10]], [[21, 10]], [[20, 10]],
                            [[19, 10]], [[18, 10]], [[17, 10]], [[16, 10]], [[15, 10]], [[14, 10]], [[13, 10]],
                            [[12, 10]], [[11, 10]]], dtype=np.int32)
    _ = analyze_object(img=img, obj=obj_contour, mask=mask)
    assert outputs.observations["default"]["longest_path"]["value"] == 30


def test_analyze_object_longest_axis_2d(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Create a test image
    img = np.zeros((50, 50, 3), dtype=np.uint8)
    img[0:5, 45:49, 0] = 255
    img[0:5, 0:5, 0] = 255
    mask = img[:, :, 0]
    obj_contour = np.array([[[45, 1]], [[45, 2]], [[45, 3]], [[45, 4]], [[46, 4]], [[47, 4]], [[48, 4]],
                            [[48, 3]], [[48, 2]], [[48, 1]], [[47, 1]], [[46, 1]], [[1, 1]], [[1, 2]],
                            [[1, 3]], [[1, 4]], [[2, 4]], [[3, 4]], [[4, 4]], [[4, 3]], [[4, 2]],
                            [[4, 1]], [[3, 1]], [[2, 1]]], dtype=np.int32)
    _ = analyze_object(img=img, obj=obj_contour, mask=mask)
    assert outputs.observations["default"]["longest_path"]["value"] == 186


def test_analyze_object_longest_axis_2e(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Create a test image
    img = np.zeros((50, 50, 3), dtype=np.uint8)
    img[10:15, 10:40, 0] = 255
    mask = img[:, :, 0]
    obj_contour = np.array([[[10, 10]], [[10, 11]], [[10, 12]], [[10, 13]], [[10, 14]], [[11, 14]], [[12, 14]],
                            [[13, 14]], [[14, 14]], [[15, 14]], [[16, 14]], [[17, 14]], [[18, 14]], [[19, 14]],
                            [[20, 14]], [[21, 14]], [[22, 14]], [[23, 14]], [[24, 14]], [[25, 14]], [[26, 14]],
                            [[27, 14]], [[28, 14]], [[29, 14]], [[30, 14]], [[31, 14]], [[32, 14]], [[33, 14]],
                            [[34, 14]], [[35, 14]], [[36, 14]], [[37, 14]], [[38, 14]], [[39, 14]], [[39, 13]],
                            [[39, 12]], [[39, 11]], [[39, 10]], [[38, 10]], [[37, 10]], [[36, 10]], [[35, 10]],
                            [[34, 10]], [[33, 10]], [[32, 10]], [[31, 10]], [[30, 10]], [[29, 10]], [[28, 10]],
                            [[27, 10]], [[26, 10]], [[25, 10]], [[24, 10]], [[23, 10]], [[22, 10]], [[21, 10]],
                            [[20, 10]], [[19, 10]], [[18, 10]], [[17, 10]], [[16, 10]], [[15, 10]], [[14, 10]],
                            [[13, 10]], [[12, 10]], [[11, 10]]], dtype=np.int32)
    _ = analyze_object(img=img, obj=obj_contour, mask=mask)
    assert outputs.observations["default"]["longest_path"]["value"] == 141


def test_analyze_object_small_contour(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    mask = cv2.imread(test_data.small_bin_img, -1)
    obj_contour = [np.array([[[0, 0]], [[0, 50]], [[50, 50]], [[50, 0]]], dtype=np.int32)]
    _ = analyze_object(img=img, obj=obj_contour, mask=mask)
    assert "defaults" not in outputs.observations
