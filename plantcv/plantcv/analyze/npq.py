"""Fluorescence Analysis (NPQ parameter)."""
import os
import numpy as np
import pandas as pd
import xarray as xr
from math import ceil, floor
from plantcv.plantcv import params, outputs, fatal_error
from plantcv.plantcv._debug import _debug
from plantcv.plantcv.photosynthesis import reassign_frame_labels


def npq(ps_da_light, ps_da_dark, labeled_mask, n_labels=1, auto_fm=False, min_bin=0, max_bin="auto",
        measurement_labels=None, label=None):
    """
    Calculate and analyze non-photochemical quenching estimates from fluorescence image data.

    Inputs:
    ps_da_light        = Photosynthesis xarray DataArray that contains frame_label `Fmp` (ojip_light)
    ps_da_dark         = Photosynthesis xarray DataArray that contains frame_label `Fm` (ojip_dark)
    labeled_mask       = Labeled mask of objects (32-bit).
    n_labels           = Total number expected individual objects (default = 1).
    auto_fm            = Automatically calculate the frame with maximum fluorescence per label, otherwise
                         use a fixed frame for all labels (default = False).
    min_bin            = minimum bin value ("auto" or user input minimum value - must be an integer)
    max_bin            = maximum bin value ("auto" or user input maximum value - must be an integer)
    measurement_labels = labels for each measurement in ps_da_light, modifies the variable name of observations recorded
    label              = Optional label parameter, modifies the variable name of
                         observations recorded (default = pcv.params.sample_label).

    Returns:
    npq_global         = DataArray of NPQ values
    npq_chart          = Histograms of NPQ estimates

    :param ps_da_light: xarray.core.dataarray.DataArray
    :param ps_da_dark: xarray.core.dataarray.DataArray
    :param labeled_mask: numpy.ndarray
    :param n_labels: int
    :param auto_fm: bool
    :param min_bin: int, str
    :param max_bin: int, str
    :param measurement_labels: list
    :param label: str
    :return npq_global: xarray.core.dataarray.DataArray
    :return npq_chart: altair.vegalite.v4.api.FacetChart
    """
    # Set labels
    labels = _set_labels(label, n_labels)

    if labeled_mask.shape != ps_da_light.shape[:2] or labeled_mask.shape != ps_da_dark.shape[:2]:
        fatal_error(f"Mask needs to have shape {ps_da_dark.shape[:2]}")

    if (measurement_labels is not None) and (len(measurement_labels) != ps_da_light.coords['measurement'].shape[0]):
        fatal_error('measurement_labels must be the same length as the number of measurements in `ps_da_light`')

    if ps_da_light.name.lower() != 'ojip_light' or ps_da_dark.name.lower() != 'ojip_dark':
        fatal_error(f"ps_da_light and ps_da_dark must be DataArrays with names 'ojip_light' and 'ojip_dark', "
                    f"respectively. Instead the inputs are: "
                    f"ps_da_light: {ps_da_light.name}, ps_da_dark: {ps_da_dark.name}"
                    )

    # Make an zeroed array of the same shape as the input DataArray
    npq_global = xr.zeros_like(ps_da_light, dtype=float)
    # Drop the frame_label coordinate
    npq_global = npq_global[:, :, 0, :].drop_vars('frame_label')

    # Make a copy of the labeled mask
    mask_copy = np.copy(labeled_mask)

    # If the labeled mask is a binary mask with values 0 and 255, convert to 0 and 1
    if len(np.unique(mask_copy)) == 2 and np.max(mask_copy) == 255:
        mask_copy = np.where(mask_copy == 255, 1, 0).astype(np.uint8)

    # Iterate over the label values 1 to n_labels
    for i in range(1, n_labels + 1):
        # Create a binary submask for each label
        submask = np.where(mask_copy == i, 255, 0).astype(np.uint8)

        # If auto_fm is True, reassign frame labels to choose the best Fm or Fm' for each labeled region
        if auto_fm:
            ps_da_light = reassign_frame_labels(ps_da=ps_da_light, mask=submask)
            ps_da_dark = reassign_frame_labels(ps_da=ps_da_dark, mask=submask)

        # Mask the Fm frame with the label submask
        fm = ps_da_dark.sel(measurement='t0', frame_label='Fm').where(submask > 0, other=0)
        # Calculate NPQ for the labeled region
        npq_lbl = ps_da_light.sel(frame_label='Fmp').groupby('measurement', squeeze=False).map(_calc_npq, fm=fm)

        # Drop the frame_label coordinate - not needed with xarray v2022.11.0+
        # npq_lbl = npq_lbl.drop_vars('frame_label')
        # Fill NaN values with 0 so that we can add DataArrays together
        npq_lbl = npq_lbl.fillna(0)
        # Add the NPQ values for this label to the NPQ DataArray
        npq_global = npq_global + npq_lbl

        # Record observations for each labeled region
        _add_observations(npq_da=npq_lbl, measurements=ps_da_light.measurement.values,
                          measurement_labels=measurement_labels, label=f"{labels[i - 1]}_{i}",
                          max_bin=max_bin, min_bin=min_bin)

    # Convert the labeled mask to a binary mask
    bin_mask = np.where(labeled_mask > 0, 255, 0)

    # Expand the binary mask to the same shape as the YII DataArray
    bin_mask = bin_mask[..., None]

    # Set the background values to NaN
    npq_global = npq_global.where(bin_mask > 0, other=np.nan)

    # drop coords identifying frames if they exist
    res = [i for i in list(npq_global.coords) if 'frame' in i]
    npq_global = npq_global.drop_vars(res)  # does not fail if res is []

    # Create a ridgeline plot of the NPQ values
    npq_chart = _ridgeline_plots(measurements=ps_da_light.measurement.values, measurement_labels=measurement_labels)

    # Plot/print dataarray
    _debug(visual=npq_global,
           filename=os.path.join(params.debug_outdir, str(params.device) + "_NPQ_dataarray.png"),
           col='measurement',
           col_wrap=int(np.ceil(npq_global.measurement.size / 4)),
           robust=True)

    # this only returns the last histogram..... xarray does not seem to support panels of histograms
    # but does support matplotlib subplots....
    return npq_global.squeeze(), npq_chart


def _set_labels(label, n_labels):
    """Create list of labels."""
    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label
    # Set labels to label
    labels = label
    # If label is a string, make a list of labels
    if isinstance(label, str):
        labels = [label] * n_labels
    # If the length of the labels list is not equal to the number of labels, raise an error
    if len(labels) != n_labels:
        fatal_error(f"Number of labels ({len(labels)}) does not match number of objects ({n_labels})")
    return labels


def _calc_npq(fmp, fm):
    """NPQ = Fm/Fmp - 1."""
    out_flt = np.ones(shape=fm.shape) * np.nan
    fmp = np.squeeze(fmp)
    where_arr = np.logical_and(fm > 0, np.logical_and(fmp > 0, fm > fmp))
    div = np.divide(fm, fmp, out=out_flt, where=where_arr.to_numpy())
    sub = np.subtract(div, 1, out=out_flt.copy(), where=div.to_numpy() >= 1)
    return sub


def _create_histogram(npq_img, mlabel, min_bin, max_bin):
    """
    Compute histogram of NPQ.

    Inputs:
    npq_img     = numpy array of npq
    mlabel      = measurement label
    min_bin     = minimum bin value
    max_bin     = maximum bin value

    Returns:
    hist_df   = Dataframe of histogram
    npq_mode  = which non-zero bin has the maximum Fv/Fm value

    :param npq_img: numpy.ndarray
    :param mlabel: str
    :param obs: dict
    :param min_bin: int
    :param max_bin: int
    :return hist_df: pandas.DataFrame
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

    # Convert the histogram pixel counts to proportional frequencies
    npq_percent = (npq_hist / float(np.sum(npq_hist))) * 100

    # Create a dataframe
    hist_df = pd.DataFrame({'proportion of pixels (%)': npq_percent, mlabel: npq_bins[:-1]})

    return hist_df, npq_mode


def _add_observations(npq_da, measurements, measurement_labels, label, max_bin, min_bin):
    """Add observations for each labeled region."""
    # Auto calculate max_bin if set
    if isinstance(max_bin, str) and (max_bin.upper() == "AUTO"):
        max_bin = ceil(np.nanmax(npq_da))  # Auto bins will detect the max value to use for calculating labels/bins
    if isinstance(min_bin, str) and (min_bin.upper() == "AUTO"):
        min_bin = floor(np.nanmin(npq_da))  # Auto bins will detect the min value to use for calculating labels/bins

    # compute observations to store in Outputs, per labeled region
    npq_mean = npq_da.where(npq_da > 0).groupby('measurement').mean(['x', 'y']).values
    npq_median = npq_da.where(npq_da > 0).groupby('measurement').median(['x', 'y']).values
    npq_max = npq_da.where(npq_da > 0).groupby('measurement').max(['x', 'y']).values

    # Create variables to label traits based on measurement label in data array
    for i, mlabel in enumerate(measurements):
        if measurement_labels is not None:
            mlabel = measurement_labels[i]

        # mean value
        outputs.add_observation(sample=label, variable=f"npq_mean_{mlabel}", trait="mean npq value",
                                method='plantcv.plantcv.analyze.npq', scale='none', datatype=float,
                                value=float(npq_mean[i]), label='none')
        # median value
        outputs.add_observation(sample=label, variable=f"npq_median_{mlabel}", trait="median npq value",
                                method='plantcv.plantcv.analyze.npq', scale='none', datatype=float,
                                value=float(npq_median[i]), label='none')
        # max value
        outputs.add_observation(sample=label, variable=f"npq_max_{mlabel}", trait="peak npq value",
                                method='plantcv.plantcv.analyze.npq', scale='none', datatype=float,
                                value=float(npq_max[i]), label='none')

        hist_df, npq_mode = _create_histogram(npq_da.isel({'measurement': i}).values, mlabel, min_bin, max_bin)

        # mode value
        outputs.add_observation(sample=label, variable=f"npq_mode_{mlabel}", trait="mode npq value",
                                method='plantcv.plantcv.analyze.npq', scale='none', datatype=float,
                                value=float(npq_mode), label='none')
        # hist frequencies
        outputs.add_observation(sample=label, variable=f"npq_hist_{mlabel}", trait="frequencies",
                                method='plantcv.plantcv.analyze.npq', scale='none', datatype=list,
                                value=hist_df['proportion of pixels (%)'].values.tolist(),
                                label=np.around(hist_df[mlabel].values.tolist(), decimals=2).tolist())


def _ridgeline_plots(measurements, measurement_labels):
    """Create ridgeline plots of NPQ values."""
    npq_chart = None
    for i, mlabel in enumerate(measurements):
        if measurement_labels is not None:
            mlabel = measurement_labels[i]
        npq_chart = outputs.plot_dists(variable=f"npq_hist_{mlabel}")
        _debug(visual=npq_chart, filename=os.path.join(params.debug_outdir, str(params.device) + '_npq_hist.png'))
    return npq_chart
