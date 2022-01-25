import pytest
import cv2
import numpy as np
from plantcv.plantcv.visualize import overlay_two_imgs


def test_overlay_two_imgs(visualize_test_data):
    """Test for PlantCV."""
    img1 = cv2.imread(visualize_test_data.small_rgb_img)
    img2 = cv2.imread(visualize_test_data.small_bin_img)
    out_img = overlay_two_imgs(img1=img1, img2=img2)
    sample_pt1 = img1[0, 0]
    sample_pt2 = img2[0, 0]
    sample_pt3 = out_img[0, 0]
    pred_rgb = (sample_pt1 * 0.5) + (sample_pt2 * 0.5)
    pred_rgb = pred_rgb.astype(np.uint8)
    assert np.array_equal(sample_pt3, pred_rgb)


def test_overlay_two_imgs_grayscale(visualize_test_data):
    """Test for PlantCV."""
    img1 = cv2.imread(visualize_test_data.small_gray_img, -1)
    img2 = cv2.imread(visualize_test_data.small_bin_img, -1)
    out_img = overlay_two_imgs(img1=img1, img2=img2)
    sample_pt1 = np.array([img1[0, 0], img1[0, 0], img1[0, 0]])
    sample_pt2 = np.array([img2[0, 0], img2[0, 0], img2[0, 0]])
    sample_pt3 = out_img[0, 0]
    pred_rgb = (sample_pt1 * 0.5) + (sample_pt2 * 0.5)
    pred_rgb = pred_rgb.astype(np.uint8)
    assert np.array_equal(sample_pt3, pred_rgb)


def test_overlay_two_imgs_bad_alpha(visualize_test_data):
    """Test for PlantCV."""
    img1 = cv2.imread(visualize_test_data.small_rgb_img)
    img2 = cv2.imread(visualize_test_data.small_bin_img, -1)
    alpha = -1
    with pytest.raises(RuntimeError):
        _ = overlay_two_imgs(img1=img1, img2=img2, alpha=alpha)


def test_overlay_two_imgs_size_mismatch(visualize_test_data):
    """Test for PlantCV."""
    img1 = cv2.imread(visualize_test_data.small_rgb_img)
    img2 = img1.copy()
    img2 = img2[1:, 1:, :]
    with pytest.raises(RuntimeError):
        _ = overlay_two_imgs(img1=img1, img2=img2)
