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
    params.device += 1
    
    # Min and max available wavelength will be used to determine if an index can be extracted
    max_wavelength = max([float(i.rstrip()) for i in header_dict['wavelength']])
    min_wavelength = min([float(i.rstrip()) for i in header_dict['wavelength']])
    # Dictionary of wavelength and it's index in the list
    wavelength_dict = {}
    for j, wavelength in enumerate(header_dict["wavelength"]):
        wavelength_dict.update({wavelength: j})

    if index.upper() == "NDVI":
        if (max_wavelength + fudge_factor) >= 800 and (min_wavelength - fudge_factor) <= 670:
            # Obtain index that best represents NIR and red bands
            nir_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 800)
            red_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 670)
            nir = (array[:, :, [nir_index]] + array[:, :, [nir_index + 4]] + array[:, :, [nir_index - 4]]) / 3
            red = (array[:, :, [red_index]] + array[:, :, [red_index + 4]] + array[:, :, [red_index - 4]]) / 3
            ndvi = (nir - red) / (nir + red)
            index_array_raw = np.transpose(np.transpose(ndvi)[0])

            # Resulting array is float 32 from -1 to 1, transform into uint8 for plotting
            all_positive = np.add(index_array_raw, np.ones(np.shape(index_array_raw)))
            datandvi = all_positive.astype(np.float64) / 2  # normalize the data to 0 - 1
            index_array = (255 * datandvi).astype(np.uint8)  # scale to 255
        else:
            fatal_error("Available wavelengths are not suitable for calculating NDVI. Try increasing fudge factor." )


    elif index.upper() == "GDVI":
        # Green Difference Vegetation Index [Sripada et al. (2006)]
        if (max_wavelength + fudge_factor) >= 800 and (min_wavelength - fudge_factor) <= 680:
            nir_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 800)
            red_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 680)
            nir = (array[:, :, [nir_index]] + array[:, :, [nir_index + 4]] + array[:, :, [nir_index - 4]]) / 3
            red = (array[:, :, [red_index]] + array[:, :, [red_index + 4]] + array[:, :, [red_index - 4]]) / 3
            gdvi = nir - red
            index_array_raw = np.transpose(np.transpose(gdvi)[0])

            # Resulting array is float 32 from -1 to 1, transform into uint8 for plotting
            all_positive = np.add(index_array_raw, np.ones(np.shape(index_array_raw)))
            datagdvi = all_positive.astype(np.float64) / 2  # normalize the data to 0 - 1
            index_array = (255 * datagdvi).astype(np.uint8)  # scale to 255
        else:
            fatal_error("Available wavelengths are not suitable for calculating GDVI. Try increasing fudge factor.")

    elif index.upper() == "SAVI":
        # Soil Adjusted Vegetation Index [Huete et al. (1988)]
        if (max_wavelength + fudge_factor) >= 800 and (min_wavelength - fudge_factor) <= 680:
            nir_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 800)
            red_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 680)
            nir = (array[:, :, [nir_index]])
            red = (array[:, :, [red_index]])
            savi = (1.5 * (nir - red)) / (red + nir + 0.5)
            index_array_raw = np.transpose(np.transpose(savi)[0])

            # Resulting array is float 32 from -1 to 1, transform into uint8 for plotting
            all_positive = np.add(index_array_raw, np.ones(np.shape(index_array_raw)))
            datagdvi = all_positive.astype(np.float64) / 2  # normalize the data to 0 - 1
            index_array = (255 * datagdvi).astype(np.uint8)  # scale to 255
        else:
            fatal_error("Available wavelengths are not suitable for calculating SAVI. Try increasing fudge factor.")

    if params.debug == "plot":
        # Gamma correct pseudo_rgb image
        plot_image(index_array)
    elif params.debug == "print":
        print_image(index_array, os.path.join(params.debug_outdir, str(params.device) + index + "_index.png"))

    return index_array
