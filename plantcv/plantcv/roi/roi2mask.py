# Helper function to take an ROI and turn it into a binary mask

import os
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug


def roi2mask(img, roi):
    """
    Create a binary mask from an ROI contour
    Inputs:
    img                  = RGB or grayscale image data
    roi                  = A region of interest as an instance of the class Objects

    Returns:
    mask   = Binary mask

    :param img: numpy.ndarray
    :param roi: plantcv.plantcv.classes.Objects
    :return mask: numpy.ndarray
    """
    # create a blank image of same size
    shape_info = np.shape(img)
    mask = np.zeros((shape_info[0], shape_info[1]), dtype=np.uint8)

    for single_roi_cnt in roi:
        _ = cv2.drawContours(mask, single_roi_cnt.contours[0], 0, 255, -1)

    _debug(visual=mask,
           filename=os.path.join(params.debug_outdir, str(params.device) + '_roi_mask.png'),
           cmap='gray')

    return mask
