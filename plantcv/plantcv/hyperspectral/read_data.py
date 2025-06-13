# Read in a hyperspectral data cube as an array and parse metadata from the header file

import os
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv.readimage import _read_hyper
from plantcv.plantcv.transform import rescale


def _make_pseudo_rgb(spectral_array):
    """Create the best pseudo-rgb image possible from a hyperspectral datacube

    Inputs:
        spectral_array = Hyperspectral data instance

    Returns:
        pseudo_rgb     = Pseudo-rgb image

    :param spectral_array: __main__.Spectral_data
    :return pseudo_rgb: numpy.ndarray
    """
    # Make shorter variable names for data from the spectral class instance object
    array_data = spectral_array.array_data
    default_bands = spectral_array.default_bands
    wl_keys = spectral_array.wavelength_dict.keys()

    if default_bands is not None:
        pseudo_rgb = cv2.merge((array_data[:, :, int(default_bands[0])],
                                array_data[:, :, int(default_bands[1])],
                                array_data[:, :, int(default_bands[2])]))

    else:
        max_wavelength = max(float(i) for i in wl_keys)
        min_wavelength = min(float(i) for i in wl_keys)
        # Check range of available wavelength
        if max_wavelength >= 600 and min_wavelength <= 490:
            id_red = _find_closest(spectral_array=np.array([float(i) for i in wl_keys]), target=630)
            id_green = _find_closest(spectral_array=np.array([float(i) for i in wl_keys]), target=540)
            id_blue = _find_closest(spectral_array=np.array([float(i) for i in wl_keys]), target=480)

            pseudo_rgb = cv2.merge((array_data[:, :, [id_blue]],
                                    array_data[:, :, [id_green]],
                                    array_data[:, :, [id_red]]))
        else:
            # Otherwise take 3 wavelengths, first, middle and last available wavelength
            id_red = int(len(spectral_array.wavelength_dict)) - 1
            id_green = int(id_red / 2)
            pseudo_rgb = cv2.merge((array_data[:, :, [0]],
                                    array_data[:, :, [id_green]],
                                    array_data[:, :, [id_red]]))

    # Gamma correct pseudo_rgb image
    pseudo_rgb = pseudo_rgb ** (1 / 2.2)
    # Scale each of the channels up to 255
    debug = params.debug
    params.debug = None
    pseudo_rgb = cv2.merge((rescale(pseudo_rgb[:, :, 0]),
                            rescale(pseudo_rgb[:, :, 1]),
                            rescale(pseudo_rgb[:, :, 2])))

    # Reset debugging mode
    params.debug = debug

    return pseudo_rgb


def read_data(filename, mode="ENVI"):
    """Read hyperspectral image data from file.
    Inputs:
    filename          = Name of image file
    mode              = Format of img data (ENVI or ARCGIS, case insensitive)

    Returns:
    spectral_array    = Hyperspectral data instance

    :param filename: str
    :param mode: str
    :return spectral_array: __main__.Spectral_data
    """

    # Call the helper function in readimage
    spectral_array = _read_hyper(filename, mode=mode)

    pseudo_rgb = spectral_array.pseudo_rgb
    _debug(visual=pseudo_rgb, filename=os.path.join(params.debug_outdir, str(params.device) + "_pseudo_rgb.png"))

    return spectral_array
