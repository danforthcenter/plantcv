# Discover which spectral indices can be calculated from a dataset

import numpy as np

from plantcv.plantcv import Spectral_data
from plantcv.plantcv import fatal_error

# Required wavelength range (in nanometers) and default distance of each index in the
# plantcv.spectral_index subpackage, kept in sync with the guard conditions inside the index
# functions themselves, e.g. for ndvi:
#     if (float(hsi.max_wavelength) + distance) >= 800 and (float(hsi.min_wavelength) - distance) <= 670:
# Entries are (max_wavelength, min_wavelength, default_distance); test_available.py pins every
# entry to the actual behavior of the corresponding index function.
# When adding a new index function: add its entry here, export it in __init__.py, and document it
# in docs/spectral_index.md.
_INDEX_REQUIREMENTS = {
    "ndvi": (800, 670, 20),
    "gdvi": (800, 550, 20),
    "savi": (800, 680, 20),
    "pri": (570, 531, 20),
    "ari": (700, 550, 20),
    "ci_rededge": (800, 700, 20),
    "cri550": (550, 510, 20),
    "cri700": (700, 510, 20),
    "egi": (700, 460, 40),
    "evi": (800, 480, 20),
    "gli": (670, 480, 20),
    "mari": (800, 550, 20),
    "mcari": (700, 550, 20),
    "mtci": (753.75, 681.25, 20),
    "ndci": (708, 665, 20),
    "ndre": (790, 720, 20),
    "npci": (680, 430, 20),
    "psnd_chla": (800, 680, 20),
    "psnd_chlb": (800, 635, 20),
    "psnd_car": (800, 470, 20),
    "psri": (750, 500, 20),
    "pssr_chla": (800, 680, 20),
    "pssr_chlb": (800, 635, 20),
    "pssr_car": (800, 470, 20),
    "rgri": (670, 560, 20),
    "rvsi": (752, 714, 20),
    "sipi": (800, 480, 20),
    "sr": (800, 670, 20),
    "vari": (670, 480, 20),
    "vi_green": (670, 550, 20),
    "wi": (970, 900, 20),
}

# Indices that also accept a color image (numpy array) directly
_RGB_INDICES = ("egi", "gli")


def available(data, distance=None):
    """List the spectral indices that can be calculated from the input data.

    For a `Spectral_data` object (multi- or hyperspectral datacube), each index in the
    plantcv.spectral_index subpackage is checked with the same wavelength condition used by the
    index function itself. For a color image (numpy array), the indices that accept color images
    directly are listed.

    When `distance` is None each index is tested with its own default distance (20 for most
    indices, 40 for egi), matching what happens when the index function itself is called without
    an explicit distance.

    Inputs:
    data        = Multi- or hyperspectral image (PlantCV Spectral_data instance) or color image (numpy.ndarray)
    distance    = Amount of flexibility (in nanometers) regarding the wavelengths used to calculate an index

    Returns:
    index_names = Sorted list of names of the indices that can be calculated from `data`

    :param data: __main__.Spectral_data or numpy.ndarray
    :param distance: int
    :return index_names: list of str
    """
    if isinstance(data, Spectral_data):
        index_names = []
        for name, (max_wavelength, min_wavelength, default_distance) in _INDEX_REQUIREMENTS.items():
            leniency = default_distance if distance is None else distance
            if (float(data.max_wavelength) + leniency) >= max_wavelength \
                    and (float(data.min_wavelength) - leniency) <= min_wavelength:
                index_names.append(name)
        return sorted(index_names)

    if isinstance(data, np.ndarray):
        return sorted(_RGB_INDICES)

    fatal_error("Input must be a Spectral_data object or a numpy.ndarray (color image), got "
                + type(data).__name__)
