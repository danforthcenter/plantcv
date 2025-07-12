# Automatically detect a color card and color correct to standard chip values

from plantcv.plantcv import params, deprecation_warning
from plantcv.plantcv.transform.detect_color_card import detect_color_card
from plantcv.plantcv.transform.color_correction import get_color_matrix, std_color_matrix, affine_color_correction


def auto_correct_color(rgb_img, label=None, card_type=0, **kwargs):
    """Automatically detect a color card.
    Parameters
    ----------
    rgb_img : numpy.ndarray
        Input RGB image data containing a color card.
    label : str, optional
        Modifies the variable name of observations recorded (default = pcv.params.sample_label).
    card_type : int
        reference value indicating the type of card being used for correction:
                card_type = 0: calibrite color card (default)
                card_type = 1: astrobotany.com AIRI calibration sticker
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
        Color corrected image
    """
    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label
    deprecation_warning(
        "The 'label' parameter is no longer utilized, since color chip size is now metadata. "
        "It will be removed in PlantCV v5.0."
        )
    # Get keyword arguments and set defaults if not set
    labeled_mask = detect_color_card(rgb_img=rgb_img, card_type=card_type,
                                     min_size=kwargs.get("min_size", 1000),
                                     radius=kwargs.get("radius", 20),
                                     adaptive_method=kwargs.get("adaptive_method", 1),
                                     block_size=kwargs.get("block_size", 51))
    _, card_matrix = get_color_matrix(rgb_img=rgb_img, mask=labeled_mask, card_type=card_type)
    std_matrix = std_color_matrix(pos=3, card_type=card_type)

    return affine_color_correction(rgb_img=rgb_img, source_matrix=card_matrix,
                                   target_matrix=std_matrix)
