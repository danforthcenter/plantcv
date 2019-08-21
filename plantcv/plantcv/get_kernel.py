# Create a kernel structuring element

import cv2
import numpy as np
import os
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import params



def get_kernel(size, shape):
    """Creates a kernel structuring element of specified size and shape.

    size   = Kernel size (int). A (m x n) kernel will be built. Must be greater than 1 to have an effect.
    shape  = Element shape, either rectangle, cross, or ellipse.

    Returns:
    kernel = Structuring element kernel

    :param size: tuple
    :param shape: str
    :return kernel: numpy.ndarray
    """

    if size <= 1:
        raise ValueError('size needs to be greater than 1 for the function to have an effect')


