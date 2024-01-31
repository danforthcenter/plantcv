import numpy as np
import cv2
from plantcv.plantcv.transform import checkerboard_calib, calibrate_camera


def test_checkerboard_calibration_mtx(transform_test_data):
    """Test for PlantCV."""
    _, mtx, _ = checkerboard_calib(img_path=transform_test_data.checkerboard_imgdir, row_corners=13, col_corners=19)
    assert isinstance(mtx, np.ndarray)


def test_checkerboard_calibration_dist(transform_test_data):
    """Test for PlantCV."""
    _, _, dist = checkerboard_calib(img_path=transform_test_data.checkerboard_imgdir, row_corners=13, col_corners=19)
    assert isinstance(dist, np.ndarray)


def test_calibrate_camera(transform_test_data):
    img = cv2.imread(transform_test_data.fisheye_test_img)
    mtx = np.loadtxt(transform_test_data.mtx)
    dist = np.loadtxt(transform_test_data.dist)
    corrected_img = calibrate_camera(img, mtx, dist)
    assert np.sum(img) != np.sum(corrected_img)
