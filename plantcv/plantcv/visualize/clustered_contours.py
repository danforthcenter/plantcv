# Help visualize which objects got clustered together by plantcv.cluster_contours

import os
import cv2
import numpy as np
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import color_palette
from plantcv.plantcv import params


def clustered_contours(img, grouped_contour_indices, roi_objects, roi_obj_hierarchy, nrow=1, ncol=1, bounding = True):
    """
    This function takes the outputs from cluster_contours

    Inputs:
    img                     = RGB or grayscale image data for plotting
    grouped_contour_indices = Indices for grouping contours
    roi_objects             = object contours in an image that are needed to be clustered.
    roi_obj_hierarchy       = object hierarchy
    nrow                    = Optional, number of rows. If changed from default, grid gets plot.
    ncol                    = Optional, number of columns. If changed from default, grid gets plot.
    bounding                = Optional circles to bound the individual clusters (default bounding=True)

    Returns:
    clustered_image         = Labeled clusters image

    :param img: numpy.ndarray
    :param grouped_contour_indices: list
    :param roi_objects: list
    :param roi_obj_hierarchy: numpy.ndarray
    :param nrow: int
    :param ncol: int
    :param bounding: bool 

    :return clustered_image: numpy.ndarray
    """

    clustered_image = np.copy(img)
    iy, ix = np.shape(img)[:2]

    # Gray input images need to get converted to RGB for plotting colors
    if len(np.shape(img)) == 2:
        clustered_image = cv2.cvtColor(clustered_image, cv2.COLOR_GRAY2RGB)

    # Plot grid if nrow or ncol are changed from the default
    if nrow > 1 or ncol > 1:
        rbreaks = range(0, iy, int(np.rint(iy / nrow)))
        cbreaks = range(0, ix, int(np.rint(ix / ncol)))
        for y in rbreaks:
            cv2.line(clustered_image, (0, y), (ix, y), (255, 0, 0), params.line_thickness)
        for x in cbreaks:
            cv2.line(clustered_image, (x, 0), (x, iy), (255, 0, 0), params.line_thickness)

    rand_color = color_palette(len(grouped_contour_indices))
    grouped_contours = []
    for i, x in enumerate(grouped_contour_indices):
        for a in x:
            if roi_obj_hierarchy[0][a][3] > -1:
                pass
            else:
                cv2.drawContours(clustered_image, roi_objects, a, rand_color[i], -1, hierarchy=roi_obj_hierarchy)
                # Add contour to list to get grouped
                grouped_contours.append(roi_objects[a])
        if len(grouped_contours) > 0:
            # Combine contours into a single contour
            grouped_contours = np.vstack(grouped_contours)
            # Plot the bounding circle around the contours that got grouped together
            if bounding:
                center, radius = cv2.minEnclosingCircle(points=grouped_contours)
                cv2.circle(img=clustered_image, center=(int(center[0]), int(center[1])), radius=int(radius),
                       color=rand_color[i], thickness=params.line_thickness, lineType=8)
                #Label the cluster ID
                cv2.putText(img=clustered_image, text=str(i),
                        org=(int(center[0]), int(center[1])), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=params.text_size, color=(200, 200, 200), thickness=params.text_thickness)
        # Empty the grouped_contours list for the next group
        grouped_contours = []

    params.device += 1

    if params.debug == 'print':
        print_image(clustered_image, os.path.join(params.debug_outdir, str(params.device) + '_clusters.png'))
    elif params.debug == 'plot':
        plot_image(clustered_image)

    return clustered_image
