# Calculate masked average background reflectance

import numpy as np


def _avg_reflectance(spectral_data, mask):
    """ Find average reflectance of masked hyperspectral data instance. This is useful for calculating a target
        signature (n_band x 1 - column array) which is required in various GatorSense hyperspectral tools
        (https://github.com/GatorSense/hsi_toolkit_py)

        Inputs:
            spectral_array = Hyperspectral data instance
            mask           = Target wavelength value

        Returns:
            idx            = Index

        :param spectral_data: __main__.Spectral_data
        :param mask: numpy.ndarray
        :return spectral_array: __main__.Spectral_data
        """
    # Initialize list of average reflectance values
    avg_r = []

    # For each band in a hyperspectral datacube mask and take the average
    for i in range(0, len(spectral_data.wavelength_dict)):
        band = spectral_data.array_data[:, :, [i]]
        band_reshape = np.transpose(np.transpose(band)[0])
        masked_band = band_reshape[np.where(mask > 0)]
        band_avg = np.average(masked_band)
        avg_r.append(band_avg)

    # Convert into array object rather than list
    avg_r = np.asarray(avg_r)

    return avg_r
