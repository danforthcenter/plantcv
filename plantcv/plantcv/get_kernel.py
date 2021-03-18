# Create a kernel structuring element

import cv2
from plantcv.plantcv import fatal_error


def get_kernel(size, shape):
    """Creates a kernel structuring element of specified size and shape.

    size   = Kernel size (n,m). A (n x m) kernel will be built. Must be greater than 1 to have an effect.
    shape  = Element shape, either rectangle, cross, or ellipse.

    Returns:
    kernel = Numpy array structuring element kernel

    :param size: tuple
    :param shape: str
    :return kernel: numpy.ndarray
    """

    if size[0] <= 1 and size[1] <= 1:
        raise ValueError('size needs to be greater than 1 for the function to have an effect')

    if shape.upper() == "RECTANGLE":
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, size)
    elif shape.upper() == "ELLIPSE":
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, size)
    elif shape.upper() == "CROSS":
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, size)
    else:
        fatal_error("Shape " + str(shape) + " is not rectangle, ellipse or cross!")

    return kernel
