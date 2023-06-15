import pytest
import numpy as np
import cv2
from plantcv.plantcv import auto_crop


@pytest.mark.parametrize('padx,pady,expected', [[20, 20, (98, 56, 4)], [(400, 400), (400, 400), (58, 16, 4)]])
def test_auto_crop(padx, pady, expected, test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img, -1)
    blank = np.zeros(img.shape[:2], dtype=np.uint8)
    contour = test_data.load_composed_contours(test_data.small_composed_contours_file)
    mask = cv2.drawContours(blank, contour, -1, (255), thickness=-1)
    cropped = auto_crop(img=img, mask=mask, padding_x=padx, padding_y=pady, color='image')
    assert cropped.shape == expected


@pytest.mark.parametrize("color", ["black", "white", "image"])
def test_auto_crop_grayscale(color, test_data):
    """Test for PlantCV."""
    # Read in test data
    gray_img = cv2.imread(test_data.small_gray_img, -1)
    blank = np.zeros(np.shape(gray_img), dtype=np.uint8)
    contour = test_data.load_composed_contours(test_data.small_composed_contours_file)
    mask = cv2.drawContours(blank, contour, -1, (255), thickness=-1)
    cropped = auto_crop(img=gray_img, mask=mask, padding_x=20, padding_y=20, color=color)
    assert cropped.shape == (98, 56)


def test_auto_crop_bad_color_input(test_data):
    """Test for PlantCV."""
    # Read in test data
    gray_img = cv2.imread(test_data.small_gray_img, -1)
    blank = np.zeros(np.shape(gray_img), dtype=np.uint8)
    contour = test_data.load_composed_contours(test_data.small_composed_contours_file)
    mask = cv2.drawContours(blank, contour, -1, (255), thickness=-1)
    with pytest.raises(RuntimeError):
        _ = auto_crop(img=gray_img, mask=mask, padding_x=20, padding_y=20, color='wite')


def test_auto_crop_bad_padding_input(test_data):
    """Test for PlantCV."""
    # Read in test data
    gray_img = cv2.imread(test_data.small_gray_img, -1)
    blank = np.zeros(np.shape(gray_img), dtype=np.uint8)
    contour = test_data.load_composed_contours(test_data.small_composed_contours_file)
    mask = cv2.drawContours(blank, contour, -1, (255), thickness=-1)
    with pytest.raises(RuntimeError):
        _ = auto_crop(img=gray_img, mask=mask, padding_x="one", padding_y=20, color='white')
