# Variance texture filter


import os
import numpy as np
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import params
from scipy.ndimage import generic_filter


def stdev_filter(gray_img, ksize, offset=3, texture_method='dissimilarity', borders='nearest'):
    """Creates a binary image from a grayscale image using skimage texture calculation for thresholding.
    This function is quite slow.

    Inputs:
    gray_img       = Grayscale image data
    ksize          = Kernel size for texture measure calculation
    threshold      = Threshold value (0-255)
    offset         = Distance offsets
    texture_method = Feature of a grey level co-occurrence matrix, either
                     'contrast', 'dissimilarity', 'homogeneity', 'ASM', 'energy',
                     or 'correlation'.For equations of different features see
                     scikit-image.
    borders        = How the array borders are handled, either 'reflect',
                     'constant', 'nearest', 'mirror', or 'wrap'
    max_value      = Value to apply above threshold (usually 255 = white)

    Returns:
    bin_img        = Thresholded, binary image

    :param gray_img: numpy.ndarray
    :param ksize: int
    :param threshold: int
    :param offset: int
    :param texture_method: str
    :param borders: str
    :param max_value: int
    :return bin_img: numpy.ndarray
    """

    # Make an array the same size as the original image
    output = np.zeros(gray_img.shape, dtype=gray_img.dtype)

    # Apply the texture function over the whole image
    generic_filter(gray_img, np.std, size=ksize, output=output, mode=borders)

    if params.debug == "print":
        # If debug is print, save the image to a file
        print_image(output, os.path.join(params.debug_outdir, str(params.device) + "_variance.png"))
    elif params.debug == "plot":
        # If debug is plot, print to the plotting device
        plot_image(output)

    return output
