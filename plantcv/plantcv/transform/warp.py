# warp image

import cv2
import os
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import fatal_error
from plantcv.plantcv import color_palette
from plantcv.plantcv.visualize import overlay_two_imgs
from plantcv.plantcv.transform import rescale
from skimage import img_as_ubyte


def _preprocess_img_dtype(img):
    """Transform the input image such that the datatype after transformation is uint8, ready for opencv functions
    :param img: numpy.ndarray
    :return: img_: numpy.ndarray
    """
    debug_mode = params.debug
    params.debug = None
    try:
        img_ = rescale(img)
    except RuntimeError:
        img_ = img_as_ubyte(img)
    params.debug = debug_mode
    return img_


def warp(img, refimg, pts, refpts, method='default'):
    """Calculate a projective transform from 4 pairs of the corresponding points between image and reference image,
    then performs the projective transformation on input image to align the input image to reference image

    Inputs:
    img    = image to be warped
    refimg = image to be used as reference
    pts    = 4 coordinates on img
    refpts = 4 coordinates on refimg
    method = Available options are 'default', 'ransac', 'lmeds', 'rho' which correspond to the opencv methods
             and vary based on whether they handle outlier points and how they handle outlier points.
             - 'default': a regular method (the least squares method) using all the points
             - 'ransac': RANSAC-based robust method
             - 'lmeds': Least-Median robust method
             - 'RHO': PROSAC-based robust method
    Returns:
    warped_img = warped image
    mat        = transformation matrix

    :param img: numpy.ndarray
    :param refimg: numpy.ndarray
    :param pts: list of tuples
    :param refpts: list of tuples
    :param method: str
    :return warped_img: numpy.ndarray
    :return mat: numpy.ndarray
    """
    if len(pts) != len(refpts):
        fatal_error('Please provide same number of corresponding coordinates.')
    if not (len(pts) >= 4 and len(refpts) >= 4):
        fatal_error('Please provide at least 4 pairs of points!')
    # convert coordinates to int if they are not int
    pts = [tuple(map(int, tup)) for tup in pts]
    refpts = [tuple(map(int, tup)) for tup in refpts]

    methods = {
        'default': 0,
        'ransac': cv2.RANSAC,
        'lmeds': cv2.LMEDS,
        'rho': cv2.RHO}

    shape_img = img.shape
    shape_ref = refimg.shape
    rows_ref, cols_ref = shape_ref[0:2]
    rows_img, _ = shape_img[0:2]

    # convert list of tuples to array for cv2 functions
    ptsarr = np.array(pts, dtype='float32')
    refptsarr = np.array(refpts, dtype='float32')

    # find tranformation matrix and warp
    mat, status = cv2.findHomography(ptsarr, refptsarr, method=methods.get(method))
    if mat is None:
        fatal_error(f"""Cannot calculate a robust model with given corresponding coordinates and with desired robust
        estimation algorithm {method}!""")
    warped_img = cv2.warpPerspective(src=img, M=mat, dsize=(cols_ref, rows_ref))

    # preserve binary
    if len(np.unique(img)) == 2:
        warped_img[warped_img > 0] = 255

    # scale marker_size and line_thickness for different resolutions
    if rows_img > rows_ref:
        res_ratio_i = int(np.ceil(rows_img / rows_ref))  # ratio never smaller than 1 with np.ceil
        res_ratio_r = 1
    else:
        res_ratio_r = int(np.ceil(rows_ref / rows_img))
        res_ratio_i = 1
    # marker colors
    colors = color_palette(len(pts))

    # convert image types to accepted ones for cv2.cvtColor, also compatible with colors generated by color_palette
    # (color_palette generated colors that are in range of (0,255)
    img_ = _preprocess_img_dtype(img)
    refimg_ = _preprocess_img_dtype(refimg)

    # rgb image for colored markers on img
    img_marked = img_.copy()
    # convert to RGB image if not
    if len(shape_img) == 2:
        img_marked = cv2.cvtColor(img_marked, cv2.COLOR_GRAY2RGB)

    for i, pt in enumerate(pts):
        if status[i][0] == 1:
            cv2.drawMarker(img_marked, pt, color=colors[i], markerType=cv2.MARKER_CROSS,
                           markerSize=params.marker_size * res_ratio_i,
                           thickness=params.line_thickness * res_ratio_i)
        else:
            cv2.drawMarker(img_marked, pt, color=colors[i], markerType=cv2.MARKER_TRIANGLE_UP,
                           markerSize=params.marker_size * res_ratio_i,
                           thickness=params.line_thickness * res_ratio_i)

    # rgb image for colored markers on refimg
    refimg_marked = refimg_.copy()
    if len(shape_ref) == 2:
        refimg_marked = cv2.cvtColor(refimg_marked, cv2.COLOR_GRAY2RGB)

    for i, pt in enumerate(refpts):
        if status[i][0] == 1:
            cv2.drawMarker(refimg_marked, pt, color=colors[i], markerType=cv2.MARKER_CROSS,
                           markerSize=params.marker_size * res_ratio_r,
                           thickness=params.line_thickness * res_ratio_r)
        else:
            cv2.drawMarker(refimg_marked, pt, color=colors[i], markerType=cv2.MARKER_TRIANGLE_UP,
                           markerSize=params.marker_size * res_ratio_r,
                           thickness=params.line_thickness * res_ratio_r)

    debug_mode = params.debug
    params.debug = None

    # make sure the input image for "overlay_two_imgs" is of dtype "uint8" such that it would be acceptable for
    # overlay_two_imgs (cv2.cvtColor)
    img_blend = overlay_two_imgs(_preprocess_img_dtype(warped_img), refimg_)
    params.debug = debug_mode

    _debug(visual=img_marked, filename=os.path.join(params.debug_outdir, str(params.device) + "_img-to-warp.png"))
    _debug(visual=refimg_marked, filename=os.path.join(params.debug_outdir, str(params.device) + "_img-ref.png"))
    _debug(visual=img_blend, filename=os.path.join(params.debug_outdir, str(params.device) + "_warp_overlay.png"))

    return warped_img, mat


def warp_align(img, refimg, mat):
    """Warp the input image based on given transformation matrix mat, to align with the refimg

    Inputs:
    img    = image to be warped
    refimg = reference image
    mat    = transformation matrix (size: (3,3))

    Returns:
    warped_img = warped image

    :param img: numpy.ndarray
    :param refimg: numpy.ndarray
    :param mat: numpy.ndarray
    :return warpped image: numpy.ndarray
    """
    # Ensure refimg is compatible with OpenCV
    refimg = _preprocess_img_dtype(refimg.copy())

    # The output size is the shape of the refimg
    rows_ref, cols_ref = refimg.shape[0:2]

    # Transform img to fit on refimg
    warped_img = cv2.warpPerspective(src=img, M=mat, dsize=(cols_ref, rows_ref))

    # Create an overlay of img on refimg
    debug_mode = params.debug
    params.debug = None
    img_blend = overlay_two_imgs(_preprocess_img_dtype(warped_img), refimg)

    # Debug images
    params.debug = debug_mode
    _debug(visual=warped_img, filename=os.path.join(params.debug_outdir, str(params.device) + "_warped.png"))
    _debug(visual=img_blend, filename=os.path.join(params.debug_outdir, str(params.device) + "_warp_overlay.png"))

    return warped_img
