"""Convert RGB to CMYK colorspace and return the specified subchannel as a grayscale image."""

import os
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import params
from plantcv.plantcv._helpers import _rgb2cmyk


def rgb2gray_cmyk(rgb_img, channel):
    """Convert image from RGB colorspace to CMYK colorspace. Returns the specified subchannel as a gray image.

    Parameters
    ----------
    rgb_img : numpy.ndarray
        RGB image data
    channel : str
        color subchannel (c = cyan, m = magenta, y = yellow, k=black)

    Returns
    -------
    numpy.ndarray
        grayscale image from one CMYK color channel
    """
    # Convert RGB to CMYK and return the specified subchannel as a gray image
    gray_img = _rgb2cmyk(rgb_img=rgb_img, channel=channel)

    # The allowable channel inputs are c, m , y or k
    names = {"c": "cyan", "m": "magenta", "y": "yellow", "k": "black"}

    # Save or display the grayscale image
    _debug(visual=gray_img,
           filename=os.path.join(params.debug_outdir, f"{params.device}_cmyk_{names[channel.lower()]}.png"), cmap="gray")

    return gray_img
