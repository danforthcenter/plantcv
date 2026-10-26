# Automatically detect a color card and color correct to standard chip values
from plantcv.plantcv.transform.detect_color_card import detect_color_card
from plantcv.plantcv.transform.color_correction import (
    apply_transformation_matrix,
    affine_color_correction,
    calc_transformation_matrix
)
from plantcv.plantcv.transform.get_color_matrix import get_matrix_m
from plantcv.plantcv.transform.standard_matrices import (xrite_old_color_matrix, xrite_color_matrix,
                                                         astro_color_matrix, ctrax_color_matrix)


def auto_correct_color(rgb_img, color_chip_size=None, roi=None, delta_E=True, xrite_old=False, **kwargs):
    """Automatically detect a color card.
    Parameters
    ----------
    rgb_img : numpy.ndarray
        Input RGB image data containing a color card.
    color_chip_size: str, tuple, optional
        "passport", "classic", "nano", "mini", "cameratrax", or "astro"; or tuple formatted (width, height)
        in millimeters (default = None)
    roi: plantcv.plantcv.Objects, optional
        Objects class rectangular ROI passed to detect_color_card (default None)
    delta_E : Boolean, optional
        Should DeltaE be calculated between the observed vs expected color card? Defaults to True.
    xrite_old : boolean (default False)
        Option if using xrite color targets with the old (pre-2014) formulations. Typically only useful for legacy images.
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
    card_matrix, _ = detect_color_card(rgb_img=rgb_img, color_chip_size=color_chip_size, roi=roi, delta_E=delta_E,
                                    xrite_old=xrite_old, **kwargs)

    if isinstance(color_chip_size, str) and color_chip_size.upper() == 'ASTRO':
        std_matrix = astro_color_matrix()
    elif isinstance(color_chip_size, str) and color_chip_size.upper() == 'CAMERATRAX':
        std_matrix = ctrax_color_matrix(pos=3)
    else:
        if xrite_old:
            std_matrix = xrite_old_color_matrix(pos=3)
        else:
            std_matrix = xrite_color_matrix(pos=3)

    corr_img = affine_color_correction(rgb_img=rgb_img, source_matrix=card_matrix, target_matrix=std_matrix, rerun_delta_E=delta_E)

    return corr_img


def auto_correct_color_nonlinear(rgb_img, color_chip_size=None, roi=None, delta_E=True, xrite_old=False, **kwargs):
    """Automatically detect a color card and applies non-linear color correction
    Parameters
    ----------
    rgb_img : numpy.ndarray
        Input RGB image data containing a color card.
    color_chip_size: str, tuple, optional
        "passport", "classic", "nano", "mini", "cameratrax", or "astro"; or tuple formatted (width, height)
        in millimeters (default = None)
    roi: plantcv.plantcv.Objects, optional
        Objects class rectangular ROI passed to detect_color_card (default None)
    delta_E : Boolean, optional
        Should DeltaE be calculated between the observed vs expected color card? Defaults to True.
    xrite_old : boolean (default False)
        Option if using xrite color targets with the old (pre-2014) formulations. Typically only useful for legacy images.
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
    # Measure colors in image
    card_matrix, _ = detect_color_card(rgb_img=rgb_img, color_chip_size=color_chip_size, roi=roi, delta_E=delta_E,
                                    xrite_old=xrite_old, **kwargs)

    # Fetch reference values for the given type of color card
    if isinstance(color_chip_size, str) and color_chip_size.upper() == 'ASTRO':
        std_matrix = astro_color_matrix()
    elif isinstance(color_chip_size, str) and color_chip_size.upper() == 'CAMERATRAX':
        std_matrix = ctrax_color_matrix(pos=3)
    else:
        if xrite_old:
            std_matrix = xrite_old_color_matrix(pos=3)
        else:
            std_matrix = xrite_color_matrix(pos=3)

    _, matrix_m, matrix_b = get_matrix_m(target_matrix=std_matrix, source_matrix=card_matrix)
    # calculate transformation_matrix and save
    _, transformation_matrix = calc_transformation_matrix(matrix_m, matrix_b)
    # apply non-linear color transformation to the input image
    corrected = apply_transformation_matrix(source_img=rgb_img, transformation_matrix=transformation_matrix, rerun_delta_E=delta_E)

    return corrected
