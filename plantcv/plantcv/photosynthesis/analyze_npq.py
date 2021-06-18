# Fluorescence Analysis (Fv/Fm parameter)

import os
import numpy as np
import pandas as pd
from plotnine import ggplot, aes, geom_line, geom_label
from plotnine.labels import labs
from plantcv.plantcv import fatal_error
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import params
from plantcv.plantcv import outputs


def analyze_npq(ps_da, mask, bins=256, measurement_labels=None, label="default"):
    """
    Calculate and analyze PSII efficiency estimates from fluorescence image data.

    Inputs:
    ps_da                     = photosynthesis xarray DataArray
    mask                      = mask of plant (binary, single channel)
    bins                      = number of bins for the histogram (1 to 256 for 8-bit; 1 to 65,536 for 16-bit; default is 256)
    measurement_labels        = labels for each measurement, modifies the variable name of observations recorded
    label                     = optional label parameter, modifies the variable name of observations recorded

    Returns:
    hist_fig  = Histogram of efficiency estimate
    npq   = DataArray of efficiency estimate values

    :param ps_da: xarray.core.dataarray.DataArray
    :param mask: numpy.ndarray
    :param bins: int
    :param measurement_labels: list
    :return hist_fig: plotnine.ggplot.ggplot
    :return npq: xarray.core.dataarray.DataArray
    """

    if (measurement_labels is not None) and (len(measurement_labels) != ps_da.coords['measurement'].shape[0]):
        fatal_error('measurement_labels must be the same length as the number of measurements in the DataArray')

    var = ps_da.name.lower()

    mask = mask[..., None, None]
    if var == 'darkadapted':
        npq0 = ps_da.astype('float').where(mask > 0, other = np.nan)
        npq = (npq0.sel(frame_label='Fm') - npq0.sel(frame_label='F0')) / npq0.sel(frame_label='Fm')

    elif var == 'lightadapted':
        def _calc_npq(ps_da):
            return (ps_da.sel(frame_label='Fmp') - ps_da.sel(frame_label='Fp')) / ps_da.sel(frame_label='Fmp')
        npq0 = ps_da.astype('float').where(mask > 0, other = np.nan)
        npq = npq0.groupby('measurement', squeeze=True).map(_calc_npq)

    # compute observations to store in Outputs
    npq_median = npq.where(npq > 0).groupby('measurement').median(['x', 'y']).values
    npq_max = npq.where(npq > 0).groupby('measurement').max(['x', 'y']).values
    
    # Create variables to label traits based on measurement label in data array
    for i, mlabel in enumerate(ps_da.measurement.values):
        if measurement_labels is not None:
            mlabel = measurement_labels[i]

        hist_df, hist_fig = _create_histogram(npq.isel({'measurement':i}).values, mlabel, bins)

        # median value
        outputs.add_observation(sample=label, variable=f"{mlabel} median npq", trait="median npq value",
                                method='plantcv.plantcv.photosynthesis.analyze_npq', scale='none', datatype=float,
                                value=float(np.around(npq_median[i], decimals=4)), label='none')
        # max value
        outputs.add_observation(sample=label, variable=f"{mlabel} peak npq", trait="peak npq value",
                                method='plantcv.plantcv.photosynthesis.analyze_npq', scale='none', datatype=float,
                                value=float(npq_max[i]), label='none')
        # hist frequencies
        outputs.add_observation(sample=label, variable=f"{mlabel} freq npq", trait="frequencies",
                                method='plantcv.plantcv.photosynthesis.analyze_npq', scale='none', datatype=list,
                                value=hist_df['Plant Pixels'].values.tolist(), 
                                label=np.around(hist_df[mlabel].values.tolist(), decimals=2).tolist())

        # Plot/Print out the histograms
        _debug(visual=hist_fig, 
               filename=os.path.join(params.debug_outdir, str(params.device) + f"_NPQ_{mlabel}_histogram.png"))

    # Store images
    outputs.images.append(npq)

    return hist_fig, npq.drop_vars(['frame_label', 'frame_num'])


def _create_histogram(npq_img, mlabel, bins):
    """
    Compute histogram of NPQ

    Inputs:
    npq_img     = numpy array of npq
    bins        = number of bins for the histogram (1 to 256 for 8-bit; 1 to 65,536 for 16-bit; default is 256)

    Returns:
    hist_fig  = Histogram of efficiency estimate
    npq_img   = DataArray of efficiency estimate values

    :param npq_img: numpy.ndarray
    :param bins: int
    :return hist_df: pandas.DataFrame
    :return hist_fig: plotnine.ggplot.ggplot
    """
    
    # Calculate the histogram of Fv/Fm, Fv'/Fm', or Fq'/Fm' non-zero values
    npq_hist, npq_bins = np.histogram(npq_img[np.where(npq_img > 0)], bins, range=(0, 1))
    # npq_bins is a bins + 1 length list of bin endpoints, so we need to calculate bin midpoints so that
    # the we have a one-to-one list of x (NPQ) and y (frequency) values.
    # To do this we add half the bin width to each lower bin edge x-value
    midpoints = npq_bins[:-1] + 0.5 * np.diff(npq_bins)

    # Calculate which non-zero bin has the maximum Fv/Fm value
    max_bin = midpoints[np.argmax(npq_hist)]

    # Create a dataframe
    hist_df = pd.DataFrame({'Plant Pixels': npq_hist, mlabel : midpoints})

    # Make the histogram figure using plotnine
    hist_fig = (ggplot(data=hist_df, mapping=aes(x=mlabel, y='Plant Pixels'))
                + geom_line(show_legend=True, color="green")
                + geom_label(label=f"Peak Bin Value: {str(max_bin)}", x=.15, y=205, size=8, color="green")
                + labs(title = f"measurement: {mlabel}",
                       x = 'nonphotochemical quenching (npq)'))

    return hist_df, hist_fig

