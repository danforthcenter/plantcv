# Variance texture filter


import os
import numpy as np
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import params
from scipy.ndimage import generic_filter


def stdev_filter(img, ksize, borders='nearest'):
    """
    Creates a binary image from a grayscale image using skimage texture calculation for thresholding.
    This function is quite slow.

    Inputs:
    gray_img       = Grayscale image data
    ksize          = Kernel size for texture measure calculation
    borders        = How the array borders are handled, either 'reflect',
                     'constant', 'nearest', 'mirror', or 'wrap'

    Returns:
    output         = Standard deviation values image

    :param img: numpy.ndarray
    :param ksize: int
    :param borders: str
    :return output: numpy.ndarray
    """

    # Make an array the same size as the original image
    output = np.zeros(img.shape, dtype=img.dtype)

    # Apply the texture function over the whole image
    generic_filter(img, np.std, size=ksize, output=output, mode=borders)

    _debug(visual=output,
           filename=os.path.join(params.debug_outdir, str(params.device) + "_variance.png"))

    return output
