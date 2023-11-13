"""Analyzes the grayscale values of objects in an image."""
import os
import numpy as np
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import params, outputs
from plantcv.plantcv.visualize import histogram
from plantcv.plantcv._helpers import _iterate_analysis


def grayscale(gray_img, labeled_mask, n_labels=1, bins=100, label=None):
    """Analyzes the grayscale values of a masked region of an image.

    Inputs:
    gray_img     = 8- or 16-bit grayscale image data.
    labeled_mask = Labeled mask of objects (32-bit).
    n_labels     = Total number expected individual objects (default = 1).
    bins         = Number of histogram bins.
    label        = Optional label parameter, modifies the variable name of
                   observations recorded (default = pcv.params.sample_label).

    Returns:
    analysis_image = Grayscale histogram image

    :param gray_img: numpy.ndarray
    :param labeled_mask: numpy.ndarray
    :param n_labels: int
    :param bins: int
    :param label: str
    :return analysis_image: altair.vegalite.v5.api.FacetChart
    """
    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label

    _ = _iterate_analysis(img=gray_img, labeled_mask=labeled_mask, n_labels=n_labels, label=label, function=_analyze_grayscale,
                          **{"bins": bins})
    gray_chart = outputs.plot_dists(variable="gray_frequencies")
    _debug(visual=gray_chart, filename=os.path.join(params.debug_outdir, str(params.device) + '_hue_hist.png'))
    return gray_chart


def _analyze_grayscale(img, mask, bins=100, label=None):
    """Analyzes the grayscale values of a masked region of an image.

    Inputs:
    img          = 8- or 16-bit grayscale image data.
    mask         = Labeled mask of objects (32-bit).
    bins         = Number of histogram bins.
    label        = optional label parameter, modifies the variable name of observations recorded (default = "default")

    Returns:
    img          = Input image

    :param gray_img: numpy.ndarray
    :param mask: numpy.ndarray
    :param bins: int
    :param label: str
    :return img: numpy.ndarray
    """
    # Save user debug setting
    debug = params.debug
    params.debug = None

    # Initialize output measurements
    hist_gray = [0] * bins
    bin_labels = list(range(0, bins))
    masked_gray_mean = 0
    masked_gray_median = 0
    masked_gray_std = 0

    # Skip empty masks
    if np.count_nonzero(mask) != 0:
        # calculate histogram
        if img.dtype == 'uint16':
            maxval = 65536
        else:
            maxval = 256

        masked_array = img[np.where(mask > 0)]
        masked_gray_mean = np.average(masked_array)
        masked_gray_median = np.median(masked_array)
        masked_gray_std = np.std(masked_array)

        # Calculate histogram
        _, hist_data = histogram(img, mask=mask, bins=bins, lower_bound=0, upper_bound=maxval, title=None,
                                 hist_data=True)

        bin_labels, hist_gray = hist_data["pixel intensity"].tolist(), hist_data['hist_count'].tolist()

        outputs.add_observation(sample=label, variable='gray_frequencies', trait='grayscale frequencies',
                                method='plantcv.plantcv.analyze.grayscale', scale='frequency', datatype=list,
                                value=hist_gray, label=bin_labels)
        outputs.add_observation(sample=label, variable='gray_mean', trait='grayscale mean',
                                method='plantcv.plantcv.analyze.grayscale', scale='none', datatype=float,
                                value=masked_gray_mean, label='none')
        outputs.add_observation(sample=label, variable='gray_median', trait='grayscale median',
                                method='plantcv.plantcv.analyze.grayscale', scale='none', datatype=float,
                                value=masked_gray_median, label='none')
        outputs.add_observation(sample=label, variable='gray_stdev', trait='grayscale standard deviation',
                                method='plantcv.plantcv.analyze.grayscale', scale='none', datatype=float,
                                value=masked_gray_std, label='none')
    # Restore user debug setting
    params.debug = debug

    return img
