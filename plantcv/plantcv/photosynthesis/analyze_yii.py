# photosynthetic efficiency (psiII) analysis from psII camera

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


def analyze_yii(fdark, fmin, fmax, mask, bins=256, parameter='Fv/Fm'):
    """Analyze PSII camera images.
    Inputs:
    fdark       = grayscale fdark image
    fmin        = grayscale fmin image
    fmax        = grayscale fmax image
    mask        = mask of plant (binary, single channel)
    parameter   = a string to identify the photosynthetic parameter. It will be used to label the output plots. default is 'Fv/Fm'
    bins        = number of bins (1 to 256 for 8-bit; 1 to 65,536 for 16-bit; default is 256)
    
    Returns:
    analysis_images = list of images (YII image and YII histogram image)

    :param fdark: numpy.ndarray
    :param fmin: numpy.ndarray
    :param fmax: numpy.ndarray
    :param mask: numpy.ndarray
    :param bins: int
    :return analysis_images: numpy.ndarray
    """

    # Auto-increment the device counter
    params.device += 1
    # Check that fdark, fmin, and fmax are grayscale (single channel)
    if not all(len(np.shape(i)) == 2 for i in [fdark, fmin, fmax]):
        fatal_error(
            "The fdark, fmin, and fmax images must be grayscale images.")
    # # Check that fdark, fmin, and fmax are the same bit
    # if  not (all(i.dtype == "uint16" for i in [fdark, fmin, fmax]) or
    #         (all(i.dtype == "uint8" for i in [fdark, fmin, fmax]))):
    #     fatal_error("The fdark, fmin, and fmax images must all be the same bit depth.")
    # Check that fdark, fmin, and fmax are 16-bit images
    # if not all(i.dtype == "uint16" for i in [fdark, fmin, fmax]):
    #     fatal_error("The fdark, fmin, and fmax images must be 16-bit images.")

    # Mask Fmin and Fmax Image
    fmin_mask = cv2.bitwise_and(fmin, fmin, mask=mask)
    fmax_mask = cv2.bitwise_and(fmax, fmax, mask=mask)

    # To calculate the divisions properly we need to change from unit16 to float64 data types
    out_flt = np.zeros_like(mask, dtype='float64')
    # Calculate Fvariable, where Fv = Fmax - Fmin (masked)
    fv = np.subtract(fmax_mask, fmin_mask, out=out_flt.copy(),
                     where=fmin_mask < fmax_mask)

    # make sure to initialize with out=. using where= provides random values at False pixels. you will get a strange result.
    # this was a problem when (because?) mask comes from Fm instead of Fm' so the plant pixels can be different
    #mask<0, fmax>0 = FALSE: not part of plant but fluorescence detected.
    #mask>0, fmax<=0 = FALSE: part of plant in Fm but no fluorescence detected(!!!, plant movement?)
    yii = np.divide(fv, fmax_mask, out=out_flt.copy(),
                    where=np.logical_and(fv > 0, fmax_mask > 0))

    analysis_images = []
    analysis_images.append(yii)

    # Calculate the median and std YII values for non-zero pixels
    yii_median = masked_stats.masked_median(yii, mask)
    yii_std = masked_stats.masked_std(yii, mask)

    # Calculate the histogram of Fv/Fm non-zero values
    yii_hist, yii_bins = np.histogram(
        yii[np.where(yii > 0)], bins, range=(0, 1))
    # yii_bins is a bins + 1 length list of bin endpoints, so we need to calculate bin midpoints so that
    # the we have a one-to-one list of x (yii) and y (frequency) values.
    # To do this we add half the bin width to each lower bin edge x-value
    midpoints = yii_bins[:-1] + 0.5 * np.diff(yii_bins)

    # Calculate which non-zero bin has the maximum Fv/Fm value
    max_bin = midpoints[np.argmax(yii_hist)]

    # Create Histogram Plot, if you change the bin number you might need to change binx so that it prints
    # an appropriate number of labels
    # Create a dataframe
    dataset = pd.DataFrame({'Plant Pixels': yii_hist, parameter: midpoints})
    # Make the histogram figure using plotnine
    yii_hist_fig = (ggplot(data=dataset, mapping=aes(x=parameter, y='Plant Pixels'))
                    + geom_line(color='green', show_legend=True)
                    + geom_label(label='Peak Bin Value: ' + str(max_bin),
                                 x=.15, y=205, size=8, color='green'))
    analysis_images.append(yii_hist_fig)

    if params.debug == 'print':
        print_image(fmin_mask, os.path.join(params.debug_outdir,
                                            str(params.device) + '_fmin_mask.png'))
        print_image(fmax_mask, os.path.join(params.debug_outdir,
                                            str(params.device) + '_fmax_mask.png'))
        print_image(yii, os.path.join(params.debug_outdir,
                                      str(params.device) + '_yii.png'))
        yii_hist_fig.save(os.path.join(params.debug_outdir,
                                       str(params.device) + '_yii_hist.png'))
    elif params.debug == 'plot':
        plot_image(fmin_mask, cmap='gray')
        plot_image(fmax_mask, cmap='gray')
        plot_image(yii, cmap='gray')
        print(yii_hist_fig)

    outputs.add_observation(variable='yii_hist', trait='YII frequencies',
                            method='plantcv.plantcv.photosynthesis.analyze_yii', scale='none', datatype=list,
                            value=yii_hist.tolist(), label=np.around(midpoints, decimals=len(str(bins))).tolist())
    outputs.add_observation(variable='yii_hist_peak', trait='peak YII value',
                            method='plantcv.plantcv.photosynthesis.analyze_yii', scale='none', datatype=float,
                            value=float(max_bin), label='none')
    outputs.add_observation(variable='yii_median', trait='YII median',
                            method='plantcv.plantcv.photosynthesis.analyze_yii', scale='none', datatype=float,
                            value=float(np.around(yii_median, decimals=4)), label='none')
    outputs.add_observation(variable='yii_std', trait='yii standard deviation',
                            method='plantcv.plantcv.photosynthesis.analyze_yii', scale='none', datatype=float,
                            value=float(np.around(yii_std, decimals=4)), label='none')

    # Store images
    outputs.images.append(analysis_images)

    return analysis_images
