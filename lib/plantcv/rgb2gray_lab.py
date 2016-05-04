# RGB -> LAB -> Gray

import cv2
from . import print_image
from . import plot_image
from . import fatal_error


def rgb2gray_lab(img, channel, device, debug=None):
    """Convert image from RGB colorspace to LAB colorspace. Returns the specified subchannel as a gray image.

    Inputs:
    img       = image object, RGB colorspace
    channel   = color subchannel (l = lightness, a = green-magenta, b = blue-yellow)
    device    = device number. Used to count steps in the pipeline
    debug     = None, print, or plot. Print = save to file, Plot = print to screen.

    Returns:
    device    = device number
    l | a | b = grayscale image from one LAB color channel

    :param img: numpy array
    :param channel: str
    :param device: int
    :param debug: str
    :return device: int
    :return channel: numpy array
    """

    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    # Split HSV channels
    l, a, b = cv2.split(lab)
    device += 1
    if channel == 'l':
        if debug == 'print':
            print_image(l, (str(device) + '_lab_lightness.png'))
        elif debug == 'plot':
            plot_image(l, cmap='gray')
        return device, l
    elif channel == 'a':
        if debug == 'print':
            print_image(a, (str(device) + '_lab_green-magenta.png'))
        elif debug == 'plot':
            plot_image(a, cmap='gray')
        return device, a
    elif channel == 'b':
        if debug == 'print':
            print_image(b, (str(device) + '_lab_blue-yellow.png'))
        elif debug == 'plot':
            plot_image(b, cmap='gray')
        return device, b
    else:
        fatal_error('Channel ' + str(channel) + ' is not l, a or b!')
