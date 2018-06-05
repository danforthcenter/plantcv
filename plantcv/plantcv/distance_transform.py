# Distance transform of binary image

import cv2
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image


def distance_transform(img, distanceType, maskSize, device, debug=None):
    """Creates an image where for each object pixel, a number is assigned that corresponds to the distance to the
    nearest background pixel.

    Inputs:
    img             = img object, binary
    distanceType    = Type of distance. It can be CV_DIST_L1, CV_DIST_L2 , or CV_DIST_C which are 1, 2 and 3,
                      respectively.
    device          = device number. Used to count steps in the pipeline
    debug           = None, print, or plot. Print = save to file, Plot = print to screen.
    maskSize        = Size of the distance transform mask. It can be 3, 5, or CV_DIST_MASK_PRECISE (the latter option
                      is only supported by the first function). In case of the CV_DIST_L1 or CV_DIST_C distance type,
                      the parameter is forced to 3 because a 3 by 3 mask gives the same result as 5 by 5 or any larger
                      aperture.

    Returns:
    device          = device number
    norm_image      = grayscale distance-transformed image normalized between [0,1]

    :param img: numpy array
    :param distanceType: int
    :param maskSize: int
    :param device: int
    :param debug: str
    :return device: int
    :return norm_image: numpy array
    """

    device += 1
    dist = cv2.distanceTransform(src=img, distanceType=distanceType, maskSize=maskSize)
    norm_image = cv2.normalize(src=dist, dst=dist, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

    if debug == 'print':
        print_image(norm_image, (str(device) + '_distance_transform.png'))
    elif debug == 'plot':
        plot_image(norm_image, cmap='gray')

    return device, norm_image
