# Sobel filtering

import cv2
from . import print_image
from . import plot_image


def sobel_filter(img, dx, dy, k, scale, device, debug=None):
    """This is a filtering method used to identify and highlight gradient edges/features using the 1st derivative.
       Typically used to identify gradients along the x-axis (dx = 1, dy = 0) and y-axis (dx = 0, dy = 1) independently.
       Performance is quite similar to Scharr filter. Used to detect edges / changes in pixel intensity. ddepth = -1
       specifies that the dimensions of output image will be the same as the input image.

    Inputs:
    # img    = image
    # dx     = derivative of x to analyze (1-3)
    # dy     = derivative of x to analyze (1-3)
    # k      = specifies the size of the kernel (must be an odd integer: 1,3,5...)
    # scale  = scaling factor applied (multiplied) to computed Sobel values (scale = 1 is unscaled)
    # device = device number. Used to count steps in the pipeline
    # debug  = None, print, or plot. Print = save to file, Plot = print to screen.

    Returns:
    device   = device number
    sb_img   = Sobel filtered image

    :param img: numpy array
    :param dx: int
    :param dy: int
    :param k: int
    :param scale: int
    :param device: int
    :param debug: str
    :return device: int
    :return sb_img: numpy array
    """

    sb_img = cv2.Sobel(src=img, ddepth=-1, dx=dx, dy=dy, ksize=k)
    device += 1
    if debug is 'print':
        print_image(sb_img, str(device) + '_sb_img' + '_dx_' + str(dx) + '_dy_' + str(dy) + '_k_' + str(k) + '.png')
    elif debug is 'plot':
        plot_image(sb_img, cmap='gray')
    return device, sb_img
