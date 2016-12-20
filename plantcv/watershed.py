# Watershed boundry detection function

import cv2
import numpy as np
from scipy import ndimage as ndi
from skimage.feature import peak_local_max
from skimage import morphology
from skimage.morphology import watershed
from . import print_image
from . import plot_image
from plantcv.apply_mask import apply_mask
from plantcv.dev.color_palette import color_palette



def watershed_segmentation(device, img, mask, distance=10, filename=False, debug=None):
    """Uses the watershed algorithm to detect boundry of objects. Needs a marker file which specifies area which is
       object (white), background (grey), unknown area (black).

    Inputs:
    device = device number. Used to count steps in the pipeline
    img    = image to perform watershed on needs to be 3D (i.e. np.shape = x,y,z not np.shape = x,y)
    mask = binary image, single channel, object in white and background black
    distance = min_distance of local maximum
    filename = if user wants to output analysis images change filenames from false
    debug  = None, print, or plot. Print = save to file, Plot = print to screen.

    Returns:
    device = device number
    watershed_header    = shape data table headers
    watershed_data      = shape data table values
    analysis_images = list of output images

    :param img: numpy array
    :param marker: numpy array
    :param device: int
    :param debug: str
    :return device: int
    :return marker: numpy array
    """
    device += 1

    dist_transform = cv2.distanceTransform(mask, cv2.cv.CV_DIST_L2, maskSize=0)

    localMax = peak_local_max(dist_transform, indices=False, min_distance=distance, labels=mask)

    #markers = ndi.label(localMax, structure=ndi.generate_binary_structure(2, 2))[0]
    markers = ndi.label(localMax)[0]
    labels = watershed(-dist_transform, markers, mask=mask)

    img1 = np.copy(img)

    for x in np.unique(labels):
        rand_color = color_palette(len(np.unique(labels)))
        img1[labels == x] = rand_color[x]

    device, img2 =apply_mask(img1, mask, 'black', device, debug=None)

    joined = np.concatenate((img2, img), axis=1)

    estimated_object_count=len(np.unique(markers))-1

    analysis_images=[]
    if filename:
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
        print_image(dist_transform, str(device) + 'watershed_dist_img.png')
        print_image(joined, str(device) + 'watershed_img.png')
    elif debug == 'plot':
        plot_image(dist_transform,cmap='gray')
        plot_image(joined)

    return device, watershed_header,watershed_data, analysis_images
