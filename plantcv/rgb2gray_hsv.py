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
    # Auto-increment the device counter
    device += 1

    # The allowable channel inputs are h, s or v
    names = {"h": "hue", "s": "saturation", "v": "value"}
    if channel not in names:
        fatal_error("Channel " + str(channel) + " is not h, s or v!")

    # Convert the input BGR image to HSV colorspace
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Split HSV channels
    h, s, v = cv2.split(hsv)
    # Create a channel dictionaries for lookups by a channel name index
    channels = {"h": h, "s": s, "v": v}

    if debug == "print":
        print_image(channels[channel], str(device) + "_hsv_" + names[channel] + ".png")
    elif debug == "plot":
        plot_image(channels[channel], cmap="gray")

    return device, channels[channel]
