# Read in a hyperspectral data cube as an array and parse metadata from the header file

import os
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv.readimage import _read_hyper


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

    spectral_array = _read_hyper(filename, mode=mode)

    pseudo_rgb = spectral_array.pseudo_rgb
    _debug(visual=pseudo_rgb, filename=os.path.join(params.debug_outdir, str(params.device) + "_pseudo_rgb.png"))

    return spectral_array
