# NPQ analysis from PSII cameras

import os
import cv2
import numpy as np
import pandas as pd
from plotnine import ggplot, geom_label, aes, geom_line
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params
from plantcv.plantcv import outputs
from plantcv.plantcv import masked_stats as masked_stats



def analyze_npq(fmax, fm, mask, bins=256):
    """Analyze NPQ from PSII camera images.
    Inputs:
    fmax        = grayscale fmax image (maximum fluoresence after the saturating pulse for your measurement)
    fm          = grayscale fm image (maximum fluoresence after the saturating pulse for a dark-adapted plant)
    mask        = mask of plant (binary, single channel)
    bins        = number of bins (1 to 256 for 8-bit; 1 to 65,536 for 16-bit; default is 256)
    
    Returns:
    analysis_images = list of images (npq image and npq histogram image)

    :param fmax: numpy.ndarray
    :param fm: numpy.ndarray
    :param mask: numpy.ndarray
    :param bins: int
    :return analysis_images: list
    """

    # Auto-increment the device counter
    params.device += 1
    # Check that fdark, fmin, and fmax are grayscale (single channel)
    if not all(len(np.shape(i)) == 2 for i in [fmax, fm]):
        fatal_error(
            "The fmax, fm images must be grayscale images.")
    # # Check that fdark, fmin, and fmax are the same bit
    # if  not (all(i.dtype == "uint16" for i in [fdark, fmin, fmax]) or
    #         (all(i.dtype == "uint8" for i in [fdark, fmin, fmax]))):
    #     fatal_error("The fdark, fmin, and fmax images must all be the same bit depth.")
    # Check that fdark, fmin, and fmax are 16-bit images
    # if not all(i.dtype == "uint16" for i in [fdark, fmin, fmax]):
    #     fatal_error("The fdark, fmin, and fmax images must be 16-bit images.")

    # Mask Fmin and Fmax Image
    fmax_mask = cv2.bitwise_and(fmax, fmax, mask=mask)
    fm_mask = cv2.bitwise_and(fm, fm, mask=mask)

    # Initialize floatingpoint array
    out_flt = np.zeros_like(mask, dtype='float64')

    # Calculate NPQ, where NPQ = Fm/Fm' - 1 (masked)
    npq = np.divide(fm_mask, fmax_mask, out=out_flt.copy(),
                    where=fmax_mask > 0)
    npq = np.subtract(npq, 1, out=out_flt.copy(),
                      where=np.logical_and(npq >= 1, fmax_mask > 0))

    analysis_images = []
    analysis_images.append(npq)

    # Calculate the median and std NPQ values for non-zero pixels
    npq_median = masked_stats.median(npq, mask)
    npq_std = masked_stats.std(npq, mask)

    # Calculate the histogram of Fv/Fm non-zero values
    npq_hist, npq_bins = np.histogram(
        npq[np.where(npq > 0)], bins, range=(0, 3))
    # npq_bins is a bins + 1 length list of bin endpoints, so we need to calculate bin midpoints so that
    # the we have a one-to-one list of x (npq) and y (frequency) values.
    # To do this we add half the bin width to each lower bin edge x-value
    midpoints = npq_bins[:-1] + 0.5 * np.diff(npq_bins)

    # Calculate which non-zero bin has the maximum Fv/Fm value
    max_bin = midpoints[np.argmax(npq_hist)]

    # Create Histogram Plot, if you change the bin number you might need to change binx so that it prints
    # an appropriate number of labels
    # Create a dataframe
    dataset = pd.DataFrame({'Plant Pixels': npq_hist, 'NPQ': midpoints})
    # Make the histogram figure using plotnine
    npq_hist_fig = (ggplot(data=dataset, mapping=aes(x='NPQ', y='Plant Pixels'))
                    + geom_line(color='green', show_legend=True)
                    + geom_label(label='Peak Bin Value: ' + str(max_bin),
                                 x=.15, y=205, size=8, color='green'))
    analysis_images.append(npq_hist_fig)

    if params.debug == 'print':
        print_image(fm_mask, os.path.join(params.debug_outdir,
                                          str(params.device) + '_fm_mask.png'))
        print_image(fmax_mask, os.path.join(params.debug_outdir,
                                            str(params.device) + '_fmax_mask.png'))
        print_image(npq, os.path.join(params.debug_outdir,
                                      str(params.device) + '_npq.png'))
        npq_hist_fig.save(os.path.join(params.debug_outdir,
                                       str(params.device) + '_npq_hist.png'))
    elif params.debug == 'plot':
        plot_image(fm_mask, cmap='gray')
        plot_image(fmax_mask, cmap='gray')
        plot_image(npq, cmap='gray')
        print(npq_hist_fig)

    outputs.add_observation(variable='npq_hist', trait='npq frequencies',
                            method='plantcv.plantcv.photosynthesis.analyze_npq', scale='none', datatype=list,
                            value=npq_hist.tolist(), label=np.around(midpoints, decimals=len(str(bins))).tolist())
    outputs.add_observation(variable='npq_hist_peak', trait='peak npq value',
                            method='plantcv.plantcv.photosynthesis.analyze_npq', scale='none', datatype=float,
                            value=float(max_bin), label='none')
    outputs.add_observation(variable='npq_median', trait='npq median',
                            method='plantcv.plantcv.photosynthesis.analyze_npq', scale='none', datatype=float,
                            value=float(np.around(npq_median, decimals=4)), label='none')
    outputs.add_observation(variable='npq_std', trait='npq standard deviation',
                            method='plantcv.plantcv.photosynthesis.analyze_npq', scale='none',datatype=float,
                            value=float(np.around(npq_std, decimals=4)), label='none')

    # Store images
    outputs.images.append(analysis_images)

    return analysis_images
