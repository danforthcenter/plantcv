# Binary image threshold device

import cv2
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params

def binary_threshold(img, threshold, maxValue, object_type):
    """Creates a binary image from a gray image based on the threshold value.

    Inputs:
    img         = img object, grayscale
    threshold   = threshold value (0-255)
    maxValue    = value to apply above threshold (usually 255 = white)
    object_type = light or dark
                  - If object is light then standard thresholding is done
                  - If object is dark then inverse thresholding is done

    Returns:
    t_img       = thresholded image

    :param img: numpy array
    :param threshold: int
    :param maxValue: int
    :param object_type: str
    :return t_img: numpy array
    """

    params.device += 1
    if object_type == 'light':
        ret, t_img = cv2.threshold(img, threshold, maxValue, cv2.THRESH_BINARY)
        if params.debug == 'print':
            print_image(t_img, os.path.join(params.debug_outdir, str(params.device) + '_binary_threshold' + str(threshold) + '.png'))
        elif params.debug == 'plot':
            plot_image(t_img, cmap='gray')
        return t_img
    elif object_type == 'dark':
        ret, t_img = cv2.threshold(img, threshold, maxValue, cv2.THRESH_BINARY_INV)
        if params.debug == 'print':
            print_image(t_img, os.path.join(params.debug_outdir, str(params.device) + '_binary_threshold' + str(threshold) + '_inv.png'))
        elif params.debug == 'plot':
            plot_image(t_img, cmap='gray')
        return t_img
    else:
        fatal_error('Object type ' + str(object_type) + ' is not "light" or "dark"!')
