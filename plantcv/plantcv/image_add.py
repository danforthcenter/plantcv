# Image addition

import os
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import params


def image_add(gray_img1, gray_img2):
    """
    This is a function used to add images. The numpy addition function '+' is used. This is a modulo operation
       rather than the cv2.add fxn which is a saturation operation. ddepth = -1 specifies that the dimensions of output
       image will be the same as the input image.

    Inputs:
    gray_img1      = Grayscale image data to be added to image 2
    gray_img2      = Grayscale image data to be added to image 1

    Returns:
    added_img      = summed images

    :param gray_img1: numpy.ndarray
    :param gray_img2: numpy.ndarray
    :return added_img: numpy.ndarray
    """

    added_img = gray_img1 + gray_img2

    _debug(visual=added_img,
           filename=os.path.join(params.debug_outdir, str(params.device) + '_added' + '.png'),
           cmap='gray')

    return added_img
