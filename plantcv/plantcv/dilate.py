# Dilation filter

import os
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _dilate
from plantcv.plantcv import params


def dilate(gray_img, ksize, i, roi=None):
    """
    Performs morphological 'dilation' filtering. Adds pixel to center of kernel if conditions set in kernel are true.

    Inputs:
    gray_img = Grayscale (usually binary) image data
    ksize   = Kernel size (int). A k x k kernel will be built. Must be greater than 1 to have an effect.
    i        = iterations, i.e. number of consecutive filtering passes
    roi      = rectangular ROI to dilate within

    Returns:
    dil_img = dilated image

    :param gray_img: numpy.ndarray
    :param ksize: int
    :param i: int
    :param roi: plantcv.plantcv.Objects
    :return dil_img: numpy.ndarray
    """
    dil_img = _dilate(gray_img, ksize, i, roi=roi)

    _debug(visual=dil_img,
           filename=os.path.join(params.debug_outdir,
                                 str(params.device) + '_dil_image' + str(ksize) + '_itr' + str(i) + '.png'),
           cmap='gray')

    return dil_img
