import numpy as np
from scipy import ndimage as ndi
from skimage.segmentation import watershed
from plantcv.plantcv import fatal_error
from plantcv.plantcv import color_palette


def segment_image_series(img_series, masks, ref_frame=0, expand_labels=True):
    """

    Inputs:
    img_series    = 3D stack of grayscale images
    masks         = 3D stack of binary masks
    ref_frame     = Index of the reference image to extract markers
    expand_labels = If True, stack the labels frame in the 3rd dimension 

    Returns:
    markers      = 3D stack of segmented images

    :param ime_series: numpy.ndarray
    :param mask: numpy.ndarray
    :params ref_frame: int
    :params expand_dims: bool
    :return markers: numpy.ndarray
    """

    if len(img_series.shape) < 3:
        img_series = np.expand_dims(img_series,axis=2)
        masks = np.expand_dims(masks,axis=2)

    h,w,N = img_series.shape

    # Automatic label on one frame
    labels, _ = ndi.label(masks[:,:,ref_frame])
    if expand_labels:
        markers = np.tile(np.expand_dims(labels,axis=2),(1,1,N))
    else:
        markers = np.zeros((h,w,N),dtype=np.int32)
        markers[:,:,ref_frame] = labels

    # Edges using 3D sobel operator as elevation map for watershed
    edges = ndi.generic_gradient_magnitude(img_series, ndi.sobel)
    segmented_imgs = watershed(edges, markers=markers, mask=masks,compactness=0)

    return segmented_imgs

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

    if len(img.shape) < 3:
        img = np.expand_dims(img,axis=2)
        masks = np.expand_dims(masks,axis=2)

    h,w,N = img.shape

    # Edges using 3D sobel operator as elevation map for watershed
    edges = ndi.generic_gradient_magnitude(img, ndi.sobel)
    segmented_img = watershed(edges, markers=markers, mask=mask,compactness=0)

    return segmented_img
