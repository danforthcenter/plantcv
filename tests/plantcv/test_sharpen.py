import numpy as np
from plantcv.plantcv.classes import Objects
from plantcv.plantcv.sharpen import sharpen


def test_sharpen_zero_amount(synthetic_rgb):
    """Test for PlantCV."""
    sharp_img = sharpen(synthetic_rgb, (5, 5), amount=0, threshold=0)
    assert np.average(synthetic_rgb) == np.average(sharp_img)


def test_sharpen_any_amount(synthetic_rgb):
    """Test for PlantCV."""
    sharp_img = sharpen(synthetic_rgb, (5, 5), amount=1, threshold=0)
    assert np.average(synthetic_rgb) != np.average(sharp_img)


def test_sharpen_threshold(synthetic_rgb):
    """Test for PlantCV."""
    zero_thresh = sharpen(synthetic_rgb, (5, 5), amount=1, threshold=0)
    thresh = sharpen(synthetic_rgb, (5, 5), amount=1, threshold=100)
    assert np.average(thresh) != np.average(zero_thresh)


def test_sharpen_grayscale(synthetic_gray):
    """Test for PlantCV."""
    zero_thresh = sharpen(synthetic_gray, (5, 5), amount=1, threshold=0)
    thresh = sharpen(synthetic_gray, (5, 5), amount=1, threshold=100)
    assert np.average(thresh) != np.average(zero_thresh)


def test_sharpen_roi(synthetic_rgb):
    """Test for PlantCV."""
    # ROI covers rows 20:100 and columns 10:120, including the plant edges that sharpening changes
    roi_con = [np.array([[[10, 20]], [[10, 200]], [[200, 200]], [[200, 20]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi = Objects(contours=[roi_con], hierarchy=[roi_str])
    sharp_img = sharpen(synthetic_rgb, 5, amount=1, threshold=0, roi=roi)
    assert np.average(synthetic_rgb) != np.average(sharp_img)


def test_sharpen_grayscale_roi(synthetic_gray):
    """Test for PlantCV."""
    # ROI covers rows 20:100 and columns 10:120, including the plant edges that sharpening changes
    roi_con = [np.array([[[10, 20]], [[10, 200]], [[200, 200]], [[200, 20]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi = Objects(contours=[roi_con], hierarchy=[roi_str])
    sharp_img = sharpen(synthetic_gray, (5, 5), amount=1, threshold=0, roi=roi)
    assert np.average(synthetic_gray) != np.average(sharp_img)
