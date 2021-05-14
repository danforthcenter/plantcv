# Fluorescence Analysis (Fv/Fm parameter)

import os
import cv2
import numpy as np
import pandas as pd
from plotnine import ggplot, aes, geom_line, geom_label
from plantcv.plantcv import fatal_error
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import params
from plantcv.plantcv import outputs


def analyze_yii(ps, mask, measurement, bins=256, label="default"):
    """Calculate and analyze PSII efficiency estimates from fluorescence image data.

    Inputs:
    ps          = photosynthesis xarray DataArray
    mask        = mask of plant (binary, single channel)
    measurement = choose which measurement routine to analyze: "Fv/Fm", "Fv'/Fm'", or "Fq'/Fm'"
    bins        = number of bins (1 to 256 for 8-bit; 1 to 65,536 for 16-bit; default is 256)
    label       = optional label parameter, modifies the variable name of observations recorded

    Returns:
    ind_fig   = Fluorescence induction curve plot
    hist_fig  = Histogram of efficiency estimate
    yii_img   = Image of efficiency estimate values

    :param ps: xarray.core.dataarray.DataArray
    :param mask: numpy.ndarray
    :param measurement: str
    :param bins: int
    :param label: str
    :return ind_fig: plotnine.ggplot.ggplot
    :return hist_fig: plotnine.ggplot.ggplot
    :return yii_img: numpy.ndarray
    """

    prot_vars = {
        "fv/fm": {"Fm": "Fm", "F0": "F0"},
        "fv'/fm'": {"Fm": "Fm", "F0": "F0"},
        "fq'/fm'": {"Fm": "Fm'", "F0": "F'"}
    }

    if measurement.lower() not in prot_vars:
        fatal_error(f"Measurement {measurement} is not one of Fv/Fm, Fv'/Fm', or Fq'/Fm'")

    # Analyze fluorescence induction curve to identify max fluorescence
    ind_df = _fluor_induction(ps=ps, mask=mask, measurement=measurement)

    # Make fluorescence induction curve figure using plotnine
    ind_fig = (ggplot(data=ind_df, mapping=aes(x="Timepoints", y="Fluorescence", color="Measurement"))
               + geom_line(show_legend=True))

    # Select the F0, F0', or F' frame
    fmin = ps.sel(frame_label=ps.attrs[prot_vars[measurement.lower()]["F0"]]).data
    # Select the Fm or Fm' frame
    fmax = ps.sel(frame_label=ps.attrs[prot_vars[measurement.lower()]["Fm"]]).data

    # Mask Fmin and Fmax Image
    fmin_mask = cv2.bitwise_and(fmin, fmin, mask=mask)
    fmax_mask = cv2.bitwise_and(fmax, fmax, mask=mask)

    # Calculate F-delta
    # Fv = Fm - F0 (masked)
    # Fv' = Fm' - F0'
    # Fq' = Fm' - F'
    delta = np.subtract(fmax_mask, fmin_mask)

    # When Fmin is greater than Fmax, a negative value is returned.
    # Because the data type is unsigned integers, negative values roll over, resulting in nonsensical values
    # Wherever Fmin is greater than Fmax, set F-delta to zero
    delta[np.where(fmax_mask < fmin_mask)] = 0

    # Calculate Fv/Fm, Fv'/Fm', or Fq'/Fm' where Fmax is greater than zero
    # By definition above, wherever Fmax is zero, F-delta will also be zero
    # To calculate the divisions properly we need to change from unit16 to float64 data types
    yii_img = delta.astype(np.float64)
    fmax_flt = fmax_mask.astype(np.float64)
    yii_img[np.where(fmax_mask > 0)] /= fmax_flt[np.where(fmax_mask > 0)]

    # Calculate the median Fv/Fm, Fv'/Fm', or Fq'/Fm' value for non-zero pixels
    yii_median = np.median(yii_img[np.where(yii_img > 0)])

    # Calculate the histogram of Fv/Fm, Fv'/Fm', or Fq'/Fm' non-zero values
    yii_hist, yii_bins = np.histogram(yii_img[np.where(yii_img > 0)], bins, range=(0, 1))
    # yii_bins is a bins + 1 length list of bin endpoints, so we need to calculate bin midpoints so that
    # the we have a one-to-one list of x (YII) and y (frequency) values.
    # To do this we add half the bin width to each lower bin edge x-value
    midpoints = yii_bins[:-1] + 0.5 * np.diff(yii_bins)

    # Calculate which non-zero bin has the maximum Fv/Fm value
    max_bin = midpoints[np.argmax(yii_hist)]

    # Create a dataframe
    hist_df = pd.DataFrame({'Plant Pixels': yii_hist, measurement: midpoints})

    # Make the histogram figure using plotnine
    hist_fig = (ggplot(data=hist_df, mapping=aes(x=measurement, y='Plant Pixels'))
                + geom_line(show_legend=True, color="green")
                + geom_label(label=f"Peak Bin Value: {str(max_bin)}", x=.15, y=205, size=8, color="green"))

    # Plot/Print out the induction curves and the histograms
    _debug(visual=ind_fig, filename=os.path.join(params.debug_outdir, str(params.device) + "_fluor_induction.png"))
    _debug(visual=hist_fig, filename=os.path.join(params.debug_outdir, str(params.device) + "_YII_histogram.png"))

    # Store images
    outputs.images.append(yii_img)

    # Create variables to label traits as either Fv/Fm or Fv'/Fm' measurements
    var = measurement.lower()
    var = var.replace("'", "p")
    var = var.replace("/", "")

    outputs.add_observation(sample=label, variable=f"{var}_hist", trait=f"{measurement} frequencies",
                            method='plantcv.plantcv.photosynthesis.analyze_fvfm', scale='none', datatype=list,
                            value=yii_hist.tolist(), label=np.around(midpoints, decimals=len(str(bins))).tolist())
    outputs.add_observation(sample=label, variable=f"{var}_hist_peak", trait=f"peak {measurement} value",
                            method='plantcv.plantcv.photosynthesis.analyze_fvfm', scale='none', datatype=float,
                            value=float(max_bin), label='none')
    outputs.add_observation(sample=label, variable=f"{var}_median", trait=f"{measurement} median",
                            method='plantcv.plantcv.photosynthesis.analyze_fvfm', scale='none', datatype=float,
                            value=float(np.around(yii_median, decimals=4)), label='none')

    return ind_fig, hist_fig, yii_img


def _fluor_induction(ps, mask, measurement):
    """Calculate fluorescence induction curve.

    Inputs:
    ps          = photosynthesis xarray DataArray
    mask        = mask of plant (binary, single channel)
    measurement = choose which measurement routines to analyze: light, dark, or both (default)

    Returns:
    df          = data frame of fluorescence in the masked region at each timepoint

    :param ps: xarray.core.dataarray.DataArray
    :param mask: numpy.ndarray
    :param measurement: str
    :return df: pandas.core.frame.DataFrame
    """
    # Prime is empty for Fv/Fm (dark- and light-adapted) and ' for Fq'/Fm'
    prime = ""
    if measurement.lower() == "fq'/fm'":
        prime = "'"
    # Create a list of fluorescence values, measurement labels, and timepoint indices
    fluor_values = []
    meas = []
    timepts = []
    # Iterate over the PAM measurement frames
    for i in range(ps.attrs[f"F{prime}-frames"]):
        # Append the mean masked pixel value (fluorescence) to the list
        fluor_values.append(np.mean(ps.sel(frame_label=f"F{i}{prime}").data[np.where(mask > 0)]))
        # Append the measurement label (F or F')
        meas.append(f"F{prime}")
        # Append the timepoint index
        timepts.append(i)
    # Create a dataframe
    df = pd.DataFrame({"Timepoints": timepts, "Fluorescence": fluor_values, "Measurement": meas})
    # The Fm frame is the frame with the largest mean fluorescence value
    fmax_frame = f"F{np.argmax(fluor_values)}{prime}"
    ps.attrs[f"Fm{prime}"] = fmax_frame
    return df
