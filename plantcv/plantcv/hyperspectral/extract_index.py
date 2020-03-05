# Extract one of the predefined indices from a hyperspectral datacube

import os
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image
from plantcv.plantcv import fatal_error
from plantcv.plantcv import Spectral_data
from plantcv.plantcv.transform import rescale
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
            # Naturally ranges from -1 to 1
            index_array_raw = (nir - red) / (nir + red)
        else:
            fatal_error("Available wavelengths are not suitable for calculating NDVI. Try increasing distance.")

    elif index.upper() == "GDVI":
        # Green Difference Vegetation Index [Sripada et al. (2006)]
        if (max_wavelength + distance) >= 800 and (min_wavelength - distance) <= 680:
            nir_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 800)
            red_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 680)
            nir = (array_data[:, :, [nir_index]])
            red = (array_data[:, :, [red_index]])
            # Naturally ranges from -2 to 2
            index_array_raw = nir - red
        else:
            fatal_error("Available wavelengths are not suitable for calculating GDVI. Try increasing distance.")

    elif index.upper() == "SAVI":
        # Soil Adjusted Vegetation Index [Huete et al. (1988)]
        if (max_wavelength + distance) >= 800 and (min_wavelength - distance) <= 680:
            nir_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 800)
            red_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 680)
            nir = (array_data[:, :, [nir_index]])
            red = (array_data[:, :, [red_index]])
            # Naturally ranges from -1.2 to 1.2
            index_array_raw = (1.5 * (nir - red)) / (red + nir + 0.5)
        else:
            fatal_error("Available wavelengths are not suitable for calculating SAVI. Try increasing distance.")

    elif index.upper() == "PRI":
        #  Photochemical Reflectance Index (https://doi.org/10.1111/j.1469-8137.1995.tb03064.x)
        if (max_wavelength + distance) >= 570 and (min_wavelength - distance) <= 531:
            # Obtain index that best approximates 570 and 531 nm bands
            pri570_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 570)
            pri531_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 531)
            pri570 = (array_data[:, :, [pri570_index]])
            pri531 = (array_data[:, :, [pri531_index]])
            # PRI = (R531− R570)/(R531+ R570))
            denominator = pri531 + pri570
            # Avoid dividing by zero
            index_array_raw = np.where(denominator == 0, 0, ((pri531 - pri570) / denominator))
        else:
            fatal_error("Available wavelengths are not suitable for calculating PRI. Try increasing distance.")

    elif index.upper() == "ACI":
        #  Van den Berg et al. 2005
        if (max_wavelength + distance) >= 800 and (min_wavelength - distance) <= 560:
            green_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 560)
            nir_index   = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 800)
            green = (array_data[:, :, [green_index]])
            nir   = (array_data[:, :, [nir_index]])
            # Naturally ranges from -1.0 to 1.0
            index_array_raw = green/nir
        else:
            fatal_error("Available wavelengths are not suitable for calculating ACI. Try increasing distance.")
    
    elif index.upper() == "ARI":
        # Gitelson et al., 2001
        if (max_wavelength + distance) >= 700 and (min_wavelength - distance) <= 550:
            ari550_indes = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 550)
            ari700_index   = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 700)
            ari550 = (array_data[:, :, [ari550_indes]])
            ari700 = (array_data[:, :, [ari700_index]])
            index_array_raw = (1/ari550)-(1/ari700)
        else:
            fatal_error("Available wavelengths are not suitable for calculating ARI. Try increasing distance.")
    else:
        fatal_error(index + " is not one of the currently available indices for this function. Please open an issue " +
                    "on the PlantCV GitHub account so we can add more handy indicies!")

    # Reshape array into hyperspectral datacube shape
    index_array_raw = np.transpose(np.transpose(index_array_raw)[0])

    # Store debug mode
    debug = params.debug
    params.debug = None

    # Resulting array is float 32 from varying natural ranges, transform into uint8 for plotting
    all_positive = np.add(index_array_raw, 2 * np.ones(np.shape(index_array_raw)))
    scaled = rescale(all_positive)

    # Find array min and max values
    obs_max_pixel = float(np.nanmax(index_array_raw))
    obs_min_pixel = float(np.nanmin(index_array_raw))

    index_array = Spectral_data(array_data=index_array_raw, max_wavelength=0,
                                min_wavelength=0, max_value=obs_max_pixel, min_value=obs_min_pixel, d_type=np.uint8,
                                wavelength_dict={}, samples=array.samples,
                                lines=array.lines, interleave=array.interleave,
                                wavelength_units=array.wavelength_units, array_type="index_" + index.lower(),
                                pseudo_rgb=scaled, filename=array.filename, default_bands=None)

    # Restore debug mode
    params.debug = debug

    if params.debug == "plot":
        plot_image(index_array.pseudo_rgb)
    elif params.debug == "print":
        print_image(index_array.pseudo_rgb,
                    os.path.join(params.debug_outdir, str(params.device) + index + "_index.png"))

    return index_array
