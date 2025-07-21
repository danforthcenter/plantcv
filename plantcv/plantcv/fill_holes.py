# Fill in holes, flood fill

import numpy as np
import os
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params
from plantcv.plantcv._helpers import _rect_filter
from scipy.ndimage import binary_fill_holes


def fill_holes(bin_img, **kwargs):
    """
    Flood fills holes in a binary mask

    Inputs:
    bin_img      = Binary image data
    **kwargs     = other keyword arguments, namely x/y/h/w for rectangle subsetting

    Returns:
    filtered_img = image with objects filled

    :param bin_img: numpy.ndarray
    :return filtered_img: numpy.ndarray
    """
    # Make sure the image is binary
    if len(np.shape(bin_img)) != 2 or len(np.unique(bin_img)) > 2:
        fatal_error("Image is not binary")

    # Cast binary image to boolean
    bool_img = bin_img.astype(bool)

    # Flood fill holes
    bool_img = _rect_filter(bool_img,
                            xstart=kwargs.get("x", 0),
                            ystart=kwargs.get("y", 0),
                            height=kwargs.get("h", np.shape(bool_img)[0]),
                            width=kwargs.get("w", np.shape(bool_img)[1]),
                            function=binary_fill_holes,
                            replace=kwargs.get("replace", True))

    # Cast boolean image to binary and make a copy of the binary image for returning
    filtered_img = np.copy(bool_img.astype(np.uint8) * 255)

    _debug(visual=filtered_img,
           filename=os.path.join(params.debug_outdir, str(params.device) + '_fill_holes' + '.png'),
           cmap='gray')

    return filtered_img
