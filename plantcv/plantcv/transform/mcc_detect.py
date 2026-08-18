"""Wrap cv2.mcc functions for color card detection"""

import cv2
from plantcv.plantcv._globals import params
from plantcv.plantcv.helpers import _rect_filter
from plantcv.plantcv.fatal_error import fatal_error
from plantcv.plantcv.transform.delta_e import _delta_e
from plantcv.plantcv.transform.get_color_matrix import get_color_matrix


def mcc_detect(rgb_img, color_chip_size=None, roi=None, delta_E=True, **kwargs):
    """Detect a macbeth color card using cv2.mcc tools

    Parameters:
    -----------

    Returns
    -------
    
    """
    color_matrix, debug_img, marea, mheight, mwidth = _rect_filter(rgb_img,
                                                                    roi,
                                                                    function=_mcc_detection,
                                                                    **kwargs)
    # Create dataframe for easy summary stats
    chip_size = np.median(marea)
    chip_height = np.median(mheight)
    chip_width = np.median(mwidth)

    # Save out size of aruco tags in pixels (measured) and mm (known value)
    outputs.add_metadata(term="mean_color_chip_size", datatype=float, value=chip_size)
    outputs.add_metadata(term="mean_color_chip_width", datatype=float, value=chip_width)
    outputs.add_metadata(term="mean_color_chip_height", datatype=float, value=chip_height)

    # Set size scaling factor if color chip size is provided
    _set_size_scale_from_chip(color_chip_height=chip_height, color_chip_width=chip_width,
                              color_chip_size=color_chip_size)

    # Save or plot debug image of color card transformed to standard size
    _debug(visual=debug_img, filename=os.path.join(params.debug_outdir,
                                                   f'{params.device}_aligned_color_card.png'))

    return color_matrix


def _mcc_detection(rgb_img, **kwargs):
    """Internal worker to detect a macbeth color card using cv2.mcc tools"""
    
    # Make a detector object
    detector = cv2.mcc.CCheckerDetector_create()
    # give the detector the image to process
    detector.process(rgb_img, cv2.mcc.MCC24, nc=1)
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
    # For each starting corner in the 24 square chips:
    for i in range(0,96,4):
        # select the 4 points of this square
        pts = chips[i:i+4, :]
        # make a bounding box
        x, y, w, h = cv2.boundingRect(pts)
        # draw the box on the mask as a bunch of i+1's.
        cv2.rectangle(labeled_mask, (x, y), (x + w, y + h), i+1, -1)
        mheight.append(h)
        mwidth.append(w)
        marea.append(w * h)
        # now the mask is a labeled mask of color chips.
        # order is something I should check for consistency.

    # to make a debug we can use the CCheckerDraw function:
    for checker in checkers:
        # Visualize the detection
        cdraw = cv2.mcc.CCheckerDraw_create(checker)
        debug_img = rgb_img.copy()
        cdraw.draw(debug_img)
    # now img_annotated is a reasonable debug.
    # NOTE mcc reads "Dark Skin" to "Black", across rows left to right (teal towards black) then up rows (white towards black)], aka pos=0
    # but get_color_matrix works on it.
    color_matrix = get_color_matrix(rgb_img=rgb_img, mask=labeled_mask)

    return color_matrix, debug_img, marea, mheight, mwidth
    
