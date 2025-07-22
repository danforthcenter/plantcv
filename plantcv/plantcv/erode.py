# Erosion filter

import numpy as np
import os
import cv2
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _rect_filter, _rect_replace
from plantcv.plantcv import params


def erode(gray_img, ksize, i, roi=None):
    """
    Perform morphological 'erosion' filtering. Keeps pixel in center of the kernel if conditions set in kernel are
       true, otherwise removes pixel.

    Inputs:
    gray_img = Grayscale (usually binary) image data
    ksize   = Kernel size (int). A ksize x ksize kernel will be built. Must be greater than 1 to have an effect.
    i        = interations, i.e. number of consecutive filtering passes
    roi      = Rectangular ROI to erode within

    Returns:
    er_img = eroded image

    :param gray_img: numpy.ndarray
    :param ksize: int
    :param i: int
    "param roi: Objects
    :return er_img: numpy.ndarray
    """
    if ksize <= 1:
        raise ValueError('ksize needs to be greater than 1 for the function to have an effect')

    kernel1 = int(ksize)
    kernel2 = np.ones((kernel1, kernel1), np.uint8)
    sub_er_img = _rect_filter(img = gray_img,
                           roi=roi,
                           function=cv2.erode,
                           **{"kernel":kernel2, "iterations":i})
    er_img = _rect_replace(gray_img, sub_er_img, roi)
    
    _debug(er_img,
           filename=os.path.join(params.debug_outdir,
                                 str(params.device) + '_er_image' + str(ksize) + '_itr_' + str(i) + '.png'),
           cmap='gray')

    return er_img
