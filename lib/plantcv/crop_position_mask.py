# Crop position mask

import cv2
import numpy as np
import math
from . import print_image
from . import plot_image
from . import fatal_error


def crop_position_mask(img, mask, device, x, y, v_pos, h_pos="right", debug=None):
    """Crop position mask

    Inputs:
    img     = image to mask
    mask    = mask to use (must be correct size, if, not use make_resize_mask function)
    x       = x position
    y       = y position
    v_pos   = push from "top" or "bottom"
    h_pos   = push to "right" or "left"
    device  = device counter
    debug   = None, print, or plot. Print = save to file, Plot = print to screen.

    Returns:
    device  = device number
    newmask = image mask

    :param img: numpy array
    :param mask: numpy array
    :param device: int
    :param x: int
    :param y: int
    :param v_pos: str
    :param h_pos: str
    :param debug: str
    :return device: int
    :return newmask: numpy array
    """

    ori_mask = np.copy(mask)

    device += 1

    if x < 0 or y < 0:
        fatal_error("x and y cannot be negative numbers or non-integers")

    # subtract 1 from x and y since python counts start from 0
    if y != 0:
        y = y - 1
    if x != 0:
        x = x - 1

    if len(np.shape(img)) == 3:
        ix, iy, iz = np.shape(img)
        ori_img = np.copy(img)
    else:
        ix, iy = np.shape(img)
        ori_img = np.dstack((img, img, img))

    if len(np.shape(mask)) == 3:
        mx, my, mz = np.shape(mask)
    else:
        mx, my = np.shape(mask)

    npimg = np.zeros((ix, iy), dtype=np.uint8)

    if v_pos == "top":
        # Add rows to the top
        top = np.zeros((x, my), dtype=np.uint8)
        maskv = np.vstack((top, mask))

        if len(np.shape(maskv)) == 3:
            mx, my, mz = np.shape(maskv)
        else:
            mx, my = np.shape(maskv)

        if mx >= ix:
            maskv = maskv[0:ix, 0:my]

        if mx < ix:
            r = ix - mx
            if r % 2 == 0:
                r1 = int(r / 2.0)
                rows1 = np.zeros((r1, my), dtype=np.uint8)
                maskv = np.vstack((rows1, maskv, rows1))
            else:
                r1 = int(math.ceil(r / 2.0))
                r2 = r1 - 1
                rows1 = np.zeros((r1, my), dtype=np.uint8)
                rows2 = np.zeros((r2, my), dtype=np.uint8)
                maskv = np.vstack((rows1, maskv, rows2))
        if debug == 'print':
            print_image(maskv, (str(device) + "_push-top_.png"))
        elif debug == 'plot':
            plot_image(maskv)

    if v_pos == "bottom":
        # Add rows to the bottom
        bottom = np.zeros((x, my), dtype=np.uint8)
        maskv = np.vstack((mask, bottom))
        # print_image(maskv,(str(device)+"_push-bottom-test.png"))

        if len(np.shape(maskv)) == 3:
            mx, my, mz = np.shape(maskv)
        else:
            mx, my = np.shape(maskv)

        if mx >= ix:
            maskdiff = mx - ix
            maskv = maskv[maskdiff:mx, 0:my]
            # print_image(maskv,(str(device)+"_push-bottom-test.png"))

        if mx < ix:
            r = ix - mx
            if r % 2 == 0:
                r1 = int(r / 2.0)
                rows1 = np.zeros((r1, my), dtype=np.uint8)
                maskv = np.vstack((rows1, maskv, rows1))
            else:
                r1 = int(math.ceil(r / 2.0))
                r2 = r1 - 1
                rows1 = np.zeros((r1, my), dtype=np.uint8)
                rows2 = np.zeros((r2, my), dtype=np.uint8)
                maskv = np.vstack((rows1, maskv, rows2))
        if debug == 'print':
            print_image(maskv, (str(device) + "_push-bottom.png"))
        elif debug == 'plot':
            plot_image(maskv)

    if h_pos == "left":
        if len(np.shape(maskv)) == 3:
            mx, my, mz = np.shape(maskv)
        else:
            mx, my = np.shape(maskv)

        # Add rows to the left
        left = np.zeros((mx, y), dtype=np.uint8)
        maskv = np.hstack((left, maskv))

        if len(np.shape(maskv)) == 3:
            mx, my, mz = np.shape(maskv)
        else:
            mx, my = np.shape(maskv)

        if my >= iy:
            maskv = maskv[0:mx, 0:iy]

        if my < iy:
            c = iy - my
            if c % 2 == 0:
                c1 = int(c / 2.0)
                col = np.zeros((mx, c1), dtype=np.uint8)
                maskv = np.hstack((col, maskv, col))
            else:
                c1 = int(math.ceil(c / 2.0))
                c2 = c1 - 1
                col1 = np.zeros((mx, c1), dtype=np.uint8)
                col2 = np.zeros((mx, c2), dtype=np.uint8)
                maskv = np.hstack((col1, maskv, col2))
        if debug == 'print':
            print_image(maskv, (str(device) + "_push-left.png"))
        elif debug == 'plot':
            plot_image(maskv)

    if h_pos == "right":
        if len(np.shape(maskv)) == 3:
            mx, my, mz = np.shape(maskv)
        else:
            mx, my = np.shape(maskv)

        # Add rows to the left
        right = np.zeros((mx, y), dtype=np.uint8)
        maskv = np.hstack((maskv, right))

        if len(np.shape(maskv)) == 3:
            mx, my, mz = np.shape(maskv)
        else:
            mx, my = np.shape(maskv)

        if my >= iy:
            ex = my - iy
            maskv = maskv[0:mx, ex:my]

        if my < iy:
            c = iy - my
            if c % 2 == 0:
                c1 = int(c / 2.0)
                col = np.zeros((mx, c1), dtype=np.uint8)
                maskv = np.hstack((col, maskv, col))
            else:
                c1 = int(math.ceil(c / 2.0))
                c2 = c1 - 1
                col1 = np.zeros((mx, c1), dtype=np.uint8)
                col2 = np.zeros((mx, c2), dtype=np.uint8)
                maskv = np.hstack((col1, maskv, col2))
        if debug == 'print':
            print_image(maskv, (str(device) + "_push-right.png"))
        elif debug == 'plot':
            plot_image(maskv)

    newmask = np.array(maskv)
    if debug is not None:
        if debug == 'print':
            print_image(newmask, (str(device) + "_newmask.png"))
        elif debug == 'plot':
            plot_image(newmask, cmap='gray')
        objects, hierarchy = cv2.findContours(newmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        for i, cnt in enumerate(objects):
            cv2.drawContours(ori_img, objects, i, (255, 102, 255), -1, lineType=8, hierarchy=hierarchy)
        if debug == 'print':
            print_image(ori_img, (str(device) + '_mask_overlay.png'))
        elif debug == 'plot':
            plot_image(ori_img)

    return device, newmask
