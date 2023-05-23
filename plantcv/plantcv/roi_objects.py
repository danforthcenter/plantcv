# Find objects partially inside a region of interest or cuts objects to the ROI

import cv2
import numpy as np
import os
from plantcv.plantcv import logical_and
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _cv2_findcontours
from plantcv.plantcv import fatal_error, warn
from plantcv.plantcv import params
from plantcv.plantcv import Objects


def roi_objects(img, roi, obj, roi_type="partial"):
    """
    Find objects partially inside a region of interest or cut objects to the ROI.

    Inputs:
    img            = RGB or grayscale image data for plotting
    roi            = region of interest, an instance of the Object class output from a roi function
    obj            = contours of objects, output from "find_objects" function
    roi_type       = 'cutto', 'partial' (for partially inside, default), or 'largest' (keep only the largest contour)

    Returns:
    kept_cnt       = kept contours as an instance of the Object class
    mask           = mask image
    obj_area       = total object pixel area

    :param img: numpy.ndarray
    :param roi: plantcv.plantcv.classes.Objects
    :param obj: plantcv.plantcv.classes.Objects
    :param roi_type: str
    :return kept_cnt: plantcv.plantcv.classes.Objects
    :return mask: numpy.ndarray
    :return obj_area: int
    """
    # Store debug
    debug = params.debug
    params.debug = None

    if len(roi.contours) > 1:
        warn("Received a multi-ROI but only the first ROI will be used. Consider using a for loop for multi-ROI")

    roi_contour = roi.contours[0]
    roi_hierarchy = roi.hierarchy[0]
    object_contour = obj.contours[0]
    obj_hierarchy = obj.hierarchy[0]

    # Create an empty grayscale (black) image the same dimensions as the input image
    mask = np.zeros(np.shape(img)[:2], dtype=np.uint8)
    cv2.drawContours(mask, object_contour, -1, (255), -1, lineType=8, hierarchy=obj_hierarchy)

    # Create a mask of the filled in ROI
    roi_mask = np.zeros(np.shape(img)[:2], dtype=np.uint8)
    roi_points = np.vstack(roi_contour[0])
    cv2.fillPoly(roi_mask, [roi_points], (255))

    # Make a copy of the input image for plotting
    ori_img = np.copy(img)
    # If the reference image is grayscale convert it to color
    if len(np.shape(ori_img)) == 2:
        ori_img = cv2.cvtColor(ori_img, cv2.COLOR_GRAY2BGR)

    # Allows user to find all objects that are completely inside or overlapping with ROI
    if roi_type.upper() in ('PARTIAL', 'LARGEST'):
        # Filter contours outside of the region of interest
        for c, cnt in enumerate(object_contour):
            filtering_mask = np.zeros(np.shape(img)[:2], dtype=np.uint8)
            cv2.fillPoly(filtering_mask, [np.vstack(object_contour[c])], (255))
            overlap_img = logical_and(filtering_mask, roi_mask)
            # Delete contours that do not overlap at all with the ROI
            if np.sum(overlap_img) == 0:
                cv2.drawContours(mask, object_contour, c, (0), -1, lineType=8, hierarchy=obj_hierarchy)

        # Find the kept contours and area
        kept_cnt, kept_hierarchy = _cv2_findcontours(bin_img=mask)
        obj_area = cv2.countNonZero(mask)

        # Find the largest contour if roi_type is set to 'largest'
        if roi_type.upper() == 'LARGEST':
            # Print warning statement about this feature
            warn("roi_type='largest' will only return the largest contour and its immediate children. Other "
                 "subcontours will be dropped.")
            # Find the index of the largest contour in the list of contours
            largest_area = 0
            index = 0
            for c, cnt in enumerate(kept_cnt):
                area = len(cnt)
                if area > largest_area:
                    largest_area = area
                    index = c

            # Store the largest contour as a list
            largest_cnt = [kept_cnt[index]]

            # Store the hierarchy of the largest contour into a list
            largest_hierarchy = [kept_hierarchy[0][index]]

            # Iterate through contours to find children of the largest contour
            for i, khi in enumerate(kept_hierarchy[0]):
                if khi[3] == index:  # is the parent equal to the largest contour?
                    largest_hierarchy.append(khi)
                    largest_cnt.append(kept_cnt[i])

            # Make the kept hierarchies into an array so that cv2 can use it
            largest_hierarchy = np.array([largest_hierarchy])

            # Overwrite mask so it only has the largest contour
            mask = np.zeros(np.shape(img)[:2], dtype=np.uint8)
            for i, cnt in enumerate(largest_cnt):
                if i == 0:
                    color = (255)
                else:
                    color = (0)
                cv2.drawContours(mask, largest_cnt, i, color, -1, lineType=8, hierarchy=largest_hierarchy, maxLevel=0)

            # Refind contours and hierarchy from new mask so they are easier to work with downstream
            kept_cnt, kept_hierarchy = _cv2_findcontours(bin_img=mask)

            # Compute object area
            obj_area = cv2.countNonZero(mask)

        cv2.drawContours(ori_img, kept_cnt, -1, (0, 255, 0), -1, lineType=8, hierarchy=kept_hierarchy)
        cv2.drawContours(ori_img, roi_contour, -1, (255, 0, 0), params.line_thickness, lineType=8,
                         hierarchy=roi_hierarchy)
    # Allows user to cut objects to the ROI (all objects completely outside ROI will not be kept)
    elif roi_type.upper() == 'CUTTO':
        background1 = np.zeros(np.shape(img)[:2], dtype=np.uint8)
        background2 = np.zeros(np.shape(img)[:2], dtype=np.uint8)
        cv2.drawContours(background1, object_contour, -1, (255), -1, lineType=8, hierarchy=obj_hierarchy)
        roi_points = np.vstack(roi_contour[0])
        cv2.fillPoly(background2, [roi_points], (255))
        mask = cv2.multiply(background1, background2)
        obj_area = cv2.countNonZero(mask)
        kept_cnt, kept_hierarchy = _cv2_findcontours(bin_img=mask)
        cv2.drawContours(ori_img, kept_cnt, -1, (0, 255, 0), -1, lineType=8, hierarchy=kept_hierarchy)
        cv2.drawContours(ori_img, roi_contour, -1, (255, 0, 0), params.line_thickness, lineType=8,
                         hierarchy=roi_hierarchy)
    else:
        # Reset debug mode
        params.debug = debug
        fatal_error('ROI Type ' + str(roi_type) + ' is not "cutto", "largest", or "partial"!')

    # Reset debug mode
    params.debug = debug
    _debug(ori_img, filename=os.path.join(params.debug_outdir, str(params.device) + '_obj_on_img.png'))
    _debug(mask, filename=os.path.join(params.debug_outdir, str(params.device) + '_roi_mask.png'), cmap='gray')

    return Objects(contours=[kept_cnt], hierarchy=[kept_hierarchy]), mask, obj_area
