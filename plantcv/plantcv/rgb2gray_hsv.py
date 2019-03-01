# RGB -> HSV -> Gray

import cv2
import os
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params


def rgb2gray_hsv(rgb_img, channel):
    """Convert an RGB color image to HSV colorspace and return a gray image (one channel).

    Inputs:
    rgb_img = RGB image data
    channel = color subchannel (h = hue, s = saturation, v = value/intensity/brightness)

    Returns:
    h | s | v = image from single HSV channel

    :param rgb_img: numpy.ndarray
    :param channel: str
    :return channel: numpy.ndarray
    """
    # Auto-increment the device counter
    params.device += 1

    # The allowable channel inputs are h, s or v
    names = {"h": "hue", "s": "saturation", "v": "value"}
    channel = channel.lower()
    if channel not in names:
        fatal_error("Channel " + str(channel) + " is not h, s or v!")

    # Convert the input BGR image to HSV colorspace
    hsv = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2HSV)
    # Split HSV channels
    h, s, v = cv2.split(hsv)
    # Create a channel dictionaries for lookups by a channel name index
    channels = {"h": h, "s": s, "v": v}

    if params.debug == "print":
        print_image(channels[channel], os.path.join(params.debug_outdir,
                                                    str(params.device) + "_hsv_" + names[channel] + ".png"))
    elif params.debug == "plot":
        plot_image(channels[channel], cmap="gray")

    return channels[channel]
