# Erosion filter

import cv2
import numpy as np
import os
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import params


def erode(gray_img, ksize, i):
    """
    Perform morphological 'erosion' filtering. Keeps pixel in center of the kernel if conditions set in kernel are
       true, otherwise removes pixel.

    Inputs:
    gray_img = Grayscale (usually binary) image data
    ksize   = Kernel size (int). A ksize x ksize kernel will be built. Must be greater than 1 to have an effect.
    i        = interations, i.e. number of consecutive filtering passes

    Returns:
    er_img = eroded image

    :param gray_img: numpy.ndarray
    :param ksize: int
    :param i: int
    :return er_img: numpy.ndarray
    """

    if ksize <= 1:
        raise ValueError('ksize needs to be greater than 1 for the function to have an effect')

    kernel1 = int(ksize)
    kernel2 = np.ones((kernel1, kernel1), np.uint8)
    er_img = cv2.erode(src=gray_img, kernel=kernel2, iterations=i)

    _debug(er_img,
           filename=os.path.join(params.debug_outdir,
                                 str(params.device) + '_er_image' + str(ksize) + '_itr_' + str(i) + '.png'),
           cmap='gray')

    return er_img
