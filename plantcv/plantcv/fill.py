# Object fill device

import inspect
import numpy as np
import os
from plantcv.plantcv._globals import params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv.fatal_error import fatal_error
from plantcv.plantcv._helpers import _rect_filter, _rect_replace
from skimage.morphology import remove_small_objects

_SKIMAGE_USE_MAX_SIZE = "max_size" in inspect.signature(remove_small_objects).parameters


def fill(bin_img, size, roi=None, scale_size=False):
    """
    Identifies objects and fills objects that are less than size.

    Parameters:
    -----------
    bin_img      : numpy.ndarray,
        Binary image data
    size         : int,
        minimum object area size in pixels (integer)
    roi          : plantcv.plantcv.Objects,
        optional Objects class rectangular ROI
    scale_size   : bool,
        Is size given in unit other than pixels?
        If True then params.px_height and params.px_width
        are used to rescale the given size to pixels from
        other units.

    Returns:
    --------
    filtered_img : numpy.ndarray,
        image with objects filled
    """
    # Make sure the image is binary
    if len(np.shape(bin_img)) != 2 or len(np.unique(bin_img)) > 2:
        fatal_error("Image is not binary")
    # if scale_size then set the pixel size based on given size and params
    size_px = size
    if scale_size:
        size_px = size / (params.px_height * params.px_width)

    # Cast binary image to boolean
    bool_img = bin_img.astype(bool)

    # Find and fill contours, possibly within bounding rectangle
    _size_kwarg = {"max_size": size_px} if _SKIMAGE_USE_MAX_SIZE else {"min_size": size_px}
    bool_img = _rect_filter(bool_img,
                            roi=roi,
                            function=remove_small_objects,
                            **_size_kwarg)
    # Cast boolean image to binary and make a copy of the binary image for returning
    filtered_img = np.copy(bool_img.astype(np.uint8) * 255)
    # slice the subset image back into full size binary image
    replaced_img = _rect_replace(bin_img.astype(bool) * 255, filtered_img, roi)

    _debug(visual=replaced_img,
           filename=os.path.join(params.debug_outdir, str(params.device) + "_fill" + str(size_px) + '.png'))

    return replaced_img
