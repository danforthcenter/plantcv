# Remove small bright spots

import os
import numpy as np
from skimage import morphology
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _rect_filter, _rect_replace
from plantcv.plantcv import fatal_error


def opening(gray_img, kernel=None, roi=None):
    """
    Wrapper for scikit-image opening functions. Opening can remove small bright spots (i.e. salt).

    Inputs:
    gray_img = input image (grayscale or binary)
    kernel   = optional neighborhood, expressed as an array of 1s and 0s. If None, use cross-shaped structuring element.
    roi      = optional rectangular ROI to open within

    :param gray_img: ndarray
    :param kernel: ndarray
    :param roi: plantcv.plantcv.Objects
    :return filtered_img: ndarray
    """
    # Make sure the image is binary/grayscale
    if len(np.shape(gray_img)) != 2:
        fatal_error("Input image must be grayscale or binary")

    # If image is binary use the faster method
    if len(np.unique(gray_img)) == 2:
        bool_img = gray_img.astype(bool)
        sub_img = _rect_filter(bool_img, roi, function=morphology.binary_opening,
                               **{"footprint": kernel})
        filtered_img = sub_img.astype(np.uint8) * 255
        replaced_img = _rect_replace(bool_img.astype(np.uint8) * 255, filtered_img, roi)
    # Otherwise use method appropriate for grayscale images
    else:
        filtered_img = _rect_filter(gray_img, roi=roi, function=morphology.opening,
                                    **{"footprint": kernel})
        replaced_img = _rect_replace(gray_img, filtered_img, roi)

    _debug(visual=replaced_img,
           filename=os.path.join(params.debug_outdir, str(params.device) + '_opening.png'),
           cmap='gray')

    return replaced_img
