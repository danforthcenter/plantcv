# Watershed Se detection function
# This function is based on code contributed by Suxing Liu, Arkansas State University.
# For more information see https://github.com/lsx1980/Leaf_count

import cv2
import numpy as np
from scipy import ndimage as ndi
from skimage.feature import peak_local_max
from skimage.morphology import watershed
from . import print_image
from . import plot_image
from . import apply_mask
from . import color_palette


def watershed_segmentation(device, img, mask, distance=10, filename=False, debug=None):
    """Uses the watershed algorithm to detect boundary of objects. Needs a marker file which specifies area which is
       object (white), background (grey), unknown area (black).

    Inputs:
    device              = device number. Used to count steps in the pipeline
    img                 = image to perform watershed on needs to be 3D (i.e. np.shape = x,y,z not np.shape = x,y)
    mask                = binary image, single channel, object in white and background black
    distance            = min_distance of local maximum
    filename            = if user wants to output analysis images change filenames from false
    debug               = None, print, or plot. Print = save to file, Plot = print to screen.

    Returns:
    device              = device number
    watershed_header    = shape data table headers
    watershed_data      = shape data table values
    analysis_images     = list of output images

    :param device: int
    :param img: numpy array
    :param mask: numpy array
    :param distance: int
    :param filename: str
    :param debug: str
    :return device: int
    :return watershed_header: list
    :return watershed_data: list
    :return analysis_images: list
    """

    if cv2.__version__[0] == '2':
        dist_transform = cv2.distanceTransform(mask, cv2.cv.CV_DIST_L2, maskSize=0)
    else:
        dist_transform = cv2.distanceTransformWithLabels(mask, cv2.DIST_L2, maskSize=0)[0]

    localMax = peak_local_max(dist_transform, indices=False, min_distance=distance, labels=mask)

    markers = ndi.label(localMax, structure=np.ones((3, 3)))[0]
    dist_transform1 = -dist_transform
    labels = watershed(dist_transform1, markers, mask=mask)

    img1 = np.copy(img)

    for x in np.unique(labels):
        rand_color = color_palette(len(np.unique(labels)))
        img1[labels == x] = rand_color[x]

    device, img2 = apply_mask(img1, mask, 'black', device, debug=None)

    joined = np.concatenate((img2, img), axis=1)

    estimated_object_count = len(np.unique(markers)) - 1

    analysis_images = []
    if filename != False:
        out_file = str(filename[0:-4]) + '_watershed.jpg'
        print_image(joined, out_file)
        analysis_images.append(['IMAGE', 'watershed', out_file])

    watershed_header = (
        'HEADER_WATERSHED',
        'estimated_object_count'
    )

    watershed_data = (
        'WATERSHED_DATA',
        estimated_object_count
    )

    if debug == 'print':
        print_image(dist_transform, str(device) + '_watershed_dist_img.png')
        print_image(joined, str(device) + '_watershed_img.png')
    elif debug == 'plot':
        plot_image(dist_transform, cmap='gray')
        plot_image(joined)

    return device, watershed_header, watershed_data, analysis_images
