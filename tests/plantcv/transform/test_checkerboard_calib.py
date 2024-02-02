import numpy as np
import cv2
import os
from plantcv.plantcv.transform import checkerboard_calib, calibrate_camera


def test_checkerboard_calibration(transform_test_data, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("cache")
    # test the checkerboard_calib function
    row_corners = 13
    col_corners = 19
    checkerboard_dir = transform_test_data.checkerboard_imgdir
    mtx, dist = checkerboard_calib(checkerboard_dir, row_corners, col_corners, cache_dir)
    # assert that mtx and dist are numpy arrays and that the output files exist
    assert isinstance(mtx, np.ndarray)
    assert isinstance(dist, np.ndarray)
    assert os.path.exists(os.path.join(cache_dir, "mtx.npz")) is True
    assert os.path.exists(os.path.join(cache_dir, "dist.npz")) is True


def test_checkerboard_calibration_dne(transform_test_data, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    cache_dir = os.path.join(tmp_dir, "outputs")
    # test the checkerboard_calib function
    row_corners = 13
    col_corners = 19
    checkerboard_dir = transform_test_data.checkerboard_imgdir
    mtx, dist = checkerboard_calib(checkerboard_dir, row_corners, col_corners, cache_dir)
    # assert that mtx and dist are numpy arrays and that the output files exist
    assert isinstance(mtx, np.ndarray)
    assert isinstance(dist, np.ndarray)
    assert os.path.exists(os.path.join(cache_dir, "mtx.npz")) is True
    assert os.path.exists(os.path.join(cache_dir, "dist.npz")) is True


def test_calibrate_camera(transform_test_data):
    """Test for PlantCV."""
    # read in test image and test the calibration camera function
    img = cv2.imread(transform_test_data.fisheye_test_img)
    mtx = os.path.abspath(transform_test_data.mtx)
    dist = os.path.abspath(transform_test_data.dist)
    corrected_img = calibrate_camera(img, mtx, dist)
    assert np.sum(img) != np.sum(corrected_img)
