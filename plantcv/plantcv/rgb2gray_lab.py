# RGB -> LAB -> Gray

import cv2
import os
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params


def rgb2gray_lab(rgb_img, channel):
    """Convert image from RGB colorspace to LAB colorspace. Returns the specified subchannel as a gray image.

    Inputs:
    rgb_img   = RGB image data
    channel   = color subchannel (l = lightness, a = green-magenta, b = blue-yellow)

    Returns:
    l | a | b = grayscale image from one LAB color channel

    :param rgb_img: numpy.ndarray
    :param channel: str
    :return channel: numpy.ndarray
    """
    # Auto-increment the device counter
    params.device += 1
    # The allowable channel inputs are l, a or b
    names = {"l": "lightness", "a": "green-magenta", "b": "blue-yellow"}
    channel = channel.lower()
    if channel not in names:
        fatal_error("Channel " + str(channel) + " is not l, a or b!")

    # Convert the input BGR image to LAB colorspace
    lab = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2LAB)
    # Split LAB channels
    l, a, b = cv2.split(lab)
    # Create a channel dictionaries for lookups by a channel name index
    channels = {"l": l, "a": a, "b": b}

    if params.debug == "print":
        print_image(channels[channel], os.path.join(params.debug_outdir,
                                                    str(params.device) + "_lab_" + names[channel] + ".png"))
    elif params.debug == "plot":
        plot_image(channels[channel], cmap="gray")

    return channels[channel]
