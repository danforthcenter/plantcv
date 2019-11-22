# Analyze reflectance signal data in an index

import os
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import outputs
from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image
from plantcv.plantcv import fatal_error


def analyze_index(index_array, mask):
    """This extracts the hyperspectral index statistics and writes the values  as observations out to
       the Outputs class.

    Inputs:
    array        = Instance of the Spectral_data class,
    mask         = Binary mask made from selected contours

    :param array: __main__.Spectral_data
    :param mask: numpy array
    """
    params.device += 1

    if len(np.shape(mask)) > 2 or len(np.unique(mask)) > 2:
        fatal_error("Mask should be a binary image of 0 and nonzero values.")

    if len(np.shape(index_array.array_data)) > 2:
        fatal_error("index_array data should be a grayscale image.")

    masked_array = index_array.array_data[np.where(mask > 0)]
    index_mean = np.average(masked_array)
    index_median = np.median(masked_array)
    index_std = np.std(masked_array)

    outputs.add_observation(variable='mean_' + index_array.array_type,
                            trait='Average ' + index_array.array_type + ' reflectance',
                            method='plantcv.plantcv.hyperspectral.analyze_index', scale='reflectance', datatype=float,
                            value=index_mean, label='none')

    outputs.add_observation(variable='med_' + index_array.array_type,
                            trait='Median ' + index_array.array_type + ' reflectance',
                            method='plantcv.plantcv.hyperspectral.analyze_index', scale='reflectance', datatype=float,
                            value=index_median, label='none')

    outputs.add_observation(variable='std_' + index_array.array_type,
                            trait='Standard deviation ' + index_array.array_type + ' reflectance',
                            method='plantcv.plantcv.hyperspectral.analyze_index', scale='reflectance', datatype=float,
                            value=index_std, label='none')

    if params.debug == "plot":
        plot_image(masked_array)
    elif params.debug == "print":
        print_image(img=masked_array, filename=os.path.join(params.debug_outdir, str(params.device) +
                                                            index_array.array_type + "_index.png"))
