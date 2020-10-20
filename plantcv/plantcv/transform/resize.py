# Resize image

import cv2
import os
import numpy as np
import copy
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params

def _set_interpolation(**kw):
    if ("size_old" in kw) and ("size" in kw):
        old_area = kw["size_old"][0] * kw["size_old"][1]
        new_area = kw["size"][0] * kw["size"][1]
        if new_area >= old_area:
            interp_mtd = cv2.INTER_CUBIC
        else:
            interp_mtd = cv2.INTER_AREA
    elif ("factor_x" in kw) and ("factor_y" in kw):
        if kw["factor_x"] * kw["factor_y"] >=1:
            interp_mtd = cv2.INTER_CUBIC
        else:
            interp_mtd = cv2.INTER_AREA
    return interp_mtd

def resize(img, size, interpolation=True, **kw):
    """
    Resize input image to a desired new size
    By default, the resizing is done by interpolation
    If interpolation is False, the resizing is done by either cropping or padding (zero-padding by default now)
    :param img: (numpy.ndarray) grayscale image or RGB image
    :param size: (tuple) (Width, Height), equilvalent to (num_cols, num_rols)
    :param interpolation: (bool) By default Ture
    :return: resized image
    """

    params.device += 1
    if interpolation:
        if "interp_mtd" in kw:
            interp_mtd = kw["interp_mtd"]
        else:
            interp_mtd = _set_interpolation(size_old=img.shape, size=size)
        resized_im = cv2.resize(img, dsize=size, interpolation=interp_mtd)

    else:
        # original image size
        r_ori, c_ori = img.shape[0], img.shape[1]
        # desired image size
        r, c = size[1], size[0]

        # check whether the input image is RGB or binary
        if len(img.shape) > 2:
            b = np.shape(img)[2]
            img = copy.deepcopy(img)
        else:
            b = 1
            img = np.expand_dims(img, axis=2)

        dt_r = r - r_ori
        dt_c = c - c_ori

        top = int(abs(dt_r) / 2)
        bot = abs(dt_r) - top
        left = int(abs(dt_c) / 2)
        right = abs(dt_c) - left

        temp_im = copy.deepcopy(img)
        if dt_r <= 0:
            temp_im = temp_im[top:top + r:, :, :]
            top = 0
            bot = 0
        if dt_c <= 0:
            temp_im = temp_im[:, left:left + c, :]
            left = 0
            right = 0

        resized_im = np.array(
            [np.pad(temp_im[:, :, ib], ((top, bot), (left, right)), 'constant') for ib in range(0, b)])
        resized_im = np.transpose(resized_im, (1, 2, 0))
        if b == 1:
            resized_im = np.squeeze(resized_im, axis=2)

    if params.debug == 'print':
        print_image(resized_im, os.path.join(params.debug_outdir, str(params.device) + "_resize.png"))
    elif params.debug == 'plot':
        plot_image(resized_im)

    return resized_im

def resize_factor(img, factor_x, factor_y, **kw):
    """
    Resize input image to a new size using resize factors along x and y axes
    :param img: (numpy.ndarray) grayscale image or RGB image
    :param factor_x: (float) resizing factor along x axis (width)
    :param factor_y: float) resizing factor along y axis (height)
    :return: resized image
    """

    params.device += 1

    if factor_x <= 0 or factor_y <= 0:
        fatal_error("Resize values both cannot be 0 or negative values!")

    if "interp_mtd" in kw:
        interp_mtd = kw["interp_mtd"]
    else:
        interp_mtd = _set_interpolation(factor_x=factor_x, factor_y=factor_y)

    resized_im = cv2.resize(img, (0, 0), fx=factor_x, fy=factor_y, interpolation=interp_mtd)

    if params.debug == 'print':
        print_image(resized_im, os.path.join(params.debug_outdir, str(params.device) + "_resize.png"))
    elif params.debug == 'plot':
        plot_image(resized_im)

    return resized_im
