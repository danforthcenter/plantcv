# Calculate the inverse covariance matrix of a hyperspectral datacube

import numpy as np


def _inverse_covariance(spectral_array):
    """ Calculate the inverse covariance matrix of a hyperspectral datacube, which is used in various
        GatorSense hyperspectral tools (https://github.com/GatorSense/hsi_toolkit_py)

            Inputs:
                spectral_array      = Hyperspectral data instance

            Returns:
                inverse_covariance  = Inverse covariance matrix of a hyperspectral datacube

            :param spectral_array: __main__.Spectral_data
            :return inverse_covariance: numpy array
            """

    hsi_img = spectral_array.array_data

    n_lines, n_samples, n_band = hsi_img.shape
    n_pixels = n_lines * n_samples
    hsi_data = np.reshape(hsi_img, (n_pixels, n_band), order='F').T
    inverse_covariance = np.linalg.pinv(np.cov(hsi_data.T, rowvar=False))

    return inverse_covariance
