#

import numpy as np



def _inverse_covariance(spectral_array):
    """ which is used in various GatorSense hyperspectral tools
            (https://github.com/GatorSense/hsi_toolkit_py)

            Inputs:
                spectral_array      = Hyperspectral data instance

            Returns:
                inverse_covariance  = Inverse covariance matrix of a hyperspectral datacube

            :param spectral_array: __main__.Spectral_data
            :return inverse_covariance: numpy array
            """

    hsi_data = spectral_array.array_data
    inverse_covariance = np.linalg.pinv(np.cov(hsi_data.T, rowvar=False))
    return inverse_covariance
