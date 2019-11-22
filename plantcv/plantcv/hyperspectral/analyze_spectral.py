# Analyze reflectance signal hyperspectral images

import os
import numpy as np
import pandas as pd
from plantcv.plantcv import params
from plantcv.plantcv import outputs
from plotnine import ggplot, aes, geom_line, scale_x_continuous


def analyze_spectral(array, mask, histplot=True):
    """This extracts the hyperspectral reflectance values of each pixel writes the values out to
       a file. It can also print out a histogram plot of pixel intensity
       and a pseudocolor image of the plant.

    Inputs:
    array        = Hyperspectral data instance
    mask         = Binary mask made from selected contours
    histplot     = if True plots histogram of reflectance intensity values

    Returns:
    analysis_img = output image

    :param array: __main__.Spectral_data
    :param mask: numpy array
    :param histplot: bool
    :return analysis_img: ggplot
    """
    params.device += 1

    # Store debug mode
    debug = params.debug
    params.debug = None

    array_data = array.array_data

    # List of wavelengths recorded created from parsing the header file will be string, make list of floats
    wavelength_data = array_data[np.where(mask > 0)]

    # Calculate mean reflectance across wavelengths
    wavelength_freq = wavelength_data.mean(axis=0)

    # Identify smallest and largest wavelengths available to scale the x-axis
    min_wavelength = array.min_wavelength
    max_wavelength = array.max_wavelength

    # Create lists with wavelengths in float format rather than as strings
    # and make a list of the frequencies since they are in an array
    new_wavelengths = []
    new_freq = []

    for i, wavelength in enumerate(array.wavelength_dict):
        new_wavelengths.append(wavelength)
        new_freq.append((wavelength_freq[i]).astype(np.float))

    # Calculate reflectance statistics
    max_reflectance = np.amax(wavelength_data)
    min_reflectance = np.amin(wavelength_data)
    avg_reflectance = np.average(wavelength_data)
    median_reflectance = np.median(wavelength_data)

    wavelength_labels = []
    for i in array.wavelength_dict.keys():
        wavelength_labels.append(i)

    # Store data into outputs class
    outputs.add_observation(variable='max_reflectance', trait='maximum reflectance',
                            method='plantcv.plantcv.hyperspectral.analyze_spectral', scale='reflectance', datatype=float,
                            value=float(max_reflectance), label='reflectance')
    outputs.add_observation(variable='min_reflectance', trait='minimum reflectance',
                            method='plantcv.plantcv.hyperspectral.analyze_spectral', scale='reflectance', datatype=float,
                            value=float(min_reflectance), label='reflectance')
    outputs.add_observation(variable='mean_reflectance', trait='mean_reflectance',
                            method='plantcv.plantcv.hyperspectral.analyze_spectral', scale='reflectance', datatype=float,
                            value=float(avg_reflectance), label='reflectance')
    outputs.add_observation(variable='median_reflectance', trait='median_reflectance',
                            method='plantcv.plantcv.hyperspectral.analyze_spectral', scale='reflectance', datatype=float,
                            value=float(median_reflectance), label='reflectance')
    outputs.add_observation(variable='spectral_frequencies', trait='spectral frequencies',
                            method='plantcv.plantcv.hyperspectral.analyze_spectral', scale='frequency', datatype=list,
                            value=new_freq, label=wavelength_labels)

    params.debug = debug
    analysis_img = None

    if histplot is True:
        dataset = pd.DataFrame({'Wavelength ('+ array.wavelength_units+')': new_wavelengths,
                                'Reflectance': wavelength_freq})
        fig_hist = (ggplot(data=dataset,
                           mapping=aes(x='Wavelength ('+ array.wavelength_units+')',
                                       y='Reflectance'))
                    + geom_line(color='purple')
                    + scale_x_continuous(
                    breaks=list(range(int(np.floor(min_wavelength)), int(np.ceil(max_wavelength)), 50)))
                    )

        analysis_img = fig_hist

        if params.debug == "print":
            fig_hist.save(os.path.join(params.debug_outdir, str(params.device) + '_spectral_histogram.png'))
        elif params.debug == "plot":
            print(fig_hist)

    return analysis_img
