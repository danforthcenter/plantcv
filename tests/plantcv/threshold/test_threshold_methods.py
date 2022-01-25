import pytest
import numpy as np
import cv2
from plantcv.plantcv.threshold import binary, gaussian, mean, otsu, custom_range, saturation, triangle, texture, mask_bad
from plantcv.plantcv import params


@pytest.mark.parametrize("objtype", ["dark", "light"])
def test_binary(objtype, threshold_test_data):
    """Test for PlantCV."""
    # Read in test data
    gray_img = cv2.imread(threshold_test_data.small_gray_img, -1)
    binary_img = binary(gray_img=gray_img, threshold=25, max_value=255, object_type=objtype)
    # Assert that the output image has the dimensions of the input image and is binary
    assert gray_img.shape == binary_img.shape and np.array_equal(np.unique(binary_img), np.array([0, 255]))


def test_binary_incorrect_object_type(threshold_test_data):
    """Test for PlantCV."""
    # Read in test data
    gray_img = cv2.imread(threshold_test_data.small_gray_img, -1)
    with pytest.raises(RuntimeError):
        _ = binary(gray_img=gray_img, threshold=25, max_value=255, object_type="lite")


@pytest.mark.parametrize("objtype", ["dark", "light"])
def test_gaussian(objtype, threshold_test_data):
    """Test for PlantCV."""
    # Read in test data
    gray_img = cv2.imread(threshold_test_data.small_gray_img, -1)
    binary_img = gaussian(gray_img=gray_img, max_value=255, object_type=objtype)
    # Assert that the output image has the dimensions of the input image and is binary
    assert gray_img.shape == binary_img.shape and np.array_equal(np.unique(binary_img), np.array([0, 255]))


def test_gaussian_incorrect_object_type(threshold_test_data):
    """Test for PlantCV."""
    # Read in test data
    gray_img = cv2.imread(threshold_test_data.small_gray_img, -1)
    with pytest.raises(RuntimeError):
        _ = gaussian(gray_img=gray_img, max_value=255, object_type="lite")


@pytest.mark.parametrize("objtype", ["dark", "light"])
def test_mean(objtype, threshold_test_data):
    """Test for PlantCV."""
    # Read in test data
    gray_img = cv2.imread(threshold_test_data.small_gray_img, -1)
    binary_img = mean(gray_img=gray_img, max_value=255, object_type=objtype)
    # Assert that the output image has the dimensions of the input image and is binary
    assert gray_img.shape == binary_img.shape and np.array_equal(np.unique(binary_img), np.array([0, 255]))


def test_mean_incorrect_object_type(threshold_test_data):
    """Test for PlantCV."""
    # Read in test data
    gray_img = cv2.imread(threshold_test_data.small_gray_img, -1)
    with pytest.raises(RuntimeError):
        _ = mean(gray_img=gray_img, max_value=255, object_type="lite")


@pytest.mark.parametrize("objtype", ["dark", "light"])
def test_otsu(objtype, threshold_test_data):
    """Test for PlantCV."""
    # Read in test data
    gray_img = cv2.imread(threshold_test_data.small_gray_img, -1)
    binary_img = otsu(gray_img=gray_img, max_value=255, object_type=objtype)
    # Assert that the output image has the dimensions of the input image and is binary
    assert gray_img.shape == binary_img.shape and np.array_equal(np.unique(binary_img), np.array([0, 255]))


def test_otsu_incorrect_object_type(threshold_test_data):
    """Test for PlantCV."""
    # Read in test data
    gray_img = cv2.imread(threshold_test_data.small_gray_img, -1)
    with pytest.raises(RuntimeError):
        _ = otsu(gray_img=gray_img, max_value=255, object_type="lite")


@pytest.mark.parametrize("channel,lower_thresh,upper_thresh", [["HSV", [0, 0, 0], [100, 100, 100]],
                                                               ["LAB", [100, 100, 100], [255, 255, 255]],
                                                               ["RGB", [0, 0, 0], [100, 100, 100]],
                                                               ["GRAY", [0], [100]]])
def test_custom_range_rgb(channel, lower_thresh, upper_thresh, threshold_test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(threshold_test_data.small_rgb_img)
    binary_img, _ = custom_range(img, lower_thresh=lower_thresh, upper_thresh=upper_thresh, channel=channel)
    # Assert that the output image has the dimensions of the input image and is binary
    assert img.shape[:2] == binary_img.shape and np.array_equal(np.unique(binary_img), np.array([0, 255]))


def test_custom_range_grayscale(threshold_test_data):
    """Test for PlantCV."""
    # Read in test data
    gray_img = cv2.imread(threshold_test_data.small_gray_img, -1)
    # # Test channel='gray'
    binary_img, _ = custom_range(gray_img, lower_thresh=[0], upper_thresh=[100], channel='gray')
    # Assert that the output image has the dimensions of the input image and is binary
    assert gray_img.shape == binary_img.shape and np.array_equal(np.unique(binary_img), np.array([0, 255]))


@pytest.mark.parametrize("channel,lower_thresh,upper_thresh", [["HSV", [0, 0], [2, 2, 2, 2]],
                                                               ["LAB", [0, 0], [2, 2, 2, 2]],
                                                               ["RGB", [0, 0], [2, 2, 2, 2]],
                                                               ["GRAY", [0, 0], [2]],
                                                               ["CMYK", [0], [2]]])
def test_custom_range_bad_input(channel, lower_thresh, upper_thresh, threshold_test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(threshold_test_data.small_rgb_img)
    with pytest.raises(RuntimeError):
        _, _ = custom_range(img, lower_thresh=lower_thresh, upper_thresh=upper_thresh, channel=channel)


@pytest.mark.parametrize("channel", ["all", "any"])
def test_saturation(channel, threshold_test_data):
    """Test for PlantCV."""
    # Read in test data
    rgb_img = cv2.imread(threshold_test_data.small_rgb_img)
    thresh = saturation(rgb_img=rgb_img, threshold=254, channel=channel)
    assert len(np.unique(thresh)) == 2


def test_saturation_bad_input(threshold_test_data):
    """Test for PlantCV."""
    # Read in test data
    rgb_img = cv2.imread(threshold_test_data.small_rgb_img)
    with pytest.raises(RuntimeError):
        _ = saturation(rgb_img=rgb_img, threshold=254, channel="red")


@pytest.mark.parametrize("debug", ["print", "plot", None])
def test_triangle(debug, threshold_test_data, tmpdir):
    """Test for PlantCV."""
    # Test cache directory
    cache_dir = tmpdir.mkdir("cache")
    params.debug_outdir = cache_dir
    params.debug = debug
    # Read in test data
    gray_img = cv2.imread(threshold_test_data.small_gray_img, -1)
    binary_img = triangle(gray_img=gray_img, max_value=255, object_type="light", xstep=10)
    # Assert that the output image has the dimensions of the input image and is binary
    assert gray_img.shape == binary_img.shape and np.array_equal(np.unique(binary_img), np.array([0, 255]))


def test_triangle_dark(threshold_test_data):
    """Test for PlantCV."""
    # Read in test data
    gray_img = cv2.imread(threshold_test_data.small_gray_img, -1)
    binary_img = triangle(gray_img=gray_img, max_value=255, object_type="dark", xstep=10)
    # Assert that the output image has the dimensions of the input image and is binary
    assert gray_img.shape == binary_img.shape and np.array_equal(np.unique(binary_img), np.array([0, 255]))


def test_triangle_incorrect_object_type(threshold_test_data):
    """Test for PlantCV."""
    # Read in test data
    gray_img = cv2.imread(threshold_test_data.small_gray_img, -1)
    with pytest.raises(RuntimeError):
        _ = triangle(gray_img=gray_img, max_value=255, object_type="lite", xstep=10)


def test_texture(threshold_test_data):
    """Test for PlantCV."""
    # Read in test data
    gray_img = cv2.imread(threshold_test_data.small_gray_img, -1)
    # Subset input data
    gray_img = gray_img[150:200, 200:250]
    binary_img = texture(gray_img, ksize=6, threshold=7, offset=3, texture_method='dissimilarity', borders='nearest',
                         max_value=255)
    # Assert that the output image has the dimensions of the input image and is binary
    assert gray_img.shape == binary_img.shape and np.array_equal(np.unique(binary_img), np.array([0, 255]))


@pytest.mark.parametrize("bad_type", ["native", "nan", "inf"])
def test_mask_bad(bad_type):
    """Test for PlantCV."""
    # Create a synthetic bad image
    bad_img = np.reshape(np.random.rand(25), (5, 5))
    bad_img[2, 2] = np.inf
    bad_img[2, 3] = np.nan
    mask = mask_bad(bad_img, bad_type=bad_type)
    # Assert that the output image has the dimensions of the input image and is binary
    assert bad_img.shape == mask.shape and np.array_equal(np.unique(mask), np.array([0, 255]))


def test_mask_bad_native_bad_input():
    """Test for PlantCV."""
    # Create a synthetic bad image
    bad_img = np.reshape(np.random.rand(25), (5, 5))
    mask = mask_bad(bad_img, bad_type='native')
    assert np.sum(mask) == 0


def test_mask_bad_nan_bad_input():
    """Test for PlantCV."""
    # Create a synthetic bad image
    bad_img = np.reshape(np.random.rand(25), (5, 5))
    bad_img[2, 2] = np.inf
    mask = mask_bad(bad_img, bad_type='nan')
    assert np.sum(mask) == 0


def test_mask_bad_input_color_img(threshold_test_data):
    """Test for PlantCV."""
    # Read in test data
    bad_img = cv2.imread(threshold_test_data.small_rgb_img)
    with pytest.raises(RuntimeError):
        _ = mask_bad(bad_img, bad_type='nan')
