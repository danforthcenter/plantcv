# QC analysis of fdark image from PSII cameras

import os
import cv2
import numpy as np
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params
from plantcv.plantcv import outputs


def qc_fdark(fdark, mask, threshold = 5):
    """Analyze PSII camera images.
    Inputs:
    fdark       = grayscale fdark image
    mask        = mask of plant (binary, single channel)
    threshold   = an integer for the amount of noise you are willing to accept in fdark. default is 5. You may want to change this, particularly if you are using a 16-bit image.
    
    Returns:
    fdark_qc_flag = True or False indicating whether fdark as indeed dark

    :param fdark: numpy.ndarray
    :param mask: numpy.ndarray
    :param threshold: integer
    :return fdark_qc_flag: boolean
    """

    # Check that fdark, fmin, and fmax are grayscale (single channel)
    if not all(len(np.shape(i)) == 2 for i in [fdark]):
        fatal_error("The fdark image must be a grayscale image.")
 
    # QC Fdark Image
    fdark_mask = cv2.bitwise_and(fdark, fdark, mask = mask)
    if fdark.dtype == 'uint16' and np.amax(fdark_mask) > threshold:
        qc_fdark = False
    elif fdark.dtype == 'uint8' and np.amax(fdark_mask) > threshold:
        qc_fdark = False
    else:
        qc_fdark = True

    outputs.add_observation(variable='fdark_passed_qc', trait='Fdark passed QC',
                            method='plantcv.photosynthesis.analyze_qc_fdark', scale='none', datatype=bool,
                            value=qc_fdark, label='none')

    return qc_fdark