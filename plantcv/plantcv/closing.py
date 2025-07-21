import os
import numpy as np
from skimage.morphology import binary_closing, closing
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _rect_filter
from plantcv.plantcv import fatal_error


def closing(gray_img, kernel=None, **kwargs):
    """Wrapper for scikit-image closing functions. Opening can remove small dark spots (i.e. pepper).

    Inputs:
    gray_img = input image (grayscale or binary)
    kernel   = optional neighborhood, expressed as an array of 1s and 0s. If None, use cross-shaped structuring element.
    **kwargs     = other keyword arguments, namely x/y/h/w for rectangle subsetting

    :param gray_img: ndarray
    :param kernel = ndarray
    :return filtered_img: ndarray
    """
    # Make sure the image is binary/grayscale
    if len(np.shape(gray_img)) != 2:
        fatal_error("Input image must be grayscale or binary")

    # If image is binary use the faster method
    if len(np.unique(gray_img)) <= 2:
        bool_img = _rect_filter(gray_img.astype(bool),
                            xstart=kwargs.get("x", 0),
                            ystart=kwargs.get("y", 0),
                            height=kwargs.get("h", np.shape(gray_img)[0]),
                            width=kwargs.get("w", np.shape(gray_img)[1]),
                            function=binary_closing,
                            replace=kwargs.get("replace", True),
                            **{"footprint" : kernel})
        filtered_img = np.copy(bool_img.astype(np.uint8) * 255)
    # Otherwise use method appropriate for grayscale images
    else:
        filtered_img = _rect_filter(gray_img,
                            xstart=kwargs.get("x", 0),
                            ystart=kwargs.get("y", 0),
                            height=kwargs.get("h", np.shape(gray_img)[0]),
                            width=kwargs.get("w", np.shape(gray_img)[1]),
                            function=binary_closing,
                            replace=kwargs.get("replace", True),
                            **{"footprint" : kernel})

    _debug(visual=filtered_img,
           filename=os.path.join(params.debug_outdir, str(params.device) + '_opening' + '.png'),
           cmap='gray')

    return filtered_img
