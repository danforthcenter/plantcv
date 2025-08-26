# Image subtraction

from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _image_subtract
from plantcv.plantcv import params
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
    new_img = _image_subtract(gray_img1, gray_img2)

    _debug(visual=new_img,
           filename=os.path.join(params.debug_outdir, str(params.device) + "_subtraction.png"),
           cmap='gray')

    return new_img  # return
