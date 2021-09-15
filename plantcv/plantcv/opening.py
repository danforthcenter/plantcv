# Remove small bright spots

import os
import numpy as np
from skimage import morphology
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import fatal_error


def opening(gray_img, kernel=None):
    """
    Wrapper for scikit-image opening functions. Opening can remove small bright spots (i.e. salt).

    Inputs:
    gray_img = input image (grayscale or binary)
    kernel   = optional neighborhood, expressed as an array of 1s and 0s. If None, use cross-shaped structuring element.

    :param gray_img: ndarray
    :param kernel = ndarray
    :return filtered_img: ndarray
    """

    # Make sure the image is binary/grayscale
    if len(np.shape(gray_img)) != 2:
        fatal_error("Input image must be grayscale or binary")

    # If image is binary use the faster method
    if len(np.unique(gray_img)) == 2:
        bool_img = morphology.binary_opening(gray_img, kernel)
        filtered_img = np.copy(bool_img.astype(np.uint8) * 255)
    # Otherwise use method appropriate for grayscale images
    else:
        filtered_img = morphology.opening(gray_img, kernel)

    _debug(visual=filtered_img,
           filename=os.path.join(params.debug_outdir, str(params.device) + '_opening.png'),
           cmap='gray')

    return filtered_img
