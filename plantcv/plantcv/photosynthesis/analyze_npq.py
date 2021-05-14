# Fluorescence Analysis (NPQ parameter)

import os
import cv2
import numpy as np
import pandas as pd
from plotnine import ggplot, geom_label, aes, geom_line
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import params
from plantcv.plantcv import outputs


def analyze_npq(ps, mask, bins=256, label="default"):
    """Calculate and analyze NPQ from fluorescence image data.

    Inputs:
    ps          = photosynthesis xarray DataArray
    mask        = mask of plant (binary, single channel)
    bins        = number of bins (1 to 256 for 8-bit; 1 to 65,536 for 16-bit; default is 256)
    label       = optional label parameter, modifies the variable name of observations recorded

    Returns:
    npq_hist_fig = NPQ histogram figure
    npq          = NPQ image

    :param ps: xarray.core.dataarray.DataArray
    :param mask: numpy.ndarray
    :param bins: int
    :param label: str
    :return npq_hist_fig: plotnine.ggplot.ggplot
    :return npq: numpy.ndarray
    """

    # Extract frames of interest
    fmp = ps.sel(frame_label=ps.attrs["Fm'"]).data
    fm = ps.sel(frame_label=ps.attrs["Fm"]).data

    # Mask Fm and Fm' images
    fmp_masked = cv2.bitwise_and(fmp, fmp, mask=mask)
    fm_masked = cv2.bitwise_and(fm, fm, mask=mask)

    # Change masked images to 64-bit float
    fmp_masked = fmp_masked.astype(np.float64)
    fm_masked = fm_masked.astype(np.float64)

    # Calculate NQP (Fm / Fm') - 1
    npq = np.divide(fm_masked, fmp_masked)
    npq[np.where(fmp_masked == 0)] = 0
    npq -= 1

    # Calculate the median Fv/Fm value for non-zero pixels
    npq_median = np.median(npq[np.where(npq > 0)])

    # Calculate the histogram of NPQ non-zero values
    npq_hist, npq_bins = np.histogram(npq[np.where(npq > 0)], bins, range=(0, 1))
    # npq_bins is a bins + 1 length list of bin endpoints, so we need to calculate bin midpoints so that
    # the we have a one-to-one list of x (NPQ) and y (frequency) values.
    # To do this we add half the bin width to each lower bin edge x-value
    midpoints = npq_bins[:-1] + 0.5 * np.diff(npq_bins)

    # Calculate which non-zero bin has the maximum NPQ value
    max_bin = midpoints[np.argmax(npq_hist)]

    # Create a dataframe
    dataset = pd.DataFrame({'Plant Pixels': npq_hist, 'NPQ': midpoints})
    # Make the histogram figure using plotnine
    npq_hist_fig = (ggplot(data=dataset, mapping=aes(x='NPQ', y='Plant Pixels'))
                     + geom_line(color='green', show_legend=True)
                     + geom_label(label='Peak Bin Value: ' + str(max_bin),
                                  x=.15, y=205, size=8, color='green'))

    _debug(visual=npq_hist_fig, filename=os.path.join(params.debug_outdir, str(params.device) + "_NPQ_histogram.png"))

    outputs.add_observation(sample=label, variable='npq_hist', trait='NPQ frequencies',
                            method='plantcv.plantcv.photosynthesis.analyze_npq', scale='none', datatype=list,
                            value=npq_hist.tolist(), label=np.around(midpoints, decimals=len(str(bins))).tolist())
    outputs.add_observation(sample=label, variable='npq_hist_peak', trait='peak NPQ value',
                            method='plantcv.plantcv.photosynthesis.analyze_npq', scale='none', datatype=float,
                            value=float(max_bin), label='none')
    outputs.add_observation(sample=label, variable='npq_median', trait='NPQ median',
                            method='plantcv.plantcv.photosynthesis.analyze_npq', scale='none', datatype=float,
                            value=float(np.around(npq_median, decimals=4)), label='none')

    # Store images
    outputs.images.append(npq_hist_fig)

    return npq_hist_fig, npq
