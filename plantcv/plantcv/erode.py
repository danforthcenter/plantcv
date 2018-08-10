# Erosion filter

import cv2
import numpy as np
import os
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import params


def erode(img, kernel, i):
    """Perform morphological 'erosion' filtering. Keeps pixel in center of the kernel if conditions set in kernel are
       true, otherwise removes pixel.

    Inputs:
    img    = input image
    kernel = filtering window, you'll need to make your own using as such:
             kernal = np.zeros((x,y), dtype=np.uint8), then fill the kernal with appropriate values
    i      = interations, i.e. number of consecutive filtering passes

    Returns:
    er_img = eroded image

    :param img: numpy array
    :param kernel: numpy array
    :param i: int
    :return er_img: numpy array
    """

    kernel1 = int(kernel)
    kernel2 = np.ones((kernel1, kernel1), np.uint8)
    er_img = cv2.erode(src=img, kernel=kernel2, iterations=i)
    params.device += 1
    if params.debug == 'print':
        print_image(er_img, os.path.join(params.debug_outdir,
                                         str(params.device) + '_er_image_' + 'itr_' + str(i) + '.png'))
    elif params.debug == 'plot':
        plot_image(er_img, cmap='gray')
    return er_img
