# Sobel filtering

import cv2
import os
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _rect_filter, _rect_replace
from plantcv.plantcv import params


def sobel_filter(gray_img, dx, dy, ksize, roi=None):
    """
    This is a filtering method used to identify and highlight gradient edges/features using the 1st derivative.
    Typically used to identify gradients along the x-axis (dx = 1, dy = 0) and y-axis (dx = 0, dy = 1) independently.
    Performance is quite similar to Scharr filter. Used to detect edges / changes in pixel intensity. ddepth = -1
    specifies that the dimensions of output image will be the same as the input image.

    Inputs:
    gray_img = Grayscale image data
    dx       = derivative of x to analyze
    dy       = derivative of x to analyze
    ksize    = specifies the size of the kernel (must be an odd integer: 1,3,5, ... , 31)
    roi      = optional rectangular roi to apply sobel filter within

    Returns:
    sb_img   = Sobel filtered image

    :param gray_img: numpy.ndarray
    :param dx: int
    :param dy: int
    :param ksize: int
    :param roi: plantcv.plantcv.Objects
    :return sb_img: numpy.ndarray
    """
    sub_sb_img = _rect_filter(gray_img, roi, function=cv2.Sobel,
                              **{"ddepth": -1, "dx": dx, "dy": dy, "ksize": ksize})
    sb_img = _rect_replace(gray_img, sub_sb_img, roi)

    fname = str(params.device) + '_sb_img_dx' + str(dx) + '_dy' + str(dy) + '_kernel' + str(ksize) + '.png'
    _debug(visual=sb_img,
           filename=os.path.join(params.debug_outdir, fname),
           cmap='gray')

    return sb_img
