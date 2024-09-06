"""Analyzes spectral index values of objects in an image."""
import os
import numpy as np
from plantcv.plantcv import outputs, params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import fatal_error, warn
from plantcv.plantcv.visualize import histogram
from plantcv.plantcv._helpers import _iterate_analysis


def spectral_index(index_img, labeled_mask, n_labels=1, bins=100, min_bin=0, max_bin=1, label=None):
    """Analyze spectral index values of objects in an image.

    Inputs:
    index_img    = Index image data (PlantCV Spectral_data object)
    labeled_mask = Labeled mask of objects (32-bit).
    n_labels     = Total number expected individual objects (default = 1).
    bins         = Number of histogram bins (default = 100)
    min_bin      = Minimum bin value (default = 0). "auto" will use the minimum value of the index image.
    max_bin      = Maximum bin value (default = 1). "auto" will use the maximum value of the index image.
    label        = Optional label parameter, modifies the variable name of
                   observations recorded (default = pcv.params.sample_label).

    Returns:
    index_hist = Spectral index histogram plot

    :param index_img: plantcv.plantcv.Spectral_data
    :param labeled_mask: numpy.ndarray
    :param n_labels: int
    :param bins: int
    :param min_bin: float
    :param max_bin: float
    :param label: str
    :return index_hist: altair.vegalite.v5.api.FacetChart
    """
    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label

    _ = _iterate_analysis(img=index_img, labeled_mask=labeled_mask, n_labels=n_labels, label=label, function=_analyze_index,
                          **{"bins": bins, "min_bin": min_bin, "max_bin": max_bin})
    index_hist = outputs.plot_dists(variable=f"index_frequencies_{index_img.array_type}")
    _debug(visual=index_hist, filename=os.path.join(params.debug_outdir, str(params.device) + "_index_hist.png"))
    return index_hist


def _analyze_index(img, mask, bins=100, min_bin=0, max_bin=1, label=None):
    """This extracts the hyperspectral index statistics and writes the values  as observations out to
       the Outputs class.

    Inputs:
    img          = Instance of the Spectral_data class, usually the output from pcv.hyperspectral.extract_index
    mask         = Binary mask made from selected contours
    bins         = optional, number of classes to divide spectrum into
    min_bin      = optional, minimum bin value ("auto" or user input minimum value)
    max_bin      = optional, maximum bin value ("auto" or user input maximum value)
    label        = optional label parameter, modifies the variable name of observations recorded

    :param index_array: plantcv.plantcv.Spectral_data
    :param mask: numpy.ndarray
    :param bins: int
    :param max_bin: float, str
    :param min_bin: float, str
    :param label: str
    :return img: plantcv.plantcv.Spectral_data
    """
    debug = params.debug
    params.debug = None

    if len(np.shape(mask)) > 2 or len(np.unique(mask)) > 2:
        fatal_error("Mask should be a binary image of 0 and nonzero values.")

    if len(np.shape(img.array_data)) > 2:
        fatal_error("index_array data should be a grayscale image.")

    # Mask data and collect statistics about pixels within the masked image
    masked_array = img.array_data[np.where(mask > 0)]
    masked_array = masked_array[np.isfinite(masked_array)]

    index_mean = np.nanmean(masked_array)
    index_median = np.nanmedian(masked_array)
    index_std = np.nanstd(masked_array)

    # Set starting point and max bin values
    maxval = max_bin
    b = min_bin
    observed_max = 0
    observed_min = 0

    # Calculate observed min and max pixel values of the masked array
    if masked_array.any():
        observed_max = np.nanmax(masked_array)
        observed_min = np.nanmin(masked_array)

    # Auto calculate max_bin if set
    if type(max_bin) is str and (max_bin.upper() == "AUTO"):
        maxval = float(round(observed_max, 8))  # Auto bins will detect maxval to use for calculating labels/bins
    if type(min_bin) is str and (min_bin.upper() == "AUTO"):
        b = float(round(observed_min, 8))  # If bin_min is auto then overwrite starting value

    # Print a warning if observed min/max outside user defined range
    if observed_max > maxval or observed_min < b:
        warn(f"The observed range of pixel values in your masked index provided is [{str(observed_min)}"
             f", {str(observed_max)}] but the user defined range of bins for pixel frequencies is [{str(b)}, "
             f"{str(maxval)}]. Adjust min_bin and max_bin in order to avoid cutting off data being collected.")

    # Calculate histogram
    bin_labels, hist_percent = [], []
    if mask.any():
        _, hist_data = histogram(img.array_data, mask=mask, bins=bins, lower_bound=b, upper_bound=maxval,
                                 hist_data=True)
        bin_labels, hist_percent = hist_data["pixel intensity"].tolist(), hist_data["proportion of pixels (%)"].tolist()

    # Restore user debug setting
    params.debug = debug

    outputs.add_observation(sample=label, variable=f"mean_{img.array_type}", trait=f"Average {img.array_type} reflectance",
                            method="plantcv.plantcv.analyze.spectral_index", scale="reflectance", datatype=float,
                            value=float(index_mean), label="none")

    outputs.add_observation(sample=label, variable=f"med_{img.array_type}", trait=f"Median {img.array_type} reflectance",
                            method="plantcv.plantcv.analyze.spectral_index", scale="reflectance", datatype=float,
                            value=float(index_median), label="none")

    outputs.add_observation(sample=label, variable=f"std_{img.array_type}",
                            trait=f"Standard deviation {img.array_type} reflectance",
                            method="plantcv.plantcv.analyze.spectral_index", scale="reflectance", datatype=float,
                            value=float(index_std), label="none")

    outputs.add_observation(sample=label, variable=f"index_frequencies_{img.array_type}",
                            trait="index frequencies", method="plantcv.plantcv.analyze.spectral_index", scale="frequency",
                            datatype=list, value=hist_percent, label=bin_labels)
    return img
