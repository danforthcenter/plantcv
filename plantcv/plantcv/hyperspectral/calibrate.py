# Calibrate hyperspectral image data

import os
import numpy as np
from plantcv.plantcv import params


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

    d_reference = dark_reference
    w_reference = white_reference

    # Collect the number of wavelengths present
    num_bands = len(w_reference.wavelength_dict)
    den = w_reference.array_data - d_reference.array_data

    # Calibrate using reflectance = (raw data - dark reference) / (white reference - dark reference)
    output_num = []
    for i in range(0, raw_data.lines):
        ans = raw_data.array_data[i,] - d_reference.array_data
        output_num.append(ans)
    num = np.stack(output_num, axis=2)
    output_calibrated = []
    for i in range(0, raw_data.lines):
        ans1 = raw_data.array_data[i,] / den
        output_calibrated.append(ans1)

    # Reshape into hyperspectral datacube
    scalibrated = np.stack(output_calibrated, axis=2)
    raw_data.array_data = np.transpose(scalibrated[0], (1, 0, 2))
    calibrated = raw_data

    return calibrated
