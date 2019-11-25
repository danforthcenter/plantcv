# Extract one of the predefined indices from a hyperspectral datacube

import os
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image
from plantcv.plantcv import fatal_error
from plantcv.plantcv import Spectral_data
from plantcv.plantcv.hyperspectral import _find_closest



def extract_index(array, index="NDVI", distance=20):
    """Pull out indices of interest from a hyperspectral datacube.

        Inputs:
        array = hyperspectral data instance
        index = index of interest, either "ndvi", "gdvi", or "savi"
        distance = how lenient to be if the required wavelengths are not available

        Returns:
        index_array    = Index data as a Spectral_data instance

        :param array: __main__.Spectral_data
        :param index: str
        :param distance: int
        :return index_array: __main__.Spectral_data
        """
    params.device += 1

    # Min and max available wavelength will be used to determine if an index can be extracted
    max_wavelength = float(array.max_wavelength)
    min_wavelength = float(array.min_wavelength)

    # Dictionary of wavelength and it's index in the list
    wavelength_dict = array.wavelength_dict.copy()
    array_data = array.array_data.copy()

    if index.upper() == "NDVI":
        if (max_wavelength + distance) >= 800 and (min_wavelength - distance) <= 670:
            # Obtain index that best represents NIR and red bands
            nir_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 800)
            red_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 670)
            nir = (array_data[:, :, [nir_index]])
            red = (array_data[:, :, [red_index]])
            index_array_raw = (nir - red) / (nir + red)
        else:
            fatal_error("Available wavelengths are not suitable for calculating NDVI. Try increasing fudge factor.")

    elif index.upper() == "GDVI":
        # Green Difference Vegetation Index [Sripada et al. (2006)]
        if (max_wavelength + distance) >= 800 and (min_wavelength - distance) <= 680:
            nir_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 800)
            red_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 680)
            nir = (array_data[:, :, [nir_index]])
            red = (array_data[:, :, [red_index]])
            index_array_raw = nir - red
        else:
            fatal_error("Available wavelengths are not suitable for calculating GDVI. Try increasing fudge factor.")

    elif index.upper() == "SAVI":
        # Soil Adjusted Vegetation Index [Huete et al. (1988)]
        if (max_wavelength + distance) >= 800 and (min_wavelength - distance) <= 680:
            nir_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 800)
            red_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 680)
            nir = (array_data[:, :, [nir_index]])
            red = (array_data[:, :, [red_index]])
            index_array_raw = (1.5 * (nir - red)) / (red + nir + 0.5)
        else:
            fatal_error("Available wavelengths are not suitable for calculating SAVI. Try increasing fudge factor.")

    else:
        fatal_error(index + " is not one of the currently available indices for this function.")

    # Reshape array into hyperspectral datacube shape
    index_array_raw = np.transpose(np.transpose(index_array_raw)[0])

    # Resulting array is float 32 from -1 to 1, transform into uint8 for plotting
    all_positive = np.add(index_array_raw, np.ones(np.shape(index_array_raw)))
    data = all_positive.astype(np.float64) / 2  # normalize the data to 0 - 1
    index_array = (255 * data).astype(np.uint8)  # scale to 255

    index_array = Spectral_data(array_data=index_array, max_wavelength=0,
                                min_wavelength=0, d_type=np.uint8,
                                wavelength_dict={}, samples=array.samples,
                                lines=array.lines, interleave=array.interleave,
                                wavelength_units=array.wavelength_units, array_type="index_" + index.lower(),
                                pseudo_rgb=None, filename=array.filename, default_bands=None)

    if params.debug == "plot":
        plot_image(index_array.array_data)
    elif params.debug == "print":
        print_image(index_array.array_data,
                    os.path.join(params.debug_outdir, str(params.device) + index + "_index.png"))

    return index_array
