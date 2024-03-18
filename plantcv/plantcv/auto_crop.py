# Resize image

import os
import cv2
import numpy as np
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _cv2_findcontours, _object_composition
from plantcv.plantcv import params, fatal_error


def auto_crop(img, mask, padding_x=0, padding_y=0, color='black'):
    """
    Resize image.

    Inputs:
    img          = RGB or grayscale image data
    mask         = Binary mask image data
    padding_x    = integer or tuple to add padding the x direction
    padding_y    = integer or tuple to add padding the y direction
    color        = either 'black', 'white', or 'image'

    Returns:
    cropped   = cropped image

    :param img: numpy.ndarray
    :param mask: numpy.ndarray
    :param padding_x: int
    :param padding_y: int
    :param color: str
    :return cropped: numpy.ndarray, list
    """
    params.device += 1
    img_copy2 = np.copy(img)

    # Get the height and width of the reference image
    height, width = np.shape(img)[:2]

    # Find contours
    cnt, cnt_str = _cv2_findcontours(bin_img=mask)

    # Consolidate contours
    obj = _object_composition(contours=cnt, hierarchy=cnt_str)

    x, y, w, h = cv2.boundingRect(obj)

    crop_img = img[y:y + h, x:x + w]

    if type(padding_x) is int and type(padding_y) is int:
        offsetx_left = int(np.rint(padding_x))
        offsetx_right = int(np.rint(padding_x))
        offsety_top = int(np.rint(padding_y))
        offsety_bottom = int(np.rint(padding_y))

    elif type(padding_x) is tuple and type(padding_y) is tuple:
        offsetx_left = padding_x[0]
        offsetx_right = padding_x[1]
        offsety_top = padding_y[0]
        offsety_bottom = padding_y[1]

    else:
        fatal_error('Both padding_x and padding_x parameters must be either int or tuple.')

    if color.upper() == 'BLACK':
        colorval = (0, 0, 0)
        cropped = cv2.copyMakeBorder(crop_img, offsety_top, offsety_bottom, offsetx_left,
                                     offsetx_right, cv2.BORDER_CONSTANT, value=colorval)
    elif color.upper() == 'WHITE':
        colorval = (255, 255, 255)
        cropped = cv2.copyMakeBorder(crop_img, offsety_top, offsety_bottom, offsetx_left,
                                     offsetx_right, cv2.BORDER_CONSTANT, value=colorval)
    elif color.upper() == 'IMAGE':
        # Check whether the ROI is correctly bounded inside the image
        if x - offsetx_right < 0 or y - offsety_top < 0 or x + w + offsetx_right > width or y + h + offsety_bottom > height:
            cropped = img_copy2[y:y + h, x:x + w]
        else:
            # If padding is the image, crop the image with a buffer rather than cropping and adding a buffer
            cropped = img_copy2[y - offsety_top:y + h + offsety_bottom, x - offsetx_left:x + w + offsetx_right]
    else:
        fatal_error('Color was provided but ' + str(color) + ' is not "white", "black", or "image"!')

    cmap = None
    if len(np.shape(img_copy2)) != 3:
        cmap = 'gray'

    _debug(visual=cropped,
           filename=os.path.join(params.debug_outdir, str(params.device) + "_auto_cropped.png"),
           cmap=cmap)

    return cropped
