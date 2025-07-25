# Join images (OR)

import os
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import params
from plantcv.plantcv._helpers import _logical_operation


def logical_or(bin_img1, bin_img2):
    """Join two images using the bitwise OR operator.

    Parameters
    ----------
    bin_img1 : numpy.ndarray
        First binary image.
    bin_img2 : numpy.ndarray
        Second binary image.

    Returns
    -------
    numpy.ndarray
        Joined binary image.
    """
    merged = _logical_operation(bin_img1, bin_img2, 'or')

    _debug(visual=merged, filename=os.path.join(params.debug_outdir, f'{params.device}_or_joined.png'), cmap='gray')

    return merged
