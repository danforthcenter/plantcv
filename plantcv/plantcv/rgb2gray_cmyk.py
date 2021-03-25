# RGB -> CMYK -> Gray

import cv2
import os
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
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
    # Auto-increment the device counter
    params.device += 1
    # The allowable channel inputs are c, m , y or k
    names = {"c": "cyan", "m": "magenta", "y": "yellow", "k": "black"}
    channel = channel.lower()
    if channel not in names:
        fatal_error("Channel " + str(channel) + " is not c, m, y or k!")

    # Create float
    bgr = rgb_img.astype(float)/255.

    # K channel
    K = 1 - np.max(bgr, axis=2)

    # C Channel
    C = (1-bgr[...,2] - K)/(1-K)

    # M Channel
    M = (1-bgr[...,1] - K)/(1-K)

    # Y Channel
    Y = (1-bgr[...,0] - K)/(1-K)

    # Convert the input BGR image to LAB colorspace
    CMYK = (np.dstack((C,M,Y,K)) * 255).astype(np.uint8)
    #Split CMYK channels
    Y, K, C, M = cv2.split(CMYK)
    # Create a channel dictionaries for lookups by a channel name index
    channels = {"c": C, "m": M, "y": Y, "k": K}

    if params.debug == "print":
        print_image(channels[channel], os.path.join(params.debug_outdir,
                                                    str(params.device) + "_cmyk_" + names[channel] + ".png"))
    elif params.debug == "plot":
        plot_image(channels[channel], cmap="gray")

    return channels[channel]
