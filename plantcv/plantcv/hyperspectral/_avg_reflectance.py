# Calculate masked average background reflectance

import numpy as np


def _avg_reflectance(spectral_data, mask):

    avg_r = []
    n_bands = len(spectral_data.wavelength_dict)
    n_lines = spectral_data.lines
    n_samples = spectral_data.samples
    for i in range(0, len(spectral_data.wavelength_dict)):
        band = spectral_data.array_data[:, :, [i]]
        band_reshape = np.transpose(np.transpose(band)[0])
        masked_band = band_reshape[np.where(mask > 0)]
        band_avg = np.average(masked_band)
        avg_r.append(band_avg)
    avg_r = np.asarray(avg_r)

    return avg_r
