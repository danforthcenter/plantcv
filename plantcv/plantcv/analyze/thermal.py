"""Analyzes the temperature values of objects in an image."""
import os
import numpy as np
from plantcv.plantcv import params, outputs
from plantcv.plantcv._debug import _debug
from plantcv.plantcv.visualize import histogram
from plantcv.plantcv._helpers import _iterate_analysis


def thermal(thermal_img, labeled_mask, n_labels=1, bins=100, label=None):
    """Analyzes the temperature values of objects in an image.

    Inputs:
    thermal_img  = Thermal image data.
    labeled_mask = Labeled mask of objects (32-bit).
    n_labels     = Total number expected individual objects (default = 1).
    bins         = Number of histogram bins (default = 100)
    label        = optional label parameter, modifies the variable name of observations recorded (default = "default").

    Returns:
    analysis_image = Thermal histogram plot

    :param thermal_img: numpy.ndarray
    :param labeled_mask: numpy.ndarray
    :param n_labels: int
    :param bins: int
    :param label: str
    :return analysis_image: altair.vegalite.v5.api.FacetChart
    """
    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label

    _ = _iterate_analysis(img=thermal_img, labeled_mask=labeled_mask, n_labels=n_labels, label=label,
                          function=_analyze_thermal,  **{"bins": bins})
    temp_chart = outputs.plot_dists(variable="thermal_frequencies")
    _debug(visual=temp_chart, filename=os.path.join(params.debug_outdir, str(params.device) + '_temperature_hist.png'))
    return temp_chart


def _analyze_thermal(img, mask, bins=100, label=None):
    """Extract the temperature values of an object in an image.

    Inputs:
    thermal_img  = numpy array of thermal values
    mask         = Binary mask made from selected contours
    bins         = Number of histogram bins (default = 100)
    label        = optional label parameter, modifies the variable name of observations recorded

    Returns:
    thermal_img  = output image

    :param thermal_array: numpy.ndarray
    :param mask: numpy.ndarray
    :param bins: int
    :param label: str
    :return thermal_img: numpy.ndarray
    """
    # Store debug mode
    debug = params.debug

    # apply plant shaped mask to image and calculate statistics based on the masked image
    masked_thermal = img[np.where(mask > 0)]
    maxtemp = np.amax(masked_thermal)
    mintemp = np.amin(masked_thermal)
    avgtemp = np.average(masked_thermal)
    mediantemp = np.median(masked_thermal)

    # call the histogram function
    params.debug = None
    _, hist_data = histogram(img, mask=mask, bins=bins, hist_data=True)
    bin_labels, hist_percent = hist_data['pixel intensity'].tolist(), hist_data['proportion of pixels (%)'].tolist()

    # Store data into outputs class
    outputs.add_observation(sample=label, variable='max_temp', trait='maximum temperature',
                            method='plantcv.plantcv.analyze.thermal', scale='degrees', datatype=float,
                            value=maxtemp, label='degrees')
    outputs.add_observation(sample=label, variable='min_temp', trait='minimum temperature',
                            method='plantcv.plantcv.analyze.thermal', scale='degrees', datatype=float,
                            value=mintemp, label='degrees')
    outputs.add_observation(sample=label, variable='mean_temp', trait='mean temperature',
                            method='plantcv.plantcv.analyze.thermal', scale='degrees', datatype=float,
                            value=avgtemp, label='degrees')
    outputs.add_observation(sample=label, variable='median_temp', trait='median temperature',
                            method='plantcv.plantcv.analyze.thermal', scale='degrees', datatype=float,
                            value=mediantemp, label='degrees')
    outputs.add_observation(sample=label, variable='thermal_frequencies', trait='thermal frequencies',
                            method='plantcv.plantcv.analyze.thermal', scale='frequency', datatype=list,
                            value=hist_percent, label=bin_labels)
    # Restore user debug setting
    params.debug = debug

    return img
