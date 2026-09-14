# Correct for variable lighting using Contrast Limited Adaptive Histogram Equalization (CLAHE)

import os
import cv2
import numpy as np
from plantcv.plantcv._globals import params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _rgb2gray
from plantcv.plantcv.get_kernel import _format_kernel

def clahe(img, kernel=8, contrast_threshold=2.0):
    """Apply Contrast Limited Adaptive Histogram Equalization (CLAHE)

    Parameters:
    -----------
    img                = numpy.ndarray,
        RGB or grayscale image. RGB image will be converted to LAB and
        the L channel will be corrected.
    kernel             = int, numpy.ndarray, or tuple
        Kernel specification. Default will make an 8x8 window.
    contrast_threshold = float
        Threshold for contrast within each window. Larger numbers
        will result in more dramatic changes to the image.

    Returns:
    --------
    corrected_img = numpy.ndarray
        CLAHE adjusted image
    """
    k = _format_kernel(kernel, tuple)
    if len(np.shape(img)) == 3:
        corrected_img = _rgb_clahe(img, k, contrast_threshold)
    else:
        corrected_img = _gray_clahe(img, k, contrast_threshold)
    _debug(visual=corrected_img,
           filename=os.path.join(params.debug_outdir, str(params.device) + '_clahe_correction.png'))

    return corrected_img


def _rgb_clahe(img, k, contrast_threshold):
    """Apply Contrast Limited Adaptive Histogram Equalization (CLAHE) to an RGB image

    Parameters:
    -----------
    img                = numpy.ndarray,
        RGB or grayscale image. RGB image will be converted to LAB and
        the L channel will be corrected.
    kernel             = int, numpy.ndarray, or tuple
        Kernel specification. Default will make an 8x8 window.
    contrast_threshold = float
        Threshold for contrast within each window. Larger numbers
        will result in more dramatic changes to the image.

    Returns:
    --------
    corrected_img = numpy.ndarray
        CLAHE adjusted image
    """
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    clahe = cv2.createCLAHE(clipLimit=contrast_threshold, tileGridSize=k)
    lab[:,:,0] = clahe.apply(lab[:,:,0])
    clahe_img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    return clahe_img


def _gray_clahe(img, k, contrast_threshold):
    """Apply Contrast Limited Adaptive Histogram Equalization (CLAHE) to a grayscale image

    Parameters:
    -----------
    img                = numpy.ndarray,
        RGB or grayscale image. RGB image will be converted to LAB and
        the L channel will be corrected.
    kernel             = int, numpy.ndarray, or tuple
        Kernel specification. Default will make an 8x8 window.
    contrast_threshold = float
        Threshold for contrast within each window. Larger numbers
        will result in more dramatic changes to the image.

    Returns:
    --------
    corrected_img = numpy.ndarray
        CLAHE adjusted image
    """
    clahe = cv2.createCLAHE(clipLimit=contrast_threshold, tileGridSize=k)
    clahe_img = clahe.apply(img)
    return clahe_img
