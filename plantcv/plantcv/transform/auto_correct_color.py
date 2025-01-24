# Automatically detect a color card and color correct to standard chip values

from plantcv.plantcv import params
from plantcv.plantcv.transform.detect_color_card import detect_color_card
from plantcv.plantcv.transform.color_correction import get_color_matrix, std_color_matrix, affine_color_correction


def auto_correct_color(rgb_img, **kwargs):
    """Automatically detect a color card.
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
        Color corrected image
    """
    # Get keyword arguments and set defaults if not set
    labeled_mask = detect_color_card(rgb_img=rgb_img, min_size=kwargs.get("min_size", 1000),
                                     radius=kwargs.get("radius", 20),
                                     adaptive_method=kwargs.get("adaptive_method", 1),
                                     block_size=kwargs.get("block_size", 51))
    _, card_matrix = get_color_matrix(rgb_img=rgb_img, mask=labeled_mask)
    std_matrix = std_color_matrix(pos=3)
    return affine_color_correction(rgb_img=rgb_img, source_matrix=card_matrix,
                                   target_matrix=std_matrix)
