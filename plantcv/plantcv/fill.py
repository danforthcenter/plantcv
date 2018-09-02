# Object fill device

import numpy as np
import cv2
import os
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params


def fill(bin_img, size):
    """Identifies objects and fills objects that are less than size.

    Inputs:
    bin_img      = Binary image data
    size         = minimum object area size in pixels (integer)


    Returns:
    filtered_img = image with objects filled

    :param bin_img: numpy.ndarray
    :param size: int
    :return filtered_img: numpy.ndarray
    """
    params.device += 1

    # Make sure the image is binary
    if len(np.shape(bin_img)) != 2 or len(np.unique(bin_img)) != 2:
        fatal_error("Image is not binary")

    # Find contours
    contours, hierarchy = cv2.findContours(np.copy(bin_img), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]

    # Make a copy of the binary image for returning
    filtered_img = np.copy(bin_img)

    # Loop through contours, fill contours less than or equal to size in area
    for c, cnt in enumerate(contours):
        # if hierarchy[0][c][0]==-1:
        m = cv2.moments(cnt)
        area = m['m00']
        if area <= size:
            # cv2.fillPoly(img, pts = cnt, color=(0,0,0))
            cv2.drawContours(filtered_img, contours, c, (0, 0, 0), -1, lineType=8, hierarchy=hierarchy)

    if params.debug == 'print':
        print_image(filtered_img, os.path.join(params.debug_outdir, str(params.device) + '_fill' + str(size) + '.png'))
    elif params.debug == 'plot':
        plot_image(filtered_img, cmap='gray')

    return filtered_img
