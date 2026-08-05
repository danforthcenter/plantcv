"""Fluorescence Analysis (Fv/Fm parameter)."""
import os
import numpy as np
import pandas as pd
import xarray as xr
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import params, outputs, fatal_error
from plantcv.plantcv.photosynthesis import reassign_frame_labels


def yii(ps, labeled_mask, n_labels=1, auto_fm=False, measurement_labels=None, label=None):
    """Calculate and analyze PSII efficiency estimates from fluorescence image data.

    Parameters
    ----------
    ps                  = plantcv.plantcv.classes.PSII_data
        Photosynthesis data as read by plantcv.plantcv.photosynthesis.read_cropreporter
        Will analyze PSD (photosynthesis/ojip dark) and PSL (photosynthesis/ojip light)
        if present.
    labeled_mask        = numpy.ndarray,
        Labeled mask of objects (32-bit).
    n_labels            = int,
        Total number expected individual objects (default = 1).
    auto_fm             = boolean,
        Automatically calculate the frame with maximum fluorescence per label, otherwise
        use a fixed frame for all labels (default = False).
    measurement_labels  = list,
        labels for each measurement, modifies the variable name of observations recorded
    label               = str,
        optional label parameter, modifies the variable name of observations recorded

    Returns
    -------
    yii_global          = list of xarray.core.dataarray.DataArray,
        DataArray of efficiency estimate values
    yii_chart           = list of altair.vegalite.v4.api.FacetChart,
        Histograms of efficiency estimate
    """
    # Set labels
    labels = _set_labels(label, n_labels)

    # Validate that the input mask has the same 2D shape as the input DataArray
    ps_shape = (int(ps.metadata["ImageRows"]), int(ps.metadata["ImageCols"]))
    if labeled_mask.shape != ps_shape:
        fatal_error(f"Mask needs to have shape {ps_shape}")

    if getattr(ps, "pmt", None) is None:
        frame_functions = {
            "psl": {"ojip_light": _psl_calc_fqfm},
            "psd": {"ojip_dark": _psd_calc_fvfm},
            "pml": {"pam_light": _psl_calc_fqfm},
            "pmd": {"pam_dark": _psd_calc_fvfm},
            "npq": {"ojip_light": _psl_calc_fqfm, "ojip_dark": _psd_calc_fvfm}
        }
        frame_properties = {
            "psl": ["ojip_light"],
            "psd": ["ojip_dark"],
            "pml": ["pam_light"],
            "pmd": ["pam_dark"],
            "npq": ["ojip_light", "ojip_dark"]
        }
        frames = ["psl", "psd", "pml", "pmd", "npq"]
        yii_globals, yii_charts = _yii_single(ps, labeled_mask,
                                              frame_functions, frame_properties,
                                              frames, n_labels, auto_fm,
                                              measurement_labels, labels)
    else:
        yii_globals, yii_charts = _yii_multi(ps, labeled_mask,
                                             n_labels, measurement_labels, labels)

    return yii_globals, yii_charts


def _yii_multi(ps, labeled_mask,
               n_labels=1, measurement_labels=None, labels=None):
    """Calculate and analyze PSII efficiency estimates from pam time fluorescence image data.

    Parameters
    ----------
    ps                  = plantcv.plantcv.classes.PSII_data
        Photosynthesis data as read by plantcv.plantcv.photosynthesis.read_cropreporter
        Will analyze PMT (pam time) data.
    labeled_mask        = numpy.ndarray,
        Labeled mask of objects (32-bit).
    n_labels            = int,
        Total number expected individual objects (default = 1).
    measurement_labels  = list,
        labels for each measurement, modifies the variable name of observations recorded
    labels              = list,
        optional label parameter, modifies the variable name of observations recorded

    Returns
    -------
    yii_global          = list of xarray.core.dataarray.DataArray,
        DataArray of efficiency estimate values
    yii_chart           = list of altair.vegalite.v4.api.FacetChart,
        Histograms of efficiency estimate
    """
    yii_charts_fvfm = []
    yii_globals_fvfm = []
    yii_charts_fqfm = []
    yii_globals_fqfm = []
    yii_charts_fvfm_pp = []
    yii_globals_fvfm_pp = []

    ps_da = ps.pmt.pam_time
    # Validate that the input measurement_labels is the same length as the number of measurements in the DataArray
    if (measurement_labels is not None) and (len(measurement_labels) != ps_da.coords['measurement'].shape[0]):
        fatal_error('measurement_labels must be the same length as the number of measurements in the DataArray')
    # Make an zeroed array of the same shape as the input DataArray
    yii_global_fvfm = xr.zeros_like(ps_da, dtype=float)
    yii_global_fqfm = xr.zeros_like(ps_da, dtype=float)
    yii_global_fvfm_pp = xr.zeros_like(ps_da, dtype=float)
    # Drop the frame_label coordinate
    yii_global_fvfm = yii_global_fvfm[:, :, 0, :].drop_vars('frame_label')
    yii_global_fqfm = yii_global_fqfm[:, :, 0, :].drop_vars('frame_label')
    yii_global_fvfm_pp = yii_global_fvfm_pp[:, :, 0, :].drop_vars('frame_label')
    # Make a copy of the labeled mask
    mask_copy = np.copy(labeled_mask)
    # If the labeled mask is a binary mask with values 0 and 255, convert to 0 and 1
    if len(np.unique(mask_copy)) <= 2 and np.max(mask_copy) == 255:
        mask_copy = np.where(mask_copy == 255, 1, 0).astype(np.uint8)
    # Convert the labeled mask to a binary mask
    bin_mask = np.where(labeled_mask > 0, 255, 0)
    # Expand the binary mask to the same shape as the YII DataArray
    bin_mask = bin_mask[..., None]
    # Iterate over the label values 1 to n_labels
    for i in range(1, n_labels + 1):
        # Create a binary submask for each label
        submask = np.where(mask_copy == i, 255, 0).astype(np.uint8)
        # Expand the submask to the same shape as the input DataArray
        submask = submask[..., None, None]
        # Mask the input DataArray with the submask
        yii_masked = ps_da.astype('float').where(submask > 0, other=np.nan)

        # Calculate Fv/Fm
        yii_fvfm = _psd_calc_fvfm(yii_masked)
        yii_fvfm = yii_fvfm.drop_vars('frame_label')
        yii_fvfm = yii_fvfm.fillna(0)
        yii_global_fvfm = yii_global_fvfm + yii_fvfm
        _add_observations(
                yii_da=yii_fvfm,
                measurements=ps_da.measurement.values,
                label=f"{labels[i - 1]}_{i}",
                measurement_labels=measurement_labels,
                yii_trait="fvfm"
        )
        # Set the background values to NaN
        yii_global_fvfm = yii_global_fvfm.where(bin_mask > 0, other=np.nan)
        # drop coords identifying frames if they exist
        res = [i for i in list(yii_global_fvfm.coords) if 'frame' in i]
        yii_global_fvfm = yii_global_fvfm.drop_vars(res)  # does not fail if res is []
        # Create a ridgeline plot of the YII values
        yii_chart_fvfm = _ridgeline_plots(
            measurements=ps_da.measurement.values,
            measurement_labels=measurement_labels,
            yii_trait="fvfm")
        yii_charts_fvfm.append(yii_chart_fvfm)
        yii_globals_fvfm.append(yii_global_fvfm)

        # Calculate Fq'/Fm' series
        yii_fqfm = _psl_calc_fqfm(yii_masked)
        yii_fqfm = yii_fqfm.drop_vars('frame_label')
        yii_fqfm = yii_fqfm.fillna(0)
        yii_global_fqfm = yii_global_fqfm + yii_fvfm
        _add_observations(
                yii_da=yii_fqfm,
                measurements=ps_da.measurement.values,
                label=f"{labels[i - 1]}_{i}",
                measurement_labels=measurement_labels,
                yii_trait="fqfm"
        )
        # Set the background values to NaN
        yii_global_fqfm = yii_global_fqfm.where(bin_mask > 0, other=np.nan)
        # drop coords identifying frames if they exist
        res = [i for i in list(yii_global_fqfm.coords) if 'frame' in i]
        yii_global_fqfm = yii_global_fqfm.drop_vars(res)
        # Create a ridgeline plot of the YII values
        yii_chart_fqfm = _ridgeline_plots(
            measurements=ps_da.measurement.values,
            measurement_labels=measurement_labels,
            yii_trait="fqfm")
        yii_charts_fqfm.append(yii_chart_fqfm)
        yii_globals_fqfm.append(yii_global_fqfm)

        # Calculate Fv''/Fm'' if exists
        if yii_masked.frame_label.str.contains("pp").any():
            yii_fvfm_pp = _psd_calc_fvfm_double_prime(yii_masked)
            yii_fvfm_pp = yii_fvfm_pp.drop_vars('frame_label')
            yii_fvfm_pp = yii_fvfm_pp.fillna(0)
            yii_global_fvfm_pp = yii_global_fvfm_pp + yii_fvfm_pp
            _add_observations(
                yii_da=yii_fvfm_pp,
                measurements=ps_da.measurement.values,
                label=f"{labels[i - 1]}_{i}",
                measurement_labels=measurement_labels,
                yii_trait="fvfmpp"
            )
            # Set the background values to NaN
            yii_global_fvfm_pp = yii_global_fvfm_pp.where(bin_mask > 0, other=np.nan)
            # drop coords identifying frames if they exist
            res = [i for i in list(yii_global_fvfm_pp.coords) if 'frame' in i]
            yii_global_fvfm_pp = yii_global_fvfm_pp.drop_vars(res)
            # Create a ridgeline plot of the YII values
            yii_chart_fvfm_pp = _ridgeline_plots(
                measurements=ps_da.measurement.values,
                measurement_labels=measurement_labels,
                yii_trait="fvfmpp")
            yii_charts_fvfm_pp.append(yii_chart_fvfm_pp)
            yii_globals_fvfm_pp.append(yii_global_fvfm_pp)

    yii_globals = [yii_global_fvfm, yii_global_fqfm]
    yii_charts = [yii_charts_fvfm, yii_charts_fqfm]
    if ps_da.frame_label.str.contains("pp").any():
        yii_globals = [yii_global_fvfm, yii_global_fqfm, yii_global_fvfm_pp]
        yii_charts = [yii_charts_fvfm, yii_charts_fqfm, yii_charts_fvfm_pp]

    return yii_globals, yii_charts


def _yii_single(ps, labeled_mask,
                frame_functions, frame_properties, frames,
                n_labels=1, auto_fm=False, measurement_labels=None, labels=None):
    """Calculate and analyze PSII efficiency estimates from fluorescence image data.

    Parameters
    ----------
    ps                  = plantcv.plantcv.classes.PSII_data
        Photosynthesis data as read by plantcv.plantcv.photosynthesis.read_cropreporter
        Will analyze PSD (photosynthesis/ojip dark) and PSL (photosynthesis/ojip light)
        if present.
    labeled_mask        = numpy.ndarray,
        Labeled mask of objects (32-bit).
    frame_functions     = dict
        Dictionary of helper functions named for the frame they are made to work with
    frame_properties    = dict
        Dictionary of property names for frames to access xarray/data objects
    frames              = list
        list of frames to iterate over
    n_labels            = int,
        Total number expected individual objects (default = 1).
    auto_fm             = boolean,
        Automatically calculate the frame with maximum fluorescence per label, otherwise
        use a fixed frame for all labels (default = False).
    measurement_labels  = list,
        labels for each measurement, modifies the variable name of observations recorded
    labels              = list,
        optional label parameter, modifies the variable name of observations recorded

    Returns
    -------
    yii_global          = list of xarray.core.dataarray.DataArray,
        DataArray of efficiency estimate values
    yii_chart           = list of altair.vegalite.v4.api.FacetChart,
        Histograms of efficiency estimate
    """
    # Validate that ps has the right frames with information in them
    _validate_psii_yii_frames(ps)

    yii_charts = []
    yii_globals = []
    # check for the presence of each frame
    for frame in frames:
        # for every frame that is populated in the data, keep going
        if getattr(ps, frame) is not None:
            # npq has multiple properties, loop over the list (generally 1L)
            for frame_prop in frame_properties.get(frame):
                ps_da_loader = getattr(ps, frame)
                ps_da = getattr(ps_da_loader, frame_prop)
                # Validate that the input measurement_labels is the same length as the number of measurements in the DataArray
                if (measurement_labels is not None) and (len(measurement_labels) != ps_da.coords['measurement'].shape[0]):
                    fatal_error('measurement_labels must be the same length as the number of measurements in the DataArray')
                # Make an zeroed array of the same shape as the input DataArray
                yii_global = xr.zeros_like(ps_da, dtype=float)
                # Drop the frame_label coordinate
                yii_global = yii_global[:, :, 0, :].drop_vars('frame_label')
                # Make a copy of the labeled mask
                mask_copy = np.copy(labeled_mask)
                # If the labeled mask is a binary mask with values 0 and 255, convert to 0 and 1
                if len(np.unique(mask_copy)) <= 2 and np.max(mask_copy) == 255:
                    mask_copy = np.where(mask_copy == 255, 1, 0).astype(np.uint8)
                # Iterate over the label values 1 to n_labels
                for i in range(1, n_labels + 1):
                    # Create a binary submask for each label
                    submask = np.where(mask_copy == i, 255, 0).astype(np.uint8)
                    # Expand the submask to the same shape as the input DataArray
                    submask = submask[..., None, None]
                    # If auto_fm is True, reassign frame labels to choose the best Fm or Fm' for each labeled region
                    if auto_fm:
                        ps_da = reassign_frame_labels(ps_da=ps_da, mask=submask.squeeze().squeeze())
                    # Mask the input DataArray with the submask
                    yii_masked = ps_da.astype('float').where(submask > 0, other=np.nan)
                    lbl_fun = frame_functions.get(frame).get(frame_prop)
                    yii_lbl = lbl_fun(yii_masked)
                    # Drop the frame_label coordinate
                    yii_lbl = yii_lbl.drop_vars('frame_label')
                    # Fill NaN values with 0 so that we can add DataArrays together
                    yii_lbl = yii_lbl.fillna(0)
                    # Add the Fv/Fm values for this label to the yii DataArray
                    yii_global = yii_global + yii_lbl
                    # Record observations for each labeled region
                    _add_observations(yii_da=yii_lbl, measurements=ps_da.measurement.values, label=f"{labels[i - 1]}_{i}",
                                      measurement_labels=measurement_labels)
                # Convert the labeled mask to a binary mask
                bin_mask = np.where(labeled_mask > 0, 255, 0)
                # Expand the binary mask to the same shape as the YII DataArray
                bin_mask = bin_mask[..., None]
                # Set the background values to NaN
                yii_global = yii_global.where(bin_mask > 0, other=np.nan)
                # drop coords identifying frames if they exist
                res = [i for i in list(yii_global.coords) if 'frame' in i]
                yii_global = yii_global.drop_vars(res)  # does not fail if res is []
                # Create a ridgeline plot of the YII values
                yii_chart = _ridgeline_plots(measurements=ps_da.measurement.values, measurement_labels=measurement_labels)
                yii_charts.append(yii_chart)

                # Create a pseudocolor image of the YII values
                _debug(visual=yii_global,
                       filename=os.path.join(params.debug_outdir, str(params.device) + "_" + frame + "_YII_dataarray.png"),
                       robust=True,
                       col='measurement',
                       col_wrap=int(np.ceil(yii_global.measurement.size / 4)),
                       vmin=0, vmax=1)
                yii_globals.append(yii_global.squeeze())

    return yii_globals, yii_charts


def _validate_psii_yii_frames(ps):
    """Helper to validate psii_data object has yii frames with information"""
    if not bool([x for x in ["psd", "psl",
                             "ojip_light", "ojip_dark",
                             "pml", "pmd", "pmt",
                             "npq"] if getattr(ps, x) is not None]):
        fatal_error("Unsupported DataArray type, pmt, pam_light/pam_dark, psl/psd, or npq frames are required")


def _psl_calc_fqfm(yii_masked):
    """Helper to calculate fq/fm from psl array"""
    yii_lbl = yii_masked.groupby('measurement', squeeze=False).map(_calc_yii)
    return yii_lbl


def _psd_calc_fvfm(yii_masked):
    """Helper to calculate fv/fm from psd array"""
    yii_lbl = (yii_masked.sel(frame_label='Fm') -
               yii_masked.sel(frame_label='F0')) / yii_masked.sel(frame_label='Fm')
    return yii_lbl


def _psd_calc_fvfm_double_prime(yii_masked):
    """Helper to calculate fv/fm from psd array"""
    yii_lbl = (yii_masked.sel(frame_label='Fmpp') -
               yii_masked.sel(frame_label='F0pp')) / yii_masked.sel(frame_label='Fmpp')
    return yii_lbl


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


def _create_histogram(yii_img, mlabel):
    """
    Compute histogram of YII.

    Inputs:
    yii_img     = numpy array of yii
    mlabel      = measurement label
    obs         = PlantCV observations used to retrieve statistics

    Returns:
    hist_df    = Histogram of efficiency estimate
    yii_mode   = DataArray of efficiency estimate values

    :param yii_img: numpy.ndarray
    :param mlabel: str
    :param obs: dict
    :return hist_df: pandas.DataFrame
    :return yii_mode: float
    """
    # Calculate the histogram of Fv/Fm, Fv'/Fm', or Fq'/Fm' non-zero values
    yii_hist, yii_bins = np.histogram(yii_img[np.where(yii_img > 0)], 100, range=(0, 1))
    # yii_bins is a bins + 1 length list of bin endpoints, so we need to calculate bin midpoints so that
    # the we have a one-to-one list of x (YII) and y (frequency) values.
    # To do this we add half the bin width to each lower bin edge x-value
    # midpoints = yii_bins[:-1] + 0.5 * np.diff(yii_bins)

    # Calculate which non-zero bin has the maximum Fv/Fm value
    yii_mode = yii_bins[np.argmax(yii_hist)]

    # Convert the histogram pixel counts to proportional frequencies
    yii_percent = (yii_hist / float(np.sum(yii_hist))) * 100

    # Create a dataframe for the histogram
    hist_df = pd.DataFrame({'proportion of pixels (%)': yii_percent, mlabel: yii_bins[:-1]})

    return hist_df, yii_mode


def _add_observations(yii_da, measurements, measurement_labels, label, yii_trait=" "):
    """Add observations for each labeled region."""
    # compute observations to store in Outputs, per labeled region
    yii_mean = yii_da.where(yii_da > 0).groupby('measurement').mean(['x', 'y']).values
    yii_median = yii_da.where(yii_da > 0).groupby('measurement').median(['x', 'y']).values
    yii_max = yii_da.where(yii_da > 0).groupby('measurement').max(['x', 'y']).values

    # Create variables to label traits based on measurement label in data array
    for n, mlabel in enumerate(measurements):
        if measurement_labels is not None:
            mlabel = measurement_labels[n]

        # mean value
        var = "_".join(s.strip() for s in ["yii", "mean", mlabel, yii_trait] if s.strip())
        outputs.add_observation(sample=label, variable=var,
                                trait=f"mean yii{yii_trait}value",
                                method='plantcv.plantcv.analyze.yii', scale='none', datatype=float,
                                value=float(yii_mean[n]), label='none')
        # median value
        var = "_".join(s.strip() for s in ["yii", "median", mlabel, yii_trait] if s.strip())
        outputs.add_observation(sample=label, variable=var,
                                trait=f"median yii{yii_trait}value",
                                method='plantcv.plantcv.analyze.yii', scale='none', datatype=float,
                                value=float(yii_median[n]), label='none')
        # max value
        var = "_".join(s.strip() for s in ["yii", "max", mlabel, yii_trait] if s.strip())
        outputs.add_observation(sample=label, variable=var,
                                trait=f"peak yii{yii_trait}value",
                                method='plantcv.plantcv.analyze.yii', scale='none', datatype=float,
                                value=float(yii_max[n]), label='none')

        hist_df, yii_mode = _create_histogram(yii_da.isel({'measurement': n}).values, mlabel)

        # mode value
        var = "_".join(s.strip() for s in ["yii", "mode", mlabel, yii_trait] if s.strip())
        outputs.add_observation(sample=label, variable=var,
                                trait=f"mode yii{yii_trait}value",
                                method='plantcv.plantcv.analyze.yii', scale='none', datatype=float,
                                value=float(yii_mode), label='none')
        # hist frequencies
        var = "_".join(s.strip() for s in ["yii", "hist", mlabel, yii_trait] if s.strip())
        outputs.add_observation(sample=label, variable=var,
                                trait=f"yii{yii_trait}frequencies",
                                method='plantcv.plantcv.analyze.yii', scale='none', datatype=list,
                                value=hist_df['proportion of pixels (%)'].values.tolist(),
                                label=np.around(hist_df[mlabel].values.tolist(), decimals=2).tolist())


def _calc_yii(da):
    """Apply the Fq'/Fm' calculation to the DataArray."""
    return (da.sel(frame_label='Fmp') - da.sel(frame_label='Fp')) / da.sel(frame_label='Fmp')


def _ridgeline_plots(measurements, measurement_labels, yii_trait=""):
    """Create ridgeline plots of YII values."""
    yii_chart = None
    for i, mlabel in enumerate(measurements):
        if measurement_labels is not None:
            mlabel = measurement_labels[i]
        var = ["yii", "hist", mlabel, yii_trait]
        yii_chart = outputs.plot_dists(
            variable="_".join(s.strip() for s in var if s and s.strip())
        )
        _debug(visual=yii_chart, filename=os.path.join(params.debug_outdir, str(params.device) + '_yii_hist.png'))
    return yii_chart
