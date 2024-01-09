# camera calibration function using checkerboard images

import cv2 as cv
import os
import numpy as np
from plantcv.plantcv.readimage import readimage
from plantcv.plantcv.rgb2gray import rgb2gray
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug


def checkerboard_calib(img_path, col_corners, row_corners):
    """
    Use several checkerboard images to calibrate a camera with image distortions.

    Inputs:
    img_path    = directory of checkerboard images to be used for calibration
    col_corners = the number from inside corners in a column of the checkerboard
    row_corners = the number from inside corners in a row of the checkerboard

    :param img_path: path to directory of checkerboard images
    :param col_corners: non-negative real number
    :param row_corners: non-negative real number
    :return mtx: numpy.ndarray
    :return dist: numpy.ndarray
    """

    images = os.listdir(img_path)
    objp = np.zeros((col_corners*row_corners, 3), np.float32)
    objp[:, :2] = np.mgrid[0:col_corners, 0:row_corners].T.reshape(-1, 2)
    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane

    for fname in images:
        img, path, _ = readimage(filename=os.path.join(img_path + "/" + fname), mode="native")
        img1 = np.copy(img)
        gray_img = rgb2gray(img1)
        ret, corners = cv.findChessboardCorners(gray_img, (col_corners, row_corners))
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        if ret is False:
            print("Checkerboard image " + fname + " does not match given dimensions.")
            continue
        if ret is True:
            objpoints.append(objp)
            corners2 = cv.cornerSubPix(gray_img, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)
            # Draw and display the corners
            cv.drawChessboardCorners(img1, (col_corners, row_corners), corners2, ret)

    _, mtx, dist, _, _ = cv.calibrateCamera(objpoints, imgpoints, gray_img.shape[::-1], None, None)

    # Debug images
    _debug(visual=img1, filename=os.path.join(params.debug_outdir, "_checkerboard_corners.png"))

    return mtx, dist


def calibrate_camera(rgb_img, mtx, dist):
    """
    Use the outputs from checkerboard_calib to correct the distortions in an image

    Inputs:
    img  = an RGB image
    mtx  = an output of checkerboar_calib
    dist = ret = an output of checkerboar_calib

    :param img: path to an image
    :param ret: float
    :param mtx: numpy.ndarray
    :param dist: numpy.ndarray
    :return corrected_img: numpy.ndarray
    """
    h, w = rgb_img.shape[:2]

    newcameramtx, _ = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

    dst = cv.undistort(rgb_img, mtx, dist, None, newcameramtx)

    # Debug images
    _debug(visual=dst, filename=os.path.join(params.debug_outdir, str(params.device) + "_checkerboard_corners.png"))

    return dst
