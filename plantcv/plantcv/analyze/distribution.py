"""Analyzes the X and Y spatial distribution of objects in an image."""
import os
import numpy as np
from plantcv.plantcv import auto_crop, outputs, params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _iterate_analysis


def distribution(labeled_mask, n_labels=1, direction="down", bin_size=100, hist_range="absolute", label=None):
    """Analyze the distribution of objects along an axis of an image.

    Parameters
    ----------
    labeled_mask : numpy.ndarray
        Labeled mask of objects (32-bit).
    n_labels : int, optional
        Total number expected individual objects, by default 1
    direction : str, optional
        Image axis to calculate the distribution of object pixels ("down" or "across"), by default "down"
    bin_size : int, optional
        Histogram bin size in pixels, by default 100
    hist_range : str, optional
        The histogram range can be set to the image dimensions ("absolute") or "relative" to each object, by default "absolute"
    label : str or None, optional
        Optional label parameter, modifies the variable name of observations recorded, by default pcv.params.sample_label

    Returns
    -------
    alt.vegalite.v5.api.FacetChart
        Facet chart of the object distribution histograms
    """
    # Increment the device counter
    params.device += 1

    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label

    # If direction is "across" then swap the x and y axes
    axis = "y"
    if direction == "across":
        axis = "x"
        labeled_mask = np.swapaxes(labeled_mask, 0, 1)

    # Create combined mask as "img" for iterative analysis input
    img = np.where(labeled_mask > 0, 255, 0).astype(np.uint8)

    # Iterate over each labeled object and analyze the distribution
    _ = _iterate_analysis(img=img, labeled_mask=labeled_mask, n_labels=n_labels, label=label,
                          function=_analyze_distribution,
                          **{"bin_size": bin_size, "direction": axis, "hist_range": hist_range})

    # Plot distributions
    dist_chart = outputs.plot_dists(variable=f"{axis}_frequencies")
    # Add plot labels
    dist_chart = dist_chart.properties(title=f"{axis}-axis distribution")

    # Display or save the debug plot
    _debug(visual=dist_chart, filename=os.path.join(params.debug_outdir, f"{params.device}_{axis}_distribution_hist.png"))

    return dist_chart


def _analyze_distribution(img, mask, direction="y", bin_size=100, hist_range="absolute", label=None):
    """Analyze the color properties of an image object
    Inputs:
    mask             = Binary mask made from selected contours
    bin_size         = Size in pixels of the histogram bins
    label            = optional label parameter, modifies the variable name of observations recorded

    Returns:
    distribution_image   = histogram output

    :param img: numpy.ndarray
    :param mask: numpy.ndarray
    :param bin_size: int
    :param label: str
    :return distribution_images: list
    """
    # Image not needed
    img -= 0

    # Store debug
    debug = params.debug
    params.debug = None

    # Autocrop the mask if hist_range is "relative" to set the scale to the object size
    if hist_range == "relative" and np.count_nonzero(mask) != 0:
        mask = auto_crop(img=mask, mask=mask, padding_x=0, padding_y=0, color="black")

    # Initialize output data
    # find the height, in pixels, for this image
    height = mask.shape[0]
    num_bins = height // bin_size

    # Initialize output measurements
    hist = np.zeros(num_bins)  # Histogram of the distribution
    counts = []  # Weighted list of bin values to calculate the median bin
    mean_bin = 0  # Mean bin value
    median_bin = 0  # Median bin value
    dist_std = 0  # Standard deviation of the distribution
    bin_labels = np.arange(num_bins) * bin_size  # Labels for the bins (pixel position)

    # Skip empty masks
    if np.count_nonzero(mask) != 0:
        # Calculate histogram
        for i in range(0, height, bin_size):
            # Extract a slice from the mask the width of bin_size at each step
            mask_slice = mask[i:min(i+bin_size, height), :]
            count = np.count_nonzero(mask_slice)  # Count white pixels
            bin_index = min(i // bin_size, num_bins - 1)  # Ensure index within range
            hist[bin_index] += count  # Add count to the bin
            counts += [bin_index * bin_size] * count

        # Calculate the median value distribution
        median_bin = np.median(counts)

        # Calculate the mean and standard deviation X and Y  value distribution
        mean_bin = np.mean(counts)
        dist_std = np.std(counts)

    # Save histograms
    outputs.add_observation(sample=label, variable=f'{direction}_frequencies', trait=f'{direction} frequencies',
                            method='plantcv.plantcv.analyze.distribution', scale='frequency', datatype=list,
                            value=hist.tolist(), label=bin_labels.tolist())

    # Save average measurements
    outputs.add_observation(sample=label, variable=f'{direction}_distribution_mean',
                            trait=f'{direction} distribution mean',
                            method='plantcv.plantcv.analyze.distribution', scale='pixels', datatype=float,
                            value=mean_bin, label='pixel')
    outputs.add_observation(sample=label, variable=f'{direction}_distribution_median',
                            trait=f'{direction} distribution median',
                            method='plantcv.plantcv.analyze.distribution', scale='pixel', datatype=float,
                            value=median_bin, label='pixel')
    outputs.add_observation(sample=label, variable=f'{direction}_distribution_std',
                            trait=f'{direction} distribution standard deviation',
                            method='plantcv.plantcv.analyze.distribution', scale='pixel', datatype=float,
                            value=dist_std, label='pixel')
    # Restore debug
    params.debug = debug

    return mask
