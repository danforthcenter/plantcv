# Dilation filter

import numpy as np
import os
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import params
from cv2 import dilate

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
    :param roi: Objects
    :return dil_img: numpy.ndarray
    """
    from  plantcv.plantcv._helpers import _rect_filter, _rect_replace
    if ksize <= 1:
        raise ValueError('ksize needs to be greater than 1 for the function to have an effect')

    kernel1 = int(ksize)
    kernel2 = np.ones((kernel1, kernel1), np.uint8)
    sub_dil_img = _rect_filter(img = gray_img,
                           roi=roi,
                           function=dilate,
                           **{"kernel":kernel2, "iterations":i})
    dil_img =  plantcv.plantcv._helpers._rect_replace(gray_img, sub_dil_img, roi)

    _debug(visual=dil_img,
           filename=os.path.join(params.debug_outdir,
                                 str(params.device) + '_dil_image' + str(ksize) + '_itr' + str(i) + '.png'),
           cmap='gray')

    return dil_img
