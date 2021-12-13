# Calibrate hyperspectral image data

import os
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug
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
    # Average dark reference over the first axis (repeated line scans) -> float64
    # Converts the input shape from (y, x, z) to (1, x, z)
    dark = np.mean(dark_reference.array_data, axis=0, keepdims=True)

    # Average white reference over the first axis (repeated line scans) -> float64
    # Converts the input shape from (y, x, z) to (1, x, z)
    white = np.mean(white_reference.array_data, axis=0, keepdims=True)

    # Convert the raw data to float64
    raw = raw_data.array_data.astype("float64")

    # Calibrate using reflectance = (raw data - dark reference) / (white reference - dark reference)
    # Note that dark and white are broadcast over each line (y) in raw
    cal = (raw - dark) / (white - dark)

    # Clip the calibrated values to the range 0 - 1
    np.clip(cal, a_min=0, a_max=1, out=cal)

    # Make a new class instance with the calibrated hyperspectral image
    calibrated = Spectral_data(array_data=cal, max_wavelength=raw_data.max_wavelength, min_wavelength=raw_data.min_wavelength,
                               max_value=np.amax(cal), min_value=np.amin(cal), d_type=cal.dtype,
                               wavelength_dict=raw_data.wavelength_dict, samples=raw_data.samples, lines=raw_data.lines,
                               interleave=raw_data.interleave, wavelength_units=raw_data.wavelength_units,
                               array_type=raw_data.array_type, pseudo_rgb=None, filename=raw_data.filename,
                               default_bands=raw_data.default_bands)

    # Make pseudo-rgb image for the calibrated image
    calibrated.pseudo_rgb = _make_pseudo_rgb(spectral_array=calibrated)

    # Debug visualization
    _debug(visual=calibrated.pseudo_rgb,
           filename=os.path.join(params.debug_outdir, str(params.device) + '_calibrated_rgb.png'))

    return calibrated
