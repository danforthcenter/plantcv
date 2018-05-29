# Scharr filtering

import cv2
from plantcv.base import print_image
from plantcv.base import plot_image


def scharr_filter(img, dX, dY, scale, device, debug=None):
    """This is a filtering method used to identify and highlight gradient edges/features using the 1st derivative.
       Typically used to identify gradients along the x-axis (dx = 1, dy = 0) and y-axis (dx = 0, dy = 1) independently.
       Performance is quite similar to Sobel filter. Used to detect edges / changes in pixel intensity. ddepth = -1
       specifies that the dimensions of output image will be the same as the input image.

    Inputs:
    # img    = image
    # dx     = derivative of x to analyze (1-3)
    # dy     = derivative of x to analyze (1-3)
    # scale  = scaling factor applied (multiplied) to computed Scharr values (scale = 1 is unscaled)
    # device = device number. Used to count steps in the pipeline
    # debug  = None, print, or plot. Print = save to file, Plot = print to screen.

    Returns:
    device   = device number
    sr_img   = Scharr filtered image

    :param img: numpy array
    :param dX: int
    :param dY: int
    :param scale: int
    :param device: int
    :param debug: str
    :return device: int
    :return sr_img: numpy array
    """

    sr_img = cv2.Scharr(src=img, ddepth=-1, dx=dX, dy=dY, scale=scale)
    device += 1
    if debug == 'print':
        print_image(sr_img,
                    str(device) + '_sr_img_dx' + str(dX) + '_dy' + str(dY) + '_scale' + str(scale) + '.png')
    elif debug == 'plot':
        plot_image(sr_img, cmap='gray')
    return device, sr_img
