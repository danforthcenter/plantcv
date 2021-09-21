import os
import numpy as np
from skimage.measure import label, regionprops
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug

def detect_discs(bin_img, ecc_thresh=0):
    """ Detect disc-shaped regions in a binary image based on eccentricity.
    A value of eccentricity between 0 and 1 corresponds to an ellipse.
    The closer the value to 0 the closer the shape is to a circle.

    Inputs:
    bin_img       = Binary image containing the connected regions to consider
    ecc_thresh    = Eccentricity threshold below which a region is kept


    Returns:
    discs_mask  = Binary image that contains only the detected discs
    discs_coor  = List of coordinates (as row,column) of the centroids of the
                  detected discs

    :param bin_img: numpy.ndarray
    :param ecc_thresh: float
    :return discs_mask: numpy.ndarray
    :return discs_coor: list
    """

    # label connected regions
    labeled_img = label(bin_img)
    # measure regions
    obj_measures = regionprops(labeled_img)

    # Check the eccentricity of each region.
    # A value closer to 0 keeps only the most circular objects
    discs_mask = np.zeros(labeled_img.shape, dtype=np.uint8)
    # Store the list of coordinates (row,col) for the objects that pass the
    discs_coor = []
    for i,obj in enumerate(obj_measures):
        if obj.eccentricity < ecc_thresh:
            # Convert coord values to int
            coords = tuple(map(int, obj.centroid))
            discs_coor.append(coords)
            discs_mask = discs_mask + (labeled_img == i+1)

    _debug(visual=255*discs_mask, filename=os.path.join(params.debug_outdir,
            str(params.device) + "_discs_mask" +
            str(int(ecc_thresh*10)) + ".png"))

    return 255*discs_mask, discs_coor
