# Rotate hyperspectral datacubes (in increments of 90 degrees)

# imports
import numpy.rot90
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import Spectral_data

def rot90(spectral_array, k):
    """This function allows you rotate hyperspectral image data in 90 degree increments.

    Inputs:
    spectral_array  = Hyperspectral data instance
    k               = Number of times the array is rotated by 90 degrees

    Returns:
    rot_array    = Rotated array data

    :param spectral_array: numpy.ndarray
    :param k: int
    :return rot_array: numpy.ndarray
    """

    array_data = spectral_array.array_data
    rot_array = rot90(array_data)

    return rot_array
