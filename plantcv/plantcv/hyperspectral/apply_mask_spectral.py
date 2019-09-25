# Apply White or Black Background Mask

import os
import cv2
import numpy as np
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params


def apply_mask_spectral(array, mask):
    """Apply mask to hyperspectral datacube with numpy.where

    Inputs:
    array      = Array data
    mask       = Binary mask image data

    Returns:
    masked_array = masked array data

    :param array: numpy.ndarray
    :param mask: numpy.ndarray
    :return masked_array: numpy.ndarray
    """
    params.device += 1

    rescaled_array[np.where(kept_mask == 0)] = 0
