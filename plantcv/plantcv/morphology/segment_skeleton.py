# Break skeleton into segments
from plantcv.plantcv.morphology.find_branch_pts import _find_branch_pts
from plantcv.plantcv._helpers import _cv2_findcontours, _dilate, _image_subtract


def _segment_skeleton(skel_img):
    """Segment a skeleton image into pieces.

    Parameters
    ----------
    skel_img = numpy.ndarray,
        Skeletonized image

    Returns
    -------
    segmented_img    = numpy.ndarray,
        Segmented debugging image
    segment_objects  = list,
        list of contours
    """
    # Find branch points
    _, _, bp = _find_branch_pts(skel_img)
    bp = _dilate(bp, 3, 1)
    # Subtract from the skeleton so that leaves are no longer connected
    segments = _image_subtract(skel_img, bp)
    # Gather contours of leaves
    segment_objects, _ = _cv2_findcontours(bin_img=segments)

    return segment_objects
