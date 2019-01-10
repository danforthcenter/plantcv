# Dilation filter

import cv2
import numpy as np
import os
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import params


def dilate(gray_img, kernel, i):
    """Performs morphological 'dilation' filtering. Adds pixel to center of kernel if conditions set in kernel are true.

    Inputs:
    gray_img = Grayscale (usually binary) image data
    kernel   = Kernel size (int). A k x k kernel will be built. Must be greater than 1 to have an effect.
    i        = iterations, i.e. number of consecutive filtering passes

    Returns:
    dil_img = dilated image

    :param gray_img: numpy.ndarray
    :param kernel: int
    :param i: int
    :return dil_img: numpy.ndarray
    """

    kernel1 = int(kernel)
    kernel2 = np.ones((kernel1, kernel1), np.uint8)
    dil_img = cv2.dilate(src=gray_img, kernel=kernel2, iterations=i)
    params.device += 1
    if params.debug == 'print':
        print_image(dil_img, os.path.join(params.debug, str(params.device) + '_dil_image_' + 'itr_' + str(i) + '.png'))
    elif params.debug == 'plot':
        plot_image(dil_img, cmap='gray')
    return dil_img
