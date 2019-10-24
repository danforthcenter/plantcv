# Analyze signal data in Thermal image

import os
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import outputs
from plantcv.plantcv import fatal_error



def analyze_index(index_array, mask):
    """This extracts the hyperspectral index statistics and writes the values  as observations out to
       the Outputs class.

    Inputs:
    array        = Instance of the Spectral_data class
    mask         = Binary mask made from selected contours
    histplot     = if True plots histogram of intensity values

    Returns:
    analysis_img = output image

    :param array: numpy array
    :param header_dict: dict
    :param mask: numpy array
    :param histplot: bool
    :return analysis_img: ggplot
    """
    params.device += 1

    if len(np.shape(mask)) > 2 or len(np.unique(mask)) > 2:
        fatal_error("Mask should be a binary image of 0 and nonzero values.")

    masked_array = index_array.array_data[np.where(mask > 0)]
    index_mean = np.average(masked_array)
    index_median = np.median(masked_array)
    index_std = np.std(masked_array)

    outputs.add_observation(variable='mean_' + index_array.array_type,
                            trait='Average ' + index_array.array_type + ' reflectance',
                            method='plantcv.plantcv.hyperspectral.analyze_index', scale='none', datatype=float,
                            value=index_mean, label='none')

    outputs.add_observation(variable='med_' + index_array.array_type,
                            trait='Median ' + index_array.array_type + ' reflectance',
                            method='plantcv.plantcv.hyperspectral.analyze_index', scale='none', datatype=float,
                            value=index_median, label='none')

    outputs.add_observation(variable='std_' + index_array.array_type,
                            trait='Standard deviation ' + index_array.array_type + ' reflectance',
                            method='plantcv.plantcv.hyperspectral.analyze_index', scale='none', datatype=float,
                            value=index_std, label='none')

