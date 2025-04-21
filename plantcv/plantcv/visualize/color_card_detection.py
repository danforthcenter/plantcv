# Visualize the results of the color card detection algorithm

from plantcv.plantcv.transform.detect_color_card import _color_card_detection 
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import params
import os

def color_card_detection(rgb_img, **kwargs):
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
        Labeled mask of chips.
    numpy.ndarray
        Debug image of color card detection
    numpy.ndarray
        Binary convex hull mask of the detected color card chips
    """
    labeled_mask, debug_img, convex_hull_mask, _, _, _ = _color_card_detection(rgb_img, **kwargs)

    # Debugging
    _debug(visual=debug_img, filename=os.path.join(params.debug_outdir, f'{params.device}_color_card.png'))

    return labeled_mask, debug_img, convex_hull_mask
