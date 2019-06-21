# Watershed Se detection function
# This function is based on code contributed by Suxing Liu, Arkansas State University.
# For more information see https://github.com/lsx1980/Leaf_count

import cv2
import os
import numpy as np
from scipy import ndimage as ndi
from skimage.feature import peak_local_max
from skimage.morphology import watershed
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import apply_mask
from plantcv.plantcv import color_palette
from plantcv.plantcv import params
from plantcv.plantcv import outputs


def watershed_segmentation(rgb_img, mask, distance=10):
    """Uses the watershed algorithm to detect boundary of objects. Needs a marker file which specifies area which is
       object (white), background (grey), unknown area (black).

    Inputs:
    rgb_img             = image to perform watershed on needs to be 3D (i.e. np.shape = x,y,z not np.shape = x,y)
    mask                = binary image, single channel, object in white and background black
    distance            = min_distance of local maximum

    Returns:
    analysis_images     = list of output images

    :param rgb_img: numpy.ndarray
    :param mask: numpy.ndarray
    :param distance: int
    :return analysis_images: list
    """
    params.device += 1

    # Store debug mode
    debug = params.debug
    params.debug = None
    # # Will be depricating opencv version 2
    # if cv2.__version__[0] == '2':
    #     dist_transform = cv2.distanceTransform(mask, cv2.cv.CV_DIST_L2, maskSize=0)
    # else:
    dist_transform = cv2.distanceTransformWithLabels(mask, cv2.DIST_L2, maskSize=0)[0]

    localMax = peak_local_max(dist_transform, indices=False, min_distance=distance, labels=mask)

    markers = ndi.label(localMax, structure=np.ones((3, 3)))[0]
    dist_transform1 = -dist_transform
    labels = watershed(dist_transform1, markers, mask=mask)

    img1 = np.copy(rgb_img)

    for x in np.unique(labels):
        rand_color = color_palette(len(np.unique(labels)))
        img1[labels == x] = rand_color[x]

    img2 = apply_mask(img1, mask, 'black')

    joined = np.concatenate((img2, rgb_img), axis=1)

    estimated_object_count = len(np.unique(markers)) - 1

    # Reset debug mode
    params.debug = debug
    if params.debug == 'print':
        print_image(dist_transform, os.path.join(params.debug_outdir, str(params.device) + '_watershed_dist_img.png'))
        print_image(joined, os.path.join(params.debug_outdir, str(params.device) + '_watershed_img.png'))
    elif params.debug == 'plot':
        plot_image(dist_transform, cmap='gray')
        plot_image(joined)

    outputs.add_observation(variable='estimated_object_count', trait='estimated object count',
                            method='plantcv.plantcv.watershed', scale='none', datatype=int,
                            value=estimated_object_count, label='none')

    # Store images
    outputs.images.append([dist_transform, joined])

    return joined
