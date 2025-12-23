# Automatically detect a color card and color correct to standard chip values
from plantcv.plantcv.transform.detect_color_card import detect_color_card
from plantcv.plantcv.transform.color_correction import (
    apply_transformation_matrix,
    get_color_matrix,
    std_color_matrix,
    affine_color_correction,
    calc_transformation_matrix,
    get_matrix_m,
)


def auto_correct_color(rgb_img, color_chip_size=None, roi=None, **kwargs):
    """Automatically detect a color card.
    Parameters
    ----------
    rgb_img : numpy.ndarray
        Input RGB image data containing a color card.
    color_chip_size: str, tuple, optional
        "passport", "classic", "nano", "mini", or "cameratrax"; or tuple formatted (width, height)
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
    labeled_mask = detect_color_card(rgb_img=rgb_img, color_chip_size=color_chip_size, roi=roi, **kwargs)
    _, card_matrix = get_color_matrix(rgb_img=rgb_img, mask=labeled_mask)
    std_matrix = std_color_matrix(pos=3)
    return affine_color_correction(rgb_img=rgb_img, source_matrix=card_matrix,
                                   target_matrix=std_matrix)


def auto_correct_color_nonlinear(rgb_img, color_chip_size=None, roi=None, **kwargs):
    """Automatically detect a color card and applies non-linear color correction
    Parameters
    ----------
    rgb_img : numpy.ndarray
        Input RGB image data containing a color card.
    color_chip_size: str, tuple, optional
        "passport", "classic", "nano", "mini", or "cameratrax"; or tuple formatted (width, height)
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
    labeled_mask = detect_color_card(rgb_img=rgb_img, color_chip_size=color_chip_size, roi=roi, **kwargs)
    _, card_matrix = get_color_matrix(rgb_img=rgb_img, mask=labeled_mask)
    std_matrix = std_color_matrix(pos=3)
    _, matrix_m, matrix_b = get_matrix_m(target_matrix=std_matrix, source_matrix=card_matrix)
    # calculate transformation_matrix and save
    _, transformation_matrix = calc_transformation_matrix(matrix_m, matrix_b)
    # apply non-linear color transformation to the input image
    corrected = apply_transformation_matrix(source_img=rgb_img, transformation_matrix=transformation_matrix)
    return corrected
