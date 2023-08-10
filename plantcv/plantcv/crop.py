"""Crop an image."""
import os
import cv2
import numpy as np
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import params
from plantcv.plantcv import Spectral_data


def crop(img, x, y, h, w):
    """Crop image.

    Inputs:
    img       = RGB, grayscale, or hyperspectral image data
    x         = X coordinate of starting point
    y         = Y coordinate of starting point
    h         = Height
    w         = Width

    Returns:
    cropped   = cropped image

    :param img: numpy.ndarray
    :param x: int
    :param y: int
    :param h: int
    :param w: int
    :return cropped: numpy.ndarray
    """
    # Check if the array data format
    if isinstance(img, Spectral_data):
        # Copy the HSI array
        array = np.copy(img.array_data)
        # Copy the pseudo_rgb image
        ref_img = np.copy(img.pseudo_rgb)
        # Crop the HSI data
        cropped_array = array[y:y + h, x:x + w, :]
        # Calculate the array dimensions
        dims1 = cropped_array.shape

        # Create a new Spectral_data object
        cropped = Spectral_data(
            array_data=cropped_array,
            min_wavelength=img.min_wavelength,
            max_wavelength=img.max_wavelength,
            min_value=np.min(cropped_array),
            max_value=np.max(cropped_array),
            d_type=cropped_array.dtype,
            wavelength_dict=img.wavelength_dict,
            samples=int(dims1[1]),
            lines=int(dims1[0]),
            interleave=img.interleave,
            wavelength_units=img.wavelength_units,
            array_type=img.array_type,
            pseudo_rgb=ref_img[y:y + h, x:x + w, :],
            default_bands=img.default_bands,
            filename=img.filename
        )

    else:
        if len(np.shape(img)) > 2 and np.shape(img)[-1] > 3:
            ref_img = img[:, :, [0]]
            ref_img = np.transpose(np.transpose(ref_img)[0])
            cropped = img[y:y + h, x:x + w, :]
        else:
            ref_img = np.copy(img)
            cropped = img[y:y + h, x:x + w]

    # Create the rectangle contour vertices
    pt1 = (x, y)
    pt2 = (x + w - 1, y + h - 1)

    ref_img = cv2.rectangle(img=np.copy(ref_img), pt1=pt1, pt2=pt2, color=(255, 0, 0), thickness=params.line_thickness)

    _debug(visual=ref_img, filename=os.path.join(params.debug_outdir, str(params.device) + "_crop.png"))

    return cropped
