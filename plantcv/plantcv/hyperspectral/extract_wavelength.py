# Extract one of the predefined indices from a hyperspectral datacube

import os
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image
from plantcv.plantcv import Spectral_data
from plantcv.plantcv.hyperspectral.read_data import _find_closest


def extract_wavelength(spectral_data, wavelength):
    """Find index of a target wavelength band in a hyperspectral data instance.

        Inputs:
            spectral_data  = Hyperspectral data instance
            wavelength     = Target wavelength value

        Returns:
            index_array    = Data instance of request wavelength band

        :param spectral_data: __main__.Spectral_data
        :param wavelength: float
        :return index_array: __main__.Spectral_data
        """
    # Make a list of all keys which are the wavelengths
    all_wavelengths = spectral_data.wavelength_dict.keys()

    # Find index of the band with the closest wavelengths
    band_index = _find_closest(np.array([float(i) for i in all_wavelengths]), wavelength)

    # Print which wavelength will be used
    wl_dict = spectral_data.wavelength_dict
    print("The closest band found to " + str(wavelength) + spectral_data.wavelength_units + " is: " +
          str(list(wl_dict.keys())[band_index]))

    # Reshape
    index_array_raw = spectral_data.array_data[:, :, [band_index]]
    index_array_raw = np.transpose(np.transpose(index_array_raw)[0])

    # Resulting array is float 32 from -1 to 1, transform into uint8 for plotting
    all_positive = np.add(index_array_raw, np.ones(np.shape(index_array_raw)))
    normalized = all_positive.astype(np.float64) / 2  # normalize the data to 0 - 1
    index_array = (255 * normalized).astype(np.uint8)  # scale to 255

    # Plot out grayscale image
    if params.debug == "plot":
        plot_image(index_array)
    elif params.debug == "print":
        print_image(index_array,
                    os.path.join(params.debug_outdir, str(params.device) + str(wavelength) + "_index.png"))

    # Find array min and max values
    max_pixel = float(np.amax(index_array_raw))
    min_pixel = float(np.amin(index_array_raw))

    # Make a spectral data instance
    index_array = Spectral_data(array_data=index_array_raw, max_wavelength=wavelength,
                                min_wavelength=wavelength, max_value=max_pixel, min_value=min_pixel, d_type=np.uint8,
                                wavelength_dict={}, samples=spectral_data.samples,
                                lines=spectral_data.lines, interleave=spectral_data.interleave,
                                wavelength_units=spectral_data.wavelength_units,
                                array_type="index_" + str(wavelength),
                                pseudo_rgb=None, filename=spectral_data.filename, default_bands=None)

    return index_array
