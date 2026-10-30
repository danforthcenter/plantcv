import pytest
import cv2
import numpy as np
from plantcv.plantcv.visualize import overlay_two_imgs
from tests import synthetic


def test_overlay_two_imgs(synthetic_rgb, synthetic_mask):
    """Test for PlantCV."""
    img1 = synthetic_rgb
    img2 = cv2.cvtColor(synthetic_mask, cv2.COLOR_GRAY2BGR)
    out_img = overlay_two_imgs(img1=img1, img2=img2)
    sample_pt1 = img1[0, 0]
    sample_pt2 = img2[0, 0]
    sample_pt3 = out_img[0, 0]
    pred_rgb = (sample_pt1 * 0.5) + (sample_pt2 * 0.5)
    pred_rgb = pred_rgb.astype(np.uint8)
    assert np.array_equal(sample_pt3, pred_rgb)


def test_overlay_two_imgs_grayscale(synthetic_mask):
    """Test for PlantCV."""
    # Grayscale image spanning 0-255, which the rescaling inside overlay_two_imgs leaves unchanged
    img1 = synthetic.random_image((100, 120))
    img2 = synthetic_mask
    out_img = overlay_two_imgs(img1=img1, img2=img2)
    sample_pt1 = np.array([img1[0, 0], img1[0, 0], img1[0, 0]])
    sample_pt2 = np.array([img2[0, 0], img2[0, 0], img2[0, 0]])
    sample_pt3 = out_img[0, 0]
    pred_rgb = (sample_pt1 * 0.5) + (sample_pt2 * 0.5)
    pred_rgb = pred_rgb.astype(np.uint8)
    assert np.array_equal(sample_pt3, pred_rgb)


def test_overlay_two_imgs_bad_alpha(synthetic_rgb, synthetic_mask):
    """Test for PlantCV."""
    img1 = synthetic_rgb
    img2 = synthetic_mask
    alpha = -1
    with pytest.raises(RuntimeError):
        _ = overlay_two_imgs(img1=img1, img2=img2, alpha=alpha)


def test_overlay_two_imgs_size_mismatch(synthetic_rgb):
    """Test for PlantCV."""
    img1 = synthetic_rgb
    img2 = img1.copy()
    img2 = img2[1:, 1:, :]
    with pytest.raises(RuntimeError):
        _ = overlay_two_imgs(img1=img1, img2=img2)
