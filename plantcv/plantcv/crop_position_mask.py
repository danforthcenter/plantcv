import cv2
import numpy as np
import math
import os
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _cv2_findcontours, _grayscale_to_rgb
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params


def _check_inputs(x, y, v_pos, h_pos):
    """Helper function to check edge cases"""
    if x < 0 or y < 0:
        fatal_error("x and y cannot be negative numbers or non-integers")

    if v_pos.upper() not in ["TOP", "BOTTOM"]:
        fatal_error(f'{v_pos} is not valid, must be "top" or "bottom"!')

    if h_pos.upper() not in ["LEFT", "RIGHT"]:
        fatal_error(f'{h_pos} is not valid, must be "left" or "right"!')


def _adjust_size(mask, ix, iy):
    """Resize the mask to fit within the image dimensions"""
    mx, my = mask.shape
    if mx >= ix:
        r = mx - ix
        r1 = int(np.rint(r / 2.0))
        r2 = r1 if r % 2 == 0 else r1 - 1
        mask = mask[r1:mx - r2, 0:my]
    if my >= iy:
        r = my - iy
        r1 = int(np.rint(r / 2.0))
        r2 = r1 if r % 2 == 0 else r1 - 1
        mask = mask[0:mx, r1:my - r2]
    return mask


def _add_rows(maskv, ix, my, position):
    """Add rows to the top or bottom"""
    mx, my = maskv.shape
    x = ix - mx
    if x <= 0:
        return maskv[:ix, :my]

    rows1 = np.zeros((x, my), dtype=np.uint8)
    if position == "top":
        maskv = np.vstack((rows1, maskv))
    else:
        maskv = np.vstack((maskv, rows1))

    if maskv.shape[0] > ix:
        return maskv[:ix, :my]
    return _adjust_height(maskv, ix, my)


def _adjust_height(maskv, ix, my):
    """Adjust the height of the mask to match the image dimensions"""
    mx, _ = maskv.shape
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
    return maskv


def _add_columns(maskv, iy, y, position):
    """Add columns to the left or right"""
    mx, _ = maskv.shape
    if position == "left":
        cols = np.zeros((mx, y), dtype=np.uint8)
        maskv = np.hstack((cols, maskv))
    else:
        cols = np.zeros((mx, y), dtype=np.uint8)
        maskv = np.hstack((maskv, cols))

    if maskv.shape[1] > iy:
        return maskv[:, :iy]
    return _adjust_width(maskv, iy, mx)


def _adjust_width(maskv, iy, mx):
    """Adjust the width of the mask to match the image dimensions"""
    _, my = maskv.shape
    c = iy - my
    if c % 2 == 0:
        c1 = int(c / 2.0)
        cols = np.zeros((mx, c1), dtype=np.uint8)
        maskv = np.hstack((cols, maskv, cols))
    else:
        c1 = int(math.ceil(c / 2.0))
        c2 = c1 - 1
        col1 = np.zeros((mx, c1), dtype=np.uint8)
        col2 = np.zeros((mx, c2), dtype=np.uint8)
        maskv = np.hstack((col1, maskv, col2))
    return maskv


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
    _check_inputs(x, y, v_pos, h_pos)

    y = max(y - 1, 0)
    x = max(x - 1, 0)

    ori_img = _grayscale_to_rgb(img)
    ix, iy = img.shape[:2]

    if len(mask.shape) == 3:
        mask = mask[:, :, 0]

    mask = _adjust_size(mask, ix, iy)

    if v_pos.upper() == "TOP":
        maskv = _add_rows(mask, ix, mask.shape[1], "top")
    else:
        maskv = _add_rows(mask, ix, mask.shape[1], "bottom")

    if h_pos.upper() == "LEFT":
        maskv = _add_columns(maskv, iy, y, "left")
    else:
        maskv = _add_columns(maskv, iy, y, "right")

    newmask = np.array(maskv)
    _debug(visual=newmask, filename=os.path.join(params.debug_outdir, str(params.device) + "_newmask.png"), cmap='gray')

    objects, hierarchy = _cv2_findcontours(bin_img=newmask)
    for i, _ in enumerate(objects):
        cv2.drawContours(ori_img, objects, i, (255, 102, 255), -1, lineType=8, hierarchy=hierarchy)
    _debug(visual=ori_img, filename=os.path.join(params.debug_outdir, str(params.device) + '_mask_overlay.png'))

    return newmask
