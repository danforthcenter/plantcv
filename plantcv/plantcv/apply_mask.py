# Apply White or Black Background Mask

import os
import numpy as np
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params


def apply_mask(rgb_img, mask, mask_color):
    """Apply white image mask to image, with bitwise AND operator bitwise NOT operator and ADD operator.

    Inputs:
    rgb_img    = RGB image data
    mask       = Binary mask image data
    mask_color = 'white' or 'black'

    Returns:
    masked_img = masked image data

    :param rgb_img: numpy.ndarray
    :param mask: numpy.ndarray
    :param mask_color: str
    :return masked_img: numpy.ndarray
    """

    params.device += 1

    if mask_color.upper() == "WHITE":
        color_val = 255
    elif mask_color.upper() == "BLACK":
        color_val = 0
    else:
        fatal_error('Mask Color ' + str(mask_color) + ' is not "white" or "black"!')

    array_data = rgb_img.copy()

    # Mask the array
    array_data[np.where(mask == 0)] = color_val

    # Check if the array data is
    if params.debug == 'print':
        print_image(array_data, os.path.join(params.debug_outdir, str(params.device) + '_masked.png'))
    elif params.debug == 'plot':
        plot_image(array_data)

    return array_data
