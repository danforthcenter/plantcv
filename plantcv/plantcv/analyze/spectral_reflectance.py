"""Analyzes the spectral reflectance values of objects in an image."""
import os
import numpy as np
from plantcv.plantcv import outputs, params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _iterate_analysis


def spectral_reflectance(hsi, labeled_mask, n_labels=1, label=None):
    """Analyze spectral reflectance values of objects in an image.

    Inputs:
    hsi          = Hyperspectral image data
    labeled_mask = Labeled mask of objects (32-bit).
    n_labels     = Total number expected individual objects (default = 1).
    label        = Optional label parameter, modifies the variable name of observations recorded (default = "default").

    Returns:
    spectral_chart = Spectral reflectance plot.

    :param hsi: plantcv.plantcv.Spectral_data
    :param labeled_mask: numpy.ndarray
    :param n_labels: int
    :param label: str
    :return spectral_chart: altair.vegalite.v5.api.FacetChart
    """
    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label

    _ = _iterate_analysis(img=hsi, labeled_mask=labeled_mask, n_labels=n_labels, label=label, function=_analyze_spectral)
    spectral_chart = outputs.plot_dists(variable="wavelength_means")
    _debug(visual=spectral_chart, filename=os.path.join(params.debug_outdir, str(params.device) + '_mean_reflectance.png'))
    return spectral_chart


def _analyze_spectral(img, mask, label):
    """This extracts the hyperspectral reflectance values of each pixel.

    Inputs:
    img          = Hyperspectral data instance
    mask         = Binary mask made from selected contours
    label        = optional label parameter, modifies the variable name of observations recorded

    Returns:
    analysis_img = output image

    :param array: __main__.Spectral_data
    :param mask: numpy array
    :param histplot: bool
    :param label: str
    :return img: plantcv.plantcv.Spectral_data
    """
    array_data = img.array_data

    # List of wavelengths recorded created from parsing the header file will be string, make list of floats
    wavelength_data = array_data[np.where(mask > 0)]

    # Initialize analysis output values with zeros
    wavelength_means = np.full(len(img.wavelength_dict), 0)
    max_per_band = np.full(len(img.wavelength_dict), 0)
    min_per_band = np.full(len(img.wavelength_dict), 0)
    std_per_band = np.full(len(img.wavelength_dict), 0)

    avg_reflectance = 0
    std_reflectance = 0
    median_reflectance = 0

    # check if mask is empty and procees only if it is not
    if wavelength_data.size != 0:
        # Calculate mean reflectance across wavelengths
        wavelength_means = wavelength_data.mean(axis=0)
        max_per_band = wavelength_data.max(axis=0)
        min_per_band = wavelength_data.min(axis=0)
        std_per_band = wavelength_data.std(axis=0)

        # Calculate reflectance statistics
        avg_reflectance = np.average(wavelength_data)
        std_reflectance = np.std(wavelength_data)
        median_reflectance = np.median(wavelength_data)

    # Create lists with wavelengths in float format rather than as strings
    # and make a list of the frequencies since they are in an array
    new_wavelengths = []
    band_averages = []
    new_std_per_band = []
    new_max_per_band = []
    new_min_per_band = []

    for i, wavelength in enumerate(img.wavelength_dict):
        new_wavelengths.append(wavelength)
        band_averages.append((wavelength_means[i]).astype(float))
        new_std_per_band.append(std_per_band[i].astype(float))
        new_max_per_band.append(max_per_band[i].astype(float))
        new_min_per_band.append(min_per_band[i].astype(float))

    wavelength_labels = []
    for i in img.wavelength_dict.keys():
        wavelength_labels.append(i)

    # Store data into outputs class
    outputs.add_observation(sample=label, variable='global_mean_reflectance', trait='global mean reflectance',
                            method='plantcv.plantcv.analyze.spectral_reflectance', scale='reflectance',
                            datatype=float, value=float(avg_reflectance), label='reflectance')
    outputs.add_observation(sample=label, variable='global_median_reflectance', trait='global median reflectance',
                            method='plantcv.plantcv.analyze.spectral_reflectance', scale='reflectance',
                            datatype=float, value=float(median_reflectance), label='reflectance')
    outputs.add_observation(sample=label, variable='global_spectral_std',
                            trait='pixel-wise standard deviation per band',
                            method='plantcv.plantcv.analyze.spectral_reflectance', scale='None', datatype=float,
                            value=float(std_reflectance), label='reflectance')
    outputs.add_observation(sample=label, variable='wavelength_means', trait='mean reflectance per band',
                            method='plantcv.plantcv.analyze.spectral_reflectance', scale='reflectance', datatype=list,
                            value=band_averages, label=wavelength_labels)
    outputs.add_observation(sample=label, variable='max_reflectance', trait='maximum reflectance per band',
                            method='plantcv.plantcv.analyze.spectral_reflectance', scale='reflectance', datatype=list,
                            value=new_max_per_band, label=wavelength_labels)
    outputs.add_observation(sample=label, variable='min_reflectance', trait='minimum reflectance per band',
                            method='plantcv.plantcv.analyze.spectral_reflectance', scale='reflectance', datatype=list,
                            value=new_min_per_band, label=wavelength_labels)
    outputs.add_observation(sample=label, variable='spectral_std', trait='pixel-wise standard deviation per band',
                            method='plantcv.plantcv.analyze.spectral_reflectance', scale='None', datatype=list,
                            value=new_std_per_band, label=wavelength_labels)
    return img
