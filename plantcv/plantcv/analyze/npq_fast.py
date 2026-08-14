"""Fast Fluorescence Analysis (NPQ without dark measurements)"""
import os
import re
import numpy as np
import xarray as xr
from math import ceil, floor
from plantcv.plantcv import params, outputs, fatal_error
from plantcv.plantcv._debug import _debug
from plantcv.plantcv.analyze.npq import _set_labels, _make_var, _create_histogram, _ridgeline_plots


def npqfast(ps, labeled_mask, n_labels=1, min_bin=0, max_bin="auto", measurement_labels=None, label=None):
    """
    Calculate and analyze non-photochemical quenching estimates from fluorescence image data.

    Parameters:
    -----------
    ps                 = plantcv.plantcv.classes.PSII_Data,
        Object containing ojip_light data or PSL/PMT/PML data.
    labeled_mask       = numpy.ndarray,
        Labeled mask of objects (32-bit).
    n_labels           = int,
        Total number expected individual objects (default = 1).
    auto_fm            = bool,
        Automatically calculate the frame with maximum fluorescence per label, otherwise
        use a fixed frame for all labels (default = False).
    min_bin            = int, str
        minimum bin value ("auto" or user input minimum value - must be an integer)
    max_bin            = int, str
        maximum bin value ("auto" or user input maximum value - must be an integer)
    measurement_labels = list,
        labels for each measurement in ps, modifies the variable name of observations recorded
    label              = str,
        Optional label parameter, modifies the variable name of
        observations recorded (default = pcv.params.sample_label).

    Returns:
    --------
    npq_global         = list of xarray.core.dataarray.DataArray,
        NPQ values, one element per light input frame
    npq_chart          = list of altair.vegalite.v4.api.FacetChart,
        Histograms of NPQ estimates, one element per light input frame
    """
    # Set labels
    labels = _set_labels(label, n_labels)

    ps_da_lights = _get_light_frames(ps)
    npq_globals = []
    npq_charts = []

    for ps_da_light in ps_da_lights:
        if labeled_mask.shape != ps_da_light.shape[:2]:
            fatal_error(f"Mask needs to have shape {ps_da_light.shape[:2]}")
        if (measurement_labels is not None) and (len(measurement_labels) != ps_da_light.coords['measurement'].shape[0]):
            fatal_error(f'measurement_labels (len {len(measurement_labels)}) ' +
                        'must be the same length as the number of measurements in `ps_da_light`' +
                        f'({ps_da_light.measurement.shape[0]})')

        # Make an zeroed array of the same shape as the input DataArray
        npq_global = xr.zeros_like(ps_da_light.sel(frame_label="F0p"), dtype=float)
        # Drop the frame_label coordinate
        npq_global = npq_global.drop_vars('frame_label')

        # Make a copy of the labeled mask
        mask_copy = np.copy(labeled_mask)

        # If the labeled mask is a binary mask with values 0 and 255, convert to 0 and 1
        if len(np.unique(mask_copy)) <= 2 and np.max(mask_copy) == 255:
            mask_copy = np.where(mask_copy == 255, 1, 0).astype(np.uint8)

        # Iterate over the label values 1 to n_labels
        for i in range(1, n_labels + 1):
            # Create a binary submask for each label
            submask = np.where(mask_copy == i, 255, 0).astype(np.uint8)

            # Mask the Fm frame with the label submask
            first_meas = str(ps_da_light.measurement[0].values)
            f0p = ps_da_light.sel(measurement=first_meas,
                                  frame_label="F0p", drop=True).where(submask > 0, other=0)
            # Calculate NPQ fast
            fmp_var = str(ps_da_light.frame_label.values[ps_da_light.frame_label.str.match("Fmp+")][0])
            npq_lbl = ps_da_light.sel(
                frame_label=ps_da_light.frame_label.str.match(
                    'Fmp+'
                )).groupby('measurement', squeeze=False).map(_calc_npq_fast, f0p=f0p)
            # drop frame label
            npq_lbl = npq_lbl.drop_vars('frame_label')
            # Fill NaN values with 0 so that we can add DataArrays together
            npq_lbl = npq_lbl.squeeze('frame_label').fillna(0)
            # Add the NPQ values for this label to the NPQ DataArray
            npq_global = npq_global + npq_lbl

            # Record observations for each labeled region
            _add_fast_observations(npq_da=npq_lbl, measurements=ps_da_light.measurement.values,
                                   measurement_labels=measurement_labels, label=f"{labels[i - 1]}_{i}",
                                   max_bin=max_bin, min_bin=min_bin, fmp_trait=fmp_var)

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
        npq_globals.append(npq_global.squeeze())
        npq_charts.append(npq_chart)

        # Plot/print dataarray
        _debug(visual=npq_global,
               filename=os.path.join(params.debug_outdir, str(params.device) + "_NPQ_dataarray.png"),
               col='measurement',
               col_wrap=int(np.ceil(npq_global.measurement.size / 4)),
               robust=True)

    return npq_globals, npq_charts


def _add_fast_observations(npq_da, measurements, measurement_labels, label, max_bin, min_bin, fmp_trait="Fmp"):
    """Add observations for each labeled region."""
    # default to standard labeling, only add label if >1 prime
    fmp_trait = fmp_trait.strip("Fmp")
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
        var = _make_var(["npqfast", "mean", mlabel, fmp_trait])
        outputs.add_observation(sample=label, variable=var, trait="npqfast mean value",
                                method='plantcv.plantcv.analyze.npqfast', scale='none', datatype=float,
                                value=float(npq_mean[i]), label='none')
        # median value
        var = _make_var(["npqfast", "median", mlabel, fmp_trait])
        outputs.add_observation(sample=label, variable=var, trait="npqfast median value",
                                method='plantcv.plantcv.analyze.npqfast', scale='none', datatype=float,
                                value=float(npq_median[i]), label='none')
        # max value
        var = _make_var(["npqfast", "max", mlabel, fmp_trait])
        outputs.add_observation(sample=label, variable=var, trait="peak npqfast value",
                                method='plantcv.plantcv.analyze.npqfast', scale='none', datatype=float,
                                value=float(npq_max[i]), label='none')

        hist_df, npq_mode = _create_histogram(npq_da.isel({'measurement': i}).values, mlabel, min_bin, max_bin)

        # mode value
        var = _make_var(["npqfast", "mode", mlabel, fmp_trait])
        outputs.add_observation(sample=label, variable=var, trait="mode npqfast value",
                                method='plantcv.plantcv.analyze.npqfast', scale='none', datatype=float,
                                value=float(npq_mode), label='none')
        # hist frequencies
        var = _make_var(["npqfast", "hist", mlabel, fmp_trait])
        outputs.add_observation(sample=label, variable=var, trait="frequencies",
                                method='plantcv.plantcv.analyze.npqfast', scale='none', datatype=list,
                                value=hist_df['proportion of pixels (%)'].values.tolist(),
                                label=np.around(hist_df[mlabel].values.tolist(), decimals=2).tolist())


def _calc_npq_fast(fmp, f0p):
    """NPQ_fast = 4.88 / (Fmp / F0p - 1) - 1"""
    out_flt = np.ones(shape=fmp.shape) * np.nan
    f0p = np.squeeze(f0p)
    where_arr = np.logical_and(fmp > 0, np.logical_and(f0p > 0, fmp > f0p))
    div = 4.88 / (np.divide(fmp, f0p, out=out_flt, where=where_arr) - 1)
    sub = div - 1
    return sub


def _get_light_frames(ps):
    """Get light frames from classes in a PSII_data object

    Parameters
    ----------
    ps = plantcv.plantcv.classes.PSII_data,
        PSII_data object with npq, pml, psl, or pmt frames

    Returns
    -------
    ps_da_lights = list of xarray.core.dataarray.DataArray
        light measurements, potentially >1 length if multiple were taken
    """
    if ps.pmt is not None:
        p = ps.pmt.pam_time
        all_non_fmp_frames = [str(f.values) for f in p.frame_label if not re.search("Fmp+", str(f))]
        all_fmp_frames = [str(f.values) for f in p.frame_label if re.search("Fmp+", str(f))]
        ps_da_lights = []
        for f in all_fmp_frames:
            labels_to_check = all_non_fmp_frames + [f]
            ps_da_lights.append(p.sel(frame_label=p.frame_label.isin(labels_to_check)))
    else:
        fatal_error(
            "ps must have ojip_light DataArrays from psl, pml, " +
            "or npq images or pmt (pam time) measurements"
        )
    return ps_da_lights
