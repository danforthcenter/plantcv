
import cv2
import numpy as np
from skimage.segmentation import watershed
from plantcv.plantcv import fatal_error
from plantcv.plantcv import outputs
from plantcv.plantcv import color_palette


# These functions use the watershed algorithm

def fill_segments(mask, objects):
    """Fills masked segments from contours.

    Inputs:
    mask         = Binary image, single channel, object = 1 and background = 0
    objects      = List of contours

    Returns:
    filled_img   = Filled mask

    :param mask: numpy.ndarray
    :param object: list
    :return filled_img: numpy.ndarray
    """

    h,w = mask.shape
    markers = np.zeros((h,w))

    labels = np.arange(len(objects)) + 1
    for i,l in enumerate(labels):
        cv2.drawContours(markers, objects, i ,int(l) , 5)

    filled_mask = watershed(mask==0, markers=markers,
                            mask=mask!=0,compactness=0)

    # Count area in pixels of each segment
    ids, counts = np.unique(filled_mask, return_counts=True)
    outputs.add_observation(variable='segment_area', trait='segment area',
                            method='plantcv.plantcv.morphology.fill_segments',
                            scale='pixels', datatype=list,
                            value=counts[1:].tolist(),
                            label=(ids[1:]-1).tolist())

    rgb_vals = color_palette(num=len(labels), saved=False)
    filled_img = np.zeros((h,w,3), dtype=np.int32)
    for l in labels:
        for ch in range(3):
            filled_img[:,:,ch][filled_mask==l] = rgb_vals[l-1][ch]

    return filled_img

def fill_skeleton_segmentation_old(skel_segment, mask):
    """Fills masked regions from a segmented skeleton.

    Inputs:
    skel_segment = Image of segmented skeleton
    mask         = Binary image, single cannel, object = 1 and background = 0

    Returns:
    filled_img   = Filled mask

    :param skel_segment: numpy.ndarray
    :param mask: numpy.ndarray
    :return filled_img: numpy.ndarray
    """

    if (np.amax(skel_segment) <= 1) or (np.amax(skel_segment) > 255):
        fatal_error('Pixel values are not in the range 0-255')

    mask = mask.astype(np.dtype('int8'))

    # Convert rgb values into single channel labels
    labeled_img = skel_segment.astype(np.int32)
    single_ch = (256**2)*labeled_img[:,:,0] + 256*labeled_img[:,:,1] + labeled_img[:,:,2]
    label_vals = np.unique(single_ch)

    labels = np.arange(label_vals.shape[0])
    labels[-1] = 0 # remove mask
    for i,c in enumerate(label_vals):
        single_ch[single_ch==c] = labels[i]

    filled_img = watershed(mask==0, markers=single_ch, mask=mask, compactness=0)

    # filled_img = filled_img.astype(np.int32)
    # for i,c in enumerate(label_vals[:-1]):
    #     filled_img[filled_img==labels[i]] = c
    #
    #
    # filled_rgb = np.zeros(labeled_img.shape,dtype=np.int32)
    # filled_rgb[:,:,0] = np.floor(filled_img/(256**2))
    # filled_rgb[:,:,1] = np.floor((filled_img - (filled_rgb[:,:,0]*(256**2)))/256)
    # filled_rgb[:,:,2] = filled_img - filled_rgb[:,:,0]*(256**2) - filled_rgb[:,:,1]*256


    filled_rgb = np.zeros(labeled_img.shape,dtype=np.int32)
    for i,c in enumerate(label_vals[:-1]):
        r = np.floor(c/(256**2))
        g = np.floor((c - r*(256**2))/256)
        b = c - r*(256**2) - g*256
        filled_rgb[:,:,0][filled_img==labels[i]] = r
        filled_rgb[:,:,1][filled_img==labels[i]] = g
        filled_rgb[:,:,2][filled_img==labels[i]] = b


    return filled_rgb





def segment_image_series(image_series, mask, ref_frame=0):
    """

    Inputs:
    image_series = 3D stack of grayscale images
    mask_series  = 3D stack of binary masks
    ref_frame    = Index of the reference image to extract markers

    Returns:
    markers      = 3D stack of segmented images

    :param image_series: numpy.ndarray
    :param mask_series: numpy.ndarray
    :params ref_frame: int
    :return markers: numpy.ndarray
    """

def segment_leaves(img, markers, mask):
    """

    Inputs:
    img     = 2D grayscale image or 3D stack of grayscale images
    markers = 2D image with a mark for each leaf
    mask    = Binary mask

    Returns:
    markers = Segmented image or stack of images

    :param img: numpy.ndarray
    :param markers: numpy.ndarray
    :params mask: numpy.ndarray
    :return markers: numpy.ndarray
    """
