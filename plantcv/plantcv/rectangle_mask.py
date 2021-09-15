# Make masking rectangle

import cv2
import numpy as np
import os
from plantcv.plantcv import fatal_error
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import params


def rectangle_mask(img, p1, p2, color="black"):
    """
    Takes an input image and returns a binary image masked by a rectangular area denoted by p1 and p2. Note that
       p1 = (0,0) is the top left hand corner bottom right hand corner is p2 = (max-value(x), max-value(y)).

    Inputs:
    img       = RGB or grayscale image data
    p1        = point 1
    p2        = point 2
    color     = black,white, or gray

    Returns:
    masked    = original image with masked image
    bnk       = binary image
    contour   = object contour vertices
    hierarchy = contour hierarchy list

    :param img: numpy.ndarray
    :param p1: tuple
    :param p2: tuple
    :param color: str
    :return masked:numpy.ndarray
    :return bnk: numpy.ndarray
    :return contour: list
    :return hierarchy: list
    """

    # get the dimensions of the input image
    if len(np.shape(img)) == 3:
        ix, iy, iz = np.shape(img)
    else:
        ix, iy = np.shape(img)
        
    # create a blank image of same size
    bnk = np.zeros((ix, iy), dtype=np.uint8)
    img1 = np.copy(img)
    # draw a rectangle denoted by pt1 and pt2 on the blank image

    cv2.rectangle(img=bnk, pt1=p1, pt2=p2, color=(255, 255, 255), thickness=-1)
    ret, bnk = cv2.threshold(bnk, 127, 255, 0)
    contour, hierarchy = cv2.findContours(bnk, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
    # make sure entire rectangle is within (visable within) plotting region or else it will not fill with
    # thickness = -1. Note that you should only print the first contour (contour[0]) if you want to fill with
    # thickness = -1. otherwise two rectangles will be drawn and the space between them will get filled

    if color.upper() == "WHITE":
        cv2.drawContours(bnk, contour, 0, (255, 255, 255), -1)
        cv2.drawContours(img1, contour, 0, (255, 255, 255), -1)
    elif color.upper() == "BLACK":
        bnk += 255
        cv2.drawContours(bnk, contour, 0, (0, 0, 0), -1)
        cv2.drawContours(img1, contour, 0, (0, 0, 0), -1)
    elif color.upper() == "GRAY" or color.upper() == "GREY":
        cv2.drawContours(bnk, contour, 0, (192, 192, 192), -1)
        cv2.drawContours(img1, contour, 0, (192, 192, 192), -1)
    else:
        fatal_error(str(color) + " is not a valid color, must be 'white', 'black', or 'gray'.")

    _debug(visual=bnk,
           filename=os.path.join(params.debug_outdir, str(params.device) + '_rectroi.png'))
    _debug(visual=img1,
           filename=os.path.join(params.debug_outdir, str(params.device) + '_rectmask.png'),
           cmap='gray')

    return img1, bnk, contour, hierarchy
