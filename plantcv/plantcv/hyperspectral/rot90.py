# Rotate hyperspectral datacubes counterclockwise (in increments of 90 degrees)

# imports
import numpy as np
import os
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import Spectral_data


def rot90(spectral_data, k):
    """This function allows you rotate hyperspectral image data counterclockwise in 90 degree increments.

    Inputs:
    spectral_data   = Hyperspectral data instance
    k               = Number of times the array is rotated by 90 degrees

    Returns:
    rot_hsi         = Rotated array data

    :param spectral_data: __main__.Spectral_data
    :param k: int
    :return rot_hsi: __main__.Spectral_data
    """
    # Extract array data and rotate with numpy function
    rot_array = np.rot90(m=spectral_data.array_data, k=k)
    rot_rgb = np.rot90(m=spectral_data.pseudo_rgb, k=k)

    # Dimensions of datacube might change depending on degree of rotation
    dims = np.shape(rot_array)

    # Create new spectral data object with rotated image data and metadata
    rot_hsi = Spectral_data(array_data=rot_array, min_wavelength=spectral_data.min_wavelength,
                            max_wavelength=spectral_data.max_wavelength, min_value=spectral_data.min_value,
                            max_value=spectral_data.max_value, d_type=spectral_data.d_type,
                            wavelength_dict=spectral_data.wavelength_dict, samples=int(dims[2]), lines=int(dims[0]),
                            interleave=spectral_data.interleave, wavelength_units=spectral_data.wavelength_units,
                            array_type="datacube", pseudo_rgb=rot_rgb, default_bands=spectral_data.default_bands,
                            filename="rot_k" + str(k) + spectral_data.filename)

    _debug(visual=rot_rgb,
           filename=os.path.join(params.debug_outdir, str(params.device) + "_pseudo_rgb_rot_k" + str(k) + ".png"))

    return rot_hsi
