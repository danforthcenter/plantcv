"""Outputs the average pixel values from a percentile radially outward from an object's center."""
from plantcv.plantcv import params, Objects, apply_mask, auto_crop, outputs
from plantcv.plantcv import roi as roi_
from plantcv.plantcv._debug import _debug
import cv2
import os
import numpy as np


def _calc_dists(img, mask, percentile, store_debug, ind=None):
    """Calculates the distances of each pixel,
    the cutoff based on given percentile,
    and the average pixel values within that cutoff.

    Parameters
    ----------
    img : numpy.ndarray
        RGB or grayscale image cropped to a focal object
    mask : numpy.ndarray
        Segmented mask of the object from img
    percentile : number
        Cutoff for inclusion of pixels (percent from center)
    store_debug : str or None
        Value for params.debug when function is called
    ind : int, optional
        Tracker for which in multi ROI gets a debug, by default None

    Returns
    -------
    avgs : float or list
        average pixel values (gray or RGB) within the distance percentile
    """
    # Analyze shape properties
    m = cv2.moments(mask, binaryImage=True)
    cmx = m['m10'] / m['m00']
    cmy = m['m01'] / m['m00']
    center = (cmx, cmy)
    # Calculate point distances from center
    y, x = np.ogrid[:img.shape[0], :img.shape[1]]
    distances = np.sqrt((x - center[0])**2 + (y - center[1])**2)
    if len(img.shape) == 3:
        distances = np.stack([distances for _ in range(3)], axis=2)
    # Distance cutoff based on percentile
    cutoff = (np.sqrt((img.shape[0]/2)**2 + (img.shape[1]/2)**2))*(percentile/100)
    img_cutoff = np.where(distances < cutoff, img, np.nan)
    # One example debug
    if ind == 0:
        example = np.where(distances < cutoff, img, 0)
        params.debug = store_debug
        _debug(visual=example, filename=os.path.join(params.debug_outdir, str(params.device) + "_radial_average.png"))
        params.debug = None

    avgs = float(np.nanmean(img_cutoff))

    if len(img.shape) == 3:
        avgs = [float(np.nanmean(img_cutoff[:, :, [2]])),
                float(np.nanmean(img_cutoff[:, :, [1]])),
                float(np.nanmean(img_cutoff[:, :, [0]]))]

    return avgs


def radial_percentile(img, mask, roi=None, percentile=50, label=None):
    """_summary_

    Parameters
    ----------
    img : numpy.ndarray
        RGB or grayscale image
    mask : numpy.ndarray
        Binary mask with objects of interest segmented
    roi : plantcv.plantcv.Objects, optional
        Region of Interest, single or multi, to identify objects, by default None
    percentile : int, optional
        Percentile of max distance from center in which to average pixel values, by default 50
    label : str, optional
        Optional label for outputs (default = pcv.params.sample_label)

    Returns
    -------
    avgs : list
        average pixel values (gray or RGB) within the distance percentile
    """
    if label is None:
        label = params.sample_label

    store_debug = params.debug
    params.debug = None
    if roi:
        avgs = []
        for i, _ in enumerate(roi.contours):
            # Loop through rois (even if there is only 1)
            roi_ind = Objects(contours=[roi.contours[i]], hierarchy=[roi.hierarchy[i]])
            # Filter mask by roi and apply it to the image
            filt = roi_.filter(mask=mask, roi=roi_ind)
            # Check for empty
            if len(np.unique(filt)) == 1:
                if len(img.shape) == 3:
                    avgs.append(["nan", "nan", "nan"])
                else:
                    avgs.append("nan")
            else:
                masked = apply_mask(img=img, mask=filt, mask_color='black')
                # Crop the image and the mask to the roi
                crop_img = auto_crop(img=masked, mask=filt, padding_x=1, padding_y=1, color='black')
                crop_mask = auto_crop(img=filt, mask=filt, padding_x=1, padding_y=1, color='black')

                # Calculate average of each channel
                avgs.append(_calc_dists(img=crop_img, mask=crop_mask, percentile=percentile, store_debug=store_debug, ind=i))

    else:
        masked = apply_mask(img=img, mask=mask, mask_color='black')
        # Crop the image and the mask to the roi
        crop_img = auto_crop(img=masked, mask=mask, padding_x=1, padding_y=1, color='black')
        crop_mask = auto_crop(img=mask, mask=mask, padding_x=1, padding_y=1, color='black')

        # Calculate averages of each channel
        avgs = [_calc_dists(img=crop_img, mask=crop_mask, percentile=percentile, store_debug=store_debug, ind=0)]

    # Outputs
    for idx, i in enumerate(avgs):
        if isinstance(i, float):
            outputs.add_observation(sample=label+"_"+str(idx+1), variable='gray_'+str(percentile)+'%_avg',
                                    trait='gray_'+str(percentile)+'%_radial_average',
                                    method='plantcv.plantcv.analyze.radial',
                                    scale='none', datatype=float, value=i, label='none')
        elif isinstance(i, list):
            outputs.add_observation(sample=label+"_"+str(idx+1), variable='red_'+str(percentile)+'%_avg',
                                    trait='red_'+str(percentile)+'%_radial_average',
                                    method='plantcv.plantcv.analyze.radial',
                                    scale='none', datatype=float, value=i[0], label='none')
            outputs.add_observation(sample=label+"_"+str(idx+1), variable='green_'+str(percentile)+'%_avg',
                                    trait='green_'+str(percentile)+'%_radial_average',
                                    method='plantcv.plantcv.analyze.radial',
                                    scale='none', datatype=float, value=i[1], label='none')
            outputs.add_observation(sample=label+"_"+str(idx+1), variable='blue_'+str(percentile)+'%_avg',
                                    trait='blue_'+str(percentile)+'%_radial_average',
                                    method='plantcv.plantcv.analyze.radial',
                                    scale='none', datatype=float, value=i[2], label='none')

    params.debug = store_debug
    return avgs
