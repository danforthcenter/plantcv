# Image subtraction

from plantcv.plantcv._debug import _debug
from plantcv.plantcv import params
from plantcv.plantcv import fatal_error
import numpy as np
import os


def image_subtract(gray_img1, gray_img2):
    """
    This is a function used to subtract values of one gray-scale image array from another gray-scale image array. The
    resulting gray-scale image array has a minimum element value of zero. That is all negative values resulting from the
    subtraction are forced to zero.

    Inputs:
    gray_img1   = Grayscale image data from which gray_img2 will be subtracted
    gray_img2   = Grayscale image data which will be subtracted from gray_img1

    Returns:
    new_img = subtracted image

    :param gray_img1: numpy.ndarray
    :param gray_img2: numpy.ndarray
    :return new_img: numpy.ndarray
    """

    # check inputs for gray-scale
    if len(np.shape(gray_img1)) != 2 or len(np.shape(gray_img2)) != 2:
        fatal_error("Input image is not gray-scale")

    new_img = gray_img1.astype(np.float64) - gray_img2.astype(np.float64)  # subtract values
    new_img[np.where(new_img < 0)] = 0  # force negative array values to zero
    new_img = new_img.astype(np.uint8)  # typecast image to 8-bit image

    _debug(visual=new_img,
           filename=os.path.join(params.debug_outdir, str(params.device) + "_subtraction.png"),
           cmap='gray')

    return new_img  # return
