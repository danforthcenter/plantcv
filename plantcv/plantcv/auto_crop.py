# Resize image

import os
import cv2
import numpy as np
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import params


def auto_crop(img, objects, padding_x=0, padding_y=0, color='black'):
    """Resize image.

    Inputs:
    img       = RGB or grayscale image data
    objects   = contours
    padding_x = padding in the x direction
    padding_y = padding in the y direction
    color     = either 'black' or 'white'

    Returns:
    cropped   = cropped image

    :param img: numpy.ndarray
    :param objects: list
    :param padding_x: int
    :param padding_y: int
    :param color: str
    :return cropped: numpy.ndarray
    """

    params.device += 1
    img_copy = np.copy(img)

    x, y, w, h = cv2.boundingRect(objects)
    cv2.rectangle(img_copy, (x, y), (x + w, y + h), (0, 255, 0), 5)

    crop_img = img[y:y + h, x:x + w]

    offsetx = int(np.rint(padding_x))
    offsety = int(np.rint(padding_y))

    if color == 'black':
        colorval = (0, 0, 0)
    elif color == 'white':
        colorval = (255, 255, 255)

    cropped = cv2.copyMakeBorder(crop_img, offsety, offsety, offsetx, offsetx, cv2.BORDER_CONSTANT, value=colorval)

    if params.debug == 'print':
        print_image(img_copy, os.path.join(params.debug_outdir, str(params.device) + "_crop_area.png"))
        print_image(cropped, os.path.join(params.debug_outdir, str(params.device) + "_auto_cropped.png"))
    elif params.debug == 'plot':
        if len(np.shape(img_copy)) == 3:
            plot_image(img_copy)
            plot_image(cropped)
        else:
            plot_image(img_copy, cmap='gray')
            plot_image(cropped, cmap='gray')

    return cropped
