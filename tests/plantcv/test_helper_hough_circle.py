import cv2
import pytest
from plantcv.plantcv._helpers import _hough_circle


def test_hough_circle(test_data):
    """Test for PlantCV."""
    img = cv2.imread(test_data.hough_circle, -1)
    df, _ = _hough_circle(img, 20, 50, 30, 40, 50, 24)

    assert df.shape == (24, 3)


def test_hough_circle_warn(test_data):
    """Test for PlantCV."""
    img = cv2.imread(test_data.hough_circle, -1)
    df, _ = _hough_circle(img, 20, 50, 30, 35, 50, 24)

    assert df.shape == (24, 3)


def test_hough_circle_none(test_data):
    """Test for PlantCV."""
    img = cv2.imread(test_data.hough_circle, -1)
    df, _ = _hough_circle(img, 20, 50, 30, 40, 50, None)

    assert df.shape == (24, 3)


def test_hough_no_circles(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.hough_circle, -1)
    with pytest.raises(RuntimeError):
        _, _ = _hough_circle(img, 20, 50, 30, 50, 50, None)
