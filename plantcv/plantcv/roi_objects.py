# Find objects partially inside a region of interest or cuts objects to the ROI

import cv2
import numpy as np
import os
from plantcv.plantcv import logical_and
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params


def roi_objects(img, roi_contour, roi_hierarchy, object_contour, obj_hierarchy, roi_type="partial"):
    """
    Find objects partially inside a region of interest or cut objects to the ROI.

    Inputs:
    img            = RGB or grayscale image data for plotting
    roi_contour    = contour of roi, output from "View and Adjust ROI" function
    roi_hierarchy  = contour of roi, output from "View and Adjust ROI" function
    object_contour = contours of objects, output from "find_objects" function
    obj_hierarchy  = hierarchy of objects, output from "find_objects" function
    roi_type       = 'cutto', 'partial' (for partially inside, default), or 'largest' (keep only the largest contour)

    Returns:
    kept_cnt       = kept contours
    hierarchy      = contour hierarchy list
    mask           = mask image
    obj_area       = total object pixel area

    :param img: numpy.ndarray
    :param roi_type: str
    :param roi_contour: list
    :param roi_hierarchy: numpy.ndarray
    :param object_contour: list
    :param obj_hierarchy: numpy.ndarray
    :return kept_cnt: list
    :return hierarchy: numpy.ndarray
    :return mask: numpy.ndarray
    :return obj_area: int
    """
    # Store debug
    debug = params.debug
    params.debug = None

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
    if roi_type.upper() == 'PARTIAL' or roi_type.upper() == 'LARGEST':
        # Filter contours outside of the region of interest
        for c, cnt in enumerate(object_contour):
            filtering_mask = np.zeros(np.shape(img)[:2], dtype=np.uint8)
            cv2.fillPoly(filtering_mask, [np.vstack(object_contour[c])], (255))
            overlap_img = logical_and(filtering_mask, roi_mask)
            # Delete contours that do not overlap at all with the ROI
            if np.sum(overlap_img) == 0:
                cv2.drawContours(mask, object_contour, c, (0), -1, lineType=8, hierarchy=obj_hierarchy)

        # Find the kept contours and area
        kept_cnt, kept_hierarchy = cv2.findContours(np.copy(mask), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
        obj_area = cv2.countNonZero(mask)

        # Find the largest contour if roi_type is set to 'largest'
        if roi_type.upper() == 'LARGEST':
            # Print warning statement about this feature
            print("Warning: roi_type='largest' will only return the largest contour and its immediate children. Other "
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
                # print(cnt)
                if i == 0:
                    color = (255)
                else:
                    color = (0)
                    # print(i)
                cv2.drawContours(mask, largest_cnt, i, color, -1, lineType=8, hierarchy=largest_hierarchy, maxLevel=0)

            # Refind contours and hierarchy from new mask so they are easier to work with downstream
            kept_cnt, kept_hierarchy = cv2.findContours(np.copy(mask), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]

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
        kept_cnt, kept_hierarchy = cv2.findContours(np.copy(mask), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
        cv2.drawContours(ori_img, kept_cnt, -1, (0, 255, 0), -1, lineType=8, hierarchy=kept_hierarchy)
        cv2.drawContours(ori_img, roi_contour, -1, (255, 0, 0), params.line_thickness, lineType=8,
                         hierarchy=roi_hierarchy)
    else:
        # Reset debug mode
        params.debug = debug
        fatal_error('ROI Type ' + str(roi_type) + ' is not "cutto", "largest", or "partial"!')

    # Reset debug mode
    params.debug = debug
    _debug(ori_img,
           filename=os.path.join(params.debug_outdir, str(params.device) + '_obj_on_img.png'))
    _debug(mask, 
           filename=os.path.join(params.debug_outdir, str(params.device) + '_roi_mask.png'),
           cmap='gray')

    return kept_cnt, kept_hierarchy, mask, obj_area
