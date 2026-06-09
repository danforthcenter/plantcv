# Sobel filtering

import cv2
import os
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _rect_filter, _rect_replace
from plantcv.plantcv._globals import params
from plantcv.plantcv.get_kernel import _format_kernel


def sobel_filter(gray_img, dx, dy, ksize, roi=None):
    """
    This is a filtering method used to identify and highlight gradient edges/features using the 1st derivative.
    Typically used to identify gradients along the x-axis (dx = 1, dy = 0) and y-axis (dx = 0, dy = 1) independently.
    Performance is quite similar to Scharr filter. Used to detect edges / changes in pixel intensity. ddepth = -1
    specifies that the dimensions of output image will be the same as the input image.

    Parameters:
    -----------
    gray_img = numpy.ndarray,
        Grayscale image data
    dx       = int,
        derivative of x to analyze
    dy       = int,
        derivative of x to analyze
    ksize        = int, numpy.ndarray, or tuple
        Kernel specified as a binary numpy.ndarray for arbitrary shapes,
        shape tuple for a rectangular kernel, or integer for a square kernel.
        ksize will be coerced to int here.
    roi      = plantcv.plantcv.Objects,
        optional rectangular roi to apply sobel filter within

    Returns:
    --------
    sb_img   = numpy.ndarray,
        Sobel filtered image
    """
    k = _format_kernel(ksize, int)
    sub_sb_img = _rect_filter(gray_img, roi, function=cv2.Sobel,
                              **{"ddepth": -1, "dx": dx, "dy": dy, "ksize": k})
    sb_img = _rect_replace(gray_img, sub_sb_img, roi)

    fname = str(params.device) + '_sb_img_dx' + str(dx) + '_dy' + str(dy) + '_kernel' + str(ksize) + '.png'
    _debug(visual=sb_img,
           filename=os.path.join(params.debug_outdir, fname),
           cmap='gray')

    return sb_img
