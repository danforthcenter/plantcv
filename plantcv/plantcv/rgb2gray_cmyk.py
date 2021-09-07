# RGB -> CMYK -> Gray

import cv2
import os
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params
import numpy as np


def rgb2gray_cmyk(rgb_img, channel):
    """Convert image from RGB colorspace to CMYK colorspace. Returns the specified subchannel as a gray image.

    Inputs:
    rgb_img   = RGB image data
    channel   = color subchannel (c = cyan, m = magenta, y = yellow, k=black)

    Returns:
    c | m | y | k = grayscale image from one CMYK color channel

    :param rgb_img: numpy.ndarray
    :param channel: str
    :return channel: numpy.ndarray
    """
    # The allowable channel inputs are c, m , y or k
    names = {"c": "cyan", "m": "magenta", "y": "yellow", "k": "black"}
    channel = channel.lower()
    if channel not in names:
        fatal_error("Channel " + str(channel) + " is not c, m, y or k!")

    # Create float
    bgr = rgb_img.astype(float)/255.

    # K channel
    k = 1 - np.max(bgr, axis=2)

    # C Channel
    c = (1 - bgr[..., 2] - k) / (1 - k)

    # M Channel
    m = (1 - bgr[..., 1] - k) / (1 - k)

    # Y Channel
    y = (1 - bgr[..., 0] - k) / (1 - k)

    # Convert the input BGR image to LAB colorspace
    cmyk = (np.dstack((c, m, y, k)) * 255).astype(np.uint8)
    # Split CMYK channels
    y, m, c, k = cv2.split(cmyk)
    # Create a channel dictionaries for lookups by a channel name index
    channels = {"c": c, "m": m, "y": y, "k": k}

    # Save or display the grayscale image
    _debug(visual=channels[channel], filename=os.path.join(params.debug_outdir,
                                                           str(params.device) + "_cmyk_" + names[channel] + ".png"))

    return channels[channel]
