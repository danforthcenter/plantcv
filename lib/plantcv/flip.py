# Flip image

import cv2
from . import print_image
from . import plot_image
from . import fatal_error


def flip(img, direction, device, debug=None):
    """Flip image.

    Inputs:
    img       = image to be flipped
    direction = "horizontal" or "vertical"
    device    = device counter
    debug     = None, print, or plot. Print = save to file, Plot = print to screen.

    Returns:
    device    = device number
    vh_img    = flipped image

    :param img: numpy array
    :param direction: str
    :param device: int
    :param debug: str
    :return device: int
    :return vh_img: numpy array
    """

    if direction == "vertical":
        vh_img = cv2.flip(img, 1)
    elif direction == "horizontal":
        vh_img = cv2.flip(img, 0)
    else:
        fatal_error(str(direction) + " is not a valid direction, must be horizontal or vertical")

    if debug is 'print':
        print_image(vh_img, (str(device) + "_flipped.png"))
    elif debug is 'plot':
        plot_image(vh_img)

    return device, vh_img
