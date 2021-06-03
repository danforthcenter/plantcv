# Analyze signal data in Thermal image

import os
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import outputs
from plotnine import labs
from plantcv.plantcv.visualize import histogram
from plantcv.plantcv import deprecation_warning
from plantcv.plantcv._debug import _debug


def analyze_thermal_values(thermal_array, mask, histplot=None, label="default"):
    """This extracts the thermal values of each pixel writes the values out to
       a file. It can also print out a histogram plot of pixel intensity
       and a pseudocolor image of the plant.

    Inputs:
    array        = numpy array of thermal values
    mask         = Binary mask made from selected contours
    histplot     = if True plots histogram of intensity values
    label        = optional label parameter, modifies the variable name of observations recorded

    Returns:
    analysis_image = output image

    :param thermal_array: numpy.ndarray
    :param mask: numpy.ndarray
    :param histplot: bool
    :param label: str
    :return analysis_image: ggplot
    """

    if histplot is not None:
        deprecation_warning("'histplot' will be deprecated in a future version of PlantCV. "
                            "This function creates a histogram by default.")

    # Store debug mode
    debug = params.debug

    # apply plant shaped mask to image and calculate statistics based on the masked image
    masked_thermal = thermal_array[np.where(mask > 0)]
    maxtemp = np.amax(masked_thermal)
    mintemp = np.amin(masked_thermal)
    avgtemp = np.average(masked_thermal)
    mediantemp = np.median(masked_thermal)

    # call the histogram function
    params.debug = None
    hist_fig, hist_data = histogram(thermal_array, mask=mask, hist_data=True)
    bin_labels, hist_percent = hist_data['pixel intensity'].tolist(), hist_data['proportion of pixels (%)'].tolist()

    # Store data into outputs class
    outputs.add_observation(sample=label, variable='max_temp', trait='maximum temperature',
                            method='plantcv.plantcv.analyze_thermal_values', scale='degrees', datatype=float,
                            value=maxtemp, label='degrees')
    outputs.add_observation(sample=label, variable='min_temp', trait='minimum temperature',
                            method='plantcv.plantcv.analyze_thermal_values', scale='degrees', datatype=float,
                            value=mintemp, label='degrees')
    outputs.add_observation(sample=label, variable='mean_temp', trait='mean temperature',
                            method='plantcv.plantcv.analyze_thermal_values', scale='degrees', datatype=float,
                            value=avgtemp, label='degrees')
    outputs.add_observation(sample=label, variable='median_temp', trait='median temperature',
                            method='plantcv.plantcv.analyze_thermal_values', scale='degrees', datatype=float,
                            value=mediantemp, label='degrees')
    outputs.add_observation(sample=label, variable='thermal_frequencies', trait='thermal frequencies',
                            method='plantcv.plantcv.analyze_thermal_values', scale='frequency', datatype=list,
                            value=hist_percent, label=bin_labels)
    # Restore user debug setting
    params.debug = debug

    # change column names of "hist_data"
    hist_fig = hist_fig + labs(x="Temperature C", y="Proportion of pixels (%)")

    # Print or plot histogram
    _debug(visual=hist_fig, filename=os.path.join(params.debug_outdir, str(params.device) + "_therm_histogram.png"))

    analysis_image = hist_fig
    # Store images
    outputs.images.append(analysis_image)

    return analysis_image
