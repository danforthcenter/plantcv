# Join images (AND)

import cv2
import os
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import params


def logical_and(bin_img1, bin_img2):
    """Join two images using the bitwise AND operator.

    Inputs:
    bin_img1   = Binary image data to be compared to bin_img2
    bin_img2   = Binary image data to be compared to bin_img1

    Returns:
    merged     = joined binary image

    :param bin_img1: numpy.ndarray
    :param bin_img2: numpy.ndarray
    :return merged: numpy.ndarray
    """

    params.device += 1
    merged = cv2.bitwise_and(bin_img1, bin_img2)
    if params.debug == 'print':
        print_image(merged, os.path.join(params.debug_outdir, str(params.device) + '_and_joined.png'))
    elif params.debug == 'plot':
        plot_image(merged, cmap='gray')
    return merged
