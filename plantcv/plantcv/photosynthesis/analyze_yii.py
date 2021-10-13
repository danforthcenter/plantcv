# Fluorescence Analysis (Fv/Fm parameter)

import os
import numpy as np
import pandas as pd
from plotnine import ggplot, aes, geom_line, geom_point, theme, scale_color_brewer
from plotnine.labels import labs
from plantcv.plantcv import fatal_error
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import params
from plantcv.plantcv import outputs


def analyze_yii(ps_da, mask, measurement_labels=None, label="default"):
    """
    Calculate and analyze PSII efficiency estimates from fluorescence image data.

    Inputs:
    ps_da               = photosynthesis xarray DataArray
    mask                = mask of plant (binary, single channel)
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
    if mask.shape != ps_da.shape[:2]:
        fatal_error(f"Mask needs to have shape {ps_da.shape[:2]}")

    if len(np.unique(mask)) > 2 or mask.dtype != 'uint8':
        fatal_error("Mask must have dtype uint8 and be binary")

    if (measurement_labels is not None) and (len(measurement_labels) != ps_da.coords['measurement'].shape[0]):
        fatal_error('measurement_labels must be the same length as the number of measurements in the DataArray')

    var = ps_da.name.lower()

    mask = mask[..., None, None]
    if var == 'darkadapted':
        yii0 = ps_da.astype('float').where(mask > 0, other=np.nan)
        yii = (yii0.sel(frame_label='Fm') - yii0.sel(frame_label='F0')) / yii0.sel(frame_label='Fm')

    elif var == 'lightadapted':
        def _calc_yii(da):
            return (da.sel(frame_label='Fmp') - da.sel(frame_label='Fp')) / da.sel(frame_label='Fmp')
        yii0 = ps_da.astype('float').where(mask > 0, other=np.nan)
        yii = yii0.groupby('measurement', squeeze=False).map(_calc_yii)

    # compute observations to store in Outputs
    yii_mean = yii.where(yii > 0).groupby('measurement').mean(['x', 'y']).values
    yii_median = yii.where(yii > 0).groupby('measurement').median(['x', 'y']).values
    yii_max = yii.where(yii > 0).groupby('measurement').max(['x', 'y']).values

    # Create variables to label traits based on measurement label in data array
    for i, mlabel in enumerate(ps_da.measurement.values):
        if measurement_labels is not None:
            mlabel = measurement_labels[i]

        # mean value
        outputs.add_observation(sample=label, variable=f"yii_mean_{mlabel}", trait="mean yii value",
                                method='plantcv.plantcv.photosynthesis.analyze_yii', scale='none', datatype=float,
                                value=float(yii_mean[i]), label='none')
        # median value
        outputs.add_observation(sample=label, variable=f"yii_median_{mlabel}", trait="median yii value",
                                method='plantcv.plantcv.photosynthesis.analyze_yii', scale='none', datatype=float,
                                value=float(yii_median[i]), label='none')
        # max value
        outputs.add_observation(sample=label, variable=f"yii_max_{mlabel}", trait="peak yii value",
                                method='plantcv.plantcv.photosynthesis.analyze_yii', scale='none', datatype=float,
                                value=float(yii_max[i]), label='none')

        hist_df, hist_fig, yii_mode = _create_histogram(yii.isel({'measurement': i}).values, mlabel,
                                                        outputs.observations[label])

        # mode value
        outputs.add_observation(sample=label, variable=f"yii_mode_{mlabel}", trait="mode yii value",
                                method='plantcv.plantcv.photosynthesis.analyze_yii', scale='none', datatype=float,
                                value=float(yii_mode), label='none')
        # hist frequencies
        outputs.add_observation(sample=label, variable=f"yii_hist_{mlabel}", trait="yii frequencies",
                                method='plantcv.plantcv.photosynthesis.analyze_yii', scale='none', datatype=list,
                                value=hist_df['Plant Pixels'].values.tolist(),
                                label=np.around(hist_df[mlabel].values.tolist(), decimals=2).tolist())

        # Plot/Print out the histograms
        _debug(visual=hist_fig,
               filename=os.path.join(params.debug_outdir, str(params.device) + f"_YII_{mlabel}_histogram.png"))

    # drop coords identifying frames if they exist
    res = [i for i in list(yii.coords) if 'frame' in i]
    yii = yii.drop_vars(res)  # does not fail if res is []

    # Store images
    outputs.images.append(yii)

    # Plot/print dataarray
    # plot will default to a hist if >1 measurements so explicitly call pcolormesh
    # da_frames = yii.plot.pcolormesh(row='measurement', col_wrap=int(np.ceil(yii.measurement.size/3)), robust=True)
    _debug(visual=yii,
           filename=os.path.join(params.debug_outdir, str(params.device) + "_YII_dataarray.png"),
           robust=True,
           col='measurement',
           col_wrap=int(np.ceil(yii.measurement.size / 4)))

    # this only returns the last histogram..... xarray does not seem to support panels of histograms
    # but does support matplotlib subplots kwargs and axes
    return yii, hist_fig


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
