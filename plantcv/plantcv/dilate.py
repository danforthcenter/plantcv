# Dilation filter

import cv2
import numpy as np
import os
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import params


def dilate(img, kernel, i):
    """Performs morphological 'dilation' filtering. Adds pixel to center of kernel if conditions set in kernel are true.

    Inputs:
    img     = input image
    kernel  = filtering window, you'll need to make your own using as such:
              kernal = np.zeros((x,y), dtype=np.uint8), then fill the kernal with appropriate values
    i       = interations, i.e. number of consecutive filtering passes

    Returns:
    dil_img = dilated image

    :param img: numpy array
    :param kernel: numpy array
    :param i: int
    :return dil_img: numpy array
    """

    kernel1 = int(kernel)
    kernel2 = np.ones((kernel1, kernel1), np.uint8)
    dil_img = cv2.dilate(src=img, kernel=kernel2, iterations=i)
    params.device += 1
    if params.debug == 'print':
        print_image(dil_img, os.path.join(params.debug, str(params.device) + '_dil_image_' + 'itr_' + str(i) + '.png'))
    elif params.debug == 'plot':
        plot_image(dil_img, cmap='gray')
    return dil_img
