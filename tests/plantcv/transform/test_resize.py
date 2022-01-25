import pytest
import cv2
from plantcv.plantcv.transform import resize, resize_factor


def test_resize(transform_test_data):
    """Test for PlantCV."""
    gray_img = cv2.imread(transform_test_data.small_gray_img, -1)
    size = (500, 500)
    resized_img = resize(img=gray_img, size=size, interpolation="auto")
    assert resized_img.shape == size


def test_resize_unsupported_method(transform_test_data):
    """Test for PlantCV."""
    gray_img = cv2.imread(transform_test_data.small_gray_img, -1)
    with pytest.raises(RuntimeError):
        _ = resize(img=gray_img, size=(100, 100), interpolation="mymethod")


def test_resize_crop(transform_test_data):
    """Test for PlantCV."""
    gray_img = cv2.imread(transform_test_data.small_gray_img, -1)
    size = (20, 20)
    resized_im = resize(img=gray_img, size=size, interpolation=None)
    assert resized_im.shape == size


def test_resize_pad(transform_test_data):
    """Test for PlantCV."""
    gray_img = cv2.imread(transform_test_data.small_gray_img, -1)
    size = (100, 100)
    resized_im = resize(img=gray_img, size=size, interpolation=None)
    assert resized_im.shape == size


def test_resize_pad_crop_color(transform_test_data):
    """Test for PlantCV."""
    color_img = cv2.imread(transform_test_data.small_gray_img)
    size = (100, 100)
    resized_im = resize(img=color_img, size=size, interpolation=None)
    assert resized_im.shape == (size[1], size[0], 3)


def test_resize_factor(transform_test_data):
    """Test for PlantCV."""
    gray_img = cv2.imread(transform_test_data.small_gray_img, -1)
    # Resizing factors
    factor_x = 0.5
    factor_y = 0.2
    resized_img = resize_factor(img=gray_img, factors=(factor_x, factor_y), interpolation="auto")
    output_size = resized_img.shape
    expected_size = (int(gray_img.shape[0] * factor_y), int(gray_img.shape[1] * factor_x))
    assert output_size == expected_size


def test_resize_factor_bad_input(transform_test_data):
    """Test for PlantCV."""
    gray_img = cv2.imread(transform_test_data.small_gray_img, -1)
    with pytest.raises(RuntimeError):
        _ = resize_factor(img=gray_img, factors=(0, 2), interpolation="auto")
