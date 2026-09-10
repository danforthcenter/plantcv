# Gamma Correction Function

import os
from skimage import exposure
from plantcv.plantcv._globals import params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv.transform.rerun_delta_e import _rerun_delta_e


def gamma_correct(img, gamma=1, gain=1):
    """Apply gamma correction to an input image.

    Parameters
    ----------
    img : numpy.ndarray
        Input image (RGB or grayscale).
    gamma : float, optional
        Non-negative real number. Default is 1.
    gain : float, optional
        Constant multiplier. Default is 1.

    Returns
    -------
    numpy.ndarray
        Gamma-corrected image.
    """
    corrected_img = exposure.adjust_gamma(image=img, gamma=gamma, gain=gain)

    _debug(visual=corrected_img,
           filename=os.path.join(params.debug_outdir, str(params.device) + '_gamma_corrected.png'))

    # rerun deltaE calculation if it was previously run
    _rerun_delta_e(corrected_img, fun="gamma_correct")

    return corrected_img
