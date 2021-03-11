# Analyze signal data in Thermal image

import os
import cv2
import numpy as np
import pandas as pd
from plantcv.plantcv import params
from plantcv.plantcv import outputs
from plotnine import ggplot, aes, geom_line
from plantcv.plantcv.threshold import binary as binary_threshold


def analyze_thermal_values(thermal_array, mask, histplot=False, label="default"):
    """This extracts the thermal values of each pixel writes the values out to
       a file. It can also print out a histogram plot of pixel intensity
       and a pseudocolor image of the plant.

    Inputs:
    array        = numpy array of thermal values
    mask         = Binary mask made from selected contours
    histplot     = if True plots histogram of intensity values
    label        = optional label parameter, modifies the variable name of observations recorded

    Returns:
    analysis_img = output image

    :param thermal_array: numpy.ndarray
    :param mask: numpy.ndarray
    :param histplot: bool
    :param label: str
    :return analysis_img: ggplot
    """
    max_value = np.amax(thermal_array)
    # Calculate histogram
    hist_thermal = [float(i[0]) for i in cv2.calcHist([np.float32(thermal_array)], [0], mask, [256], [0, max_value])]
    bin_width = max_value / 256.
    b = 0
    bin_labels = [float(b)]
    for i in range(255):
        b += bin_width
        bin_labels.append(b)

    # Store debug mode
    debug = params.debug
    params.debug = None

    # apply plant shaped mask to image
    mask1 = binary_threshold(mask, 0, 255, 'light')
    params.debug = debug

    mask1 = (mask1 / 255)
    masked_thermal = thermal_array[np.where(mask > 0)]

    pixels = cv2.countNonZero(mask1)
    hist_percent = [(p / float(pixels)) * 100 for p in hist_thermal]

    maxtemp = np.amax(masked_thermal)
    mintemp = np.amin(masked_thermal)
    avgtemp = np.average(masked_thermal)
    mediantemp = np.median(masked_thermal)

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
    analysis_img = None

    if histplot is True:
        params.device += 1

        dataset = pd.DataFrame({'Temperature C': bin_labels,
                                'Proportion of pixels (%)': hist_percent})
        fig_hist = (ggplot(data=dataset,
                           mapping=aes(x='Temperature C',
                                       y='Proportion of pixels (%)'))
                    + geom_line(color='green'))

        analysis_img = fig_hist
        if params.debug == "print":
            fig_hist.save(os.path.join(params.debug_outdir, str(params.device) + '_therm_histogram.png'), verbose=False)
        elif params.debug == "plot":
            print(fig_hist)

    return analysis_img
