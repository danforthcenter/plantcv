# Image Series Segmentation

import os
import math
import numpy as np
import cv2 as cv
from scipy import ndimage as ndi
from skimage.segmentation import watershed
from skimage.color import label2rgb
from plantcv.plantcv import readimage
from plantcv.plantcv import rgb2gray
from plantcv.plantcv import fill_holes
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug


def segment_image_series(imgs_paths, masks_paths, rois, save_labels=True, ksize=3):
    """Segments the objects in a time series of images using watershed segmentation.
    The objects (labels) are given by a list of rois (region of interest) and the labels
    are propagated sequentially in the time dimension using blocks of ksize.

    Inputs:
    imgs_paths  = List of paths to the images in the time series. Ordered by time
    masks_paths = List of paths to the masks in the time series.
                  Each mask should correspond to the image in imgs_paths for the same index
    rois        = List of roi contours
    save_labels = Optional, saves the labels of each image independently
    ksize       = Size of the block in the time dimension to propagate the labels

    Returns:
    out_labels = 3D array containing the labels of the whole time series

    :param imgs_paths:  list
    :param masks_paths: list
    :param rois:        list
    :param save_labels: bool
    :param ksize:       int
    :return out_labels: numpy.ndarray
    """
    debug = params.debug
    params.debug = None
    params.color_sequence = 'random'

    # for symmetry, using blocks (kernels) of size 2*floor(ksize/2) + 1
    half_k = math.floor(ksize/2)

    image_names = [os.path.basename(img_path) for img_path in imgs_paths]

    # get the size of the images
    tmp, _, _ = readimage(filename=masks_paths[0])
    h, w = tmp.shape[0], tmp.shape[1]

    # create an image where all the pixels inside each roi have the roi label
    roi_labels = np.zeros((h, w), dtype=np.uint8)
    n_labels = len(rois)
    for i in range(n_labels):
        img_roi = np.zeros((h, w), dtype=np.uint8)
        img_roi = cv.drawContours(img_roi, rois[i], -1, 255, 3)
        img_roi = fill_holes(img_roi)
        roi_labels = roi_labels + (img_roi == 255)*(i+1)

    # output initialization
    N = len(image_names)
    out_labels = np.zeros((h, w, N), dtype=np.uint8)
    out_labels[:, :, 0] = roi_labels.copy()

    # Propagate labels sequentially n is the index in the output of the frame currently
    # in process. At each iteration only one frame is labeled.
    for n in range(0, N):
        # size of the stack used at each iteration
        d = 2*half_k+1

        # stacks init
        img_stack = np.zeros((h, w, d))
        mask_stack = np.zeros((h, w, d))
        markers = np.zeros((h, w, d), dtype=np.int32)

        # The number of frames used is always the same but the borders are
        # treated as 'constant' or 'zero padding'
        stack_idx = 0  # borders are 'constant'

        # loop to build the stacks. half_k gives the index of the frame in process
        for m in range(-half_k, half_k+1):
            frame = min(N-1, max(n+m, 0))  # border handling

            img, _, _ = readimage(filename=imgs_paths[frame])
            img_stack[:, :, stack_idx] = rgb2gray(rgb_img=img)
            mask, _, _ = readimage(filename=masks_paths[frame], mode='gray')
            mask_stack[:, :, stack_idx] = mask

            if m == 0:
                # required to create the output image
                img_n_rgb = img
                # enforcing the label inside the regions of interest
                markers[:, :, stack_idx] = (mask != 0)*roi_labels
            else:
                markers[:, :, stack_idx] = out_labels[:, :, frame]

            stack_idx += 1

        # edges using 3D sobel operator as elevation map for watershed
        edges = ndi.generic_gradient_magnitude(img_stack, ndi.sobel)

        # segmentation using the watershed algorithm
        labels = watershed(edges, markers=markers, mask=mask_stack, compactness=0)

        # add the resulting labels to the outputs block
        out_labels[:, :, n] = labels[:, :, half_k]

        # create images for plotting and printing (debug mode)
        vis_seg = label2rgb(out_labels[:, :, n], image=img_n_rgb, colors=None, alpha=0.3, bg_label=0)
        # cast visualization image as int
        vis_seg = (np.floor(255*vis_seg)).astype(np.uint8)
        if n == N - 1:
            params.debug = debug
            _debug(visual=vis_seg, filename=os.path.join(params.debug_outdir,
                                                         f"{str(params.device)}_{image_names[n][:-4]}_WSeg.png"))

    if save_labels is True:
        for i in range(N):
            np.save(os.path.join(params.debug_outdir, f"{image_names[i][:-4]}_labels"), out_labels[:, :, i])

    return out_labels
