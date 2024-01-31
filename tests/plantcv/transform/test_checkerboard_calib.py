import numpy as np
import cv2
import os
from plantcv.plantcv.transform import checkerboard_calib, calibrate_camera
from plantcv.plantcv.transform.color_correction import load_matrix


def test_checkerboard_calibration(transform_test_data, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("cache")
    # test the checkerboard_calib function
    row_corners = 13
    col_corners = 19
    checkerboard_dir = transform_test_data.checkerboard_imgdir
    _, mtx, dist = checkerboard_calib(checkerboard_dir, row_corners, col_corners, cache_dir)
    assert all(isinstance(mtx, np.ndarray),
               isinstance(dist, np.ndarray),
               os.path.exists(os.path.join(cache_dir, "mtx.npz")) is True,
               os.path.exists(os.path.join(cache_dir, "dist.npz")) is True)


def test_calibrate_camera(transform_test_data):
    """Test for PlantCV."""
    # read in test image and test the calibration camera function
    img = cv2.imread(transform_test_data.fisheye_test_img)
    mtx = load_matrix(transform_test_data.mtx)
    dist = load_matrix(transform_test_data.dist)
    corrected_img = calibrate_camera(img, mtx, dist)
    assert np.sum(img) != np.sum(corrected_img)
