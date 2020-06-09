# Helper function to take an ROI and turn it into a binary mask

import os
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image


def roi2mask(img, contour):
    """Create a binary mask from an ROI contour
    Inputs:
    img                  = RGB or grayscale image data
    contour              = An ROI set of points (contour)

    Returns:
    mask   = Binary mask

    :param img: numpy.ndarray
    :param contour: list
    :return mask: numpy.ndarray
    """
    params.device += 1

    # create a blank image of same size
    shape_info = np.shape(img)
    bnk = np.zeros((shape_info[0], shape_info[1]), dtype=np.uint8)

    mask = cv2.drawContours(bnk, contour, 0, 255, -1)

    if params.debug == 'print':
        print_image(mask, os.path.join(params.debug_outdir, str(params.device) + '_roi_mask.png'))
    elif params.debug == 'plot':
        plot_image(mask, cmap="gray")

    return mask
