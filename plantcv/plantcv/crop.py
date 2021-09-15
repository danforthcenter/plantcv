# Crop

import os
import cv2
import numpy as np
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import params


def crop(img, x, y, h, w):
    """
    Crop image.

       Inputs:
       img       = RGB, grayscale, or hyperspectral image data
       x         = X coordinate of starting point
       y         = Y coordinate of starting point
       h         = Height
       w         = Width

       Returns:
       cropped   = cropped image

       :param img: numpy.ndarray
       :param x: int
       :param y: int
       :param h: int
       :param w: int
       :return cropped: numpy.ndarray
       """

    # Check if the array data format
    if len(np.shape(img)) > 2 and np.shape(img)[-1] > 3:
        ref_img = img[:, :, [0]]
        ref_img = np.transpose(np.transpose(ref_img)[0])
        cropped = img[y:y + h, x:x + w, :]
    else:
        ref_img = np.copy(img)
        cropped = img[y:y + h, x:x + w]

    # Create the rectangle contour vertices
    pt1 = (x, y)
    pt2 = (x + w - 1, y + h - 1)

    ref_img = cv2.rectangle(img=ref_img, pt1=pt1, pt2=pt2, color=(255, 0, 0), thickness=params.line_thickness)

    _debug(visual=ref_img,
           filename=os.path.join(params.debug_outdir, str(params.device) + "_crop.png"))

    return cropped
