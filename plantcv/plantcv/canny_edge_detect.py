# Canny edge detection

from plantcv.plantcv._debug import _debug
from plantcv.plantcv import dilate
from plantcv.plantcv import params
from plantcv.plantcv import fatal_error
from skimage import feature
import numpy as np
import cv2
import os


def canny_edge_detect(img, mask=None, sigma=1.0, low_thresh=None, high_thresh=None, thickness=1,
                      mask_color=None, use_quantiles=False):
    """
    Edge filter an image using the Canny algorithm.

    Inputs:
    img           = RGB or grayscale image data
    mask          = Mask to limit the application of Canny to a certain area, takes a binary img. (OPTIONAL)
    sigma         = Standard deviation of the Gaussian filter
    low_thresh    = Lower bound for hysteresis thresholding (linking edges). If None (default) then low_thresh is set to
                    10% of the image's max (OPTIONAL)
    high_thresh   = Upper bound for hysteresis thresholding (linking edges). If None (default) then high_thresh is set
                    to 20% of the image's max (OPTIONAL)
    thickness     = How thick the edges should appear, default thickness=1 (OPTIONAL)
    mask_color    = Color of the mask provided; either None (default), 'white', or 'black'
    use_quantiles = Default is False, if True then treat low_thresh and high_thresh as quantiles of the edge magnitude
                    image, rather than the absolute edge magnitude values. If True then thresholds range is [0,1].
                    (OPTIONAL)

    Returns:
    bin_img      = Thresholded, binary image

    :param img: numpy.ndarray
    :param mask: numpy.ndarray
    :param sigma = float
    :param low_thresh: float
    :param high_thresh: float
    :param thickness: int
    :param mask_color: str
    :param use_quantiles: bool
    :return bin_img: numpy.ndarray

    Reference: Canny, J., A Computational Approach To Edge Detection, IEEE Trans.
    Pattern Analysis and Machine Intelligence, 8:679-714, 1986
    Originally part of CellProfiler, code licensed under both GPL and BSD licenses.
    Website: http://www.cellprofiler.org
    Copyright (c) 2003-2009 Massachusetts Institute of Technology
    Copyright (c) 2009-2011 Broad Institute
    All rights reserved.
    Original author: Lee Kamentsky
    """

    # Check if the image is grayscale; if color img then make it grayscale
    dimensions = np.shape(img)
    if len(dimensions) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # skimage needs a bool mask
    if mask is not None:
        if mask_color.upper() == 'WHITE':
            mask = np.array(mask, bool)
        elif mask_color.upper() == 'BLACK':
            mask = cv2.bitwise_not(mask)
            mask = np.array(mask, bool)
        else:
            fatal_error('Mask was provided but mask_color ' + str(mask_color) + ' is not "white" or "black"!')

    # Run Canny edge detection on the grayscale image
    bool_img = feature.canny(img, sigma, low_thresh, high_thresh, mask, use_quantiles)

    # Skimage returns a bool image so convert it
    bin_img = np.copy(bool_img.astype(np.uint8) * 255)

    # Adjust line thickness
    if thickness != 1:
        debug = params.debug
        params.debug = None
        bin_img = dilate(bin_img, thickness, 1)
        params.debug = debug

    # Print or plot the binary image
    _debug(visual=bin_img,
           filename=os.path.join(params.debug_outdir, (str(params.device) + '_canny_edge_detect.png')),
           cmap='gray')

    return bin_img
