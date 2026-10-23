import cv2
import numpy as np
from skimage.measure import label
from plantcv.plantcv._helpers import _cv2_findcontours

# COCO image fields that can be passed through as keyword arguments
IMAGE_FIELDS = ["license", "file_name", "date_captured", "coco_url", "flickr_url"]


def _next_id(records):
    """Next unused integer id in a list of COCO records

    Parameters
    ----------
    records : list
        List of COCO dictionaries with an "id" key

    Returns
    -------
    next_id : int
        One more than the largest existing id, or 1 if there are no records
    """
    if not records:
        return 1
    return int(max(rec["id"] for rec in records)) + 1


def _mask_to_rle(obj_mask):
    """Uncompressed COCO RLE of a single object mask

    Parameters
    ----------
    obj_mask : numpy.ndarray
        Binary mask of one object

    Returns
    -------
    rle : dict
        {"counts": [...], "size": [height, width]}, runs are column-major and start with background
    """
    flat = (obj_mask > 0).flatten(order="F").astype(np.int8)
    change = np.flatnonzero(np.diff(flat)) + 1
    counts = np.diff(np.concatenate(([0], change, [flat.size]))).tolist()
    if flat[0]:
        # RLE always starts with a (possibly empty) background run
        counts = [0] + counts
    return {"counts": counts, "size": [int(obj_mask.shape[0]), int(obj_mask.shape[1])]}


def _mask_to_polygons(obj_mask, epsilon=0):
    """COCO polygons of an object mask, traced along pixel edges

    Parameters
    ----------
    obj_mask : numpy.ndarray
        Binary mask of one object
    epsilon : float
        approxPolyDP tolerance in pixels, 0 keeps the exact pixel boundary

    Returns
    -------
    polygons : list
        List of flat [x1, y1, x2, y2, ...] polygons with vertices on pixel corners
    """
    rows = np.any(obj_mask, axis=1)
    cols = np.any(obj_mask, axis=0)
    y_min, y_max = np.where(rows)[0][[0, -1]]
    x_min, x_max = np.where(cols)[0][[0, -1]]
    # crop to only the section with this object
    crop = obj_mask[y_min:y_max + 1, x_min:x_max + 1] > 0
    # upsample the mask by a factor of 2 in each direction.
    # this puts the boundary pixels at even counts instead of halfway through a pixel
    upsampled = np.kron(crop, np.ones((2, 2))).astype(np.uint8)
    # find contours in the upscaled image
    contours, hierarchy = cv2.findContours(upsampled, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    corners = []
    for contour in contours:
        # reshape contour to original image size, undoing upscale and crop
        pts = (contour.reshape(-1, 2) + 1) // 2 + [x_min, y_min]
        # remove points identical to the preceding point, end with only unique points
        pts = pts[np.any(pts != np.roll(pts, 1, axis=0), axis=1)]
        # epsilon 0 removes collinear points, raise epsilon for simpler segments
        corners.append(cv2.approxPolyDP(pts.reshape(-1, 1, 2).astype(np.int32), epsilon, True).reshape(-1, 2))
    polygons = []
    for outer, (_, _, child, parent) in zip(corners, hierarchy[0]):
        # do not do this for "top level" objects
        if parent != -1:
            continue
        polygon = outer
        # for nested objects stack the polygons until we reach the top level
        while child != -1:
            hole = corners[child]
            polygon = np.vstack([polygon[:1], hole, hole[:1], polygon])
            child = hierarchy[0][child][0]
        polygons.append(polygon.flatten().tolist())
    return polygons


def _coco_annotation_from_mask(coco, mask, **kwargs):
    """Extract COCO traits from a mask

    Parameters
    ----------
    coco : plantcv.plantcv.COCO object
        Existing COCO object
    mask : numpy.ndarray
        Binary (8bit) or labeled (32bit) mask
    **kwargs : Other keyword arguments that will serve as key value pairs in coco

    Returns
    -------
    annotations : list,
        COCO annotations of the mask
    images : list,
        COCO image characteristics of the mask
    """
    kwargs = {k.lower(): v for k, v in kwargs.items()}
    # if there are images in the coco object then set the next image ID
    image_id = int(kwargs.get("image_id", _next_id(coco.images)))
    if image_id in [img["id"] for img in coco.images]:
        raise ValueError(f"image_id {image_id} is already used in this COCO object")
    if "filename" in kwargs and "file_name" not in kwargs:
        kwargs["file_name"] = kwargs["filename"]

    image_kwargs = {k: v for k, v in kwargs.items() if k in IMAGE_FIELDS}
    # add height, width
    h, w = np.shape(mask)
    image = {"id": image_id, "width": int(w), "height": int(h), **image_kwargs}

    iscrowd = int(kwargs.get("iscrowd", 0))
    annotation_starter = {"category_id": kwargs.get("category_id", 1),
                          "iscrowd": iscrowd,
                          "image_id": image_id}

    # binary masks are split into connected objects, labeled masks keep their labels
    labeled_mask = mask
    if np.unique(mask[mask != 0]).size <= 1:
        labeled_mask = label(mask != 0, background=0, connectivity=2)

    obj_labels = np.unique(labeled_mask[labeled_mask != 0])

    # annotation ids are unique across the whole dataset
    first_ann_id = _next_id(coco.annotations)
    annotations = []

    for offset, obj_label in enumerate(obj_labels):
        # mask of only this object
        obj_mask = np.where(labeled_mask == obj_label, 255, 0).astype(np.uint8)
        # get object area
        obj_area = int(np.count_nonzero(obj_mask))
        # get bounding box of object, [x, y, width, height] in pixels
        rows = np.any(obj_mask, axis=1)
        cols = np.any(obj_mask, axis=0)
        y_min, y_max = np.where(rows)[0][[0, -1]]
        x_min, x_max = np.where(cols)[0][[0, -1]]
        # crowd annotations are stored as RLE, others as polygons
        if iscrowd:
            segmentation = _mask_to_rle(obj_mask)
        else:
            segmentation = _mask_to_polygons(obj_mask)
        obj_dict = {"id": first_ann_id + offset,
                    "bbox": [int(x_min), int(y_min), int(x_max - x_min) + 1, int(y_max - y_min) + 1],
                    "area": obj_area,
                    "segmentation": segmentation}
        annotations.append(annotation_starter | obj_dict)

    return annotations, image
