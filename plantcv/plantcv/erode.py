# Erosion filter

import cv2
import numpy as np
import os
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import params


def erode(gray_img, kernel, i):
    """Perform morphological 'erosion' filtering. Keeps pixel in center of the kernel if conditions set in kernel are
       true, otherwise removes pixel.

    Inputs:
    gray_img = Grayscale (usually binary) image data
    kernel   = Kernel size (int). A k x k kernel will be built. Must be greater than 1 to have an effect.
    i        = interations, i.e. number of consecutive filtering passes

    Returns:
    er_img = eroded image

    :param gray_img: numpy.ndarray
    :param kernel: int
    :param i: int
    :return er_img: numpy.ndarray
    """

    kernel1 = int(kernel)
    kernel2 = np.ones((kernel1, kernel1), np.uint8)
    er_img = cv2.erode(src=gray_img, kernel=kernel2, iterations=i)
    params.device += 1
    if params.debug == 'print':
        print_image(er_img, os.path.join(params.debug_outdir,
                                         str(params.device) + '_er_image_' + 'itr_' + str(i) + '.png'))
    elif params.debug == 'plot':
        plot_image(er_img, cmap='gray')
    return er_img
