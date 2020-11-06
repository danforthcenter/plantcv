# Overlay two input images

"""
Created on Tue. September 01 21:00:01 2020
A function
@author: hudanyunsheng
"""

import os
import cv2
import numpy as np
from plantcv.plantcv import fatal_error
from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image
from plantcv.plantcv import params
import warnings


def overlay_two_imgs(img1, img2, alpha=0.5):
    """Overlay two images with a given alpha value.

    Inputs:
    img1     - RGB or grayscale image data
    img2     - RGB or grayscale image data
    alpha    - Desired opacity of 1st image, range: (0,1), default value=0.5

    Returns:
    out_img  - Blended RGB image

    :param img1: numpy.ndarray
    :param img2: numpy.ndarray
    :param alpha: float
    :return: out_img: numpy.ndarray
    """
    if alpha > 1 or alpha < 0:
        fatal_error("The value of alpha should be in the range of (0,1)!")

    # Copy the input images
    img1_ = np.copy(img1)
    img2_ = np.copy(img2)
    # If the images are grayscale convert to BGR
    if len(img1_.shape) == 2:
        img1_ = cv2.cvtColor(img1_, cv2.COLOR_GRAY2BGR)
    if len(img2_.shape) == 2:
        img2_ = cv2.cvtColor(img2_, cv2.COLOR_GRAY2BGR)

    ## sizing
    # assumption: the sizes of img1 and img2 are the same
    size_img = img1_.shape[0:2]

    # initialize the output image
    out_img = np.zeros(size_img + (3,), dtype='uint8')

    # blending
    out_img[:, :, :] = (alpha * img1_[:, :, :]) + ((1 - alpha) * img2_[:, :, :])

    params.device += 1
    if params.debug == 'print':
        print_image(out_img, os.path.join(params.debug_outdir, str(params.device) + '_overlay.png'))
    elif params.debug == 'plot':
        plot_image(out_img)
    return out_img
