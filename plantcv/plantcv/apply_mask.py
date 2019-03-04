# Apply White or Black Background Mask

import os
import cv2
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
    if mask_color.upper() == 'WHITE':
        # Mask image
        masked_img = cv2.bitwise_and(rgb_img, rgb_img, mask=mask)
        # Create inverted mask for background
        mask_inv = cv2.bitwise_not(mask)
        # Invert the background so that it is white, but apply mask_inv so you don't white out the plant
        white_mask = cv2.bitwise_not(masked_img, mask=mask_inv)
        # Add masked image to white background (can't just use mask_inv because that is a binary)
        white_masked = cv2.add(masked_img, white_mask)
        if params.debug == 'print':
            print_image(white_masked, os.path.join(params.debug_outdir, str(params.device) + '_wmasked.png'))
        elif params.debug == 'plot':
            plot_image(white_masked)
        return white_masked
    elif mask_color.upper() == 'BLACK':
        masked_img = cv2.bitwise_and(rgb_img, rgb_img, mask=mask)
        if params.debug == 'print':
            print_image(masked_img, os.path.join(params.debug_outdir, str(params.device) + '_bmasked.png'))
        elif params.debug == 'plot':
            plot_image(masked_img)
        return masked_img
    else:
        fatal_error('Mask Color ' + str(mask_color) + ' is not "white" or "black"!')
