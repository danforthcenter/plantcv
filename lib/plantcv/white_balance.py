# White Balance correction function

import cv2
import numpy as np
from . import print_image
from . import plot_image


def white_balance(img, device, roi=None, debug=None):

    """Corrects the exposure of an image based on its histogram.
    Inputs:
    img - A grayscale image on which to perform the correction
    device  - device number. Used to count steps in the pipeline
    roi - A list of 4 points (x, y, width, height) that form the rectangular ROI of the white color standard.
            If a list of 4 points is not given, whole image will be used.
    debug - None, print, or plot. Print = save to file, Plot = print to screen.


    Returns:
    img - Image after exposure correction
    """
    # Finds histogram of roi if valid roi is given. Otherwise, finds histogram of entire image
    if roi is not None and len(roi) == 4:
        hist = cv2.calcHist(tuple(img[roi[1]:roi[1]+roi[3], roi[0]:roi[0]+roi[2]]), [0], None, [256], [0, 256])
    else:
        hist = cv2.calcHist(tuple(img), [0], None, [256], [0, 256])  # Creates histogram of original image

    # Calculates index of maximum of histogram and finds alpha based on the peak
    hmax = np.argmax(hist)
    alpha = 255 / float(hmax)

    # Converts values greater than hmax to 255 and scales all others by alpha
    img = np.asarray(np.where(img <= hmax, np.multiply(alpha, img), 255), np.uint8)
    device += 1
    if debug == 'print':
        print_image(img, str(device) + '_corrected_img' + '.png')
    elif debug == 'plot':
        plot_image(img, cmap='gray')
    return img, device
