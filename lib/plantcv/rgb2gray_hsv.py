# RGB -> HSV -> Gray

import cv2
from . import print_image
from . import plot_image
from . import fatal_error


def rgb2gray_hsv(img, channel, device, debug=None):
    """Convert an RGB color image to HSV colorspace and return a gray image (one channel).

    Inputs:
    img     = image object, RGB colorspace
    channel = color subchannel (h = hue, s = saturation, v = value/intensity/brightness)
    device  = device number. Used to count steps in the pipeline
    debug   = None, print, or plot. Print = save to file, Plot = print to screen.

    Returns:
    device    = device number
    h | s | v = image from single HSV channel

    :param img: numpy array
    :param channel: str
    :param device: int
    :param debug: str
    :return device: int
    :return channel: numpy array
    """

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Split HSV channels
    h, s, v = cv2.split(hsv)
    device += 1
    if channel == 'h':
        if debug is 'print':
            print_image(h, (str(device) + '_hsv_hue.png'))
        elif debug is 'plot':
            plot_image(h, cmap='gray')
        return device, h
    elif channel == 's':
        if debug is 'print':
            print_image(s, (str(device) + '_hsv_saturation.png'))
        elif debug is 'plot':
            plot_image(s, cmap='gray')
        return device, s
    elif channel == 'v':
        if debug is 'print':
            print_image(v, (str(device) + '_hsv_value.png'))
        elif debug is 'plot':
            plot_image(v, cmap='gray')
        return device, v
    else:
        fatal_error('Channel ' + (str(channel) + ' is not h, s or v!'))
