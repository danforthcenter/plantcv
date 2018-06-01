# RGB -> HSV -> Gray

import cv2
import numpy as np
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image


def rotate(img, rotation_deg, crop, device, debug=None):
    """Rotate image, sometimes it is necessary to rotate image, especially when clustering for
       multiple plants is needed.

    Inputs:
    img          = image object, RGB colorspace (either single or three channel)
    rotation_deg = rotation angle in degrees, should be an integer, can be a negative number,
                   positive values move counter clockwise.
    crop         = either true or false, if true, dimensions of rotated image will be same as original image.
    device       = device number. Used to count steps in the pipeline
    debug        = None, print, or plot. Print = save to file, Plot = print to screen.

    Returns:
    device       = device number
    rotated_img  = rotated image

    :param img: numpy array
    :param rotation_deg: int
    :param device: int
    :param debug: str
    :return device: int
    :return rotated_img: numpy array
    """
    device += 1

    if len(np.shape(img)) == 3:
        iy, ix, iz = np.shape(img)
    else:
        iy, ix = np.shape(img)

    M = cv2.getRotationMatrix2D((ix / 2, iy / 2), rotation_deg, 1)

    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    if crop==False:
        # compute the new bounding dimensions of the image
        nW = int((iy * sin) + (ix * cos))
        nH = int((iy * cos) + (ix * sin))

        # adjust the rotation matrix to take into account translation
        M[0, 2] += (nW / 2) - (ix/2)
        M[1, 2] += (nH / 2) - (iy/2)

        rotated_img =cv2.warpAffine(img, M, (nW, nH))
    else:
        rotated_img = cv2.warpAffine(img, M, (ix, iy))

    if debug == 'print':
        print_image(rotated_img, (str(device) + '_rotated_img.png'))

    elif debug == 'plot':
        if len(np.shape(img)) == 3:
            plot_image(rotated_img)
        else:
            plot_image(rotated_img, cmap='gray')

    return device, rotated_img
