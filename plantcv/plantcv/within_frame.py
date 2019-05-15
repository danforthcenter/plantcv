import cv2 as cv2
import numpy as np

def within_frame(img, obj):
    '''
    This function tests whether the plant object is completely in the field of view
    Input:
    img - an image with the bounds you are interested in
    obj - a single object, preferably after calling pcv.image_composition(), that is from within `img`

    Returns:
    in_bounds - a boolean (True or False) whether the object touches the edge of the image

    :param img: numpy.ndarray
    :param obj: str
    :return in_bounds: boolean

    '''
    # Check if object is touching image boundaries (QC)
    if len(np.shape(img)) == 3:
        ix, iy, iz = np.shape(img)
    else:
        ix, iy = np.shape(img)
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
