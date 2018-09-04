# RGB -> Gray

import cv2
import os
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import params


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
    params.device += 1
    if params.debug == 'print':
        print_image(gray, os.path.join(params.debug_outdir, str(params.device) + '_gray.png'))
    elif params.debug == 'plot':
        plot_image(gray, cmap='gray')
    return gray
