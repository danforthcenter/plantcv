# Apply White or Black Background Mask

import os
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import fatal_error
from plantcv.plantcv.transform import rescale


def apply_mask(img, mask, mask_color):
    """Apply white image mask to image, with bitwise AND operator bitwise NOT operator and ADD operator.

    Inputs:
    img        = RGB image data
    mask       = Binary mask image data
    mask_color = 'white' or 'black'

    Returns:
    masked_img = masked image data

    :param img: numpy.ndarray
    :param mask: numpy.ndarray
    :param mask_color: str
    :return masked_img: numpy.ndarray
    """

    if mask_color.upper() == "WHITE":
        color_val = 255
    elif mask_color.upper() == "BLACK":
        color_val = 0
    else:
        fatal_error('Mask Color ' + str(mask_color) + ' is not "white" or "black"!')

    array_data = img.copy()

    # Mask the array
    array_data[np.where(mask == 0)] = color_val

    # Check the array data format
    if len(np.shape(array_data)) > 2 and np.shape(array_data)[-1] > 3:
        # Replace this part with _make_pseudo_rgb
        num_bands = np.shape(array_data)[2]
        med_band = int(num_bands / 2)
        debug = params.debug
        params.debug = None
        pseudo_rgb = cv2.merge((rescale(array_data[:, :, 0]),
                                rescale(array_data[:, :, med_band]),
                                rescale(array_data[:, :, num_bands - 1])))
        params.debug = debug

        _debug(visual=pseudo_rgb,
               filename=os.path.join(params.debug_outdir, str(params.device) + '_masked.png'))
    else:
        _debug(visual=array_data,
               filename=os.path.join(params.debug_outdir, str(params.device) + '_masked.png'))

    return array_data
