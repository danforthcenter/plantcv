# warp image

import cv2
import skimage
import os
import numpy as np
import copy
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import fatal_error
from plantcv.plantcv import color_palette
from plantcv.plantcv.visualize import overlay_two_imgs
from plantcv.plantcv.transform import rescale
import skimage

def _preprocess_img_dtype(img):
    """ Transform the input image such that the datatype after transformation is uint8, ready for opencv functions
    :param img: inut image array
    :return:
    """
    debug_mode = params.debug
    params.debug = None
    try:
        img_         = rescale(img)
    except:
        img_ = skimage.img_as_ubyte(img)
    params.debug = debug_mode
    return img_

# def _img_dtype_check(img):
#     if img.dtype == 'uint8':
#         pass
#     elif len(np.unique(img)) == 2:
#         pass
#     else:
#         fatal_error("Image have datatype 'uint8' unless binary!")


def warp(img, refimg, pts, refpts, method='default'):
    """Calculate a projective transform from 4 pairs of the corresponding points between image and reference image,
    then performs the projective transformation on input image to align the input image to reference image

    Inputs:
    img = image data to be warped
    refimg = image data to be used as reference
    pts = 4 coordinates on img
    refpts = 4 coordinates on refimg
    method = robust estimation algorithm when calculating projective transformation. 'default', 'ransac', 'lmeds', 'rho'
    Returns:
    mat = transformation matrix
    warped_img = warped image

    :param img: numpy.ndarray
    :param refimg: numpy.ndarray
    :param pts: list of tuples
    :param refpts: list of tuples
    :param method: str
    :return mat: numpy.ndarray
    :return warped_img: numpy.ndarray
    """

    params.device += 1

    if len(pts) != len(refpts):
        fatal_error('Please provide same number of corresponding coordinates.')

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
    rows_img, cols_img = shape_img[0:2]

    # convert list of tuples to array for cv2 functions
    ptsarr = np.array(pts, dtype='float32')
    refptsarr = np.array(refpts, dtype='float32')

    # find tranformation matrix and warp
    mat, status = cv2.findHomography(ptsarr, refptsarr, method=methods.get(method))
    if mat is None:
        fatal_error( "Cannot calculate a robust with given corresponding coordinates and with desired robust estimation algorithm {}!".format(method))
    warped_img = cv2.warpPerspective(src=img, M=mat, dsize=(cols_ref, rows_ref))

    # preserve binary
    if len(np.unique(img)) == 2:
        warped_img[warped_img > 0] = 255

    if params.debug is not None:
        # scale marker_size and line_thickness for different resolutions
        if rows_img > rows_ref:
            res_ratio_i = int(np.ceil(rows_img / rows_ref))  # ratio never smaller than 1 with np.ceil
            res_ratio_r = 1
        else:
            res_ratio_r = int(np.ceil(rows_ref / rows_img))
            res_ratio_i = 1
        # marker colors
        colors = color_palette(len(pts))

        # convert image types to accepted ones for cv2.cvtColor
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

        # make sure the input image for "overlay_two_imgs" is of dtype "uint8" such that it would be acceptable for overlay_two_imgs (cv2.cvtColor)
        img_blend = overlay_two_imgs(_preprocess_img_dtype(warped_img), refimg_)
        params.debug = debug_mode

        _debug(visual=img_marked, filename=os.path.join(params.debug_outdir, str(params.device) + "_img-to-warp.png"))
        _debug(visual=refimg_marked, filename=os.path.join(params.debug_outdir, str(params.device) + "_img-ref.png"))
        _debug(visual=img_blend, filename=os.path.join(params.debug_outdir, str(params.device) + "_warp_overlay.png"))

    # rescale the warped_img and preserve the original the datatype
    # if img.dtype != 'uint8':
    #     warped_img = np.interp(warped_img, (warped_img.min(), warped_img.max()), (img.min(), img.max())).astype(
    #         img.dtype)

    return warped_img, mat


def warp_align(img, mat, refimg=None):
    """
    Warp the input image based on given transformation matrix mat, to align with the refimg

    :param img: image to warp (np.ndarray)
    :param mat: transformation matrix (np.ndarray, size: (3,3))
    :param refimg: (option) reference image
    :return:
    warpped image warped_img
    """

    params.device += 1

    # if no reference image, assume the target image is to be warped to the same size of itself
    if refimg is None:
        rows_ref, cols_ref = img.shape[0:2]
    else:
        rows_ref, cols_ref = refimg.shape[0:2]

    warped_img = cv2.warpPerspective(src=img, M=mat, dsize=(cols_ref, rows_ref))

    img_blend = warped_img
    debug_mode = params.debug
    if refimg is not None:
        params.debug = None
        img_blend = overlay_two_imgs(_preprocess_img_dtype(warped_img), _preprocess_img_dtype(refimg))

    params.debug = debug_mode
    _debug(visual=warped_img, filename=os.path.join(params.debug_outdir, str(params.device) + "_warped.png"))
    _debug(visual=img_blend, filename=os.path.join(params.debug_outdir, str(params.device) + "_warp_overlay.png"))

    return warped_img