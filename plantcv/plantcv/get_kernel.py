# Create a kernel structuring element

import cv2
import numpy as np
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


def _format_kernel(k, to=int):
    """turn a kernel/ksize into an array/tuple kernel
    Parameters
    ----------
    k : int, tuple, or numpy.ndarray
        Kernel specified as a binary numpy.ndarray for arbitrary shapes,
        shape tuple for a rectangular kernel, or integer for a square kernel.
    to : tuple, accepted classes to convert k to including any of
        int, tuple, or np.ndarray. This should be set internally
        and depends on how the kernel argument is going to be used.

    Returns
    -------
    kernel specified as 'most complex' class from `to`
    """
    if k is None:
        return k
    if isinstance(k, to):
        return k
    if not isinstance(to, tuple):
        to = [to]

    # if not, pick the next most informative specification from `to`
    convert_to = [cls for cls in [np.ndarray, tuple, int] if cls in to][0]

    conversions = {
        (int, np.ndarray): lambda v: get_kernel((v, v), "rectangle"),
        (tuple, np.ndarray): lambda v: get_kernel(v, "rectangle"),
        (int, tuple): lambda v: (v, v),
        (np.ndarray, tuple): np.shape,
        (tuple, int): lambda v: v[0],
        (np.ndarray, int): lambda v: np.shape(v)[0],
    }

    return conversions[(type(k), convert_to)](k)
