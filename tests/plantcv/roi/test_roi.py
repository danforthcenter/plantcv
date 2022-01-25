import pytest
import cv2
import numpy as np
from plantcv.plantcv.roi import from_binary_image, rectangle, circle, ellipse, multi, custom


def test_from_binary_image(roi_test_data):
    """Test for PlantCV."""
    # Read in test RGB image
    rgb_img = cv2.imread(roi_test_data.small_rgb_img)
    # Create a binary image
    bin_img = np.zeros(np.shape(rgb_img)[0:2], dtype=np.uint8)
    cv2.rectangle(bin_img, (100, 100), (10, 10), 255, -1)
    roi, _ = from_binary_image(bin_img=bin_img, img=rgb_img)
    # Assert the contours and hierarchy lists contain only the ROI
    assert np.shape(roi) == (1, 360, 1, 2)


def test_from_binary_image_grayscale_input(roi_test_data):
    """Test for PlantCV."""
    # Read in a test grayscale image
    gray_img = cv2.imread(roi_test_data.small_gray_img, -1)
    # Create a binary image
    bin_img = np.zeros(np.shape(gray_img)[0:2], dtype=np.uint8)
    cv2.rectangle(bin_img, (100, 100), (10, 10), 255, -1)
    roi, _ = from_binary_image(bin_img=bin_img, img=gray_img)
    # Assert the contours and hierarchy lists contain only the ROI
    assert np.shape(roi) == (1, 360, 1, 2)


def test_from_binary_image_bad_binary_input(roi_test_data):
    """Test for PlantCV."""
    # Read in test RGB image
    rgb_img = cv2.imread(roi_test_data.small_rgb_img)
    # Binary input is required but an RGB input is provided
    with pytest.raises(RuntimeError):
        _, _ = from_binary_image(bin_img=rgb_img, img=rgb_img)


def test_rectangle(roi_test_data):
    """Test for PlantCV."""
    # Read in test RGB image
    rgb_img = cv2.imread(roi_test_data.small_rgb_img)
    roi, _ = rectangle(x=100, y=100, h=100, w=100, img=rgb_img)
    # Assert the contours and hierarchy lists contain only the ROI
    assert np.shape(roi) == (1, 4, 1, 2)


def test_rectangle_grayscale_input(roi_test_data):
    """Test for PlantCV."""
    # Read in a test grayscale image
    gray_img = cv2.imread(roi_test_data.small_gray_img, -1)
    roi, _ = rectangle(x=100, y=100, h=100, w=100, img=gray_img)
    # Assert the contours and hierarchy lists contain only the ROI
    assert np.shape(roi) == (1, 4, 1, 2)


def test_rectangle_out_of_frame(roi_test_data):
    """Test for PlantCV."""
    # Read in test RGB image
    rgb_img = cv2.imread(roi_test_data.small_rgb_img)
    # The resulting rectangle needs to be within the dimensions of the image
    with pytest.raises(RuntimeError):
        _, _ = rectangle(x=100, y=100, h=500, w=3000, img=rgb_img)


def test_circle(roi_test_data):
    """Test for PlantCV."""
    # Read in test RGB image
    rgb_img = cv2.imread(roi_test_data.small_rgb_img)
    roi, _ = circle(x=100, y=100, r=75, img=rgb_img)
    # Assert the contours and hierarchy lists contain only the ROI
    assert np.shape(roi) == (1, 424, 1, 2)


def test_circle_grayscale_input(roi_test_data):
    """Test for PlantCV."""
    # Read in a test grayscale image
    gray_img = cv2.imread(roi_test_data.small_gray_img, -1)
    roi, _ = circle(x=100, y=100, r=75, img=gray_img)
    # Assert the contours and hierarchy lists contain only the ROI
    assert np.shape(roi) == (1, 424, 1, 2)


def test_circle_out_of_frame(roi_test_data):
    """Test for PlantCV."""
    # Read in test RGB image
    rgb_img = cv2.imread(roi_test_data.small_rgb_img)
    # The resulting rectangle needs to be within the dimensions of the image
    with pytest.raises(RuntimeError):
        _, _ = circle(x=50, y=225, r=75, img=rgb_img)


def test_ellipse(roi_test_data):
    """Test for PlantCV."""
    # Read in test RGB image
    rgb_img = cv2.imread(roi_test_data.small_rgb_img)
    roi, _ = ellipse(x=100, y=100, r1=75, r2=50, angle=0, img=rgb_img)
    # Assert the contours and hierarchy lists contain only the ROI
    assert np.shape(roi) == (1, 360, 1, 2)


def test_ellipse_grayscale_input(roi_test_data):
    """Test for PlantCV."""
    # Read in a test grayscale image
    gray_img = cv2.imread(roi_test_data.small_gray_img, -1)
    roi, _ = ellipse(x=100, y=100, r1=75, r2=50, angle=0, img=gray_img)
    # Assert the contours and hierarchy lists contain only the ROI
    assert np.shape(roi) == (1, 360, 1, 2)


def test_ellipse_out_of_frame(roi_test_data):
    """Test for PlantCV."""
    # Read in test RGB image
    rgb_img = cv2.imread(roi_test_data.small_rgb_img)
    # The resulting rectangle needs to be within the dimensions of the image
    with pytest.raises(RuntimeError):
        _, _ = ellipse(x=50, y=225, r1=75, r2=50, angle=0, img=rgb_img)


def test_multi(roi_test_data):
    """Test for PlantCV."""
    # Read in test RGB image
    rgb_img = cv2.imread(roi_test_data.small_rgb_img)
    rois, _ = multi(rgb_img, coord=(10, 10), radius=10, spacing=(10, 10), nrows=2, ncols=2)
    # Assert the contours has 18 ROIs
    assert len(rois) == 4


def test_multi_input_coords(roi_test_data):
    """Test for PlantCV."""
    # Read in test RGB image
    rgb_img = cv2.imread(roi_test_data.small_rgb_img)
    rois, _ = multi(rgb_img, coord=[(25, 120), (100, 100)], radius=20)
    # Assert the contours has 18 ROIs
    assert len(rois) == 2


def test_multi_bad_input(roi_test_data):
    """Test for PlantCV."""
    # Read in test RGB image
    rgb_img = cv2.imread(roi_test_data.small_rgb_img)
    # The user must input a list of custom coordinates OR inputs to make a grid. Not both
    with pytest.raises(RuntimeError):
        _, _ = multi(rgb_img, coord=[(25, 120), (100, 100)], radius=20, spacing=(10, 10), nrows=3, ncols=6)


def test_multi_bad_input_oob(roi_test_data):
    """Test for PlantCV."""
    # Read in test RGB image
    rgb_img = cv2.imread(roi_test_data.small_rgb_img)
    # nputs to make a grid make ROIs that go off the screen
    with pytest.raises(RuntimeError):
        _, _ = multi(rgb_img, coord=(25000, 12000), radius=2, spacing=(1, 1), nrows=3, ncols=6)


def test_multi_bad_input_oob_list(roi_test_data):
    """Test for PlantCV."""
    # Read in test RGB image
    rgb_img = cv2.imread(roi_test_data.small_rgb_img)
    # All vertices in the list of centers must draw roi's that are inside the image
    with pytest.raises(RuntimeError):
        _, _ = multi(rgb_img, coord=[(25000, 25000), (25000, 12000), (12000, 12000)], radius=20)


def test_roi_custom(roi_test_data):
    """Test for PlantCV."""
    # Read in test RGB image
    img = cv2.imread(roi_test_data.small_rgb_img)
    roi, _ = custom(img=img, vertices=[[226, 1], [313, 184], [240, 202], [220, 229], [161, 171]])
    assert np.shape(roi) == (1, 5, 2)


def test_custom_bad_input(roi_test_data):
    """Test for PlantCV."""
    # Read in test RGB image
    img = cv2.imread(roi_test_data.small_rgb_img)
    # ROI goes out of bounds
    with pytest.raises(RuntimeError):
        _ = custom(img=img, vertices=[[226, -1], [3130, 1848], [2404, 2029], [2205, 2298], [1617, 1761]])
