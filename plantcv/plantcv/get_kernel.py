# Create a kernel structuring element

import cv2
import numpy as np
import os
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import params



def get_kernel(size, shape):
    """Performs morphological 'dilation' filtering. Adds pixel to center of kernel if conditions set in kernel are true.
    Inputs:
    size   = Kernel size (int). A k x k kernel will be built. Must be greater than 1 to have an effect.
    shape  = Element shape, either

    Returns:
    dil_img = dilated image

    :param gray_img: numpy.ndarray
    :param ksize: int
    :param i: int
    :return dil_img: numpy.ndarray
    """
