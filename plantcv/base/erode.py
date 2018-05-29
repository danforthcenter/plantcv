# Erosion filter

import cv2
import numpy as np
from plantcv.base import print_image
from plantcv.base import plot_image


def erode(img, kernel, i, device, debug=None):
    """Perform morphological 'erosion' filtering. Keeps pixel in center of the kernel if conditions set in kernel are
       true, otherwise removes pixel.

    Inputs:
    img    = input image
    kernel = filtering window, you'll need to make your own using as such:
             kernal = np.zeros((x,y), dtype=np.uint8), then fill the kernal with appropriate values
    i      = interations, i.e. number of consecutive filtering passes
    device = device number. Used to count steps in the pipeline
    debug  = None, print, or plot. Print = save to file, Plot = print to screen.

    Returns:
    device = device number
    er_img = eroded image

    :param img: numpy array
    :param kernel: numpy array
    :param i: int
    :param device: int
    :param debug: str
    :return device: int
    :return er_img: numpy array
    """

    kernel1 = int(kernel)
    kernel2 = np.ones((kernel1, kernel1), np.uint8)
    er_img = cv2.erode(src=img, kernel=kernel2, iterations=i)
    device += 1
    if debug == 'print':
        print_image(er_img, str(device) + '_er_image_' + 'itr_' + str(i) + '.png')
    elif debug == 'plot':
        plot_image(er_img, cmap='gray')
    return device, er_img
