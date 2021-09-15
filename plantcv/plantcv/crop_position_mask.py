# Crop position mask

import cv2
import numpy as np
import math
import os
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params


def crop_position_mask(img, mask, x, y, v_pos="top", h_pos="right"):
    """Crop position mask

    Inputs:
    img     = RGB or grayscale image data for plotting
    mask    = Binary mask to use (must be correct size, if, not use make_resize_mask function)
    x       = x position
    y       = y position
    v_pos   = push from "top" or "bottom"
    h_pos   = push to "right" or "left"

    Returns:
    newmask = image mask

    :param img: numpy.ndarray
    :param mask: numpy.ndarray
    :param x: int
    :param y: int
    :param v_pos: str
    :param h_pos: str
    :return newmask: numpy.ndarray
    """

    if x < 0 or y < 0:
        fatal_error("x and y cannot be negative numbers or non-integers")

    # get the sizes of the images
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
        mask = mask[0]
    else:
        mx, my = np.shape(mask)

    # resize the images so they are equal in size and centered
    if mx >= ix:
        r = mx - ix
        if r % 2 == 0:
            r1 = int(np.rint(r / 2.0))
            r2 = r1
        else:
            r1 = int(np.rint(r / 2.0))
            r2 = r1 - 1
        mask = mask[r1:mx - r2, 0:my]
    if my >= iy:
        r = my - iy
        if r % 2 == 0:
            r1 = int(np.rint(r / 2.0))
            r2 = r1
        else:
            r1 = int(np.rint(r / 2.0))
            r2 = r1 - 1
        mask = mask[0:mx, r1:my - r2]

    # New mask shape
    mx, my = np.shape(mask)

    if v_pos.upper() == "TOP":
        # Add rows to the top
        top = np.zeros((x, my), dtype=np.uint8)

        maskv = np.vstack((top, mask))

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
        _debug(visual=maskv,
               filename=os.path.join(params.debug_outdir, str(params.device) + "_push-top.png"),
               cmap='gray')

    elif v_pos.upper() == "BOTTOM":
        # Add rows to the bottom
        bottom = np.zeros((x, my), dtype=np.uint8)

        maskv = np.vstack((mask, bottom))

        mx, my = np.shape(maskv)

        if mx >= ix:
            maskdiff = mx - ix
            maskv = maskv[maskdiff:mx, 0:my]

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

        _debug(visual=maskv,
               filename=os.path.join(params.debug_outdir, str(params.device) + "_push-bottom.png"),
               cmap='gray')

    else:
        fatal_error(str(v_pos) + ' is not valid, must be "top" or "bottom"!')

    if h_pos.upper() == "LEFT":

        mx, my = np.shape(maskv)

        # Add rows to the left
        left = np.zeros((mx, y), dtype=np.uint8)
        maskv = np.hstack((left, maskv))

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

        _debug(visual=maskv,
               filename=os.path.join(params.debug_outdir, str(params.device) + "_push-left.png"),
               cmap='gray')

    elif h_pos.upper() == "RIGHT":

        mx, my = np.shape(maskv)

        # Add rows to the left
        right = np.zeros((mx, y), dtype=np.uint8)
        maskv = np.hstack((maskv, right))

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

        _debug(visual=maskv,
               filename=os.path.join(params.debug_outdir, str(params.device) + "_push-right.png"),
               cmap='gray')

    else:
        fatal_error(str(h_pos) + ' is not valid, must be "left" or "right"!')

    newmask = np.array(maskv)
    if params.debug is not None:
        _debug(visual=newmask,
               filename=os.path.join(params.debug_outdir, str(params.device) + "_newmask.png"),
               cmap='gray')

        objects, hierarchy = cv2.findContours(np.copy(newmask), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
        for i, cnt in enumerate(objects):
            cv2.drawContours(ori_img, objects, i, (255, 102, 255), -1, lineType=8, hierarchy=hierarchy)
        _debug(visual=ori_img,
               filename=os.path.join(params.debug_outdir, str(params.device) + '_mask_overlay.png'))

    return newmask
