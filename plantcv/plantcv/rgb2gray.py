# RGB -> Gray

import cv2
import os
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug


def rgb2gray(rgb_img):
    """Convert image from RGB colorspace to Gray.

    Inputs:
    rgb_img    = RGB image data

    Returns:
    gray   = grayscale image

    :param rgb_img: numpy.ndarray
    :return gray: numpy.ndarray
    """

    gray = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2GRAY)

    _debug(visual=gray, filename=os.path.join(params.debug_outdir, str(params.device) + "_gray.png"))

    return gray
