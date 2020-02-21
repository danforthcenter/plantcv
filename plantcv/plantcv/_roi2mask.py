# Helper function to take an ROI and turn it into a binary mask

import os
import cv2
import numpy as np
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params
from plantcv.plantcv import outputs


def _roi2mask(img, roi_contour):
    """Create a binary mask from an ROI contour
    Inputs:
    img                  = RGB or grayscale image data
    roi_contour          = RGB image data
    roi_hierarchy        = Binary mask made from selected contours

    Returns:
    mask   = Binary mask

    :param roi_contour: list
    :param roi_hierarchy: numpy.ndarray
    :return mask: numpy.ndarray
    """

    # create a blank image of same size
    shape_info = np.shape(img)
    bnk = np.zeros((shape_info[0], shape_info[1]), dtype=np.uint8)
    img1 = np.copy(img)

    cv2.drawContours(bnk, roi_contour, 0, (255, 255, 255), -1)
    cv2.drawContours(img1, roi_contour, 0, (255, 255, 255), -1)

    if params.debug == 'print':
        print_image(bnk, os.path.join(params.debug_outdir, str(params.device) + '_roi.png'))
    elif params.debug == 'plot':
        plot_image(bnk, cmap="gray")
        plot_image(img1, cmap="gray")
    return img1, bnk, contour, hierarchy
