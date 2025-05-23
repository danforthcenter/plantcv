# RGB -> HSV -> Gray

import os
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import params
from plantcv.plantcv._helpers import _rgb2hsv


def rgb2gray_hsv(rgb_img, channel):
    """Convert image from RGB colorspace to HSV colorspace. Returns the specified subchannel as a gray image.

    Parameters
    ----------
    rgb_img : numpy.ndarray
        RGB image data
    channel : str
        color subchannel (h = hue, s = saturation, v = value/intensity/brightness)

    Returns
    -------
    numpy.ndarray
        grayscale image from one HSV color channel
    """
    # Convert RGB to HSV and return the specified subchannel as a gray image
    gray_img = _rgb2hsv(rgb_img=rgb_img, channel=channel)

    # The allowable channel inputs are h, s or v
    names = {"h": "hue", "s": "saturation", "v": "value"}

    _debug(visual=gray_img,
           filename=os.path.join(params.debug_outdir, f"{params.device}_hsv_{names[channel.lower()]}.png"), cmap='gray')

    return gray_img
