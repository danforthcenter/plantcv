# RGB -> LAB -> Gray

import os
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import params
from plantcv.plantcv._helpers import _rgb2lab


def rgb2gray_lab(rgb_img, channel):
    """Convert image from RGB colorspace to LAB colorspace. Returns the specified subchannel as a gray image.

    Parameters
    ----------
    rgb_img : numpy.ndarray
        RGB image data
    channel : str
        color subchannel (l = lightness, a = green-magenta, b = blue-yellow)

    Returns
    -------
    numpy.ndarray
        grayscale image from one LAB color channel
    """
    # Convert RGB to LAB and return the specified subchannel as a gray image
    gray_img = _rgb2lab(rgb_img=rgb_img, channel=channel)

    # The allowable channel inputs are l, a or b
    names = {"l": "lightness", "a": "green-magenta", "b": "blue-yellow"}

    # Display debug image
    _debug(visual=gray_img,
           filename=os.path.join(params.debug_outdir, f"{params.device}_lab_{names[channel.lower()]}.png"), cmap="gray")

    return gray_img
