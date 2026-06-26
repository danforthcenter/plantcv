"""PlantCV fast_filter module."""
import os
import cv2
import numpy as np
from plantcv.plantcv import fatal_error
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._globals import params


def fast_filter(mask, roi, roi_type="partial"):
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
    roi_masks = _roi2masks(mask=mask, roi=roi)
    filtered_mask = _filter_by_roi_masks(mask=mask, roi_masks=roi_masks, roi_type=roi_type)
    _debug(visual=filtered_mask,
           filename=os.path.join(params.debug_outdir, f"{params.device}_roi_filter.png"),
           cmap="gray")
    return filtered_mask


def fast_rect_filter(mask, rois, roi_type="partial"):
    """Filter a binary mask using one or more rectangular ROIs.

    Parameters
    ----------
    mask : numpy.ndarray
        Binary mask to filter.
    rois : list
        Rectangular ROIs as ``(x, y, width, height)`` tuples.
    roi_type : str, optional
        Type of ROI filtering: "partial", "cutto", "within", or "largest".

    Returns
    -------
    numpy.ndarray
        Filtered binary mask.
    """
    roi_masks = _rects2masks(shape=mask.shape[:2], rois=rois)
    filtered_mask = _filter_by_roi_masks(mask=mask, roi_masks=roi_masks, roi_type=roi_type)
    _debug(visual=filtered_mask,
           filename=os.path.join(params.debug_outdir, f"{params.device}_roi_filter.png"),
           cmap="gray")
    return filtered_mask


def _roi2masks(mask, roi):
    roi_masks = []
    for single_roi in roi:
        roi_mask = np.zeros(mask.shape[:2], dtype=np.uint8)
        cv2.drawContours(roi_mask, single_roi.contours[0], -1, 255, -1)
        roi_masks.append(roi_mask)
    return roi_masks


def _rects2masks(shape, rois):
    roi_masks = []
    height, width = shape
    for x, y, w, h in rois:
        x0 = max(0, min(width, int(round(x))))
        y0 = max(0, min(height, int(round(y))))
        x1 = max(0, min(width, int(round(x + w))))
        y1 = max(0, min(height, int(round(y + h))))
        if x1 > x0 and y1 > y0:
            roi_mask = np.zeros(shape, dtype=np.uint8)
            roi_mask[y0:y1, x0:x1] = 255
            roi_masks.append(roi_mask)
    return roi_masks


def _filter_by_roi_masks(mask, roi_masks, roi_type):
    roi_type = roi_type.lower()
    binary = (mask > 0).astype(np.uint8) * 255
    roi_mask = np.maximum.reduce(roi_masks) if roi_masks else np.zeros(binary.shape[:2], dtype=np.uint8)

    if roi_type == "cutto":
        return cv2.bitwise_and(binary, roi_mask)

    if roi_type == "largest":
        return _largest_in_each_roi(binary=binary, roi_masks=roi_masks)

    num_labels, labels, _stats, _ = cv2.connectedComponentsWithStats(binary, connectivity=8)
    if num_labels <= 1:
        return np.zeros(binary.shape, dtype=np.uint8)

    inside = roi_mask > 0
    label_ids = labels.ravel()
    overlap_counts = np.bincount(
        label_ids,
        weights=inside.ravel().astype(np.uint8),
        minlength=num_labels,
    )

    if roi_type == "partial":
        selected = overlap_counts > 0
        selected[0] = False
    elif roi_type == "within":
        outside_counts = np.bincount(
            label_ids,
            weights=(~inside).ravel().astype(np.uint8),
            minlength=num_labels,
        )
        selected = (overlap_counts > 0) & (outside_counts == 0)
        selected[0] = False
    else:
        fatal_error(f'ROI Type {roi_type} is not "cutto", "largest", "within" or "partial"!')

    return np.where(selected[labels], 255, 0).astype(np.uint8)


def _largest_in_each_roi(binary, roi_masks):
    output = np.zeros(binary.shape[:2], dtype=np.uint8)
    for roi_mask in roi_masks:
        clipped = cv2.bitwise_and(binary, roi_mask)
        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats((clipped > 0).astype(np.uint8), connectivity=8)
        if num_labels <= 1:
            continue
        best = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
        output[labels == best] = 255
    return output
