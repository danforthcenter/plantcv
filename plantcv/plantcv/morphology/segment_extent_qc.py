# Check if all segments were analyzed by comparing the extent of the mask and the segments analyzed
import os
import cv2
import numpy as np
from plantcv.plantcv import params, outputs
from plantcv.plantcv._debug import _debug


def segment_extent_qc(objects, mask, label=None):
    """Find tips and segment branch points.

    Inputs:
    objects          = Segment objects, probably from segment_sort, segment_skeleton, or segment_ends
    mask             = Binary mask for comparison
    label            = Optional label parameter, modifies the variable name of
                       observations recorded (default = pcv.params.sample_label).

    :param skel_img: numpy.ndarray
    :param mask: numpy.ndarray
    :param label: str
    """
    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label

    # Draw the objects on a blank array to make a binary mask
    blank_mask = np.zeros(np.shape(mask), dtype=np.uint8)
    for i, cnt in enumerate(objects):
        cv2.drawContours(blank_mask, cnt, -1, (255), 1, lineType=8)

    # Measure the extent of the objects
    if np.sum(blank_mask) > 0: 
        obj_x, obj_y , skel_w, skel_h = cv2.boundingRect(blank_mask) 
    else:
        skel_w = 0
        skel_h = 0
    # Measure the extent of the mask
    mask_x, mask_y, mask_w, mask_h = cv2.boundingRect(mask)

    # Save outputs about the ratio of height and width extent
    outputs.add_observation(sample=label, variable='width_percent_difference', trait='perfect difference in width extent',
                            method='plantcv.plantcv.morphology.segment_extent_qc', scale='none', datatype=float,
                            value=(mask_w - skel_w)/mask_w, label="none")
    outputs.add_observation(sample=label, variable='height_percent_difference', trait='perfect difference in height extent',
                            method='plantcv.plantcv.morphology.segment_extent_qc', scale='none', datatype=float,
                            value=(mask_h - skel_h)/mask_h, label="none")

    # Create debug image to visualize
    image = cv2.cvtColor(np.copy(mask), cv2.COLOR_GRAY2RGB)
    # Draw the mask bounding box in maroon
    image = cv2.rectangle(image, (mask_x, mask_y), (mask_x + mask_w, mask_y + mask_h),
                          (0, 0, 128), params.line_thickness)
    # Draw the object bounding box in orange
    image = cv2.rectangle(image, (obj_x, obj_y), (obj_x + skel_w, obj_y + skel_h),
                          (0, 165, 255), params.line_thickness)
    _debug(visual=image, filename=os.path.join(params.debug_outdir, f"{params.device}_segment_extent.png"))
