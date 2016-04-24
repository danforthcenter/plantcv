# Flip image

import cv2
from . import print_image
from . import fatal_error


def flip(img, direction, device, debug=False):
    """Flip image.

    Inputs:
    img       = image to be flipped
    direction = "horizontal" or "vertical"
    device    = device counter
    debug     = if true prints image

    Returns:
    device    = device number
    vh_img    = flipped image

    :param img: numpy array
    :param direction: str
    :param device: int
    :param debug: bool
    :return device: int
    :return vh_img: numpy array
    """

    if direction == "vertical":
        vh_img = cv2.flip(img, 1)
    elif direction == "horizontal":
        vh_img = cv2.flip(img, 0)
    else:
        fatal_error(str(direction) + " is not a valid direction, must be horizontal or vertical")

    if debug:
        print_image(vh_img, (str(device) + "_flipped.png"))

    return device, vh_img
