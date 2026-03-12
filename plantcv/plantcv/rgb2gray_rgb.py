# RGB -> RGB channel -> Gray

import os
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._globals import params
from plantcv.plantcv._helpers import _rgb2rgb


def rgb2gray_rgb(rgb_img, channel):
    """Return the specified RGB subchannel as a grayscale image.

    Parameters
    ----------
    rgb_img : numpy.ndarray
        RGB image data
    channel : str
        color subchannel (r = red, g = green, b = blue)

    Returns
    -------
    numpy.ndarray
        grayscale image from one RGB color channel
    """
    # Return the specified RGB subchannel as a grayscale image
    gray_img = _rgb2rgb(rgb_img=rgb_img, channel=channel)

    # The allowable channel inputs are r, g or b
    names = {"r": "red", "g": "green", "b": "blue"}

    # Save or display the grayscale image
    _debug(visual=gray_img,
           filename=os.path.join(params.debug_outdir, f"{params.device}_rgb_{names[channel.lower()]}.png"),
           cmap="gray")

    return gray_img
