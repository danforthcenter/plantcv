# Invert gray image

import cv2
import os
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import params


def invert(gray_img):
    """
    Inverts grayscale images.

    Inputs:
    gray_img     = Grayscale image data

    Returns:
    img_inv = inverted image

    :param gray_img: numpy.ndarray
    :return img_inv: numpy.ndarray
    """

    img_inv = cv2.bitwise_not(gray_img)

    _debug(visual=img_inv,
           filename=os.path.join(params.debug_outdir, str(params.device) + '_invert.png'),
           cmap='gray')

    return img_inv
