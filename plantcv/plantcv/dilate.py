# Dilation filter

import cv2
import numpy as np
import os
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import params


def dilate(gray_img, ksize, i):
    """
    Performs morphological 'dilation' filtering. Adds pixel to center of kernel if conditions set in kernel are true.

    Inputs:
    gray_img = Grayscale (usually binary) image data
    ksize   = Kernel size (int). A k x k kernel will be built. Must be greater than 1 to have an effect.
    i        = iterations, i.e. number of consecutive filtering passes

    Returns:
    dil_img = dilated image

    :param gray_img: numpy.ndarray
    :param ksize: int
    :param i: int
    :return dil_img: numpy.ndarray
    """

    if ksize <= 1:
        raise ValueError('ksize needs to be greater than 1 for the function to have an effect')

    kernel1 = int(ksize)
    kernel2 = np.ones((kernel1, kernel1), np.uint8)
    dil_img = cv2.dilate(src=gray_img, kernel=kernel2, iterations=i)

    _debug(visual=dil_img,
           filename=os.path.join(params.debug_outdir,
                                 str(params.device) + '_dil_image' + str(ksize) + '_itr' + str(i) + '.png'),
           cmap='gray')

    return dil_img
