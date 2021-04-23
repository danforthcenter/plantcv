# Fluorescence Analysis (Fv/Fm parameter)

import os
import cv2
import numpy as np
import pandas as pd
from plotnine import ggplot, geom_label, aes, geom_line
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import params
from plantcv.plantcv import outputs


def analyze_fvfm(data, mask, bins=256, label="default"):
    """Calculate and analyze Fv/Fm from fluorescence image data.
    Inputs:
    data        = xarray of binary image data
    mask        = mask of plant (binary, single channel)
    bins        = number of bins (1 to 256 for 8-bit; 1 to 65,536 for 16-bit; default is 256)
    label       = optional label parameter, modifies the variable name of observations recorded

    Returns:
    analysis_images = list of images (fv image and fvfm histogram image)
    :param data: xarray.core.dataarray.DataArray
    :param mask: numpy.ndarray
    :param bins: int
    :param label: str
    :return analysis_images: numpy.ndarray
    """

    # Auto-increment the device counter
    params.device += 1
    #  Extract frames of interest
    fdark = (data.sel(frame_label='fdark').data).astype(np.uint8)
    fmax = data.sel(frame_label='fmax').data.astype(np.uint8)
    fmin = data.sel(frame_label='fmin').data.astype(np.uint8)
    mask_int = mask.astype(np.uint8)
    print(np.shape(fdark))
    print(np.shape(mask_int))

    # QC Fdark Image
    fdark_mask = cv2.bitwise_and(fdark, fdark, mask=mask_int)
    if np.amax(fdark_mask) > 2000:
        qc_fdark = False
    else:
        qc_fdark = True

    # Mask Fmin and Fmax Image
    fmin_mask = cv2.bitwise_and(fmin, fmin, mask=mask_int)
    fmax_mask = cv2.bitwise_and(fmax, fmax, mask=mask_int)

    # Calculate Fvariable, where Fv = Fmax - Fmin (masked)
    fv = np.subtract(fmax_mask, fmin_mask)

    # When Fmin is greater than Fmax, a negative value is returned.
    # Because the data type is unsigned integers, negative values roll over, resulting in nonsensical values
    # Wherever Fmin is greater than Fmax, set Fv to zero
    fv[np.where(fmax_mask < fmin_mask)] = 0
    analysis_images = []

    # Calculate Fv/Fm (Fvariable / Fmax) where Fmax is greater than zero
    # By definition above, wherever Fmax is zero, Fvariable will also be zero
    # To calculate the divisions properly we need to change from unit16 to float64 data types
    fvfm = fv.astype(np.float64)
    analysis_images.append(fvfm)
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

    # Create a dataframe
    dataset = pd.DataFrame({'Plant Pixels': fvfm_hist, 'Fv/Fm': midpoints})
    # Make the histogram figure using plotnine
    fvfm_hist_fig = (ggplot(data=dataset, mapping=aes(x='Fv/Fm', y='Plant Pixels'))
                     + geom_line(color='green', show_legend=True)
                     + geom_label(label='Peak Bin Value: ' + str(max_bin),
                                  x=.15, y=205, size=8, color='green'))
    analysis_images.append(fvfm_hist_fig)

    # Plot/Print out fvfm and the histogram
    _debug(visual=fvfm, filename=os.path.join(params.debug_outdir, str(params.device) + "_FvFm.png"))
    _debug(visual=fvfm_hist_fig, filename=os.path.join(params.debug_outdir, str(params.device) + "_FvFm_histogram.png"))

    outputs.add_observation(sample=label, variable='fvfm_hist', trait='Fv/Fm frequencies',
                            method='plantcv.plantcv.photosynthesis.analyze_fvfm', scale='none', datatype=list,
                            value=fvfm_hist.tolist(), label=np.around(midpoints, decimals=len(str(bins))).tolist())
    outputs.add_observation(sample=label, variable='fvfm_hist_peak', trait='peak Fv/Fm value',
                            method='plantcv.plantcv.photosynthesis.analyze_fvfm', scale='none', datatype=float,
                            value=float(max_bin), label='none')
    outputs.add_observation(sample=label, variable='fvfm_median', trait='Fv/Fm median',
                            method='plantcv.plantcv.photosynthesis.analyze_fvfm', scale='none', datatype=float,
                            value=float(np.around(fvfm_median, decimals=4)), label='none')
    outputs.add_observation(sample=label, variable='fdark_passed_qc', trait='Fdark passed QC',
                            method='plantcv.plantcv.photosynthesis.analyze_fvfm', scale='none', datatype=bool,
                            value=qc_fdark, label='none')

    # Store images
    outputs.images.append(analysis_images)

    return analysis_images