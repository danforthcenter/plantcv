# Analyze reflectance signal hyperspectral images

import os
import numpy as np
import pandas as pd
from plantcv.plantcv import params
from plantcv.plantcv import outputs
from plotnine import ggplot, aes, geom_line, scale_x_continuous
from plantcv.plantcv import deprecation_warning
from plantcv.plantcv._debug import _debug


def analyze_spectral(array, mask, histplot=None, label="default"):
    """This extracts the hyperspectral reflectance values of each pixel writes the values out to
       a file. It can also print out a histogram plot of pixel intensity
       and a pseudocolor image of the plant.

    Inputs:
    array        = Hyperspectral data instance
    mask         = Binary mask made from selected contours
    histplot     = (to be deprecated) if True plots histogram of reflectance intensity values
    label        = optional label parameter, modifies the variable name of observations recorded

    Returns:
    analysis_img = output image

    :param array: __main__.Spectral_data
    :param mask: numpy array
    :param histplot: bool
    :param label: str
    :return analysis_img: ggplot
    """
    if histplot is not None:
        deprecation_warning("'histplot' will be deprecated in a future version of PlantCV. "
                            "Instead of a histogram this function plots the mean of spectra in the masked area.")

    array_data = array.array_data

    # List of wavelengths recorded created from parsing the header file will be string, make list of floats
    wavelength_data = array_data[np.where(mask > 0)]

    # Calculate mean reflectance across wavelengths
    wavelength_freq = wavelength_data.mean(axis=0)
    max_per_band = wavelength_data.max(axis=0)
    min_per_band = wavelength_data.min(axis=0)
    std_per_band = wavelength_data.std(axis=0)

    # Identify smallest and largest wavelengths available to scale the x-axis
    min_wavelength = array.min_wavelength
    max_wavelength = array.max_wavelength

    # Create lists with wavelengths in float format rather than as strings
    # and make a list of the frequencies since they are in an array
    new_wavelengths = []
    new_freq = []
    new_std_per_band = []
    new_max_per_band = []
    new_min_per_band = []

    for i, wavelength in enumerate(array.wavelength_dict):
        new_wavelengths.append(wavelength)
        new_freq.append((wavelength_freq[i]).astype(float))
        new_std_per_band.append(std_per_band[i].astype(float))
        new_max_per_band.append(max_per_band[i].astype(float))
        new_min_per_band.append(min_per_band[i].astype(float))

    # Calculate reflectance statistics
    avg_reflectance = np.average(wavelength_data)
    std_reflectance = np.std(wavelength_data)
    median_reflectance = np.median(wavelength_data)

    wavelength_labels = []
    for i in array.wavelength_dict.keys():
        wavelength_labels.append(i)

    # Store data into outputs class
    outputs.add_observation(sample=label, variable='global_mean_reflectance', trait='global mean reflectance',
                            method='plantcv.plantcv.hyperspectral.analyze_spectral', scale='reflectance',
                            datatype=float, value=float(avg_reflectance), label='reflectance')
    outputs.add_observation(sample=label, variable='global_median_reflectance', trait='global median reflectance',
                            method='plantcv.plantcv.hyperspectral.analyze_spectral', scale='reflectance',
                            datatype=float, value=float(median_reflectance), label='reflectance')
    outputs.add_observation(sample=label, variable='global_spectral_std',
                            trait='pixel-wise standard deviation per band',
                            method='plantcv.plantcv.hyperspectral.analyze_spectral', scale='None', datatype=float,
                            value=float(std_reflectance), label='reflectance')
    outputs.add_observation(sample=label, variable='global_spectral_std', trait='pixel-wise standard deviation ',
                            method='plantcv.plantcv.hyperspectral.analyze_spectral', scale='None', datatype=float,
                            value=float(std_reflectance), label='reflectance')
    outputs.add_observation(sample=label, variable='max_reflectance', trait='maximum reflectance per band',
                            method='plantcv.plantcv.hyperspectral.analyze_spectral', scale='reflectance', datatype=list,
                            value=new_max_per_band, label=wavelength_labels)
    outputs.add_observation(sample=label, variable='min_reflectance', trait='minimum reflectance per band',
                            method='plantcv.plantcv.hyperspectral.analyze_spectral', scale='reflectance', datatype=list,
                            value=new_min_per_band, label=wavelength_labels)
    outputs.add_observation(sample=label, variable='spectral_std', trait='pixel-wise standard deviation per band',
                            method='plantcv.plantcv.hyperspectral.analyze_spectral', scale='None', datatype=list,
                            value=new_std_per_band, label=wavelength_labels)
    outputs.add_observation(sample=label, variable='spectral_frequencies', trait='spectral frequencies',
                            method='plantcv.plantcv.hyperspectral.analyze_spectral', scale='frequency', datatype=list,
                            value=new_freq, label=wavelength_labels)

    dataset = pd.DataFrame({'Wavelength (' + array.wavelength_units + ')': new_wavelengths,
                            'Reflectance': wavelength_freq})
    mean_spectra = (ggplot(data=dataset,
                    mapping=aes(x='Wavelength (' + array.wavelength_units + ')', y='Reflectance'))
                    + geom_line(color='purple')
                    + scale_x_continuous(breaks=list(range(int(np.floor(min_wavelength)),
                                                           int(np.ceil(max_wavelength)), 50)))
                    )

    analysis_img = mean_spectra

    _debug(visual=mean_spectra, filename=os.path.join(params.debug_outdir, str(params.device) + "_mean_spectra.png"))

    return analysis_img
