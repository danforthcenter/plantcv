"""Analyzes the X and Y spatial distribution of objects in an image."""
import os
import cv2
import numpy as np
from scipy import stats
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import outputs
from plantcv.plantcv.visualize import histogram
from plantcv.plantcv._helpers import _iterate_analysis


def distribution(labeled_mask, bin_size_x=100, bin_size_y=100, label=None):
    """A function that analyzes the X and Y distribution of objects and outputs data.

    Inputs:
    labeled_mask     = Labeled mask of objects (32-bit).
    bin_size_x       = Total number of desired bins for the histogram in the X direction
    bin_size_y       = Total number of desired bins for the histogram in the Y direction
    label            = Optional label parameter, modifies the variable name of
                       observations recorded (default = pcv.params.sample_label).

    Returns:
    distribution_image   = histogram output

    :param mask: numpy.ndarray
    :param bin_size_x: int
    :param bin_size_y: int
    :param label: str
    :return distribution_images: list
    """
    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label

    _ = _iterate_analysis(labeled_mask=labeled_mask, label=label, function=_analyze_distribution,
                          **{"bin_size_x": bin_size_x,"bin_size_y": bin_size_y})
    distribution_chart = outputs.plot_dists(variable="distribution_frequencies")
    _debug(visual=distribution_chart, filename=os.path.join(params.debug_outdir, str(params.device) + '_distribution_hist.png'))
    return distribution_chart


def _analyze_distribution(mask,  bin_size_x=100, bin_size_y=100, label=None):
    """Analyze the color properties of an image object
    Inputs:
    mask             = Binary mask made from selected contours
    bin_size_x       = Total number of desired bins for the histogram in the X direction
    bin_size_y       = Total number of desired bins for the histogram in the Y direction
    label            = optional label parameter, modifies the variable name of observations recorded

    Returns:
    distribution_image   = histogram output

    :param img: numpy.ndarray
    :param mask: numpy.ndarray
    :param bin_size_x: int
    :param bin_size_y: int
    :param label: str
    :return distribution_images: list
    """

    # Save user debug setting
    debug = params.debug
    params.debug = None

    # Initialize output data
    # find the height and width, in pixels, for this image
    height, width = mask.shape[:2]
    num_bins_y = height // bin_size_y
    num_bins_x = width // bin_size_x

    # Initialize output measurements
    Y_histogram = np.zeros(height // bin_size_y)
    X_histogram = np.zeros(width // bin_size_x)

    # Undefined defaults
    X_distribution_mean = np.nan
    X_distribution_median = np.nan
    X_distribution_std = np.nan
    Y_distribution_mean = np.nan
    Y_distribution_median = np.nan
    Y_distribution_std = np.nan

    # Skip empty masks
    if np.count_nonzero(mask) != 0:

        # Calculate histogram
        params.debug = None
        for y in range(0, height, bin_size_y):
            y_slice = mask[y:min(y+bin_size_y, height), :]
            white_pixels_y = np.sum(y_slice == 255)  # Count white pixels
            bin_index_y = min(y // bin_size_y, num_bins_y - 1)  # Ensure index within range
            Y_histogram[bin_index_y] = white_pixels_y

        for x in range(0, width, bin_size_x):
            x_slice = mask[y:min(x+bin_size_x, width), :]
            white_pixels_x = np.sum(x_slice == 255)  # Count white pixels
            bin_index_x = min(x // bin_size_x, num_bins_x - 1)  # Ensure index within range
            X_histogram[bin_index_x] = white_pixels_x

        # Restore user debug setting
        params.debug = debug

        # Determine the axes of the histograms
        y_axis = np.arange(len(Y_histogram)) * bin_size_y
        x_axis = np.arange(len(X_histogram)) * bin_size_x

        # Calculate the median X and Y value distribution
        X_distribution_median = np.median(x_axis)
        Y_distribution_median = np.median(y_axis)

        # Calculate the mean and standard deviation X and Y  value distribution
        X_distribution_mean = np.sum(X_histogram * x_axis) / np.sum(X_histogram)
        X_distribution_std = np.std(x_axis)
        Y_distribution_mean = np.sum(Y_histogram * y_axis) / np.sum(Y_histogram)
        Y_distribution_std = np.std(y_axis)

    #Save histograms
    outputs.add_observation(sample=label, variable='X_frequencies', trait='X frequencies',
                        method='plantcv.plantcv.analyze.distribution', scale='frequency', datatype=list,
                        value=X_histogram, label=x_axis)
    outputs.add_observation(sample=label, variable='Y_frequencies', trait='Y frequencies',
                         method='plantcv.plantcv.analyze.distribution', scale='frequency', datatype=list,
                        value=Y_histogram, label=y_axis)

    # Save average measurements
    outputs.add_observation(sample=label, variable='X_distribution_mean', trait='X distribution mean',
                            method='plantcv.plantcv.analyze.distribution', scale='pixels', datatype=float,
                            value=X_distribution_mean, label='pixel')
    outputs.add_observation(sample=label, variable='X_distribution_median', trait='X distribution median',
                            method='plantcv.plantcv.analyze.distribution', scale='pixel', datatype=float,
                            value=X_distribution_median, label='pixel')
    outputs.add_observation(sample=label, variable='X_distribution_std', trait='X distribution standard deviation',
                            method='plantcv.plantcv.analyze.distribution', scale='pixel', datatype=float,
                            value=X_distribution_std, label='pixel')
    outputs.add_observation(sample=label, variable='Y_distribution_mean', trait='Y distribution mean',
                            method='plantcv.plantcv.analyze.distribution', scale='pixels', datatype=float,
                            value=Y_distribution_mean, label='pixel')
    outputs.add_observation(sample=label, variable='Y_distribution_median', trait='Y distribution median',
                            method='plantcv.plantcv.analyze.distribution', scale='pixel', datatype=float,
                            value=Y_distribution_median, label='pixel')
    outputs.add_observation(sample=label, variable='Y_distribution_std', trait='Y distribution standard deviation',
                            method='plantcv.plantcv.analyze.distribution', scale='pixel', datatype=float,
                            value=Y_distribution_std, label='pixel')

    return mask
