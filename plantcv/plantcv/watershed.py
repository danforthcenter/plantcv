"""Watershed segmentation function."""
# This function is based on code contributed by Suxing Liu, Arkansas State University.
# For more information see https://github.com/lsx1980/Leaf_count

import cv2
import os
import numpy as np
from scipy import ndimage as ndi
from skimage.feature import peak_local_max
from skimage.segmentation import watershed
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import color_palette
from plantcv.plantcv import params
from plantcv.plantcv import outputs
from plantcv.plantcv._helpers import _cv2_findcontours


def watershed_segmentation(rgb_img, mask, distance=10, label=None):
    """
    Uses the watershed algorithm to detect boundary of objects. Needs a marker file which specifies area which is
    object (white), background (grey), unknown area (black).

    Inputs:
    rgb_img             = image to perform watershed on needs to be 3D (i.e. np.shape = x,y,z not np.shape = x,y)
    mask                = binary image, single channel, object in white and background black
    distance            = min_distance of local maximum
    label               = Optional label parameter, modifies the variable name of
                          observations recorded (default = pcv.params.sample_label).

    Returns:
    labels              = labeled mask with segmentation results

    :param rgb_img: numpy.ndarray
    :param mask: numpy.ndarray
    :param distance: int
    :param label: str
    :return labels: numpy.ndarray
    """
    # Store color sequence mode and set to random for watershed_img debug
    color_sequence = params.color_sequence
    params.color_sequence = "random"

    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label

    dist_transform = cv2.distanceTransformWithLabels(mask, cv2.DIST_L2, maskSize=0)[0]

    local_max_coordinates = peak_local_max(dist_transform, min_distance=distance, labels=mask)
    local_max = np.zeros_like(dist_transform, dtype=bool)
    local_max[tuple(local_max_coordinates.T)] = True

    markers = ndi.label(local_max, structure=np.ones((3, 3)))[0]
    dist_transform1 = -dist_transform
    labels = watershed(dist_transform1, markers, mask=mask)
    estimated_object_count = len(np.unique(markers)) - 1

    # Plot image
    plt_img = np.copy(rgb_img)
    rand_color = color_palette(len(np.unique(labels)))
    for i in np.unique(labels):
        # Skip black background i=0
        if i > 0:
            # Find contours
            submask = np.where(labels == i, 255, 0).astype(np.uint8)
            cnt, _ = _cv2_findcontours(bin_img=submask)
            cv2.drawContours(plt_img, cnt, -1, rand_color[i], params.line_thickness)

    _debug(visual=plt_img,
           filename=os.path.join(params.debug_outdir, str(params.device) + '_watershed_labeled_img.png'),
           cmap='gray')

    # Reset color sequence mode
    params.color_sequence = color_sequence

    outputs.add_observation(sample=label, variable='estimated_object_count', trait='estimated object count',
                            method='plantcv.plantcv.watershed', scale='none', datatype=int,
                            value=estimated_object_count, label='none')

    return labels
