# Calibrate hyperspectral image data

import os
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image
from plantcv.plantcv import Spectral_data
from plantcv.plantcv.hyperspectral import read_data


def calibrate(filename):
    """This function allows you read in hyperspectral images in raw format as array and normalize
    it with white and dark reference. Assumes that the naming structure is consistent. 

    Inputs:
    white_reference = White reference data in Spectral_data instance format
    dark_reference  = Dark reference data in Spectral_data instance format

    Returns:
    calibrated      = Calibrated hyperspectral image

    :param white_reference: __main__.Spectral_data
    :param dark_reference: __main__.Spectral_data
    :return calibrated: __main__.Spectral_data
    """
    # Auto-increment device
    params.device += 1

    raw_data = read_data(filename=filename)

    path, img_name = os.path.split(raw_data.filename)
    raw_data_filename = (img_name).split("_")

    dark_filename = raw_data_filename + "_darkReference"
    white_filename = raw_data_filename + "_whiteReference"
    dark_reference = read_data(filename=dark_filename)
    white_reference = read_data(filename=white_filename)

    # Collect the number of wavelengths present
    num_bands = len(white_reference.wavelength_dict)
    den = white_reference.array_data - dark_reference.array_data

    output_num = []
    for i in range(0, raw_data.lines):
        ans = raw_data.array_data[i,] - dark_reference.array_data
        output_num.append(ans)
    num = np.stack(output_num, axis=2)
    output_calibrated = []
    for i in range(0, raw_data.lines):
        ans1 = raw_data.array_data[i,] / den
        output_calibrated.append(ans1)
    calibrated = np.stack(output_calibrated, axis=2)
    tcalibrated = np.transpose(calibrated[0], (1, 0, 2))

    return tcalibrated