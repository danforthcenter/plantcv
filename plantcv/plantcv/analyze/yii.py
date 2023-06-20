# Fluorescence Analysis (Fv/Fm parameter)

import os
import numpy as np
import pandas as pd
import xarray as xr
from plotnine import ggplot, aes, geom_line, geom_point, theme, scale_color_brewer
from plotnine.labels import labs
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import params, outputs, fatal_error
from plantcv.plantcv.photosynthesis import reassign_frame_labels


def yii(ps_da, labeled_mask, n_labels=1, auto_fm=False, measurement_labels=None, label="default"):
    """
    Calculate and analyze PSII efficiency estimates from fluorescence image data.

    Inputs:
    ps_da               = photosynthesis xarray DataArray
    labeled_mask        = mask of plant (binary, single channel)
    measurement_labels  = labels for each measurement, modifies the variable name of observations recorded
    label               = optional label parameter, modifies the variable name of observations recorded

    Returns:
    yii       = DataArray of efficiency estimate values
    hist_fig  = Histogram of efficiency estimate

    :param ps_da: xarray.core.dataarray.DataArray
    :param mask: numpy.ndarray
    :param measurement_labels: list
    :param label: str
    :return yii: xarray.core.dataarray.DataArray
    :return hist_fig: plotnine.ggplot.ggplot
    """
    # Validate that the input mask has the same 2D shape as the input DataArray
    if labeled_mask.shape != labeled_mask.shape[:2]:
        fatal_error(f"Mask needs to have shape {ps_da.shape[:2]}")

    # Validate that the input measurement_labels is the same length as the number of measurements in the DataArray
    if (measurement_labels is not None) and (len(measurement_labels) != ps_da.coords['measurement'].shape[0]):
        fatal_error('measurement_labels must be the same length as the number of measurements in the DataArray')

    # The name of the DataArray
    var = ps_da.name.lower()

    # Make an zeroed array of the same shape as the input DataArray
    yii = xr.zeros_like(ps_da, dtype=float)
    # Drop the frame_label coordinate
    yii = yii[:, :, 0, :].drop_vars('frame_label')

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
        yii0 = ps_da.astype('float').where(submask > 0, other=np.nan)
        # Dark-adapted datasets (Fv/Fm)
        if var == 'darkadapted':
            # Calculate Fv/Fm
            yii1 = (yii0.sel(frame_label='Fm') - yii0.sel(frame_label='F0')) / yii0.sel(frame_label='Fm')
        # Light-adapted datasets (Fq'/Fm')
        elif var == 'lightadapted':
            # Create a helper function to apply the Fq'/Fm' calculation to the DataArray
            def _calc_yii(da):
                return (da.sel(frame_label='Fmp') - da.sel(frame_label='Fp')) / da.sel(frame_label='Fmp')
            # Calculate Fq'/Fm'
            yii1 = yii0.groupby('measurement', squeeze=False).map(_calc_yii)
        # Drop the frame_label coordinate
        yii1 = yii1.drop_vars('frame_label')
        # Fill NaN values with 0 so that we can add DataArrays together
        yii1 = yii1.fillna(0)
        # Add the Fv/Fm values for this label to the yii DataArray
        yii = yii + yii1

        # compute observations to store in Outputs, per labeled region
        yii_mean = yii1.where(yii1 > 0).groupby('measurement').mean(['x', 'y']).values
        yii_median = yii1.where(yii1 > 0).groupby('measurement').median(['x', 'y']).values
        yii_max = yii1.where(yii1 > 0).groupby('measurement').max(['x', 'y']).values

        # Create variables to label traits based on measurement label in data array
        for n, mlabel in enumerate(ps_da.measurement.values):
            if measurement_labels is not None:
                mlabel = measurement_labels[n]

            # mean value
            outputs.add_observation(sample=f"{label}{i}", variable=f"yii_mean_{mlabel}", trait="mean yii value",
                                    method='plantcv.plantcv.photosynthesis.analyze_yii', scale='none', datatype=float,
                                    value=float(yii_mean[n]), label='none')
            # median value
            outputs.add_observation(sample=f"{label}{i}", variable=f"yii_median_{mlabel}", trait="median yii value",
                                    method='plantcv.plantcv.photosynthesis.analyze_yii', scale='none', datatype=float,
                                    value=float(yii_median[n]), label='none')
            # max value
            outputs.add_observation(sample=f"{label}{i}", variable=f"yii_max_{mlabel}", trait="peak yii value",
                                    method='plantcv.plantcv.photosynthesis.analyze_yii', scale='none', datatype=float,
                                    value=float(yii_max[n]), label='none')

            hist_df, hist_fig, yii_mode = _create_histogram(yii.isel({'measurement': n}).values, mlabel,
                                                            outputs.observations[f"{label}{i}"])

            # mode value
            outputs.add_observation(sample=f"{label}{i}", variable=f"yii_mode_{mlabel}", trait="mode yii value",
                                    method='plantcv.plantcv.photosynthesis.analyze_yii', scale='none', datatype=float,
                                    value=float(yii_mode), label='none')
            # hist frequencies
            outputs.add_observation(sample=f"{label}{i}", variable=f"yii_hist_{mlabel}", trait="yii frequencies",
                                    method='plantcv.plantcv.photosynthesis.analyze_yii', scale='none', datatype=list,
                                    value=hist_df['Plant Pixels'].values.tolist(),
                                    label=np.around(hist_df[mlabel].values.tolist(), decimals=2).tolist())

    # Convert the labeled mask to a binary mask
    bin_mask = np.where(labeled_mask > 0, 255, 0)

    # Expand the binary mask to the same shape as the YII DataArray
    bin_mask = bin_mask[..., None]

    # Set the background values to NaN
    yii = yii.where(bin_mask > 0, other=np.nan)

    # drop coords identifying frames if they exist
    res = [i for i in list(yii.coords) if 'frame' in i]
    yii = yii.drop_vars(res)  # does not fail if res is []

    # Create a ridgeline plot of the YII values
    yii_chart = None
    for i, mlabel in enumerate(ps_da.measurement.values):
        if measurement_labels is not None:
            mlabel = measurement_labels[i]
        yii_chart = outputs.plot_dists(variable=f"yii_hist_{mlabel}")
        _debug(visual=yii_chart, filename=os.path.join(params.debug_outdir, str(params.device) + '_yii_hist.png'))

    # Create a pseudocolor image of the YII values
    _debug(visual=yii,
           filename=os.path.join(params.debug_outdir, str(params.device) + "_YII_dataarray.png"),
           robust=True,
           col='measurement',
           col_wrap=int(np.ceil(yii.measurement.size / 4)),
           vmin=0, vmax=1)

    return yii_chart, yii.squeeze()


def _create_histogram(yii_img, mlabel, obs):
    """
    Compute histogram of YII

    Inputs:
    yii_img     = numpy array of yii
    mlabel      = measurement label
    obs         = PlantCV observations used to retrieve statistics

    Returns:
    hist_fig  = Histogram of efficiency estimate
    yii_img   = DataArray of efficiency estimate values

    :param yii_img: numpy.ndarray
    :param mlabel: str
    :param obs: dict
    :return hist_df: pandas.DataFrame
    :return hist_fig: plotnine.ggplot.ggplot
    """

    # Calculate the histogram of Fv/Fm, Fv'/Fm', or Fq'/Fm' non-zero values
    yii_hist, yii_bins = np.histogram(yii_img[np.where(yii_img > 0)], 100, range=(0, 1))
    # yii_bins is a bins + 1 length list of bin endpoints, so we need to calculate bin midpoints so that
    # the we have a one-to-one list of x (YII) and y (frequency) values.
    # To do this we add half the bin width to each lower bin edge x-value
    # midpoints = yii_bins[:-1] + 0.5 * np.diff(yii_bins)

    # Calculate which non-zero bin has the maximum Fv/Fm value
    yii_mode = yii_bins[np.argmax(yii_hist)]

    # Create a dataframe for the histogram
    hist_df = pd.DataFrame({'Plant Pixels': yii_hist, mlabel: yii_bins[:-1]})

    # Round values for plotting
    bins = np.around(yii_bins, decimals=2)
    round_mean = np.around(obs[f"yii_mean_{mlabel}"]["value"], decimals=2)
    round_median = np.around(obs[f"yii_median_{mlabel}"]["value"], decimals=2)
    round_mode = np.around(yii_mode, decimals=2)
    mean_index = bins.tolist().index(round_mean)
    median_index = bins.tolist().index(round_median)
    mode_index = np.argmax(yii_hist)
    # Create a dataframe for the statistics
    stats_df = pd.DataFrame({'Plant Pixels': [yii_hist[mean_index], yii_hist[median_index], yii_hist[mode_index]],
                             mlabel: [round_mean, round_median, round_mode],
                             "Stat": ["mean", "median", "mode"]})

    # Make the histogram figure using plotnine
    hist_fig = (ggplot(data=hist_df, mapping=aes(x=mlabel, y='Plant Pixels'))
                + geom_line(show_legend=True, color="darkblue")
                + geom_point(data=stats_df, mapping=aes(color='Stat'))
                + labs(title=f"measurement: {mlabel}",
                       x='photosynthetic efficiency (yii)')
                + theme(subplots_adjust={"right": 0.8})
                + scale_color_brewer(type="qual", palette=2))

    return hist_df, hist_fig, yii_mode
