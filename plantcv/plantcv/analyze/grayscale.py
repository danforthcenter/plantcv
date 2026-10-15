"""Analyzes the grayscale values of objects in an image."""
import os
import numpy as np
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import params, outputs
from plantcv.plantcv._helpers import _iterate_objects


def grayscale(gray_img, labeled_mask, n_labels=1, bins=100, label=None):
    """Analyzes the grayscale values of a masked region of an image.

    Parameters
    ----------
    gray_img : numpy.ndarray
        8- or 16-bit grayscale image data.
    labeled_mask : numpy.ndarray
        Labeled mask of objects (32-bit).
    n_labels : int, default=1
        Total number of expected individual objects.
    bins : int, default=100
        Number of histogram bins.
    label : str, optional
        Label that modifies the variable name of recorded observations. Defaults
        to ``pcv.params.sample_label``.

    Returns
    -------
    analysis_image : altair.vegalite.v5.api.FacetChart
        Grayscale histogram image.
    """
    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label

    for sample, slices, obj_mask in _iterate_objects(labeled_mask=labeled_mask, n_labels=n_labels, label=label):
        _analyze_grayscale(img=gray_img, slices=slices, obj_mask=obj_mask, bins=bins, label=sample)
    gray_chart = outputs.plot_dists(variable="gray_frequencies")
    _debug(visual=gray_chart, filename=os.path.join(params.debug_outdir, str(params.device) + '_hue_hist.png'))
    return gray_chart


def _analyze_grayscale(img, slices, obj_mask, bins=100, label=None):
    """Analyzes the grayscale values of a masked region of an image.

    Parameters
    ----------
    img : numpy.ndarray
        8- or 16-bit grayscale image data.
    slices : tuple
        Bounding box of the object.
    obj_mask : numpy.ndarray
        Boolean mask of the object within the bounding box.
    bins : int, default=100
        Number of histogram bins.
    label : str, optional
        Label that modifies the variable name of recorded observations. Defaults
        to ``"default"``.
    """
    # Skip empty masks
    if np.count_nonzero(obj_mask) != 0:
        # calculate histogram
        if img.dtype == 'uint16':
            maxval = 65536
        else:
            maxval = 256

        # Object pixel values
        masked_array = img[slices][obj_mask]
        masked_gray_mean = np.average(masked_array)
        masked_gray_median = np.median(masked_array)
        masked_gray_std = np.std(masked_array)

        # Calculate histogram, using the middle value of every bin as the bin label
        hist_gray, bin_edges = np.histogram(masked_array, bins, (0, maxval))
        bin_labels = ((bin_edges[:-1] + bin_edges[1:]) / 2).tolist()
        hist_gray = hist_gray.tolist()

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
