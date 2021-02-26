# Rotate an image

import os
import cv2
import numpy as np
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import params


def rotate(img, rotation_deg, crop):
    """Rotate an image by an angle.

    Inputs:
    img          = RGB or grayscale image data
    rotation_deg = rotation angle in degrees, can be a negative number,
                   positive values move counter clockwise.
    crop         = either true or false, if true, dimensions of rotated image will be same as original image.

    Returns:
    rotated_img  = rotated image

    :param img: numpy.ndarray
    :param rotation_deg: double
    :param crop: bool
    :return rotated_img: numpy.ndarray
    """

    # Extract image spatial dimensions
    iy, ix = np.shape(img)[:2]

    m = cv2.getRotationMatrix2D((ix / 2, iy / 2), rotation_deg, 1)

    cos = np.abs(m[0, 0])
    sin = np.abs(m[0, 1])

    if not crop:
        # compute the new bounding dimensions of the image
        nw = int((iy * sin) + (ix * cos))
        nh = int((iy * cos) + (ix * sin))

        # adjust the rotation matrix to take into account translation
        m[0, 2] += (nw / 2) - (ix / 2)
        m[1, 2] += (nh / 2) - (iy / 2)

        rotated_img = cv2.warpAffine(img, m, (nw, nh))
    else:
        rotated_img = cv2.warpAffine(img, m, (ix, iy))

    params.device += 1

    if params.debug == 'print':
        print_image(rotated_img, os.path.join(params.debug_outdir,
                                              str(params.device) + '_' + str(rotation_deg) + '_rotated_img.png'))

    elif params.debug == 'plot':
        if len(np.shape(img)) == 3:
            plot_image(rotated_img)
        else:
            plot_image(rotated_img, cmap='gray')

    return rotated_img
