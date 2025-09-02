# Erosion filter

import os
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _erode
from plantcv.plantcv import params


def erode(gray_img, ksize, i, roi=None):
    """Perform morphological 'erosion' filtering.

    Keeps pixel in center of the kernel if conditions set in kernel are
       true, otherwise removes pixel.

    Parameters
    ----------
    gray_img : numpy.ndarray
             Grayscale (usually binary) image data
    ksize : int
             Kernel size (int). A ksize x ksize kernel will be built. Must be greater than 1 to have an effect.
    i : int
             interations, i.e. number of consecutive filtering passes
    roi : plantcv.plantcv.Objects
             Optional rectangular ROI to erode within

    Returns
    -------
    numpy.ndarray
         Eroded result image

    Raises
    ------
    ValueError
        If ksize is less than or equal to 1.
    """
    er_img = _erode(gray_img, ksize, i, roi=roi)

    _debug(er_img,
           filename=os.path.join(params.debug_outdir,
                                 str(params.device) + '_er_image' + str(ksize) + '_itr_' + str(i) + '.png'),
           cmap='gray')

    return er_img
