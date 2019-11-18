# Calibrate hyperspectral image data

import os
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv.hyperspectral import read_data


def calibrate(filename):
    """This function allows you read in hyperspectral images in raw format as array and normalize
    it with white and dark reference.

    Inputs:
    filename        = Name of raw image file (assumes the raw data is from *_raw and *_raw.hdr files, and
                    white reference is *_whiteReference, and dark reference is *_darkReference)

    Returns:
    calibrated      = Calibrated hyperspectral image

    :param white_reference: __main__.Spectral_data
    :param dark_reference: __main__.Spectral_data
    :return calibrated: __main__.Spectral_data
    """
    # Auto-increment device
    params.device += 1

    # Store debug mode
    debug = params.debug

    raw_data = read_data(filename=filename)

    # Extract base filename
    path, img_name = os.path.split(raw_data.filename)
    raw_data_filename = (img_name).split("_")

    # Read in dark and white reference images corresponding to the raw image data
    d_filename = os.path.join(path, raw_data_filename[0] + "_darkReference")
    w_filename = os.path.join(path, raw_data_filename[0] + "_whiteReference")
    d_reference = read_data(filename=d_filename)
    w_reference = read_data(filename=w_filename)

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

    # Restore debug mode
    params.debug = debug

    return calibrated
