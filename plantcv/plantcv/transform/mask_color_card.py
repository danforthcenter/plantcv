# Filter the results of the color card detection algorithm

from plantcv.plantcv._helpers import _cv2_findcontours, _object_composition
from plantcv.plantcv.transform.detect_color_card import _color_card_detection
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import params
import numpy as np
import cv2
import os


def mask_color_card(rgb_img, **kwargs):
    """Automatically detect a color card and visualizes the chips detected.

    Parameters
    ----------
    rgb_img : numpy.ndarray
        Input RGB image data containing a color card.
    **kwargs
        Other keyword arguments passed to cv2.adaptiveThreshold and cv2.circle.

        Valid keyword arguments:
        adaptive_method: 0 (mean) or 1 (Gaussian) (default = 1)
        block_size: int (default = 51)
        radius: int (default = 20)
        min_size: int (default = 1000)

    Returns
    -------

    numpy.ndarray
        Binary bounding box mask of the detected color card chips
    """
    _, _, bounding_mask, _, _, _ = _color_card_detection(rgb_img, **kwargs)

    # Find contours
    cnt, cnt_str = _cv2_findcontours(bin_img=bounding_mask)

    # Consolidate contours
    obj = _object_composition(contours=cnt, hierarchy=cnt_str)
    bb_debug = cv2.drawContours(np.copy(rgb_img), [obj], -1, (255, 0, 255), params.line_thickness)

    # Debugging
    _debug(visual=bb_debug, filename=os.path.join(params.debug_outdir, f'{params.device}_color_card.png'))

    return bounding_mask
