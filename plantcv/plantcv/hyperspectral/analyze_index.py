# Analyze reflectance signal data in an index

import os
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import outputs
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import fatal_error
from plotnine import labs
from plantcv.plantcv.visualize import histogram
from plantcv.plantcv import deprecation_warning


def analyze_index(index_array, mask, bins=100, min_bin=0, max_bin=1, histplot=None, label="default"):
    """This extracts the hyperspectral index statistics and writes the values  as observations out to
       the Outputs class.

    Inputs:
    index_array  = Instance of the Spectral_data class, usually the output from pcv.hyperspectral.extract_index
    mask         = Binary mask made from selected contours
    histplot     = if True plots histogram of intensity values
    bins         = optional, number of classes to divide spectrum into
    min_bin      = optional, minimum bin value ("auto" or user input minimum value)
    max_bin      = optional, maximum bin value ("auto" or user input maximum value)
    label        = optional label parameter, modifies the variable name of observations recorded



    :param index_array: __main__.Spectral_data
    :param mask: numpy array
    :param histplot: bool
    :param bins: int
    :param max_bin: float, str
    :param min_bin: float, str
    :param label: str
    :return analysis_image: ggplot, None
    """
    if histplot is not None:
        deprecation_warning("'histplot' will be deprecated in a future version of PlantCV. "
                            "This function creates a histogram by default.")

    debug = params.debug
    params.debug = None

    if len(np.shape(mask)) > 2 or len(np.unique(mask)) > 2:
        fatal_error("Mask should be a binary image of 0 and nonzero values.")

    if len(np.shape(index_array.array_data)) > 2:
        fatal_error("index_array data should be a grayscale image.")

    # Mask data and collect statistics about pixels within the masked image
    masked_array = index_array.array_data[np.where(mask > 0)]
    masked_array = masked_array[np.isfinite(masked_array)]

    index_mean = np.nanmean(masked_array)
    index_median = np.nanmedian(masked_array)
    index_std = np.nanstd(masked_array)

    # Set starting point and max bin values
    maxval = max_bin
    b = min_bin

    # Calculate observed min and max pixel values of the masked array
    observed_max = np.nanmax(masked_array)
    observed_min = np.nanmin(masked_array)

    # Auto calculate max_bin if set
    if type(max_bin) is str and (max_bin.upper() == "AUTO"):
        maxval = float(round(observed_max, 8))  # Auto bins will detect maxval to use for calculating labels/bins
    if type(min_bin) is str and (min_bin.upper() == "AUTO"):
        b = float(round(observed_min, 8))  # If bin_min is auto then overwrite starting value

    # Print a warning if observed min/max outside user defined range
    if observed_max > maxval or observed_min < b:
        print("WARNING!!! The observed range of pixel values in your masked index provided is [" + str(observed_min) +
              ", " + str(observed_max) + "] but the user defined range of bins for pixel frequencies is [" + str(b) +
              ", " + str(maxval) + "]. Adjust min_bin and max_bin in order to avoid cutting off data being collected.")

    # Calculate histogram
    hist_fig, hist_data = histogram(index_array.array_data, mask=mask, bins=bins, lower_bound=b, upper_bound=maxval,
                                    hist_data=True)
    bin_labels, hist_percent = hist_data['pixel intensity'].tolist(), hist_data['proportion of pixels (%)'].tolist()

    # Restore user debug setting
    params.debug = debug
    hist_fig = hist_fig + labs(x='Index Reflectance', y='Proportion of pixels (%)')

    # Print or plot histogram
    _debug(visual=hist_fig,
           filename=os.path.join(params.debug_outdir, str(params.device) + index_array.array_type + "_hist.png"))

    analysis_image = hist_fig

    outputs.add_observation(sample=label, variable='mean_' + index_array.array_type,
                            trait='Average ' + index_array.array_type + ' reflectance',
                            method='plantcv.plantcv.hyperspectral.analyze_index', scale='reflectance', datatype=float,
                            value=float(index_mean), label='none')

    outputs.add_observation(sample=label, variable='med_' + index_array.array_type,
                            trait='Median ' + index_array.array_type + ' reflectance',
                            method='plantcv.plantcv.hyperspectral.analyze_index', scale='reflectance', datatype=float,
                            value=float(index_median), label='none')

    outputs.add_observation(sample=label, variable='std_' + index_array.array_type,
                            trait='Standard deviation ' + index_array.array_type + ' reflectance',
                            method='plantcv.plantcv.hyperspectral.analyze_index', scale='reflectance', datatype=float,
                            value=float(index_std), label='none')

    outputs.add_observation(sample=label, variable='index_frequencies_' + index_array.array_type,
                            trait='index frequencies', method='plantcv.plantcv.analyze_index', scale='frequency',
                            datatype=list, value=hist_percent, label=bin_labels)

    # Print or plot the masked image
    _debug(visual=masked_array,
           filename=os.path.join(params.debug_outdir, str(params.device) + index_array.array_type + ".png"))
    # Store images
    outputs.images.append(analysis_image)

    return analysis_image
