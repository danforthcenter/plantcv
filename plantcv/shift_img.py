# Crop position mask

import cv2
import numpy as np
import math
from . import print_image
from . import plot_image
from . import fatal_error


def shift_img(img, device, number, side="right", debug=None):
    """this function allows you to shift an image over without changing dimensions

    Inputs:
    img     = image to mask
    number  = number of rows or colums to add
    side   = "top", "bottom", "right", "left" where to add the rows or columns to
    device  = device counter
    debug   = None, print, or plot. Print = save to file, Plot = print to screen.

    Returns:
    device  = device number
    newmask = image mask

    :param img: numpy array
    :param device: int
    :param number: int
    :param side: str
    :param debug: str
    :return newmask: numpy array
    """
    device += 1

    number=number-1

    if number < 0:
        fatal_error("x and y cannot be negative numbers or non-integers")

    ## get the sizes of the images

    if len(np.shape(img)) == 3:
        ix, iy, iz = np.shape(img)
        ori_img = np.copy(img)
    else:
        ix, iy = np.shape(img)
        ori_img = np.dstack((img, img, img))


    if side == "top":
        top=np.zeros((number,iy,3),dtype=np.uint8)
        adjust=ix-number
        adjusted_img = np.vstack((top, ori_img[0:adjust,0:]))

    if side=='bottom':
        bottom=np.zeros((number,iy,3),dtype=np.uint8)
        adjusted_img=np.vstack((ori_img[number:,0:],bottom))

    if side=='right':
        right=np.zeros((ix,number,3),dtype=np.uint8)
        adjusted_img=np.hstack((ori_img[0:,number:],right))
    if side=='left':
        left=np.zeros((ix,number,3),dtype=np.uint8)
        adjust=iy-number
        adjusted_img=np.hstack((left,ori_img[0:,0:adjust]))


    if len(np.shape(img))==2:
        adjusted_img, channel2, channel3=np.dsplit(adjusted_img,3)
    if debug == 'print':
        print_image(adjusted_img, (str(device) + "_shifted img.png"))
    elif debug == 'plot':
        if len(np.shape(adjusted_img))==3:
            plot_image(adjusted_img)
        else:
            plot_image(adjusted_img,cmap='gray')


    return device, adjusted_img
