"""Split RGB image channels into separate grayscale images."""

import os
import numpy as np
from plantcv.plantcv import fatal_error
from plantcv.plantcv._globals import params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _rgb2rgb
from plantcv.plantcv.classes import Spectral_data


def split_rgb_channels(img):
    """Split a Spectral_data pseudo_rgb image into red, green, and blue channels.

    Parameters
    ----------
    img : plantcv.plantcv.classes.Spectral_data
        Spectral_data object containing pseudo_rgb image data.
    Returns
    -------
    tuple of numpy.ndarray
        (r, g, b) grayscale channel images.
    """
    if not isinstance(img, Spectral_data):
        fatal_error("Input image must be a Spectral_data object.")

    rgb_img = img.pseudo_rgb
    if rgb_img is None:
        fatal_error("Input Spectral_data object does not contain pseudo_rgb data.")

    # Validate image shape.
    if len(np.shape(rgb_img)) != 3 or np.shape(rgb_img)[2] != 3:
        fatal_error("Input image must have exactly 3 channels.")

    # Extract channels.
    r = _rgb2rgb(rgb_img=rgb_img, channel="r")
    g = _rgb2rgb(rgb_img=rgb_img, channel="g")
    b = _rgb2rgb(rgb_img=rgb_img, channel="b")

    # Always convert channels to float32 so they are ready for index math.
    r = r.astype(np.float32)
    g = g.astype(np.float32)
    b = b.astype(np.float32)

    _debug(visual=r,
           filename=os.path.join(params.debug_outdir, f"{params.device}_rgb_red.png"),
           cmap="gray")
    _debug(visual=g,
           filename=os.path.join(params.debug_outdir, f"{params.device}_rgb_green.png"),
           cmap="gray")
    _debug(visual=b,
           filename=os.path.join(params.debug_outdir, f"{params.device}_rgb_blue.png"),
           cmap="gray")

    return r, g, b
