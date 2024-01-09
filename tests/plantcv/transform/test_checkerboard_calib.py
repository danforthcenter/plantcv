import numpy as np
import cv2
from plantcv.plantcv.transform import checkerboard_calib, calibrate_camera


def test_checkerboard_calibration_mtx(test_data):
    """Test for PlantCV."""
    _, mtx, _ = checkerboard_calib(img_path=test_data.checkerboard_imgdir, row_corners=13, col_corners=19)
    assert isinstance(mtx, np.ndarray)


def test_checkerboard_calibration_dist(test_data):
    """Test for PlantCV."""
    _, _, dist = checkerboard_calib(img_path=test_data.checkerboard_imgdir, row_corners=13, col_corners=19)
    assert isinstance(dist, np.ndarray)


def test_calibrate_camera(test_data):
    img = cv2.imread(test_data.fisheye_test_img)
    mtx = np.array([5197.25083, 0, 1436.76558,
                    0, 5168.71667, 1061.72915,
                    0, 0, 1])
    dist = np.array([-3.12637515, 15.8426401, -0.0216986074,
                    0.00137779962, -43.9754062])
    corrected_img = calibrate_camera(img, mtx, dist)
    assert img.shape == corrected_img.shape
