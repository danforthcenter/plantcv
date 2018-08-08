# Object fill device

import numpy as np
import cv2
import os
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params


def fill(img, mask, size):
    """Identifies objects and fills objects that are less than size.

    Inputs:
    img    = image object, grayscale. img will be returned after filling
    mask   = image object, grayscale. This image will be used to identify contours
    size   = minimum object area size in pixels (integer)


    Returns:
    device = device number
    img    = image with objects filled

    :param img: numpy array
    :param mask: numpy array
    :param size: int
    :return img: numpy array
    """

    params.device += 1

    if len(np.shape(img)) >= 3:
        fatal_error("Image is not binary")
    else:
        ix, iy = np.shape(img)

    # Find contours
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]

    # Loop through contours, fill contours less than or equal to size in area
    for c, cnt in enumerate(contours):
        # if hierarchy[0][c][0]==-1:
        m = cv2.moments(cnt)
        area = m['m00']
        if area <= size:
            # cv2.fillPoly(img, pts = cnt, color=(0,0,0))
            cv2.drawContours(img, contours, c, (0, 0, 0), -1, lineType=8, hierarchy=hierarchy)

    if params.debug == 'print':
        print_image(img, os.path.join(params.debug_outdir, str(params.device) + '_fill' + str(size) + '.png'))
    elif params.debug == 'plot':
        plot_image(img, cmap='gray')

    return img
