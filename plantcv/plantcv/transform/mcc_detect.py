"""Wrap cv2.mcc functions for color card detection"""
import os
import cv2
import numpy as np
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _rect_filter
from plantcv.plantcv.fatal_error import fatal_error
from plantcv.plantcv._globals import params
from plantcv.plantcv.transform.delta_e import _delta_e
from plantcv.plantcv.transform.get_color_matrix import get_color_matrix


def mcc_detect(rgb_img, roi=None, delta_E=True, **kwargs):
    """Detect a macbeth color card using cv2.mcc tools

    Parameters:
    -----------
    rgb_img : numpy.ndarray
        Input RGB image data containing a color card.
    roi : plantcv.plantcv.Objects, optional
        A rectangular ROI as returned from pcv.roi.rectangle to detect a color card only in that region.
    delta_E : Boolean, optional
        Should DeltaE be calculated between the observed vs expected color card? Defaults to True.
    **kwargs
        Other keyword arguments passed to cv2.mcc.CCheckerDetector.process

        Valid keyword arguments:
        chartType: int (default = cv2.mcc.MCC24, which is 0), code for type of chart
        nc: int (default = 1), number of cards to detect
        useNet: bool (default = False), use a neural network for finding the color card?
        params: cv2.mcc.DetectorParameters, should generally not be set manually without famililarity with these objects.

    Returns
    -------
    color matrix
        Matrix containing the average red value, average green value, and average blue value for each color chip
    """
    color_matrix, debug_img, _, _, _ = _rect_filter(rgb_img,
                                                    roi,
                                                    function=_mcc_detection,
                                                    **kwargs)

    # Save or plot debug image of color card transformed to standard size
    _debug(visual=debug_img, filename=os.path.join(params.debug_outdir,
                                                   f'{params.device}_aligned_color_card.png'))

    # Calculate delta E
    if delta_E:
        params.function_args["mcc_detect"] = {"roi": roi,
                                              "kwargs": kwargs}
        _ = _delta_e(color_matrix)

    return color_matrix


def _mcc_detection(rgb_img, **kwargs):
    """Internal worker to detect a macbeth color card using cv2.mcc tools"""
    
    # Make a detector object
    detector = cv2.mcc.CCheckerDetector_create()
    # get parameters from kwargs
    chart_type = kwargs.get("chartType", cv2.mcc.MCC24)
    nc = kwargs.get("nc", 1)
    useNet = kwargs.get("useNet", False)
    params = kwargs.get("params", cv2.mcc.DetectorParameters.create())
    # give the detector the image to process
    detector.process(rgb_img, chart_type, nc, useNet, params)
    # Get a list of the checkers (cards)
    checkers = detector.getListColorChecker()
    # make an empty mask
    labeled_mask = np.zeros((rgb_img.shape[0], rgb_img.shape[1]), dtype=np.uint8)
    # Checkers is a list of matches, sorted by "best", take the first ones
    # and get the color charts from it, those are the chips as a list of corners
    if len(checkers) < 1:
        fatal_error("No color card detected, consider trying pcv.transform.detect_color_card")
    chips = checkers[0].getColorCharts()
    mheight = []
    mwidth = []
    marea = []
    # reorder chips to pos=3 order from cv2's "Dark Skin" to "Black" order, long dim major
    lst = [i + o for o in [0, 1, 2, 3, 4, 5] for i in [18, 12, 6, 0]]
    cv2_order_to_pos3_order = [item * 4 for item in lst]
    # For each starting corner in the 24 square chips:
    for i, c in enumerate(cv2_order_to_pos3_order):
        # select the 4 points of this square
        pts = chips[c:c+4, :]
        # make a bounding box
        x, y, w, h = cv2.boundingRect(pts)
        # draw the box on the mask as a bunch of i+1's.
        # NOTE here we match the (i + 1) * 10 values from _draw_color_chips in detect
        cv2.rectangle(labeled_mask, (x, y), (x + w, y + h), (i + 1) * 10, -1)
        # NOTE, these h, w values are not useful for rescaling units because they are
        # the size of the masked region, not of the chip itself.
        mheight.append(h)
        mwidth.append(w)
        marea.append(w * h)

    # to make a debug we can use the CCheckerDraw function:
    for checker in checkers:
        # Visualize the detection
        cdraw = cv2.mcc.CCheckerDraw_create(checker)
        debug_img = rgb_img.copy()
        cdraw.draw(debug_img)

    _, color_matrix = get_color_matrix(rgb_img=rgb_img, mask=labeled_mask)

    return color_matrix, debug_img, marea, mheight, mwidth
    
