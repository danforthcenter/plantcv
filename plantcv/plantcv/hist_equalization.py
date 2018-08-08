# Histogram equalization

import cv2
import numpy as np
import os
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params

def hist_equalization(img):
    """Histogram equalization is a method to normalize the distribution of intensity values. If the image has low
       contrast it will make it easier to threshold.

    Inputs:
    img    = input image

    Returns:
    img_eh = normalized image

    :param img: numpy array
    :return img_eh: numpy array
    """

    if len(np.shape(img)) == 3:
        fatal_error("Input image must be gray")

    img_eh = cv2.equalizeHist(img)
    params.device += 1
    if params.debug == 'print':
        print_image(img_eh, os.path.join(params.debug_outdir, str(params.device) + '_hist_equal_img.png'))
    elif params.debug == 'plot':
        plot_image(img_eh, cmap='gray')

    return img_eh
