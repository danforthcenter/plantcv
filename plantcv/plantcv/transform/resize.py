# Resize image

import cv2
import os
import numpy as np
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params


def _set_interpolation(input_size, output_size, method):
    """Set the image resizing interpolation method.

    Inputs:
    input_size  = the absolute or relative size of the input image (x, y)
    output_size = the absolute or relative size of the output image (x, y)
    method      = interpolation method:
                      "auto" = select method automatically
                      "area" = resampling using pixel area (OpenCV INTER_AREA)
                      "bicubic" = bicubic interpolation (OpenCV INTER_CUBIC)
                      "bilinear" = bilinear interpolation (OpenCV INTER_LINEAR)
                      "lanczos" = Lanczos interpolation (OpenCV INTER_LANCZOS4)
                      "nearest" = nearest-neighbor interpolation (OpenCV INTER_NEAREST)

    Returns:
    interp_mtd  = OpenCV interpolation method ID
    :param input_size: tuple
    :param output_size: tuple
    :param method: str
    :return interp_mtd: int
    """
    # Method lookup dictionary
    methods = {
        "auto": cv2.INTER_AREA,
        "area": cv2.INTER_AREA,
        "bicubic": cv2.INTER_CUBIC,
        "bilinear": cv2.INTER_LINEAR,
        "lanczos": cv2.INTER_LANCZOS4,
        "nearest": cv2.INTER_NEAREST
    }
    # Normalize input method
    method = method.lower()
    # If input method is not in the supported methods, end the program
    if method not in methods:
        fatal_error(f"Interpolation method {method} is not supported, see the documentation for more details.")
    # Calculate the input image pixel area
    input_area = input_size[0] * input_size[1]
    # Calculate the output image pixel area
    output_area = output_size[0] * output_size[1]
    # Set the interpolation method
    interp_mtd = methods.get(method)
    # If the requested method is "auto" and the output image is larger than the input
    # Set the interpolation method to "cubic"
    if method == "auto" and output_area >= input_area:
        interp_mtd = cv2.INTER_CUBIC

    return interp_mtd


def resize(img, size, interpolation="auto"):
    """Resize input image to a desired new size.

    By default, the resizing is done by interpolation. If interpolation is None,
    the resizing is done by either cropping or padding (zero-padding by default now)

    Inputs:
    img           = RGB or grayscale image data
    size          = Output image size in pixels (width, height)
    interpolation = Interpolation method (if requested):
                      "auto" = select method automatically (default)
                      "area" = resampling using pixel area (OpenCV INTER_AREA)
                      "bicubic" = bicubic interpolation (OpenCV INTER_CUBIC)
                      "bilinear" = bilinear interpolation (OpenCV INTER_LINEAR)
                      "lanczos" = Lanczos interpolation (OpenCV INTER_LANCZOS4)
                      "nearest" = nearest-neighbor interpolation (OpenCV INTER_NEAREST)
                      None = disable interpolation and crop or pad instead

    Returns:
    resized_img   = Resized image

    :param img: numpy.ndarray
    :param size: tuple
    :param interpolation: str
    :return resized_img: numpy.ndarray
    """
    params.device += 1
    if interpolation is not None:
        interp_mtd = _set_interpolation(input_size=img.shape[0:2], output_size=size, method=interpolation)
        resized_img = cv2.resize(img, dsize=size, interpolation=interp_mtd)
    else:
        # original image size
        r_ori, c_ori = img.shape[0:2]
        # desired image size
        r, c = size[1], size[0]

        # check whether the input image is RGB or grayscale
        if len(img.shape) > 2:
            b = np.shape(img)[2]
            input_img = np.copy(img)
        else:
            b = 1
            input_img = np.expand_dims(img, axis=2)
        # Calculate the change in the number of rows and columns
        dt_r = r - r_ori
        dt_c = c - c_ori

        # Calculate padding sizes
        top = int(abs(dt_r) / 2)
        bot = abs(dt_r) - top
        left = int(abs(dt_c) / 2)
        right = abs(dt_c) - left

        if dt_r <= 0:
            input_img = input_img[top:top + r:, :, :]
            top = 0
            bot = 0
        if dt_c <= 0:
            input_img = input_img[:, left:left + c, :]
            left = 0
            right = 0

        resized_img = np.array(
            [np.pad(input_img[:, :, ib], ((top, bot), (left, right)), 'constant') for ib in range(0, b)])
        resized_img = np.transpose(resized_img, (1, 2, 0))
        if b == 1:
            resized_img = np.squeeze(resized_img, axis=2)

    if params.debug == 'print':
        print_image(resized_img, os.path.join(params.debug_outdir, str(params.device) + "_resized.png"))
    elif params.debug == 'plot':
        plot_image(resized_img)

    return resized_img


def resize_factor(img, factors, interpolation="auto"):
    """Resize input image to a new size using resize factors along x and y axes.

    Inputs:
    img           = RGB or grayscale image data
    factors       = Resizing factors (width, height). E.g. (0.5, 0.5)
    interpolation = Interpolation method (if requested):
                      "auto" = select method automatically (default)
                      "area" = resampling using pixel area (OpenCV INTER_AREA)
                      "bicubic" = bicubic interpolation (OpenCV INTER_CUBIC)
                      "bilinear" = bilinear interpolation (OpenCV INTER_LINEAR)
                      "lanczos" = Lanczos interpolation (OpenCV INTER_LANCZOS4)
                      "nearest" = nearest-neighbor interpolation (OpenCV INTER_NEAREST)

    Returns:
    resized_img   = Resized image

    :param img: numpy.ndarray
    :param factors: tuple
    :param interpolation: str
    :return resized_img: numpy.ndarray
    """
    params.device += 1
    if not isinstance(factors, tuple) or len(factors) != 2 or not all([n > 0 for n in factors]):
        fatal_error(f"The input factors={factors} should be a tuple of length 2 with values greater than 0.")

    interp_mtd = _set_interpolation(input_size=(1, 1), output_size=factors, method=interpolation)
    resized_img = cv2.resize(img, (0, 0), fx=factors[0], fy=factors[1], interpolation=interp_mtd)

    if params.debug == 'print':
        print_image(resized_img, os.path.join(params.debug_outdir, str(params.device) + "_resize.png"))
    elif params.debug == 'plot':
        plot_image(resized_img)

    return resized_img
