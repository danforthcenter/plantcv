# display instances in an image
import cv2
from matplotlib.patches import Polygon
import colorsys
import random
from skimage.measure import find_contours
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches, lines
from matplotlib.patches import Polygon
from plantcv.plantcv import fatal_error, params, color_palette
import os
from cv2 import cvtColor, COLOR_BGR2RGB

def _overlay_mask_on_img(img, mask, color, alpha=0.5):
    """ Overlay a given mask on top of an image such that the masked area (the non-zero areas in the mask) is shown in user
    defined color, the other area (the zero-valued areas in the mask) is shown in original image.
    Inputs:
        img   = image to show, can be either visible or grayscale
        mask  = mask to be put on top of the image
        color = a tuple of desired color to show the mask on top of the image
        alpha = a value (between 0 and 1) indicating the transparency when blending mask and image, by default 0.5
    Output:
        img = the original image with mask overlaied on top

    :param img: numpy.ndarray
    :param mask: numpy.ndarray
    :param color: tuple
    :param alpha: float
    :return: img: numpy.ndarray
    """
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    for c in range(img.shape[-1]):
        img[:, :, c] = np.where(mask == 1,
                                img[:, :, c] *
                                (1 - alpha) + alpha * color[c] * 255,
                                img[:, :, c])
    return img


def display_instances(img, masks, figsize=(16, 16), title="", colors=None, captions=None, show_bbox=True, ax=None):
    """ Display multiple instances in image based on the given masks
    This function is inspired by the same function used in mrcnn, showing different instances with different colors on top of the original image
    Users also have the option to specify the color for every instance, as well as the caption for every instance. Showing bounding boxes is another option.
    Inputs:
        img  = rgb image to show
        mask = a bunch of masks in a matrix
        figsize = desired size of figure, by default (16,16)
        title = desired title to show, by default ""
        colors = a list of colors for every instance to display, by default colors=None
        captions = a list of names for every instance, by default captions=None
        show_bbox = a flog indicating whether show bounding box, by default show_bbox=True
        ax = axis to show, by default ax=None
    Outputs:
        masked_img = image with instances masks overlaied on top
        colors = colors used to display every instance

    :param img: numpy.ndarray
    :param masks: numpy.ndarray
    :param figsize: tuple
    :param title: str
    :param colors: list (of tuples)
    :param captions: str
    :param show_bbox: bool
    :param ax:
    :return: masked_img: numpy.ndarray
    :return: colors: list (of tuples)
    """

    debug = params.debug
    params.debug = None

    # Auto-increment the device counter
    params.device += 1

    if img.shape[0:2] != masks.shape[0:2]:
        fatal_error("Sizes of image and mask mismatch!")
    #
    # auto_show = False
    if not ax:
        _, ax = plt.subplots(1, figsize=figsize)
        # auto_show = True

    num_insts = masks.shape[2]

    #     # Generate random colors
    #     colors = colors or _random_colors(num_insts)

    if colors is not None:
        if max(max(colors)) > 1 or min(min(colors)) < 0:
            fatal_error("RGBA values should be within 0-1 range!")
    else:
        colors_ = color_palette(num_insts)
        colors = [tuple([ci / 255 for ci in c]) for c in colors_]

    if len(colors) < num_insts:
        fatal_error("Not enough colors provided to show all instances!")
    if len(colors) > num_insts:
        colors = colors[0:num_insts]

    # Show area outside image boundaries.
    height, width = img.shape[:2]
    ax.set_ylim(height + 10, -10)
    ax.set_xlim(-10, width + 10)
    ax.axis('off')
    ax.set_title(title)

    masked_img = img.astype(np.uint32).copy()
    for i in range(num_insts):
        color = colors[i]

        # Mask
        mask = masks[:, :, i]
        # the color is in order of r-g-b, however the image is in order of b-g-r, so take the reverse of color
        masked_img = _overlay_mask_on_img(masked_img, mask, color[::-1])

        ys, xs = np.where(mask > 0)
        x1, x2 = min(xs), max(xs)
        y1, y2 = min(ys), max(ys)
        if show_bbox:
            p = patches.Rectangle((x1, y1), x2 - x1, y2 - y1, linewidth=2, alpha=0.7, linestyle="dashed", edgecolor=color, facecolor='none')
            ax.add_patch(p)

        # Mask Polygon
        # Pad to ensure proper polygons for masks that touch image edges.
        padded_mask = np.zeros((mask.shape[0] + 2, mask.shape[1] + 2), dtype=np.uint8)
        padded_mask[1:-1, 1:-1] = mask
        contours = find_contours(padded_mask, 0.5)
        for verts in contours:
            # Subtract the padding and flip (y, x) to (x, y)
            verts = np.fliplr(verts) - 1
            p = Polygon(verts, facecolor="none", edgecolor=color)
            ax.add_patch(p)
        if not captions:
            caption = str(i)
        else:
            caption = captions[i]
        ax.text(x1, y1 + 8, caption, color='w', size=13, backgroundcolor="none")

    masked_img   = cvtColor(masked_img.astype(np.uint8), COLOR_BGR2RGB)
    params.debug = debug
    if params.debug is not None:
        if params.debug == "plot":
            ax.imshow(masked_img)

        if params.debug == "print":
            ax.imshow(masked_img)
            plt.savefig(os.path.join(params.debug_outdir, str(params.device) + "_displayed_instances.png"))
            plt.close("all")

    return masked_img, colors
