# Fluorescence Analysis (NPQ parameter)

import os
import xarray as xr
import numpy as np
import pandas as pd
from plotnine import ggplot, geom_label, aes, geom_line
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import params
from plantcv.plantcv import outputs


def _calc_npq(Fmp, Fm):
    return(Fm/Fmp - 1)

def analyze_npq(data, mask, bins=256, label="default"):
    """Calculate and analyze NPQ from fluorescence image data.
    Inputs:
    data        = x-array of binary image data
    mask        = mask of plant (binary, single channel)
    bins        = number of bins (1 to 256 for 8-bit; 1 to 65,536 for 16-bit; default is 256)
    label       = optional label parameter, modifies the variable name of observations recorded

    Returns:
    analysis_images = list of images (fv image and fvfm histogram image)
    :param data: xarray.core.dataarray.DataArray
    :param mask: numpy.ndarray
    :param bins: int
    :param label: str
    :return npq_hist_fig: plotnine.ggplot.ggplot
    """

    # Auto-increment the device counter
    params.device += 1
    npq = xr.apply_ufunc(_calc_npq,
                      data.sel(frame_label='Fmp'),
                      data.sel(frame_label='fmax'))

    # Calculate the median Fv/Fm value for non-zero pixels
    npq_median = np.median(npq[np.where(npq > 0)])

    # Calculate the histogram of Fv/Fm non-zero values
    npq_hist, npq_bins = np.histogram(npq[np.where(npq > 0)], bins, range=(0, 1))
    # fvfm_bins is a bins + 1 length list of bin endpoints, so we need to calculate bin midpoints so that
    # the we have a one-to-one list of x (FvFm) and y (frequency) values.
    # To do this we add half the bin width to each lower bin edge x-value
    midpoints = npq_bins[:-1] + 0.5 * np.diff(npq_bins)

    # Calculate which non-zero bin has the maximum Fv/Fm value
    max_bin = midpoints[np.argmax(npq_hist)]

    # Create a dataframe
    dataset = pd.DataFrame({'Plant Pixels': npq_hist, 'Fv/Fm': midpoints})
    # Make the histogram figure using plotnine
    npq_hist_fig = (ggplot(data=dataset, mapping=aes(x='Fv/Fm', y='Plant Pixels'))
                     + geom_line(color='green', show_legend=True)
                     + geom_label(label='Peak Bin Value: ' + str(max_bin),
                                  x=.15, y=205, size=8, color='green'))

    _debug(visual=npq, filename=os.path.join(params.debug_outdir, str(params.device) + "_FvFm.png"))
    _debug(visual=npq_hist_fig, filename=os.path.join(params.debug_outdir, str(params.device) + "_FvFm_histogram.png"))

    outputs.add_observation(sample=label, variable='npq_hist', trait='NPQ frequencies',
                            method='plantcv.plantcv.photosynthesis.analyze_npq', scale='none', datatype=list,
                            value=npq_hist.tolist(), label=np.around(midpoints, decimals=len(str(bins))).tolist())
    outputs.add_observation(sample=label, variable='npq_hist_peak', trait='peak NPQ value',
                            method='plantcv.plantcv.photosynthesis.analyze_npq', scale='none', datatype=float,
                            value=float(max_bin), label='none')
    outputs.add_observation(sample=label, variable='npq_median', trait='NPQ median',
                            method='plantcv.plantcv.photosynthesis.analyze_npq', scale='none', datatype=float,
                            value=float(np.around(npq_median, decimals=4)), label='none')
#

    # Store images
    outputs.images.append(npq_hist_fig)

    return npq_hist_fig