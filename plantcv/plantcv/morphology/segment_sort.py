# Sort segments

import os
import cv2
import numpy as np
from plantcv.plantcv import dilate
from plantcv.plantcv import params
from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image
from plantcv.plantcv import logical_and
from plantcv.plantcv.morphology import find_tips


def segment_sort(skel_img, objects, mask=None, first_stem=True):
    """ Calculate segment curvature as defined by the ratio between geodesic and euclidean distance

        Inputs:
        skel_img          = Skeletonized image
        objects           = List of contours
        mask              = (Optional) binary mask for debugging. If provided, debug image will be overlaid on the mask.
        first_stem        = (Optional) if True, then the first (bottom) segment always gets classified as stem

        Returns:
        labeled_img       = Segmented debugging image with lengths labeled
        secondary_objects = List of secondary segments (leaf)
        primary_objects   = List of primary objects (stem)

        :param skel_img: numpy.ndarray
        :param objects: list
        :param mask: numpy.ndarray
        :param first_stem: bool
        :return secondary_objects: list
        :return other_objects: list
        """
    # Store debug
    debug = params.debug
    params.debug = None

    secondary_objects = []
    primary_objects = []

    if mask is None:
        labeled_img = np.zeros(skel_img.shape[:2], np.uint8)
    else:
        labeled_img = mask.copy()

    tips_img = find_tips(skel_img)
    tips_img = dilate(tips_img, 3, 1)

    # Loop through segment contours
    for i, cnt in enumerate(objects):
        segment_plot = np.zeros(skel_img.shape[:2], np.uint8)
        cv2.drawContours(segment_plot, objects, i, 255, 1, lineType=8)
        # is_leaf = False
        overlap_img = logical_and(segment_plot, tips_img)

        # The first contour is the base, and while it contains a tip, it isn't a leaf
        if i == 0 and first_stem:
            primary_objects.append(cnt)

        # Sort segments
        else:

            if np.sum(overlap_img) > 0:
                secondary_objects.append(cnt)
                # is_leaf = True
            else:
                primary_objects.append(cnt)

    # Reset debug mode
    params.debug = debug

    # Plot segments where green segments are leaf objects and fuschia are other objects
    labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_GRAY2RGB)
    for i, cnt in enumerate(primary_objects):
        cv2.drawContours(labeled_img, primary_objects, i, (255, 0, 255), params.line_thickness, lineType=8)
    for i, cnt in enumerate(secondary_objects):
        cv2.drawContours(labeled_img, secondary_objects, i, (0, 255, 0), params.line_thickness, lineType=8)

    # Auto-increment device
    params.device += 1

    if params.debug == 'print':
        print_image(labeled_img, os.path.join(params.debug_outdir, str(params.device) + '_sorted_segments.png'))
    elif params.debug == 'plot':
        plot_image(labeled_img)

    return secondary_objects, primary_objects
