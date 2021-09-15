# RGB -> HSV -> Gray

import cv2
import os
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params


def rgb2gray_hsv(rgb_img, channel):
    """
    Convert an RGB color image to HSV colorspace and return a gray image (one channel).

    Inputs:
    rgb_img = RGB image data
    channel = color subchannel (h = hue, s = saturation, v = value/intensity/brightness)

    Returns:
    h | s | v = image from single HSV channel

    :param rgb_img: numpy.ndarray
    :param channel: str
    :return channel: numpy.ndarray
    """

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

    _debug(visual=channels[channel],
           filename=os.path.join(params.debug_outdir,
                                 str(params.device) + "_hsv_" + names[channel] + ".png"),
           cmap='gray')

    return channels[channel]
