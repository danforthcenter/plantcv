# Rescale grayscale images to user defined range

import os
import numpy as np
from plantcv.plantcv import fatal_error
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import params


def rescale(gray_img, min_value=0, max_value=255):
    """Rescale image.

        Inputs:
        gray_img  = Grayscale image data
        min_value = (optional) new minimum value for range of interest. default = 0
        max_value = (optional) new maximum value for range of interest. default = 255

        Returns:
        rescaled_img = rescaled image

        :param gray_img: numpy.ndarray
        :param min_value: int
        :param max_value: int
        :return c: numpy.ndarray
        """
    if len(np.shape(gray_img)) != 2:
        fatal_error("Image is not grayscale")

    rescaled_img = np.interp(gray_img, (np.nanmin(gray_img), np.nanmax(gray_img)), (min_value, max_value))
    rescaled_img = (rescaled_img).astype('uint8')

    # Autoincrement the device counter
    params.device += 1

    if params.debug == 'print':
        print_image(rescaled_img, os.path.join(params.debug_outdir, str(params.device) + "_rescaled.png"))
    elif params.debug == 'plot':
        plot_image(rescaled_img, cmap='gray')

    return rescaled_img
