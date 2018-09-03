# Resize image

import cv2
import os
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params


def resize(img, resize_x, resize_y):
    """Resize image.

    Inputs:
    img      = RGB or grayscale image data to resize
    resize_x = scaling factor
    resize_y = scaling factor

    Returns:
    reimg    = resized image

    :param img: numpy.ndarray
    :param resize_x: int
    :param resize_y: int
    :return reimg: numpy.ndarray
    """

    params.device += 1

    if resize_x <= 0 and resize_y <= 0:
        fatal_error("Resize values both cannot be 0 or negative values!")

    reimg = cv2.resize(img, (0, 0), fx=resize_x, fy=resize_y)

    if params.debug == 'print':
        print_image(reimg, os.path.join(params.debug_outdir, str(params.device) + "_resize1.png"))
    elif params.debug == 'plot':
        plot_image(reimg)

    return reimg
