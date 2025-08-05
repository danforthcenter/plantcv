# Variance texture filter


import os
import numpy as np
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _rect_filter, _rect_replace
from plantcv.plantcv import params
from scipy.ndimage import generic_filter


def stdev_filter(img, ksize, borders='nearest', roi=None):
    """
    Creates a binary image from a grayscale image using skimage texture calculation for thresholding.
    This function is quite slow.

    Inputs:
    gray_img       = Grayscale image data
    ksize          = Kernel size for texture measure calculation
    borders        = How the array borders are handled, either 'reflect',
                     'constant', 'nearest', 'mirror', or 'wrap'
    roi            = optional rectangular ROI to apply filter within

    Returns:
    output         = Standard deviation values image

    :param img: numpy.ndarray
    :param ksize: int
    :param borders: str
    :param roi: plantcv.plantcv.Objects
    :return output: numpy.ndarray
    """
    # Make an array the same size as the original image
    output = np.zeros(img.shape, dtype=img.dtype)
    # Take the pieces of the empty mask and image in the ROI
    sub_zeros = _rect_filter(output, roi)
    sub_img = _rect_filter(img, roi)
    # Apply the texture function over the subset image
    generic_filter(sub_img, np.std, size=ksize, output=sub_zeros, mode=borders)
    # re-insert the subset into the full size mask
    replaced = _rect_replace(img, sub_zeros, roi)

    _debug(visual=replaced,
           filename=os.path.join(params.debug_outdir, str(params.device) + "_variance.png"))

    return replaced
