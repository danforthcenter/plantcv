# Measure culm lengths

import os
import cv2
import numpy as np
from plantcv.plantcv import dilate
from plantcv.plantcv import params
from plantcv.plantcv import outputs
from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image
from plantcv.plantcv import find_objects
from plantcv.plantcv import color_palette
from plantcv.plantcv.morphology import skeletonize


def culm_path_length(skel_img, stem_objects):
    """ Measure culm lengths. Similar to segment_path_length function but rather than adding internode
        lengths to calculate total culm length it is more accurate to combine objects of the same tiller
        together and then find the culm lengths.

    Inputs:
    skel_img     = Skeletonized image
    stem_objects = List of primary objects (stem)

    Returns:
    labeled_img = Debugging image with separate culm lengths labeled

    :param skel_img: numpy.ndarray
    :param stem_objects: list
    :return labeled_img: numpy.ndarray
    """
    # Initialize lists
    culm_lengths = []
    label_coord_x = []
    label_coord_y = []

    # Store debug mode
    debug = params.debug
    params.debug = None

    # Plot combined stem objects
    plotting_img = np.zeros(skel_img.shape[:2], np.uint8)
    cv2.drawContours(plotting_img, stem_objects, -1, 255, params.line_thickness, lineType=8)
    dilated = dilate(gray_img=plotting_img, ksize=4)
    tiller_objects, _ = find_objects(img=skel_img, mask=dilated)

    # Skeletonize the combined stems
    tiller_skeleton = skeletonize(mask=dilated)

    # Create debugging image and measure culm lengths
    rand_color = color_palette(len(tiller_objects))
    labeled_img = cv2.cvtColor(skel_img.copy(), cv2.COLOR_GRAY2RGB)
    for i, cnt in enumerate(tiller_objects):
        labeled_img = cv2.drawContours(labeled_img, cnt, -1, rand_color[i],
                                       params.line_thickness, lineType=8)

    for i, cnt in enumerate(tiller_objects):
        # Calculate geodesic distance, divide by two since cv2 seems to be taking the perimeter of the contour
        culm_lengths.append(cv2.arcLength(tiller_objects[i], False) / 2)
        # Store coordinates for labels
        label_coord_x.append(tiller_objects[i][0][0][0])
        label_coord_y.append(tiller_objects[i][0][0][1])

    segment_ids = []

    # Put labels of length
    for c, value in enumerate(culm_lengths):
        text = "{:.2f}".format(value)
        w = label_coord_x[c]
        h = label_coord_y[c]
        cv2.putText(img=labeled_img, text=text, org=(w, h), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=params.text_size, color=(150, 150, 150), thickness=params.text_thickness)
        segment_label = "ID" + str(c)
        segment_ids.append(c)

    outputs.add_observation(variable='culm_lengths', trait='culm lengths',
                            method='plantcv.plantcv.morphology.clum_path_length', scale='none', datatype=list,
                            value=culm_lengths, label=segment_ids)

    # Reset debug mode
    params.debug = debug

    # Auto-increment device
    params.device += 1

    if params.debug == 'print':
        print_image(labeled_img,
                    os.path.join(params.debug_outdir, str(params.device) + '_culm_lengths.png'))
    elif params.debug == 'plot':
        plot_image(labeled_img)

    return labeled_img
