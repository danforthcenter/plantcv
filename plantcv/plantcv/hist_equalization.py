# Histogram equalization

import cv2
import numpy as np
import os
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params


def hist_equalization(gray_img):
    """
    Histogram equalization is a method to normalize the distribution of intensity values. If the image has low
       contrast it will make it easier to threshold.

    Inputs:
    gray_img    = Grayscale image data

    Returns:
    img_eh = normalized image

    :param gray_img: numpy.ndarray
    :return img_eh: numpy.ndarray
    """

    if len(np.shape(gray_img)) == 3:
        fatal_error("Input image must be gray")

    img_eh = cv2.equalizeHist(gray_img)

    _debug(visual=img_eh,
           filename=os.path.join(params.debug_outdir, str(params.device) + '_hist_equal_img.png'),
           cmap='gray')

    return img_eh
