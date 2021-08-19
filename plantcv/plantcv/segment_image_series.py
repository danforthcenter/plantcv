import os
import math
import numpy as np
import cv2 as cv
from scipy import ndimage as ndi
from skimage.segmentation import watershed
#from skimage.measure import label

from plantcv import plantcv as pcv
#from plantcv.plantcv import fatal_error
from plantcv.plantcv import color_palette
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug


# to change for colorize_label_img once it's merged
def _labels2rgb(labels, n_labels, rgb_values):

    h,w = labels.shape
    rgb_img = np.zeros((h,w,3), dtype=np.uint8)
    for l in range(n_labels):
        rgb_img[labels == l+1] = rgb_values[l]

    return rgb_img


def segment_image_series(imgs_paths, masks_paths, rois, save_labels=True, ksize=3):

    debug = params.debug
    params.debug = None
    params.color_sequence = 'random'

    # for symmetry, using blocks (kernels) of size 2*floor(ksize/2) + 1
    half_k = math.floor(ksize/2)

    image_names = [os.path.basename(img_path) for img_path in imgs_paths]

    #get the size of the images
    tmp, _, _ = pcv.readimage(filename=masks_paths[0])
    h, w = tmp.shape[0], tmp.shape[1]

    # create an image where all the pixels inside each roi have the roi label
    roi_labels = np.zeros((h,w), dtype=np.uint8)
    n_labels = len(rois)
    for i in range(n_labels):
        img_roi = np.zeros((h,w), dtype=np.uint8)
        img_roi = cv.drawContours(img_roi, rois[i], -1, 255, 3)
        img_roi = pcv.fill_holes(img_roi)
        roi_labels = roi_labels + (img_roi==255)*(i+1)

    # output initialization
    N = len(image_names)
    out_labels = np.zeros((h,w,N),dtype=np.uint8)
    out_labels[:,:,0] = roi_labels.copy()

    # values for visualization output image
    rgb_values = color_palette(n_labels)

    # Propagate labels sequentially n is the index in the output of the frame currently
    # in process. At each iteration only one frame is labeled.
    for n in range(0,N):
        # size of the stack used at each iteration
        d = 2*half_k+1

        # stacks init
        img_stack = np.zeros((h,w,d))
        mask_stack = np.zeros((h,w,d))
        markers = np.zeros((h,w,d))

        # The number of frames used is always the same but the borders are
        # treated as 'constant' or 'zero padding'
        stack_idx = 0 # borders are 'constant'
        #stack_idx = -min(0,n-half_k) # left border is 'zero padded' not necessary

        # loop to build the stacks. half_k gives the index of the frame in process
        for m in range(-half_k,half_k+1):
            frame = min(N-1, max(n+m,0)) # borders handling

            img, _, _ = pcv.readimage(filename=imgs_paths[frame])
            img_stack[:,:,stack_idx] = pcv.rgb2gray(rgb_img=img)
            mask, _, _ = pcv.readimage(filename=masks_paths[frame], mode='gray')
            mask_stack[:,:,stack_idx] = mask

            if m == 0:
                # required to create the output image
                img_n_rgb = img
                # enforcing the label inside the regions of interest
                markers[:,:,stack_idx] = (mask!=0)*roi_labels
            else:
                markers[:,:,stack_idx] = out_labels[:,:,frame]

            stack_idx += 1

        # edges using 3D sobel operator as elevation map for watershed
        edges = ndi.generic_gradient_magnitude(img_stack, ndi.sobel)

        # segmentation using the watershed algorithm
        labels = watershed(edges, markers=markers, mask=mask_stack, compactness=0)

        # add the resulting labels to the outputs block
        out_labels[:,:,n] = labels[:,:,half_k]


        # Create images for plotting and printing (debug mode)
        rgb_seg = _labels2rgb(out_labels[:,:,n], n_labels, rgb_values)
        #vis_seg = cv.addWeighted(img_n_rgb, 0.7, rgb_seg, 0.3, 0.0)
        vis_seg = pcv.visualize.overlay_two_imgs(img1=img_n_rgb, img2=rgb_seg, alpha=0.3)
        params.debug = debug
        _debug(visual=vis_seg, filename=os.path.join(params.debug_outdir,
                                f"{str(params.device)}_{image_names[n][:-4]}_WSeg.png"))
        params.debug = None


    if save_labels == True:
        [np.save(os.path.join(params.debug_outdir, f"{image_names[i][:-4]}_labels"),
                out_labels[:,:,i]) for i in range(N)]

    return out_labels
