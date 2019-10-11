# Analyze signal data in Thermal image

import os
import numpy as np
import pandas as pd
from plantcv.plantcv import params
from plantcv.plantcv import outputs
from plotnine import ggplot, aes, geom_line, scale_x_continuous


def analyze_spectral(array, header_dict, mask, histplot=True):
    """This extracts the hyperspectral reflectance values of each pixel writes the values out to
       a file. It can also print out a histogram plot of pixel intensity
       and a pseudocolor image of the plant.

    Inputs:
    array        = numpy array of thermal values
    header_dict  =
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

    # Store debug mode
    debug = params.debug
    params.debug = None

    # List of wavelengths recorded created from parsing the header file will be string, make list of floats
    wavelength_data = array[np.where(mask > 0)]
    wavelength_freq = wavelength_data.mean(axis=0)

    # Scale x-axis based on available wavelengths
    min_wavelength = int(np.ceil(float(header_dict["wavelength"][0])))
    max_wavelength = int(np.ceil(float(header_dict["wavelength"][-1])))

    new_wavelengths = []

    # Make a list of floats since they are parsed as strings
    for i in header_dict["wavelength"]:
        new_wavelengths.append(float(i))

    # Measure reflectance statistics
    max_reflectance = np.amax(wavelength_data)
    min_reflectance = np.amin(wavelength_data)
    mean_reflectance = np.average(wavelength_data)
    median_reflectance = np.median(wavelength_data)

    # Store data into outputs class
    outputs.add_observation(variable='max_reflectance', trait='maximum reflectance',
                            method='plantcv.plantcv.hyperspectral.analyze_spectral', scale='degrees', datatype=float,
                            value=max_reflectance, label='degrees')
    outputs.add_observation(variable='min_reflectance', trait='minimum reflectance',
                            method='plantcv.plantcv.hyperspectral.analyze_spectral', scale='degrees', datatype=float,
                            value=min_reflectance, label='degrees')
    outputs.add_observation(variable='mean_reflectance', trait='mean_reflectance',
                            method='plantcv.plantcv.hyperspectral.analyze_spectral', scale='degrees', datatype=float,
                            value=mean_reflectance, label='degrees')
    outputs.add_observation(variable='median_reflectance', trait='median_reflectance',
                            method='plantcv.plantcv.hyperspectral.analyze_spectral', scale='degrees', datatype=float,
                            value=median_reflectance, label='degrees')
    outputs.add_observation(variable='spectral_frequencies', trait='thermal spectral_frequencies',
                            method='plantcv.plantcv.hyperspectral.analyze_spectral', scale='frequency', datatype=list,
                            value=wavelength_freq, label=new_wavelengths)

    # Reset debugging mode
    params.debug = debug
    analysis_img = None

    # Create the histrogram if plotting is turned on
    if histplot is True:
        # Create the dataframe with histogram data
        dataset = pd.DataFrame({'Wavelength': new_wavelengths,
                                'Reflectance': wavelength_freq})
        # Make the histogram 
        fig_hist = (ggplot(data=dataset,
                           mapping=aes(x='Wavelength',
                                       y='Reflectance'))
                    + geom_line(color='purple')
                    + scale_x_continuous(breaks=list(range(min_wavelength, max_wavelength, 50)))
                    )

        analysis_img = fig_hist

        if params.debug == "print":
            fig_hist.save(os.path.join(params.debug_outdir, str(params.device) + '_therm_histogram.png'))
        elif params.debug == "plot":
            print(fig_hist)

    # Returns none and just stores data to output class if the histogram isn't created
    return analysis_img
