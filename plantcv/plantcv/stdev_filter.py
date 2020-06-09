# Variance texture filter


import os
import numpy as np
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import params
from scipy.ndimage import generic_filter


def stdev_filter(img, ksize, borders='nearest'):
    """Creates a binary image from a grayscale image using skimage texture calculation for thresholding.
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

    if params.debug == "print":
        # If debug is print, save the image to a file
        print_image(output, os.path.join(params.debug_outdir, str(params.device) + "_variance.png"))
    elif params.debug == "plot":
        # If debug is plot, print to the plotting device
        plot_image(output)

    return output
