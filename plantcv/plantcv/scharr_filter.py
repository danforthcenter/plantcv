# Scharr filtering

import cv2
import os
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _rect_filter, _rect_replace
from plantcv.plantcv import params


def scharr_filter(img, dx, dy, scale, roi=None):
    """
    This is a filtering method used to identify and highlight gradient edges/features using the 1st derivative.
    Typically used to identify gradients along the x-axis (dx = 1, dy = 0) and y-axis (dx = 0, dy = 1) independently.
    Performance is quite similar to Sobel filter. Used to detect edges / changes in pixel intensity. ddepth = -1
    specifies that the dimensions of output image will be the same as the input image.

    Inputs:
    gray_img = grayscale image data
    dx       = derivative of x to analyze (1-3)
    dy       = derivative of y to analyze (1-3)
    scale    = scaling factor applied (multiplied) to computed Scharr values (scale = 1 is unscaled)
    roi      = optional rectangular roi to apply scharr filter within

    Returns:
    sr_img   = Scharr filtered image

    :param img: numpy.ndarray
    :param dx: int
    :param dy: int
    :param scale: int
    :param roi: plantcv.plantcv.Objects
    :return sr_img: numpy.ndarray
    """
    sub_sr_img = _rect_filter(img, roi, function=cv2.Scharr,
                              **{"ddepth": -1, "dx": dx, "dy": dy, "scale": scale})
    sr_img = _rect_replace(img, sub_sr_img, roi)
    name = os.path.join(params.debug_outdir, str(params.device))
    name += '_sr_img_dx' + str(dx) + '_dy' + str(dy) + '_scale' + str(scale) + '.png'

    _debug(visual=sr_img,
           filename=name,
           cmap='gray')

    return sr_img
