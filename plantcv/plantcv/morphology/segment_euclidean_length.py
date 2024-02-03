"""Find euclidean lengths of skeleton segments."""
import os
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import outputs
from plantcv.plantcv import fatal_error
from plantcv.plantcv import color_palette
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _cv2_findcontours
from plantcv.plantcv.morphology import find_tips
from scipy.spatial.distance import euclidean


def segment_euclidean_length(segmented_img, objects, label=None):
    """Use segmented skeleton image to gather euclidean length measurements per segment.

    Inputs:
    segmented_img = Segmented image to plot lengths on
    objects       = List of contours
    label         = Optional label parameter, modifies the variable name of
                    observations recorded (default = pcv.params.sample_label).

    Returns:
    labeled_img      = Segmented debugging image with lengths labeled

    :param segmented_img: numpy.ndarray
    :param objects: list
    :param label: str
    :return labeled_img: numpy.ndarray
    """
    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label

    x_list = []
    y_list = []
    segment_lengths = []
    # Create a color scale, use a previously stored scale if available
    rand_color = color_palette(num=len(objects), saved=True)

    labeled_img = segmented_img.copy()
    # Store debug
    debug = params.debug
    params.debug = None

    for i, obj in enumerate(objects):
        # Store coordinates for labels
        x_list.append(obj[0][0][0])
        y_list.append(obj[0][0][1])

        # Draw segments one by one to group segment tips together
        finding_tips_img = np.zeros(segmented_img.shape[:2], np.uint8)
        cv2.drawContours(finding_tips_img, objects, i, (255, 255, 255), 1, lineType=8)
        segment_tips = find_tips(finding_tips_img)
        tip_objects, _ = _cv2_findcontours(bin_img=segment_tips)
        points = []
        if not len(tip_objects) == 2:
            fatal_error("Too many tips found per segment, try pruning again")
        for t in tip_objects:
            # Gather pairs of coordinates
            x, y = t.ravel()
            coord = (x, y)
            points.append(coord)

        # Draw euclidean distance lines
        cv2.line(labeled_img, points[0], points[1], rand_color[i], 1)

        # Calculate euclidean distance between tips of each contour
        segment_lengths.append(float(euclidean(points[0], points[1])))

    segment_ids = []
    # Reset debug mode
    params.debug = debug

    # Put labels of length
    for c, value in enumerate(segment_lengths):
        text = f"{value:0,.2f}"
        w = x_list[c]
        h = y_list[c]
        cv2.putText(img=labeled_img, text=text, org=(w, h), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=params.text_size, color=(150, 150, 150), thickness=params.text_thickness)
        segment_ids.append(c)

    outputs.add_observation(sample=label, variable='segment_eu_length', trait='segment euclidean length',
                            method='plantcv.plantcv.morphology.segment_euclidean_length', scale='pixels', datatype=list,
                            value=segment_lengths, label=segment_ids)

    _debug(visual=labeled_img, filename=os.path.join(params.debug_outdir, f"{params.device}_segment_eu_lengths.png"))

    return labeled_img
