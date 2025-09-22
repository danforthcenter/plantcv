# Crop position mask

import cv2
import numpy as np
import math
import os
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _cv2_findcontours, _grayscale_to_rgb
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params


def crop_position_mask(img, mask, x, y, v_pos="top", h_pos="right"):
    """
    Crop a binary mask to a specified position within an image.

    Parameters
    ----------
    img : numpy.ndarray
        RGB or grayscale image data for plotting.
    mask : numpy.ndarray
        Binary mask to use (must be correct size; if not, use make_resize_mask function).
    x : int
        x position for cropping.
    y : int
        y position for cropping.
    v_pos : str, optional
        Vertical position to push from, either "top" or "bottom" (default is "top").
    h_pos : str, optional
        Horizontal position to push to, either "right" or "left" (default is "right").

    Returns
    -------
    newmask : numpy.ndarray
        Cropped image mask.

    Raises
    ------
    ValueError
        If x or y are negative or non-integer values.
    ValueError
        If v_pos or h_pos are not valid options.
    ValueError
        If mask is not a binary image.

    Notes
    -----
    - The function centers and resizes the mask to match the image size.
    - The mask is cropped and positioned according to the specified vertical and horizontal parameters.
    - Debug images are saved if debugging is enabled.
    """
    if not all([x > 0, y > 0]):
        fatal_error("x and y cannot be negative numbers or non-integers")

    if v_pos.upper() not in ["TOP", "BOTTOM"]:
        fatal_error(f'{v_pos} is not valid, must be "top" or "bottom"!')

    if h_pos.upper() not in ["LEFT", "RIGHT"]:
        fatal_error(f'{h_pos} is not valid, must be "left" or "right"!')

    # get the sizes of the images
    # subtract 1 from x and y since python counts start from 0
    if y != 0:
        y = y - 1
    if x != 0:
        x = x - 1
    # Convert grayscale images to color
    ori_img = _grayscale_to_rgb(img)

    # Image shape
    ix, iy = np.shape(ori_img)[0:2]

    # Convert mask to grayscale if needed and get its shape
    if any([len(np.shape(mask)) > 2, len(np.unique(mask)) > 2]):
        fatal_error("Mask should be a binary image")
    mx, my = np.shape(mask)

    # resize the images so they are equal in size and centered
    if mx >= ix:
        r = mx - ix
        r1 = int(np.rint(r / 2.0))
        r2 = _crop_modulo(r1, r)
        mask = mask[r1:mx - r2, 0:my]
    if my >= iy:
        r = my - iy
        r1 = int(np.rint(r / 2.0))
        r2 = _crop_modulo(r1, r)
        mask = mask[0:mx, r1:my - r2]

    # New mask shape
    mx, my = np.shape(mask)
    # make vertical adjustments
    if v_pos.upper() == "TOP":
        maskv = _top_crop_position(x, my, mask, ix)
    elif v_pos.upper() == "BOTTOM":
        maskv = _bottom_crop_position(x, my, mask, ix)
    # make horizontal adjustments
    if h_pos.upper() == "LEFT":
        maskv = _left_crop_position(y, maskv, iy)
    elif h_pos.upper() == "RIGHT":
        maskv = _right_crop_position(y, maskv, iy)

    newmask = np.array(maskv)
    _debug(
        visual=newmask,
        filename=os.path.join(params.debug_outdir, str(params.device) + "_newmask.png"),
        cmap="gray",
    )

    objects, hierarchy = _cv2_findcontours(bin_img=newmask)
    for i, _ in enumerate(objects):
        cv2.drawContours(
            ori_img, objects, i, (255, 102, 255), -1, lineType=8, hierarchy=hierarchy
        )
    _debug(
        visual=ori_img,
        filename=os.path.join(
            params.debug_outdir, str(params.device) + "_mask_overlay.png"
        ),
    )

    return newmask


def _crop_modulo(x1, x):
    """Force a number to make a rectangle slice

    Parameters
    ----------
    x1:       int, half the difference in size between two images
    x:        int, the difference in size between two images

    Returns
    -------
    out:      int, x1 or x1 - 1 depending on if the difference in size is even.
    """
    out = x1 if x % 2 == 0 else x1 - 1
    return out


def _top_crop_position(x, my, mask, ix):
    """Add rows to top of a mask to push it "down" on an image

    Parameters
    ----------
    x:       int, x position.
    my:      int, y-axis shape of image mask
    mask:    numpy.ndarray, binary mask
    ix:      int, x-axis shape of original image

    Returns
    -------
    maskv:   numpy.ndarray, binary mask moved vertically on original image scale.
    """
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
    _debug(
        visual=maskv,
        filename=os.path.join(
            params.debug_outdir, str(params.device) + "_push-top.png"
        ),
        cmap="gray",
    )

    return maskv


def _bottom_crop_position(x, my, mask, ix):
    """Add rows to bottom of a mask to push it "up" on an image

    Parameters
    ----------
    x:       int, x position.
    my:      int, y-axis shape of image mask
    mask:    numpy.ndarray, binary mask
    ix:      int, x-axis shape of original image

    Returns
    -------
    maskv:   numpy.ndarray, binary mask moved vertically on original image scale.
    """
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

    _debug(
        visual=maskv,
        filename=os.path.join(
            params.debug_outdir, str(params.device) + "_push-bottom.png"
        ),
        cmap="gray",
    )

    return maskv


def _left_crop_position(y, mask, iy):
    """Add rows to bottom of a mask to push it "up" on an image

    Parameters
    ----------
    y:        int, y position for left adjustment.
    mask:     numpy.ndarray, binary mask after vertical adjustments.
    iy:       int, y-axis shape of original image.

    Returns
    -------
    maskh:   numpy.ndarray, binary mask moved vertically on original image scale.
    """
    mvx, _ = np.shape(mask)

    # Add rows to the left
    left = np.zeros((mvx, y), dtype=np.uint8)
    maskh = np.hstack((left, mask))

    mx, my = np.shape(maskh)

    if my >= iy:
        maskh = maskh[0:mx, 0:iy]
    if my < iy:
        c = iy - my
        if c % 2 == 0:
            c1 = int(c / 2.0)
            col = np.zeros((mx, c1), dtype=np.uint8)
            maskh = np.hstack((col, maskh, col))
        else:
            c1 = int(math.ceil(c / 2.0))
            c2 = c1 - 1
            col1 = np.zeros((mx, c1), dtype=np.uint8)
            col2 = np.zeros((mx, c2), dtype=np.uint8)
            maskh = np.hstack((col1, maskh, col2))

    _debug(
        visual=maskh,
        filename=os.path.join(
            params.debug_outdir, str(params.device) + "_push-left.png"
        ),
        cmap="gray",
    )

    return maskh


def _right_crop_position(y, mask, iy):
    """Add rows to bottom of a mask to push it "up" on an image

    Parameters
    ----------
    y:        int, y position for left adjustment.
    mask:     numpy.ndarray, binary mask after vertical adjustments.
    iy:       int, y-axis shape of original image.

    Returns
    -------
    maskh:   numpy.ndarray, binary mask moved vertically on original image scale.
    """
    mvx, _ = np.shape(mask)

    # Add rows to the left
    right = np.zeros((mvx, y), dtype=np.uint8)
    maskh = np.hstack((mask, right))

    mx, my = np.shape(maskh)

    if my >= iy:
        ex = my - iy
        maskh = maskh[0:mx, ex:my]

    if my < iy:
        c = iy - my
        if c % 2 == 0:
            c1 = int(c / 2.0)
            col = np.zeros((mx, c1), dtype=np.uint8)
            maskh = np.hstack((col, maskh, col))
        else:
            c1 = int(math.ceil(c / 2.0))
            c2 = c1 - 1
            col1 = np.zeros((mx, c1), dtype=np.uint8)
            col2 = np.zeros((mx, c2), dtype=np.uint8)
            maskh = np.hstack((col1, maskh, col2))

    _debug(
        visual=maskh,
        filename=os.path.join(
            params.debug_outdir, str(params.device) + "_push-right.png"
        ),
        cmap="gray",
    )

    return maskh
