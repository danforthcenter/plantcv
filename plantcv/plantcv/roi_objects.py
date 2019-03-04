# not working on eroded object

import cv2
import numpy as np
import os
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params


def roi_objects(img, roi_type, roi_contour, roi_hierarchy, object_contour, obj_hierarchy):
    """Find objects partially inside a region of interest or cut objects to the ROI.

    Inputs:
    img            = RGB or grayscale image data for plotting
    roi_type       = 'cutto', 'partial' (for partially inside), or 'largest' (keep only the largest contour)
    roi_contour    = contour of roi, output from "View and Adjust ROI" function
    roi_hierarchy  = contour of roi, output from "View and Adjust ROI" function
    object_contour = contours of objects, output from "find_objects" function
    obj_hierarchy  = hierarchy of objects, output from "find_objects" function

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

    params.device += 1
    if len(np.shape(img)) == 3:
        ix, iy, iz = np.shape(img)
    else:
        ix, iy = np.shape(img)

    size = ix, iy, 3
    background = np.zeros(size, dtype=np.uint8)
    ori_img = np.copy(img)
    # If the reference image is grayscale convert it to color
    if len(np.shape(ori_img)) == 2:
        ori_img = cv2.cvtColor(ori_img, cv2.COLOR_GRAY2BGR)
    w_back = background + 255
    background1 = np.zeros(size, dtype=np.uint8)
    background2 = np.zeros(size, dtype=np.uint8)

    # Allows user to find all objects that are completely inside or overlapping with ROI
    if roi_type.upper() == 'PARTIAL':
        for c, cnt in enumerate(object_contour):
            length = (len(cnt) - 1)
            stack = np.vstack(cnt)

            keep = False
            # Test if the contours are within the ROI
            for i in range(0, length):
                pptest = cv2.pointPolygonTest(roi_contour[0], (stack[i][0], stack[i][1]), False)
                if int(pptest) != -1:
                    keep = True
            if keep:
                if obj_hierarchy[0][c][3] > -1:
                    cv2.drawContours(w_back, object_contour, c, (255, 255, 255), -1, lineType=8,
                                     hierarchy=obj_hierarchy)
                else:
                    cv2.drawContours(w_back, object_contour, c, (0, 0, 0), -1, lineType=8, hierarchy=obj_hierarchy)
            else:
                cv2.drawContours(w_back, object_contour, c, (255, 255, 255), -1, lineType=8, hierarchy=obj_hierarchy)

        kept = cv2.cvtColor(w_back, cv2.COLOR_RGB2GRAY)
        kept_obj = cv2.bitwise_not(kept)
        mask = np.copy(kept_obj)
        obj_area = cv2.countNonZero(kept_obj)
        kept_cnt, hierarchy = cv2.findContours(kept_obj, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
        cv2.drawContours(ori_img, kept_cnt, -1, (0, 255, 0), -1, lineType=8, hierarchy=hierarchy)
        cv2.drawContours(ori_img, roi_contour, -1, (255, 0, 0), params.line_thickness, lineType=8,
                         hierarchy=roi_hierarchy)

    # Find the largest contour if roi_type is set to 'largest'
    elif roi_type.upper() == 'LARGEST':
        # Print warning statement about this feature
        print(
            "Warning: roi_type='largest' will only return the largest extreme outer contour. All child contours are left behind.")

        # Filter contours outside of the region of interest
        for c, cnt in enumerate(object_contour):
            length = (len(cnt) - 1)
            stack = np.vstack(cnt)
            keep = False
            # Test if the contours are within the ROI
            for i in range(0, length):
                pptest = cv2.pointPolygonTest(roi_contour[0], (stack[i][0], stack[i][1]), False)
                if int(pptest) != -1:
                    keep = True
            if keep:
                # Color the "gap contours" white
                if obj_hierarchy[0][c][3] > -1:
                    cv2.drawContours(w_back, object_contour, c, (255, 255, 255), -1, lineType=8,
                                     hierarchy=obj_hierarchy)
                # Color the plant contour parts black
                else:
                    cv2.drawContours(w_back, object_contour, c, (0, 0, 0), -1, lineType=8, hierarchy=obj_hierarchy)
            # If the contour isn't overlapping with the ROI, color it white
            else:
                cv2.drawContours(w_back, object_contour, c, (255, 255, 255), -1, lineType=8, hierarchy=obj_hierarchy)

        # Draw the contours kept after filtering by ROI
        kept = cv2.cvtColor(w_back, cv2.COLOR_RGB2GRAY)
        kept_obj = cv2.bitwise_not(kept)
        kept_cnt, hierarchy = cv2.findContours(kept_obj, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]

        # Find the index from the largest contour in the list of contours
        largest_area = 0
        for c, cnt in enumerate(kept_cnt):
            area = cv2.contourArea(cnt)
            if (area > largest_area):
                largest_area = area
                index = c

        # Store the largest contour into a list of kept contours
        largest_cnt = [kept_cnt[index]]
        # Store the hierarchy of the largest contour into a list
        largest_hierarchy = [hierarchy[0][index].tolist()]

        # Make the kept hierarchies into arrays so that cv2 can use it
        largest_hierarchy = np.array([largest_hierarchy])

        # Make a new background for drawing on
        w_back = background + 255

        # Draw the largest contour
        cv2.drawContours(w_back, largest_cnt, -1, (0, 0, 0), -1, lineType=8, hierarchy=largest_hierarchy)
        kept = cv2.cvtColor(w_back, cv2.COLOR_RGB2GRAY)
        kept_obj = cv2.bitwise_not(kept)
        mask = np.copy(kept_obj)
        # Calculate contour area
        obj_area = cv2.countNonZero(kept_obj)

        # Draw the largest contour on the original image
        cv2.drawContours(ori_img, largest_cnt, -1, (0, 255, 0), -1, lineType=8, hierarchy=largest_hierarchy)
        # Draw the ROI contour on the original image
        cv2.drawContours(ori_img, roi_contour, -1, (255, 0, 0), params.line_thickness, lineType=8,
                         hierarchy=roi_hierarchy)

    # Allows user to cut objects to the ROI (all objects completely outside ROI will not be kept)
    elif roi_type.upper() == 'CUTTO':
        cv2.drawContours(background1, object_contour, -1, (255, 255, 255), -1, lineType=8, hierarchy=obj_hierarchy)
        roi_points = np.vstack(roi_contour[0])
        cv2.fillPoly(background2, [roi_points], (255, 255, 255))
        obj_roi = cv2.multiply(background1, background2)
        kept_obj = cv2.cvtColor(obj_roi, cv2.COLOR_RGB2GRAY)
        mask = np.copy(kept_obj)
        obj_area = cv2.countNonZero(kept_obj)
        kept_cnt, hierarchy = cv2.findContours(kept_obj, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
        cv2.drawContours(w_back, kept_cnt, -1, (0, 0, 0), -1)
        cv2.drawContours(ori_img, kept_cnt, -1, (0, 255, 0), -1, lineType=8, hierarchy=hierarchy)
        cv2.drawContours(ori_img, roi_contour, -1, (255, 0, 0), params.line_thickness, lineType=8,
                         hierarchy=roi_hierarchy)

    else:
        fatal_error('ROI Type ' + str(roi_type) + ' is not "cutto", "largest", or "partial"!')

    if params.debug == 'print':
        print_image(w_back, os.path.join(params.debug, str(params.device) + '_roi_objects.png'))
        print_image(ori_img, os.path.join(params.debug, str(params.device) + '_obj_on_img.png'))
        print_image(mask, os.path.join(params.debug, str(params.device) + '_roi_mask.png'))
    elif params.debug == 'plot':
        plot_image(w_back)
        plot_image(ori_img)
        plot_image(mask, cmap='gray')
        # print ('Object Area=', obj_area)

    return kept_cnt, hierarchy, mask, obj_area
