# Analyze signal data in Thermal image

import os
import cv2
import numpy as np
import pandas as pd
from plantcv.plantcv import params
from plantcv.plantcv import outputs
from plotnine import ggplot, aes, geom_line, scale_x_continuous
from plantcv.plantcv.threshold import binary as binary_threshold


def analyze_spectral(array, header_dict, mask, histplot=True):
    """This extracts the hyperspectral reflectance values of each pixel writes the values out to
       a file. It can also print out a histogram plot of pixel intensity
       and a pseudocolor image of the plant.

    Inputs:
    array        = numpy array of thermal values
    mask         = Binary mask made from selected contours
    histplot     = if True plots histogram of intensity values

    Returns:
    analysis_img = output image

    :param array: numpy array
    :param mask: numpy array
    :param histplot: bool
    :return analysis_img: str
    """
    params.device += 1

    # Store debug mode
    debug = params.debug
    params.debug = None

    wavelength_data = array[np.where(mask > 0)]
    wavelength_freq = wavelength_data.mean(axis=0)

    min_wavelength = int(np.ceil(float(header_dict["wavelength"][0])))
    max_wavelength = int(np.ceil(float(header_dict["wavelength"][-1])))

    new_wavelengths = []

    for i in header_dict["wavelength"]:
        new_wavelengths.append(float(i))

    ############
    dataset = pd.DataFrame({'Wavelength': new_wavelengths,
                            'Reflectance': wavelength_freq})
    fig_hist = (ggplot(data=dataset,
                       mapping=aes(x='Wavelength',
                                   y='Reflectance'))
                + geom_line(color='green')
                + scale_x_continuous(breaks=list(range(min_wavelength, max_wavelength, 50)))
                )

    maxtemp = np.amax(wavelength_data)
    mintemp = np.amin(wavelength_data)
    avgtemp = np.average(wavelength_data)
    mediantemp = np.median(wavelength_data)

    # Store data into outputs class
    outputs.add_observation(variable='max_reflectance', trait='maximum reflectance',
                            method='plantcv.plantcv.hyperspectral.analyze_spectral', scale='degrees', datatype=float,
                            value=maxtemp, label='degrees')
    outputs.add_observation(variable='min_reflectance', trait='minimum reflectance',
                            method='plantcv.plantcv.hyperspectral.analyze_spectral', scale='degrees', datatype=float,
                            value=mintemp, label='degrees')
    outputs.add_observation(variable='mean_reflectance', trait='mean_reflectance',
                            method='plantcv.plantcv.hyperspectral.analyze_spectral', scale='degrees', datatype=float,
                            value=avgtemp, label='degrees')
    outputs.add_observation(variable='median_reflectance', trait='median_reflectance',
                            method='plantcv.plantcv.hyperspectral.analyze_spectral', scale='degrees', datatype=float,
                            value=mediantemp, label='degrees')
    outputs.add_observation(variable='spectral_frequencies', trait='thermal spectral_frequencies',
                            method='plantcv.plantcv.hyperspectral.analyze_spectral', scale='frequency', datatype=list,
                            value=wavelength_freq, label=new_wavelengths)
    analysis_img = None

    params.debug = debug

    if histplot is True:
        dataset = pd.DataFrame({'Temperature C': bin_labels,
                                'Proportion of pixels (%)': hist_percent})
        fig_hist = (ggplot(data=dataset,
                           mapping=aes(x='Temperature C',
                                       y='Proportion of pixels (%)'))
                    + geom_line(color='green'))

        analysis_img = fig_hist
        if params.debug == "print":
            fig_hist.save(os.path.join(params.debug_outdir, str(params.device) + '_therm_histogram.png'))
        elif params.debug == "plot":
            print(fig_hist)

    return analysis_img
