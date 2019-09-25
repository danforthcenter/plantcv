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

    # Make a copy since we will directly mask the array
    array_data = array.copy()
    # Mask the array
    array_data[np.where(mask == 0)] = 0

    # Take 3 wavelengths, first, middle and last available wavelength
    num_bands = np.shape(array)[2]
    med_band = int(num_bands / 2)
    pseudo_rgb = cv2.merge((array_data[:, :, [0]],
                            array_data[:, :, [med_band]],
                            array_data[:, :, [num_bands]]))

        # Gamma correct pseudo_rgb image
    pseudo_rgb = pseudo_rgb ** (1 / 2.2)

    if params.debug == "plot":
        # Gamma correct pseudo_rgb image
        plot_image(pseudo_rgb)
    elif params.debug == "print":
        print_image(pseudo_rgb, os.path.join(params.debug_outdir, str(params.device) + "_masked_spectral.png"))

    return array_data
