# Automatically detect a color card and color correct to standard chip values

from plantcv.plantcv import params, deprecation_warning
from plantcv.plantcv.transform.detect_color_card import detect_color_card
from plantcv.plantcv.transform.color_correction import get_color_matrix, std_color_matrix, affine_color_correction


def auto_correct_color(rgb_img, label=None, color_chip_size=None, roi=None, **kwargs):
    """Automatically detect a color card.
    Parameters
    ----------
    rgb_img : numpy.ndarray
        Input RGB image data containing a color card.
    label : str, optional
        modifies the variable name of observations recorded (default = pcv.params.sample_label).
    color_chip_size: str, tuple, optional
        "passport", "classic", "cameratrax"; or tuple formatted (width, height)
        in millimeters (default = None)
    roi: plantcv.plantcv.Objects, optional
        Objects class rectangular ROI passed to detect_color_card (default None)
    **kwargs
        Other keyword arguments passed to cv2.adaptiveThreshold, cv2.circle and _rect_filter.
        Valid keyword arguments:
        adaptive_method: 0 (mean) or 1 (Gaussian) (default = 1)
        block_size: int (default = 51)
        radius: int (default = 20)
        min_size: int (default = 1000)
        aspect_ratio: float (default = 1.27)
        solidity: float (default = 0.8)
    Returns
    -------
    numpy.ndarray
        Color corrected image
    """
    # Set label to params.sample_label if None
    if label is None:
        label = params.sample_label
    deprecation_warning(
        "The 'label' parameter is no longer utilized, since color chip size is now metadata. "
        "It will be removed in PlantCV v5.0."
        )
    labeled_mask = detect_color_card(rgb_img=rgb_img, color_chip_size=color_chip_size, roi=roi, **kwargs)
    _, card_matrix = get_color_matrix(rgb_img=rgb_img, mask=labeled_mask)
    std_matrix = std_color_matrix(pos=3)
    return affine_color_correction(rgb_img=rgb_img, source_matrix=card_matrix,
                                   target_matrix=std_matrix)
