# Join images (AND)

import cv2
import os
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import params

def logical_and(img1, img2):
    """Join two images using the bitwise AND operator.

    Inputs:
    img1   = image object1, grayscale
    img2   = image object2, grayscale

    Returns:
    merged = joined image

    :param img1: numpy array
    :param img2: numpy array
    :return merged: numpy array
    """

    params.device += 1
    merged = cv2.bitwise_and(img1, img2)
    if params.debug == 'print':
        print_image(merged, os.path.join(params.debug_outdir, str(params.device) + '_and_joined.png'))
    elif params.debug == 'plot':
        plot_image(merged, cmap='gray')
    return merged
