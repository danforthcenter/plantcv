# Analyze signal data in Thermal image

import os
import cv2
import numpy as np
import pandas as pd
from plantcv.plantcv import outputs
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
#from plantcv.plantcv import plot_colorbar
from plantcv.plantcv.threshold import binary as binary_threshold
from plotnine import ggplot, aes, geom_line, scale_x_continuous
from plantcv.plantcv import apply_mask
from plantcv.plantcv import params


def analyze_thermal_values(rgb_img, array, mask, minrange, maxrange, histplot=False):
    """This extracts the thermal values of each pixel writes the values out to
       a file. It can also print out a histogram plot of pixel intensity
       and a pseudocolor image of the plant.

    Inputs:
    rgb_img      = rgb image to create pseudocolored img
    array        = numpy array of thermal values
    mask         = Binary mask made from selected contours
    histplot     = if True plots histogram of intensity values

    Returns:
    hist_header  = thermal histogram data table headers
    hist_data    = thermal histogram data table values
    analysis_img = output image

    :param rgb_img: numpy array
    :param array: numpy array
    :param mask: numpy array
    :param histplot: bool
    :return analysis_img: str
    """
    params.device += 1

    # apply plant shaped mask to image
    mask1 = binary_threshold(mask, 0, 255, 'light')
    mask1 = (mask1 / 255)
    masked = np.multiply(mask1, array)
    nonzero = masked[np.nonzero(masked)]

    if maxrange:
        hist_therm, hist_bins = np.histogram(nonzero, range=(minrange, maxrange))
    else:
        hist_therm, hist_bins = np.histogram(nonzero, range=(np.amin(array), np.amax(array)))
    maxtemp = np.amax(nonzero)
    mintemp = np.amin(nonzero)
    avgtemp = np.average(nonzero)
    mediantemp = np.median(nonzero)

    hist_bins1 = hist_bins[:-1]
    hist_bins2 = [l for l in hist_bins1]

    hist_therm1 = [l for l in hist_therm]

    # make hist percentage for plotting
    pixels = cv2.countNonZero(mask1)
    hist_percent = (hist_therm / float(pixels)) * 100

    # Store data into outputs class
    outputs.add_observation(variable='max_temp', trait='maximum temperature',
                            method='plantcv.plantcv.analyze_thermal_values', scale='degrees', datatype=int,
                            value=maxtemp, label='degrees')
    outputs.add_observation(variable='min_temp', trait='minimum temperature',
                            method='plantcv.plantcv.analyze_thermal_values', scale='degrees', datatype=int,
                            value=mintemp, label='degrees')
    outputs.add_observation(variable='average_temp', trait='average temperature',
                            method='plantcv.plantcv.analyze_thermal_values', scale='degrees', datatype=int,
                            value=avgtemp, label='degrees')
    outputs.add_observation(variable='median', trait='median temperature',
                            method='plantcv.plantcv.analyze_thermal_values', scale='degrees', datatype=int,
                            value=mediantemp, label='degrees')
    outputs.add_observation(variable='thermal_frequencies', trait='thermal frequencies',
                            method='plantcv.plantcv.analyze_thermal_values', scale='frequency', datatype=list,
                            value=hist_therm1, label=hist_bins2)
    analysis_img = []

    # make mask to select the background
    mask_inv = cv2.bitwise_not(mask)
    img_back = cv2.bitwise_and(rgb_img, rgb_img, mask=mask_inv)
    img_back1 = cv2.applyColorMap(img_back, colormap=1)

    # mask the background and color the plant with color scheme 'jet'
    cplant = cv2.applyColorMap(rgb_img, colormap=2)
    masked1 = apply_mask(cplant, mask, 'black')
    cplant_back = cv2.add(masked1, img_back1)
    analysis_img.append(cplant_back)

    if params.debug is not None:
        if params.debug == "print":
            print_image(masked1, os.path.join(params.debug_outdir, str(params.device) + "_therm_pseudo_plant.jpg"))
            print_image(cplant_back,
                        os.path.join(params.debug_outdir, str(params.device) + "_therm_pseudo_plant_back.jpg"))
        if params.debug == "plot":
            plot_image(masked1)
            plot_image(cplant_back)

    if histplot is True:
        dataset = pd.DataFrame({'Signal intensity': hist_bins2,
                                'Proportion of pixels (%)': hist_therm1})
        fig_hist = (ggplot(data=dataset,
                           mapping=aes(x='Tempurature C',
                                       y='Proportion of pixels (%)'))
                    + geom_line(color='green')
                    + scale_x_continuous(breaks=list(range(0, maxtemp, 25))))

        analysis_img.append(fig_hist)
        if params.debug == "print":
            fig_hist.save(os.path.join(params.debug_outdir, str(params.device) + '_nir_hist.png'))
        elif params.debug == "plot":
            print(fig_hist)

    return analysis_img
