import cv2 as cv2
import numpy as np

def within_frame(mask, obj):
    '''
    This function tests whether the plant object touches the edge of the image, i.e. it is completely in the field of view
    Input:
    mask = a single channel image (i.e. binary or greyscale) that contains the object
    obj = a single object, preferably after calling pcv.image_composition(), that is from `mask`

    Returns:
    in_bounds = a boolean (True or False) indicating that the object does not touch the edge of the image

    :param mask: numpy.ndarray
    :param obj: str
    :return in_bounds: bool

    '''

    # Check if object is touching image boundaries (QC)

    if len(np.shape(mask)) > 2:
        fatal_error("mask should be a single channel 2-d array such as a binary or greyscale image.")

    ix, iy = np.shape(mask)
    size1 = ix, iy
    frame_background = np.zeros(size1, dtype=np.uint8)
    frame = frame_background + 1
    frame_contour, frame_hierarchy = cv2.findContours(frame, cv2.RETR_TREE,  cv2.CHAIN_APPROX_NONE)[-2:]
    ptest = []
    vobj = np.vstack(obj)
    for i, c in enumerate(vobj):
        xy = tuple(c)
        pptest = cv2.pointPolygonTest(frame_contour[0], xy, measureDist=False)
        ptest.append(pptest)
    in_bounds = all(c == 1 for c in ptest)

    return(in_bounds)
