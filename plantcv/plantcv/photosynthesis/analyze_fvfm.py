# Fluorescence Analysis (Fv/Fm parameter)

import os
import cv2
import numpy as np
import pandas as pd
from plotnine import ggplot, aes, geom_line
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import params
from plantcv.plantcv import outputs


def analyze_fvfm(ps, mask, bins=256, measurement="both", label="default"):
    """Calculate and analyze Fv/Fm from fluorescence image data.
    Inputs:
    ps          = photosynthesis xarray DataArray
    mask        = mask of plant (binary, single channel)
    bins        = number of bins (1 to 256 for 8-bit; 1 to 65,536 for 16-bit; default is 256)
    measurement = choose which measurement routines to analyze: light, dark, or both (default)
    label       = optional label parameter, modifies the variable name of observations recorded

    Returns:
    ind_curve = Fluorescence induction curve plot
    fvfm_hist = Fv/Fm histogram
    analysis_images = List of Fv/Fm images

    :param ps: xarray.core.dataarray.DataArray
    :param mask: numpy.ndarray
    :param bins: int
    :param measurement: str
    :param label: str
    :return ind_curve: plotnine.ggplot.ggplot
    :return fvfm_hist: plotnine.ggplot.ggplot
    :return analysis_images: list
    """

    analysis_images = []
    ind_dfs = []
    hist_dfs = []

    if measurement.upper() == "DARK" or measurement.upper() == "BOTH":
        f_df, fmax_frame = _fluor_induction(ps=ps, mask=mask, measurement="dark")
        ps.attrs["Fm"] = fmax_frame

        #  Extract frames of interest
        fdark = ps.sel(frame_label='Fdark').data
        fmax = ps.sel(frame_label=ps.attrs["Fm"]).data
        fmin = ps.sel(frame_label='F0').data

        fvfm, fvfm_df = _fvfm(fdark=fdark, fmin=fmin, fmax=fmax, mask=mask, bins=bins,
                              measurement="Fv/Fm", label=label)
        analysis_images.append(fvfm)
        ind_dfs.append(f_df)
        hist_dfs.append(fvfm_df)

    if measurement.upper() == "LIGHT" or measurement.upper() == "BOTH":
        fp_df, fmaxp_frame = _fluor_induction(ps=ps, mask=mask, measurement="light")
        ps.attrs["Fm'"] = fmaxp_frame

        #  Extract frames of interest
        fdarkp = ps.sel(frame_label='Fdark').data
        fmaxp = ps.sel(frame_label=ps.attrs["Fm'"]).data
        fminp = ps.sel(frame_label='F0').data

        fvfmp, fvfmp_df = _fvfm(fdark=fdarkp, fmin=fminp, fmax=fmaxp, mask=mask, bins=bins,
                                measurement="Fv'/Fm'", label=label)
        analysis_images.append(fvfmp)
        ind_dfs.append(fp_df)
        hist_dfs.append(fvfmp_df)

    ind_df = ind_dfs[0]
    hist_df = hist_dfs[0]
    if measurement.upper() == "BOTH":
        ind_df = ind_df.append(ind_dfs[1])
        hist_df = hist_df.append(hist_dfs[1])

    # Make fluorescence induction curve figure using plotnine
    ind_fig = (ggplot(data=ind_df, mapping=aes(x="Timepoints", y="Fluorescence", color="Measurement"))
               + geom_line(show_legend=True))

    # Make the histogram figure using plotnine
    fvfm_hist_fig = (ggplot(data=hist_df, mapping=aes(x='Fv/Fm', y='Plant Pixels', color="Measurement"))
                     + geom_line(show_legend=True))

    # Plot/Print out the induction curves and the histograms
    _debug(visual=ind_fig, filename=os.path.join(params.debug_outdir, str(params.device) + "_fluor_induction.png"))
    _debug(visual=fvfm_hist_fig, filename=os.path.join(params.debug_outdir, str(params.device) + "_FvFm_histogram.png"))

    # Store images
    outputs.images.append(analysis_images)

    return ind_fig, fvfm_hist_fig, analysis_images


def _fluor_induction(ps, mask, measurement):
    """Calculate fluorescence induction curve.

    Inputs:
    ps          = photosynthesis xarray DataArray
    mask        = mask of plant (binary, single channel)
    measurement = choose which measurement routines to analyze: light, dark, or both (default)

    Returns:
    df          = data frame of fluorescence in the masked region at each timepoint
    fmax_frame  = the frame label where maximum fluorescence was observed

    :param ps: xarray.core.dataarray.DataArray
    :param mask: numpy.ndarray
    :param measurement: str
    :return df: pandas.core.frame.DataFrame
    :return fmax_frame: str
    """
    # Prime is empty for dark-adapted and ' for light-adapted
    prime = ""
    if measurement.upper() == "LIGHT":
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
    return df, fmax_frame


def _fvfm(fdark, fmin, fmax, mask, bins, measurement, label):
    """Calculate Fv/Fm.

    Inputs:
    fdark       = Fdark or Fdark' image
    fmin        = F0 or F0' image
    fmax        = Fm or Fm' image
    mask        = mask of plant (binary, single channel)
    bins        = number of bins (1 to 256 for 8-bit; 1 to 65,536 for 16-bit; default is 256)
    measurement = choose which measurement routines to analyze: light, dark, or both (default)
    label       = optional label parameter, modifies the variable name of observations recorded

    Returns:
    fvfm        = Fv/Fm or Fv'/Fm' image
    hist_df     = Fv/Fm or Fv'/Fm' dataframe

    :param fdark: numpy.ndarray
    :param fmin: numpy.ndarray
    :param fmax: numpy.ndarray
    :param mask: numpy.ndarray
    :param bins: int
    :param measurement: str
    :param label: str
    :return fvfm: numpy.ndarray
    :return hist_df: pandas.core.frame.DataFrame
    """
    # QC Fdark Image
    fdark_mask = cv2.bitwise_and(fdark, fdark, mask=mask)
    qc_fdark = bool(np.amax(fdark_mask) > 2000)

    # Mask Fmin and Fmax Image
    fmin_mask = cv2.bitwise_and(fmin, fmin, mask=mask)
    fmax_mask = cv2.bitwise_and(fmax, fmax, mask=mask)

    # Calculate Fvariable, where Fv = Fmax - Fmin (masked)
    fv = np.subtract(fmax_mask, fmin_mask)

    # When Fmin is greater than Fmax, a negative value is returned.
    # Because the data type is unsigned integers, negative values roll over, resulting in nonsensical values
    # Wherever Fmin is greater than Fmax, set Fv to zero
    fv[np.where(fmax_mask < fmin_mask)] = 0

    # Calculate Fv/Fm (Fvariable / Fmax) where Fmax is greater than zero
    # By definition above, wherever Fmax is zero, Fvariable will also be zero
    # To calculate the divisions properly we need to change from unit16 to float64 data types
    fvfm = fv.astype(np.float64)
    fmax_flt = fmax_mask.astype(np.float64)
    fvfm[np.where(fmax_mask > 0)] /= fmax_flt[np.where(fmax_mask > 0)]

    # Calculate the median Fv/Fm value for non-zero pixels
    fvfm_median = np.median(fvfm[np.where(fvfm > 0)])

    # Calculate the histogram of Fv/Fm non-zero values
    fvfm_hist, fvfm_bins = np.histogram(fvfm[np.where(fvfm > 0)], bins, range=(0, 1))
    # fvfm_bins is a bins + 1 length list of bin endpoints, so we need to calculate bin midpoints so that
    # the we have a one-to-one list of x (FvFm) and y (frequency) values.
    # To do this we add half the bin width to each lower bin edge x-value
    midpoints = fvfm_bins[:-1] + 0.5 * np.diff(fvfm_bins)

    # Calculate which non-zero bin has the maximum Fv/Fm value
    max_bin = midpoints[np.argmax(fvfm_hist)]

    meas_label = [measurement for _ in range(bins)]

    # Create a dataframe
    hist_df = pd.DataFrame({'Plant Pixels': fvfm_hist, 'Fv/Fm': midpoints, "Measurement": meas_label})

    # Create variables to label traits as either Fv/Fm or Fv'/Fm' measurements
    var = measurement.lower()
    var = var.replace("'", "p")
    var = var.replace("/", "")
    fdark_var = "fdark"
    fdark_meas = "Fdark"
    if "'" in measurement:
        fdark_var = fdark_var + "p"
        fdark_meas = fdark_meas + "'"

    outputs.add_observation(sample=label, variable=f"{var}_hist", trait=f"{measurement} frequencies",
                            method='plantcv.plantcv.photosynthesis.analyze_fvfm', scale='none', datatype=list,
                            value=fvfm_hist.tolist(), label=np.around(midpoints, decimals=len(str(bins))).tolist())
    outputs.add_observation(sample=label, variable=f"{var}_hist_peak", trait=f"peak {measurement} value",
                            method='plantcv.plantcv.photosynthesis.analyze_fvfm', scale='none', datatype=float,
                            value=float(max_bin), label='none')
    outputs.add_observation(sample=label, variable=f"{var}_median", trait=f"{measurement} median",
                            method='plantcv.plantcv.photosynthesis.analyze_fvfm', scale='none', datatype=float,
                            value=float(np.around(fvfm_median, decimals=4)), label='none')
    outputs.add_observation(sample=label, variable=f"{fdark_var}_passed_qc", trait=f"{fdark_meas} passed QC",
                            method='plantcv.plantcv.photosynthesis.analyze_fvfm', scale='none', datatype=bool,
                            value=qc_fdark, label='none')

    return fvfm, hist_df
