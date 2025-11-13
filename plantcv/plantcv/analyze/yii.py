"""Fluorescence Analysis (Fv/Fm parameter)."""
import os
import numpy as np
import pandas as pd
import xarray as xr
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import params, outputs, fatal_error
from plantcv.plantcv.photosynthesis import reassign_frame_labels


def yii(ps_da, labeled_mask, n_labels=1, auto_fm=False, measurement_labels=None, label=None):
    """
    Calculate and analyze PSII efficiency estimates from fluorescence image data.

    Inputs:
    ps_da               = Photosynthesis xarray DataArray (either ojip_dark, ojip_light, pam_dark, or pam_light)
    labeled_mask        = Labeled mask of objects (32-bit).
    n_labels            = Total number expected individual objects (default = 1).
    auto_fm             = Automatically calculate the frame with maximum fluorescence per label, otherwise
                          use a fixed frame for all labels (default = False).
    measurement_labels  = labels for each measurement, modifies the variable name of observations recorded
    label               = optional label parameter, modifies the variable name of observations recorded

    Returns:
    yii_global          = DataArray of efficiency estimate values
    yii_chart           = Histograms of efficiency estimate

    :param ps_da: xarray.core.dataarray.DataArray
    :param labeled_mask: numpy.ndarray
    :param n_labels: int
    :param auto_fm: bool
    :param measurement_labels: list
    :param label: str
    :return yii_global: xarray.core.dataarray.DataArray
    :return yii_chart: altair.vegalite.v4.api.FacetChart
    """
    # Set labels
    labels = _set_labels(label, n_labels)

    # Validate that the input mask has the same 2D shape as the input DataArray
    if labeled_mask.shape != ps_da.shape[:2]:
        fatal_error(f"Mask needs to have shape {ps_da.shape[:2]}")

    # Validate that the input measurement_labels is the same length as the number of measurements in the DataArray
    if (measurement_labels is not None) and (len(measurement_labels) != ps_da.coords['measurement'].shape[0]):
        fatal_error('measurement_labels must be the same length as the number of measurements in the DataArray')

    # The name of the DataArray
    var = ps_da.name.lower()

    # Validate that var is a supported type
    if var not in ['ojip_dark', 'ojip_light', 'pam_dark', 'pam_light']:
        fatal_error(f"Unsupported DataArray type: {var}")

    # Make an zeroed array of the same shape as the input DataArray
    yii_global = xr.zeros_like(ps_da, dtype=float)
    # Drop the frame_label coordinate
    yii_global = yii_global[:, :, 0, :].drop_vars('frame_label')

    # Make a copy of the labeled mask
    mask_copy = np.copy(labeled_mask)

    # If the labeled mask is a binary mask with values 0 and 255, convert to 0 and 1
    if len(np.unique(mask_copy)) == 2 and np.max(mask_copy) == 255:
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

        # Dark-adapted datasets (Fv/Fm)
        if var in ['ojip_dark', 'pam_dark']:
            # Calculate Fv/Fm
            yii_lbl = (yii_masked.sel(frame_label='Fm') - yii_masked.sel(frame_label='F0')) / yii_masked.sel(frame_label='Fm')

        # Light-adapted datasets (Fq'/Fm')
        if var in ['ojip_light', 'pam_light']:
            # Calculate Fq'/Fm'
            yii_lbl = yii_masked.groupby('measurement', squeeze=False).map(_calc_yii)

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

    # Create a pseudocolor image of the YII values
    _debug(visual=yii_global,
           filename=os.path.join(params.debug_outdir, str(params.device) + "_YII_dataarray.png"),
           robust=True,
           col='measurement',
           col_wrap=int(np.ceil(yii_global.measurement.size / 4)),
           vmin=0, vmax=1)

    return yii_global.squeeze(), yii_chart


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


def _add_observations(yii_da, measurements, measurement_labels, label):
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
        outputs.add_observation(sample=label, variable=f"yii_mean_{mlabel}", trait="mean yii value",
                                method='plantcv.plantcv.analyze.yii', scale='none', datatype=float,
                                value=float(yii_mean[n]), label='none')
        # median value
        outputs.add_observation(sample=label, variable=f"yii_median_{mlabel}", trait="median yii value",
                                method='plantcv.plantcv.analyze.yii', scale='none', datatype=float,
                                value=float(yii_median[n]), label='none')
        # max value
        outputs.add_observation(sample=label, variable=f"yii_max_{mlabel}", trait="peak yii value",
                                method='plantcv.plantcv.analyze.yii', scale='none', datatype=float,
                                value=float(yii_max[n]), label='none')

        hist_df, yii_mode = _create_histogram(yii_da.isel({'measurement': n}).values, mlabel)

        # mode value
        outputs.add_observation(sample=label, variable=f"yii_mode_{mlabel}", trait="mode yii value",
                                method='plantcv.plantcv.analyze.yii', scale='none', datatype=float,
                                value=float(yii_mode), label='none')
        # hist frequencies
        outputs.add_observation(sample=label, variable=f"yii_hist_{mlabel}", trait="yii frequencies",
                                method='plantcv.plantcv.analyze.yii', scale='none', datatype=list,
                                value=hist_df['proportion of pixels (%)'].values.tolist(),
                                label=np.around(hist_df[mlabel].values.tolist(), decimals=2).tolist())


def _calc_yii(da):
    """Apply the Fq'/Fm' calculation to the DataArray."""
    return (da.sel(frame_label='Fmp') - da.sel(frame_label='Fp')) / da.sel(frame_label='Fmp')


def _ridgeline_plots(measurements, measurement_labels):
    """Create ridgeline plots of YII values."""
    yii_chart = None
    for i, mlabel in enumerate(measurements):
        if measurement_labels is not None:
            mlabel = measurement_labels[i]
        yii_chart = outputs.plot_dists(variable=f"yii_hist_{mlabel}")
        _debug(visual=yii_chart, filename=os.path.join(params.debug_outdir, str(params.device) + '_yii_hist.png'))
    return yii_chart
