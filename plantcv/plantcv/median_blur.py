# Median blur device

import os
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _rect_filter, _rect_replace
from plantcv.plantcv._globals import params
from plantcv.plantcv.get_kernel import _format_kernel
from scipy.ndimage import median_filter


def median_blur(gray_img, ksize, roi=None):
    """
    Applies a median blur filter (applies median value to central pixel within a kernel size).

    Parameters:
    -----------
    gray_img  = numpy.ndarray,
        Grayscale image data
    ksize = int, tuple, or numpy.ndarray,
        ksize x ksize box if integer, (n, m) size box if tuple, np.shape size box if array
    roi = plantcv.plantcv.Objects,
        Optional rectangular ROI to apply median blur in

    Returns:
    --------
    img_mblur = numpy.ndarray,
        blurred image
    """
    # Make sure ksize is valid
    k = _format_kernel(ksize, to=(int, tuple))

    sub_img_mblur = _rect_filter(gray_img, roi, median_filter,
                                 **{"size": k})
    img_mblur = _rect_replace(gray_img, sub_img_mblur, roi)

    _debug(img_mblur,
           filename=os.path.join(params.debug_outdir,
                                 str(params.device) + '_median_blur' + str(k) + '.png'),
           cmap='gray')

    return img_mblur
