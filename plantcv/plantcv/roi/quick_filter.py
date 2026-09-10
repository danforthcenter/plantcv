"""PlantCV fast_filter module."""
import os
import cv2
import numpy as np
from plantcv.plantcv import fatal_error
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._globals import params


def quick_filter(mask, roi, roi_type="partial"):
    """Filter a binary mask using a region of interest and connected components.

    Parameters
    ----------
    mask : numpy.ndarray
        Binary mask to filter.
    roi : plantcv.plantcv.classes.Objects
        PlantCV ROI object.
    roi_type : str, optional
        Type of ROI filtering: "partial", "cutto", "within", or "largest".

    Returns
    -------
    numpy.ndarray
        Filtered binary mask.
    """
    params.device += 1
    roi_masks = _roi2masks(mask=mask, roi=roi)
    filtered_mask = _filter_by_roi_masks(mask=mask, roi_masks=roi_masks, roi_type=roi_type)
    _debug(visual=filtered_mask,
           filename=os.path.join(params.debug_outdir, f"{params.device}_roi_filter.png"),
           cmap="gray")
    return filtered_mask


def _roi2masks(mask, roi):
    """Turn a list of ROIs into binary masks

    Parameters
    ----------
    mask : numpy.ndarray
        Binary mask to filter.
    roi : plantcv.plantcv.classes.Objects
        PlantCV ROI object.

    Returns
    -------
    list
        ROI Masks, numpy.ndarray objects

    """
    roi_masks = []
    for single_roi in roi:
        roi_mask = np.zeros(mask.shape[:2], dtype=np.uint8)
        cv2.drawContours(roi_mask, single_roi.contours[0], -1, 255, -1)
        roi_masks.append(roi_mask)
    return roi_masks


def _filter_by_roi_masks(mask, roi_masks, roi_type):
    """Filter by ROI masks

    Parameters
    ----------
    mask : numpy.ndarray
        Binary mask to filter.
    roi_masks : list
        numpy.ndarrays of binary masks
    roi_type : str, optional
        Type of ROI filtering: "partial", "cutto", "within", or "largest".

    Returns
    -------
    numpy.ndarray
        Binary Mask
    """
    roi_type = roi_type.lower()
    binary = (mask > 0).astype(np.uint8) * 255
    # elementwise max across all roi_masks, i.e. OR them together into one combined mask
    roi_mask = np.maximum.reduce(roi_masks) if roi_masks else np.zeros(binary.shape[:2], dtype=np.uint8)

    if roi_type == "cutto":
        # keep only the binary-mask pixels that fall inside the ROI mask
        return cv2.bitwise_and(binary, roi_mask)

    if roi_type == "largest":
        return _largest_in_each_roi(binary=binary, roi_masks=roi_masks)

    # cv2.connectedComponentsWithStats: label each separate blob (8-connected neighbors) of the binary mask
    # with a unique integer ID (0 = background); returns the count of labels, a label-ID image, per-label
    # stats (bounding box/area), and centroids (_)
    num_labels, labels, _stats, _ = cv2.connectedComponentsWithStats(binary, connectivity=8)
    if num_labels <= 1:
        return np.zeros(binary.shape, dtype=np.uint8)

    inside = roi_mask > 0
    # flatten the 2D labels image into a 1D array so np.bincount can
    # tally values across every pixel
    label_ids = labels.ravel()
    # np.bincount: count, for each label ID, how many of its pixels are weighted by "inside";
    # weights must be flattened (ravel) to line up with label ids.
    overlap_counts = np.bincount(
        label_ids,
        weights=inside.ravel().astype(np.uint8),
        minlength=num_labels,
    )

    if roi_type == "partial":
        selected = overlap_counts > 0
        selected[0] = False  # never select background label 0
    elif roi_type == "within":
        # count each component's pixels out of ROI
        outside_counts = np.bincount(
            label_ids,
            weights=(~inside).ravel().astype(np.uint8),
            minlength=num_labels,
        )
        # make an index of things that do overlap the ROI and do not have any pixels outside of the ROI
        selected = (overlap_counts > 0) & (outside_counts == 0)
        selected[0] = False  # never select background label 0
    else:
        fatal_error(f'ROI Type {roi_type} is not "cutto", "largest", "within" or "partial"!')

    # make and return a binary mask of all the kept labels
    return np.where(selected[labels], 255, 0).astype(np.uint8)


def _largest_in_each_roi(binary, roi_masks):
    """Find largest object partially in each mask

    Parameters
    ----------
    binary : numpy.ndarray
        Binary Mask
    roi_masks : list
        List of ROI masks

    Returns
    numpy.ndarray
        Binary Mask of the largest object touching each ROI
    -------
    """
    output = np.zeros(binary.shape[:2], dtype=np.uint8)
    # label the whole, uncut mask once — same as "partial" — so area and
    # extent always refer to the full object, never a ROI-clipped sliver
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(binary, connectivity=8)
    if num_labels <= 1:
        return output
    label_ids = labels.ravel()
    for roi_mask in roi_masks:
        inside = roi_mask > 0
        # same overlap test "partial" uses: does this label touch the ROI at all?
        overlap_counts = np.bincount(
            label_ids,
            weights=inside.ravel().astype(np.uint8),
            minlength=num_labels,
        )
        candidates = np.flatnonzero(overlap_counts > 0)
        candidates = candidates[candidates != 0]  # exclude background label 0
        if candidates.size > 0:
            # rank candidates by their full area, not the portion inside the ROI
            best = candidates[np.argmax(stats[candidates, cv2.CC_STAT_AREA])]
            output[labels == best] = 255
    return output
