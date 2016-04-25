# Dilation filter

import cv2
import numpy as np
from . import print_image
from . import plot_image


def dilate(img, kernel, i, device, debug=None):
    """Performs morphological 'dilation' filtering. Adds pixel to center of kernel if conditions set in kernel are true.

    Inputs:
    img     = input image
    kernel  = filtering window, you'll need to make your own using as such:
              kernal = np.zeros((x,y), dtype=np.uint8), then fill the kernal with appropriate values
    i       = interations, i.e. number of consecutive filtering passes
    device  = device number. Used to count steps in the pipeline
    debug   = None, print, or plot. Print = save to file, Plot = print to screen.

    Returns:
    device  = device number
    dil_img = dilated image

    :param img: numpy array
    :param kernel: numpy array
    :param i: int
    :param device: int
    :param debug: str
    :return device: int
    :return dil_img: numpy array
    """

    kernel1=int(kernel)
    kernel2 = np.ones((kernel1,kernel1),np.uint8)
    dil_img = cv2.dilate(src = img, kernel = kernel2, iterations = i)
    device += 1
    if debug is 'print':
        print_image(dil_img, str(device) + '_dil_image_' + 'itr_' + str(i) + '.png')
    elif debug is 'plot':
        plot_image(dil_img, cmap='gray')
    return device, dil_img
