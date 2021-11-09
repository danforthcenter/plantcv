# Fluorescence Analysis (NPQ parameter)

import os
import numpy as np
import pandas as pd
from math import ceil, floor
from plotnine import ggplot, aes, geom_line, geom_point, theme, scale_color_brewer
from plotnine.labels import labs
from plantcv.plantcv import fatal_error
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import params
from plantcv.plantcv import outputs


def analyze_npq(ps_da_light, ps_da_dark, mask, min_bin=0, max_bin="auto", measurement_labels=None, label="default"):
    """
    Calculate and analyze non-photochemical quenching estimates from fluorescence image data.

    Inputs:
    ps_da_light        = photosynthesis xarray DataArray for which to compute npq
    ps_da_dark         = photosynthesis xarray DataArray that contains frame_label `Fm`
    mask               = mask of plant (binary, single channel)
    min_bin            = minimum bin value ("auto" or user input minimum value - must be an integer)
    max_bin            = maximum bin value ("auto" or user input maximum value - must be an integer)
    measurement_labels = labels for each measurement in ps_da_light, modifies the variable name of observations recorded
    label              = optional label parameter, modifies the entity name of observations recorded

    Returns:
    npq       = DataArray of npq values
    hist_fig  = Histogram of npq estimate

    :param ps_da_light: xarray.core.dataarray.DataArray
    :param ps_da_dark: xarray.core.dataarray.DataArray
    :param mask: numpy.ndarray
    :param min_bin: int, str
    :param max_bin: int, str
    :param measurement_labels: list
    :param label: str
    :return npq: xarray.core.dataarray.DataArray
    :return hist_fig: plotnine.ggplot.ggplot
    """
    if mask.shape != ps_da_light.shape[:2] or mask.shape != ps_da_dark.shape[:2]:
        fatal_error(f"Mask needs to have shape {ps_da_dark.shape[:2]}")

    if len(np.unique(mask)) > 2 or mask.dtype != 'uint8':
        fatal_error("Mask must have dtype uint8 and be binary")

    if (measurement_labels is not None) and (len(measurement_labels) != ps_da_light.coords['measurement'].shape[0]):
        fatal_error('measurement_labels must be the same length as the number of measurements in `ps_da_light`')

    fm = ps_da_dark.sel(measurement='t0', frame_label='Fm').where(mask > 0, other=0)
    npq = ps_da_light.sel(frame_label='Fmp').groupby('measurement', squeeze=False).map(_calc_npq, fm=fm)

    # Auto calculate max_bin if set
    if isinstance(max_bin, str) and (max_bin.upper() == "AUTO"):
        max_bin = ceil(np.nanmax(npq))  # Auto bins will detect the max value to use for calculating labels/bins
    if isinstance(min_bin, str) and (min_bin.upper() == "AUTO"):
        min_bin = floor(np.nanmin(npq))  # Auto bins will detect the min value to use for calculating labels/bins

    # compute observations to store in Outputs
    npq_mean = npq.where(npq > 0).groupby('measurement').mean(['x', 'y']).values
    npq_median = npq.where(npq > 0).groupby('measurement').median(['x', 'y']).values
    npq_max = npq.where(npq > 0).groupby('measurement').max(['x', 'y']).values

    # Create variables to label traits based on measurement label in data array
    for i, mlabel in enumerate(ps_da_light.measurement.values):
        if measurement_labels is not None:
            mlabel = measurement_labels[i]

        # mean value
        outputs.add_observation(sample=label, variable=f"npq_mean_{mlabel}", trait="mean npq value",
                                method='plantcv.plantcv.photosynthesis.analyze_npq', scale='none', datatype=float,
                                value=float(npq_mean[i]), label='none')
        # median value
        outputs.add_observation(sample=label, variable=f"npq_median_{mlabel}", trait="median npq value",
                                method='plantcv.plantcv.photosynthesis.analyze_npq', scale='none', datatype=float,
                                value=float(npq_median[i]), label='none')
        # max value
        outputs.add_observation(sample=label, variable=f"npq_max_{mlabel}", trait="peak npq value",
                                method='plantcv.plantcv.photosynthesis.analyze_npq', scale='none', datatype=float,
                                value=float(npq_max[i]), label='none')

        hist_df, hist_fig, npq_mode = _create_histogram(npq.isel({'measurement': i}).values, mlabel,
                                                        outputs.observations[label], min_bin, max_bin)

        # mode value
        outputs.add_observation(sample=label, variable=f"npq_mode_{mlabel}", trait="mode npq value",
                                method='plantcv.plantcv.photosynthesis.analyze_npq', scale='none', datatype=float,
                                value=float(npq_mode), label='none')
        # hist frequencies
        outputs.add_observation(sample=label, variable=f"npq_hist_{mlabel}", trait="frequencies",
                                method='plantcv.plantcv.photosynthesis.analyze_npq', scale='none', datatype=list,
                                value=hist_df['Plant Pixels'].values.tolist(),
                                label=np.around(hist_df[mlabel].values.tolist(), decimals=2).tolist())

        # Plot/Print out the histograms
        _debug(visual=hist_fig,
               filename=os.path.join(params.debug_outdir, str(params.device) + f"_NPQ_{mlabel}_histogram.png"))

    # drop coords identifying frames if they exist
    res = [i for i in list(npq.coords) if 'frame' in i]
    npq = npq.drop_vars(res)  # does not fail if res is []

    # Store images
    outputs.images.append(npq)

    # Plot/print dataarray
    _debug(visual=npq,
           filename=os.path.join(params.debug_outdir, str(params.device) + "_NPQ_dataarray.png"),
           col='measurement',
           col_wrap=int(np.ceil(npq.measurement.size / 4)),
           robust=True)

    # this only returns the last histogram..... xarray does not seem to support panels of histograms
    # but does support matplotlib subplots....
    return npq, hist_fig


def _calc_npq(fmp, fm):
    """NPQ = Fm/Fmp - 1"""

    out_flt = np.ones(shape=fm.shape) * np.nan
    fmp = np.squeeze(fmp)
    div = np.divide(fm, fmp, out=out_flt,
                    where=np.logical_and(fm > 0, np.logical_and(fmp > 0, fm > fmp)))
    sub = np.subtract(div, 1, out=out_flt.copy(),
                      where=div >= 1)
    return sub


def _create_histogram(npq_img, mlabel, obs, min_bin, max_bin):
    """
    Compute histogram of NPQ

    Inputs:
    npq_img     = numpy array of npq
    mlabel      = measurement label
    obs         = PlantCV observations used to retrieve statistics
    min_bin     = minimum bin value
    max_bin     = maximum bin value

    Returns:
    hist_fig  = Histogram of efficiency estimate
    npq_img   = DataArray of efficiency estimate values

    :param npq_img: numpy.ndarray
    :param mlabel: str
    :param obs: dict
    :param min_bin: int
    :param max_bin: int
    :return hist_df: pandas.DataFrame
    :return hist_fig: plotnine.ggplot.ggplot
    :return npq_mode: float
    """

    # Calculate the histogram of NPQ non-zero values
    npq_hist, npq_bins = np.histogram(npq_img[np.where(npq_img > 0)], 100, range=(min_bin, max_bin))
    # npq_bins is a bins + 1 length list of bin endpoints, so we need to calculate bin midpoints so that
    # the we have a one-to-one list of x (NPQ) and y (frequency) values.
    # To do this we add half the bin width to each lower bin edge x-value
    # midpoints = npq_bins[:-1] + 0.5 * np.diff(npq_bins)

    # Calculate which non-zero bin has the maximum Fv/Fm value
    npq_mode = npq_bins[np.argmax(npq_hist)]

    # Create a dataframe
    hist_df = pd.DataFrame({'Plant Pixels': npq_hist, mlabel: npq_bins[:-1]})

    # Round values for plotting
    bin_width = np.around((max_bin - min_bin) / 100, decimals=2)
    bins = np.around(npq_bins, decimals=2)
    round_mean = np.around(obs[f"npq_mean_{mlabel}"]["value"], decimals=2)
    round_median = np.around(obs[f"npq_median_{mlabel}"]["value"], decimals=2)
    round_mode = np.around(npq_mode, decimals=2)
    mean_index = bins.tolist().index(np.around(round_mean - (round_mean % bin_width), decimals=2))
    median_index = bins.tolist().index(np.around(round_median - (round_median % bin_width), decimals=2))
    mode_index = np.argmax(npq_hist)
    # Create a dataframe for the statistics
    stats_df = pd.DataFrame({'Plant Pixels': [npq_hist[mean_index], npq_hist[median_index], npq_hist[mode_index]],
                             mlabel: [round_mean, round_median, round_mode],
                             "Stat": ["mean", "median", "mode"]})

    # Make the histogram figure using plotnine
    hist_fig = (ggplot(data=hist_df, mapping=aes(x=mlabel, y='Plant Pixels'))
                + geom_line(show_legend=True, color="darkblue")
                + geom_point(data=stats_df, mapping=aes(color='Stat'))
                + labs(title=f"measurement: {mlabel}",
                       x='nonphotochemical quenching (npq)')
                + theme(subplots_adjust={"right": 0.8})
                + scale_color_brewer(type="qual", palette=2))

    return hist_df, hist_fig, npq_mode
