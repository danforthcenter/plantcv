# Sort segments

import os
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image
from plantcv.plantcv import find_objects
from plantcv.plantcv.morphology import find_tips


def segment_sort(skel_img, objects, hierarchies, mask=None):
    """ Calculate segment curvature as defined by the ratio between geodesic and euclidean distance

        Inputs:
        skel_img          = Skeletonized image
        objects           = List of contours
        hierarchy         = Contour hierarchy NumPy array
        mask              = (Optional) binary mask for debugging. If provided, debug image will be overlaid on the mask.

        Returns:
        labeled_img       = Segmented debugging image with lengths labeled
        leaf_objects      = List of leaf segments
        leaf_hierarchies  = Contour hierarchy NumPy array
        other_objects     = List of other objects (stem)
        other_hierarchies = Contour hierarchy NumPy array

        :param skel_img: numpy.ndarray
        :param objects: list
        :param hierarchy: numpy.ndarray
        :param labeled_img: numpy.ndarray
        :param mask: numpy.ndarray
        :return leaf_objects: list
        :return leaf_hierarchies: numpy.ndarray
        :return other_objects: list
        :return other_hierarchies: numpy.ndarray
        """
    # Store debug
    debug = params.debug
    params.debug = None

    leaf_objects = []
    leaf_hierarchies = []
    other_objects = []
    other_hierarchies = []

    if mask is None:
        labeled_img = np.zeros(skel_img.shape[:2], np.uint8)
    else:
        labeled_img = mask.copy()

    tips = find_tips(skel_img)
    tip_objects, tip_hierarchies = find_objects(tips, tips)


    # Create a list of tip tuples
    tip_tuples = []
    for i, cnt in enumerate(tip_objects):
        tip_tuples.append((cnt[0][0][0], cnt[0][0][1]))

    # Loop through segment contours
    for i, cnt in enumerate(objects):
        is_leaf = False
        cnt_as_tuples = []
        num_pixels = len(cnt)
        count = 0

        # Turn each contour into a list of tuples (can't search for list of coords, so reformat)
        while num_pixels > count:
            x_coord = cnt[count][0][0]
            y_coord = cnt[count][0][1]
            cnt_as_tuples.append((x_coord, y_coord))
            count += 1

        # The first contour is the base, and while it contains a tip, it isn't a leaf
        if i == 0:
            other_objects.append(cnt)
            other_hierarchies.append(hierarchies[0][i])

        # Sort segments
        else:
            for tip_tups in tip_tuples:
                # If a tip is inside the list of contour tuples then it is a leaf segment
                if tip_tups in cnt_as_tuples:
                    leaf_objects.append(cnt)
                    leaf_hierarchies.append(hierarchies[0][i])
                    is_leaf = True

        # If none of the tip tuples are inside the contour, then it isn't a leaf segment
        if is_leaf == False:
            other_objects.append(cnt)
            other_hierarchies.append(hierarchies[0][i])

    # Format list of hierarchies so that cv2 can use them
    leaf_hierarchies = np.array([leaf_hierarchies])
    other_hierarchies = np.array([other_hierarchies])

    # Plot segments where green segments are leaf objects and fuschia are other objects
    labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_GRAY2RGB)
    for i, cnt in enumerate(other_objects):
        cv2.drawContours(labeled_img, other_objects, i, (255, 0, 255), params.line_thickness,
                         lineType=8, hierarchy=other_hierarchies)
    for i, cnt in enumerate(leaf_objects):
        cv2.drawContours(labeled_img, leaf_objects, i, (0, 255, 0), params.line_thickness,
                         lineType=8, hierarchy=leaf_hierarchies)

    # Reset debug mode
    params.debug = debug
    # Auto-increment device
    params.device += 1

    if params.debug == 'print':
        print_image(labeled_img, os.path.join(params.debug_outdir, str(params.device) + '_sorted_segments.png'))
    elif params.debug == 'plot':
        plot_image(labeled_img)

    return leaf_objects, leaf_hierarchies, other_objects, other_hierarchies
