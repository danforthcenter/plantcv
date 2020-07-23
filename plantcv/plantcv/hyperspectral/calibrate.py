# Calibrate hyperspectral image data

import os
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image
from plantcv.plantcv import Spectral_data
from plantcv.plantcv.hyperspectral.read_data import _make_pseudo_rgb



def calibrate(raw_data, white_reference, dark_reference):
    """This function allows you calibrate raw hyperspectral image data with white and dark reference data.

    Inputs:
    raw_data        = Raw image 'Spectral_data' class instance
    white_reference = White reference 'Spectral_data' class instance
    dark_reference  = Dark reference 'Spectral_data' class instance

    Returns:
    calibrated      = Calibrated hyperspectral image

    :param raw_data: __main__.Spectral_data
    :param white_reference: __main__.Spectral_data
    :param dark_reference: __main__.Spectral_data
    :return calibrated: __main__.Spectral_data
    """
    # Auto-increment device
    params.device += 1

    # Collect the number of wavelengths present
    num_bands = len(white_reference.wavelength_dict)
    den = white_reference.array_data - dark_reference.array_data

    # Calibrate using reflectance = (raw data - dark reference) / (white reference - dark reference)
    output_num = []
    for i in range(0, raw_data.lines):
        ans = raw_data.array_data[i,].astype(np.float16) - dark_reference.array_data
        output_num.append(ans)
    num = np.stack(output_num, axis=2)
    output_calibrated = []
    for i in range(0, raw_data.lines):
        ans1 = raw_data.array_data[i,] / den
        output_calibrated.append(ans1)

    # Reshape into hyperspectral datacube
    scalibrated = np.stack(output_calibrated, axis=2)
    calibrated_array = np.transpose(scalibrated[0], (1, 0, 2))
    calibrated_array[np.where(calibrated_array < 0)] = 0

    # Find array min and max values
    max_pixel = float(np.amax(calibrated_array))
    min_pixel = float(np.amin(calibrated_array))

    # Make a new class instance with the calibrated hyperspectral image
    calibrated = Spectral_data(array_data=calibrated_array, max_wavelength=raw_data.max_wavelength,
                               min_wavelength=raw_data.min_wavelength, max_value=max_pixel, min_value=min_pixel,
                               d_type=raw_data.d_type,
                               wavelength_dict=raw_data.wavelength_dict, samples=raw_data.samples,
                               lines=raw_data.lines, interleave=raw_data.interleave,
                               wavelength_units=raw_data.wavelength_units, array_type=raw_data.array_type,
                               pseudo_rgb=None, filename=None, default_bands=raw_data.default_bands)

    # Make pseudo-rgb image for the calibrated image
    calibrated.pseudo_rgb = _make_pseudo_rgb(spectral_array=calibrated)

    if params.debug == "plot":
        # Gamma correct pseudo_rgb image
        plot_image(calibrated.pseudo_rgb)
    elif params.debug == "print":
        print_image(calibrated.pseudo_rgb, os.path.join(params.debug_outdir, str(params.device) + "_calibrated_rgb.png"))

    return calibrated
