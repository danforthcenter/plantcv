# Variance texture filter

import os
import cv2
import math
import numpy as np
from matplotlib import pyplot as plt
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params
from scipy.ndimage import generic_filter
from skimage.feature import greycomatrix, greycoprops


def extract_texture(gray_img, ksize, offset=3, texture_method='dissimilarity', borders='nearest'):
    """Creates a binary image from a grayscale image using skimage texture calculation for thresholding.
    This function is quite slow.

    Inputs:
    gray_img       = Grayscale image data
    ksize          = Kernel size for texture measure calculation
    offset         = Distance offsets
    texture_method = Feature of a grey level co-occurrence matrix, either
                     'contrast', 'dissimilarity', 'homogeneity', 'ASM', 'energy',
                     or 'correlation'.For equations of different features see
                     scikit-image.
    borders        = How the array borders are handled, either 'reflect',
                     'constant', 'nearest', 'mirror', or 'wrap'

    Returns:
    bin_img        = Thresholded, binary image

    :param gray_img: numpy.ndarray
    :param ksize: int
    :param offset: int
    :param texture_method: str
    :param borders: str
    :return bin_img: numpy.ndarray
    """

    # Function that calculates the texture of a kernel
    def calc_texture(inputs):
        inputs = np.reshape(a=inputs, newshape=[ksize, ksize])
        inputs = inputs.astype(np.uint8)
        # Greycomatrix takes image, distance offset, angles (in radians), symmetric, and normed
        # http://scikit-image.org/docs/dev/api/skimage.feature.html#skimage.feature.greycomatrix
        glcm = greycomatrix(inputs, [offset], [0], 256, symmetric=True, normed=True)
        diss = greycoprops(glcm, texture_method)[0, 0]
        return diss

    # Make an array the same size as the original image
    output = np.zeros(gray_img.shape, dtype=gray_img.dtype)

    # Apply the texture function over the whole image
    generic_filter(gray_img, calc_texture, size=ksize, output=output, mode=borders)

    if params.debug == "print":
        # If debug is print, save the image to a file
        print_image(output, os.path.join(params.debug_outdir, str(params.device) + "_variance.png"))
    elif params.debug == "plot":
        # If debug is plot, print to the plotting device
        plot_image(output)

    # Threshold so higher texture measurements stand out
    return output