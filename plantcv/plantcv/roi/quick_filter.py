"""PlantCV quick_filter module."""
import os
import cv2
import numpy as np
from skimage.measure import label
from skimage.color import label2rgb
from plantcv.plantcv._globals import params
from plantcv.plantcv.roi import roi2mask
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _logical_operation


def quick_filter(mask, roi, roi_type="partial"):
    """Quickly filter a binary mask using a region of interest.

    Parameters
    ----------
    mask : numpy.ndarray
        Binary mask to filter.
    roi : plantcv.plantcv.classes.Objects
        PlantCV ROI object.
    roi_type : str, optional
        filter method, one of "partial", "cutto", or "within"

    Returns
    -------
    numpy.ndarray
        Filtered binary mask.
    """
    # Check that the roi_type is valid
    if roi_type.upper() not in ["PARTIAL", "CUTTO", "WITHIN"]:
        raise ValueError(f"roi_type {roi_type} must be one of 'partial', 'cutto', or 'within'")

    # process for cutto is different, so if roi_type is cutto then use helper function
    if roi_type.upper() == "CUTTO":
        return _quick_cutto(mask, roi)[0]

    # Increment the device counter
    params.device += 1

    # Store debug
    debug = params.debug
    params.debug = None

    # Label objects in the image from 1 to n (labeled mask)
    labels, num = label(label_image=mask, return_num=True)

    # Convert the input ROI to a binary mask (only works on single ROIs)
    roi_mask = roi2mask(img=mask, roi=roi)
    params.debug = debug

    # Convert the labeled mask and ROI mask to float data types
    roi_mask = roi_mask.astype(float)
    labels = labels.astype(float)

    # Set the ROI mask value to the number of labels
    roi_mask[np.where(roi_mask == 255)] = num

    # Add the labeled mask and ROI mask together
    summed = roi_mask + labels

    # For objects that partially overlap or are contained within the ROI
    if roi_type.upper() == "PARTIAL":
        return _quick_partial(labels, summed, num)

    if roi_type.upper() == "WITHIN":
        return _quick_within(labels, summed, num)


def _quick_cutto(mask, roi):
    """Quickly filter a binary mask using a region of interest by cutting to each ROI.

    Parameters
    ----------
    mask : numpy.ndarray
        Binary mask to filter.
    roi : plantcv.plantcv.classes.Objects
        PlantCV ROI object.

    Returns
    -------
    numpy.ndarray, numpy.ndarray, int
        Filtered binary mask, labeled mask, number of labels.
    """
    # Increment the device counter
    params.device += 1

    # Store debug
    debug = params.debug
    params.debug = None

    mask_copy = np.copy(mask).astype(np.int32)
    labeled_mask = np.zeros(mask.shape, dtype=np.int32)
    bin_mask = np.copy(labeled_mask)
    num_labels = len(roi.contours)
    for i in range(num_labels):
        # Pixel intensity of (i+1) such that the first object has value
        cv2.drawContours(labeled_mask, roi.contours[i], -1, (i+1), -1)
        cv2.drawContours(bin_mask, roi.contours[i], -1, (255), -1)
    cropped_mask = _logical_operation(mask_copy, bin_mask, "and")
    # Make a labeled mask from the cropped objects
    label_mask_where = np.where(cropped_mask == 255, labeled_mask, 0)

    # Print/plot debug image
    colorful = label2rgb(label_mask_where)
    colorful2 = (255*colorful).astype(np.uint8)
    params.debug = debug
    _debug(visual=colorful2, filename=os.path.join(params.debug_outdir, f"{params.device}_label_colored_cutto_mask.png"))

    return cropped_mask.astype(np.uint8), label_mask_where, num_labels


def _quick_partial(labeled_mask, summed_mask, num):
    """Quickly filter a binary mask using a region of interest by cutting to each ROI and including partial objects.

    Parameters
    ----------
    labeled_mask : numpy.ndarray
        Labeled mask to use for filtering.
    summed_mask : numpy.ndarray
        Labeled mask plus the ROI mask.
    num : int
        Number of labels.

    Returns
    -------
    numpy.ndarray
        Filtered binary mask.
    """
    # Get the unique values in the summed image
    unique_nums = np.unique(summed_mask)
    # Create a new mask
    filtered_mask = np.zeros(labeled_mask.shape, dtype=np.uint8)
    # Loop over the unique values where a label plus the largest label were added together
    for n in unique_nums[np.where(unique_nums > num)]:
        # Get the label value by subtracting the number of labels from the unique value
        idx = n - num
        # Add the object to the new mask
        filtered_mask[np.where(labeled_mask == idx)] = 255
    # Print/plot debug image
    _debug(visual=filtered_mask, filename=os.path.join(params.debug_outdir,
                                                       f"{params.device}_roi_partial_filter.png"), cmap="gray")
    return filtered_mask


def _quick_within(labeled_mask, summed_mask, num):
    """Quickly filter a binary mask using a region of interest by including objects fully within the ROI.

    Parameters
    ----------
    labeled_mask : numpy.ndarray
        Labeled mask to use for filtering.
    summed_mask : numpy.ndarray
        Labeled mask plus the ROI mask.
    num : int
        Number of labels.

    Returns
    -------
    numpy.ndarray
         Filtered binary mask.
    """
    for i in range(1, num + 1):
        # If one pixel of the object falls outside the ROI
        # set all the label values to zero
        if i in summed_mask:
            # Remove the object from the labeled mask
            labeled_mask[np.where(labeled_mask == i)] = 0
    # Convert the labeled mask to a uint8 binary mask
    labeled_mask[np.where(labeled_mask > 0)] = 255
    labeled_mask = labeled_mask.astype(np.uint8)
    # Print/plot debug image
    _debug(visual=labeled_mask, filename=os.path.join(params.debug_outdir,
                                                      f"{params.device}_roi_within_filter.png"), cmap="gray")
    return labeled_mask
