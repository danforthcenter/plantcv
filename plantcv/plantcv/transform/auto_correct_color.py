# Automatically detect a color card and color correct to standard chip values

from plantcv.plantcv import params, deprecation_warning
from plantcv.plantcv.transform.detect_color_card import detect_color_card
from plantcv.plantcv.transform.color_correction import get_color_matrix, std_color_matrix, affine_color_correction
from plantcv.plantcv._helpers import _rect_filter
import numpy as np


def auto_correct_color(rgb_img, label=None, **kwargs):
    """Automatically detect a color card.
    Parameters
    ----------
    rgb_img : numpy.ndarray
        Input RGB image data containing a color card.
    label : str, optional
        modifies the variable name of observations recorded (default = pcv.params.sample_label).
    **kwargs
        Other keyword arguments passed to cv2.adaptiveThreshold, cv2.circle and _rect_filter.
        Valid keyword arguments:
        adaptive_method: 0 (mean) or 1 (Gaussian) (default = 1)
        block_size: int (default = 51)
        radius: int (default = 20)
        min_size: int (default = 1000)
        x: int (default = 0)
        y: int (default = 0)
        h: int (default = np.shape(rgb_img)[0])
        w: int (default = np.shape(rgb_img)[1])
    Returns
    -------
    numpy.ndarray
        Color corrected image
    """
    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label
    deprecation_warning(
        "The 'label' parameter is no longer utilized, since color chip size is now metadata. "
        "It will be removed in PlantCV v5.0."
        )
    # if x, y, h, w in kwargs then get color matrix from subset of image
    if any(key in ["x", "y", "h", "w"] for key in kwargs):
        sub_mask = _rect_filter(rgb_img,
                                xstart=kwargs.get("x", 0),
                                ystart=kwargs.get("y", 0),
                                height=kwargs.get("h", np.shape(rgb_img)[0]),
                                width=kwargs.get("w", np.shape(rgb_img)[1]),
                                function=detect_color_card,
                                **kwargs
                               )
        # make empty mask in shape of image
        labeled_mask = np.zeros((np.shape(rgb_img)[0], np.shape(rgb_img)[1]))
        # replace slice of empty mask with the subset labeled_mask
        # note that this is a little weird because get_color_matrix still has to be called.
        # once get_color_matrix is called by detect_color_card this can be simplified
        labeled_mask[kwargs.get("y", 0):kwargs.get("y", 0) + kwargs.get("h", np.shape(rgb_img)[0]) - 1,
            kwargs.get("x", 0):kwargs.get("x", 0) + kwargs.get("w", np.shape(rgb_img)[1]) - 1] = sub_mask
    else:
        # Get keyword arguments and set defaults if not set
        labeled_mask = detect_color_card(rgb_img=rgb_img, min_size=kwargs.get("min_size", 1000),
                                         radius=kwargs.get("radius", 20),
                                         adaptive_method=kwargs.get("adaptive_method", 1),
                                         block_size=kwargs.get("block_size", 51))
    _, card_matrix = get_color_matrix(rgb_img=rgb_img, mask=labeled_mask)
    std_matrix = std_color_matrix(pos=3)
    return affine_color_correction(rgb_img=rgb_img, source_matrix=card_matrix,
                                   target_matrix=std_matrix)
