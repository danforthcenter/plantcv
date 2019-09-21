import os
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image
from plantcv.plantcv import fatal_error
from plantcv.plantcv.hyperspectral import _find_closest



def extract_index(array, header_dict, index="NDVI", fudge_factor=20):
    """Pull out indices of interest from a hyperspectral datacube.

        Inputs:
        array = hyperspectral data array
        header_dict = dictionary with header information
        index = index of interest

        Returns:
        index_array    = image object as numpy array

        :param array: numpy.ndarray
        :param header_dict: dict
        :param index: str
        :return index_array: numpy.ndarray
        """
    # Min and max available wavelength will be used to determine if an index can be extracted
    max_wavelength = float(max(header_dict['wavelength']))
    min_wavelength = float(min(header_dict['wavelength']))

    # Dictionary of wavelength and it's index in the list
    wavelength_dict = {}
    for j, wavelength in enumerate(header_dict["wavelength"]):
        wavelength_dict.update({wavelength: j})


    if index.upper() == "NDVI":
        if (max_wavelength + fudge_factor) >= 800 and (min_wavelength - fudge_factor) <= 670:
            nir_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 800)
            red_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 670)
            nir = array[:, :, [nir_index]]
            red = array[:, :, [red_index]]
            ndvi = (nir - red) / (nir + red)
            index_array = np.transpose(np.transpose(ndvi)[0])
        else:
            fatal_error("Available wavelengths are not suitable for calculating NDVI. Try increasing fudge factor.")


    if params.debug == "plot":
        # Gamma correct pseudo_rgb image
        plot_image(index_array)
    elif params.debug == "print":
        print_image(index_array, os.path.join(params.debug_outdir, str(params.device) + index + "_index.png"))

    return index_array
