import cv2
import numpy as np
from skimage.measure import label
from plantcv.plantcv._helpers import _cv2_findcontours


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
    # if there are images in the coco object then set the next image ID
    image_id = kwargs.get("image_id", 1)  # we might just 1 index in this house
    if coco.images:
        image_id = int(np.max([dic["id"] for dic in coco.images]) + 1)
    # take the image field kwargs, check if instead I want to others to a new dict?
    additional_image_fields = ['license', 'filename', 'date_captured']
    image_kwargs = {k.lower(): v for k, v in kwargs.items() if k.lower() in additional_image_fields}
    # make new image dictionary
    images = {"id": image_id, **image_kwargs}
    # add height, width
    h, w = np.shape(mask)
    images["height"] = h
    images["width"] = w
    # make new annotation dict
    # by default assume that masks are of "plant" objects
    annotation_starter = {"category_id": kwargs.get("category_id", "plant"),
                          "iscrowd": kwargs.get("iscrowd", 0),
                          "image_id": image_id}
    # building this for object detection to start, I might end up
    # having helpers for object (stuff), keypoints, panoptics, captions, and densepose though.
    annotations = []
    labeled_mask, n_labels = label(mask, background=0,
                                   return_num=True, connectivity=2)

    if n_labels:
        for i in range(1, n_labels + 1):
            # mask of only this object
            obj_mask = np.where(labeled_mask == i, 255, 0).astype(np.uint8)
            # get object area
            obj_area = int(np.count_nonzero(obj_mask))
            # get bounding box of object
            rows = np.any(obj_mask, axis=1)
            cols = np.any(obj_mask, axis=0)
            x, w = np.where(rows)[0][[0, -1]]
            y, h = np.where(cols)[0][[0, -1]]
            # get segmentation (contour)
            obj_contours = []
            if obj_area:
                obj_contours, _ = _cv2_findcontours(obj_mask)
                epsilon = 0.01 * cv2.arcLength(obj_contours[0], True)
                # COCO polygons are stored as flat lists of alternating X, Y values
                vertices = cv2.approxPolyDP(obj_contours[0], epsilon, True).flatten().tolist()
            # make dictionary entry
            obj_dict = {"id": i,
                        "bbox": [int(x), int(y), int(w - x), int(h - y)],
                        "area": obj_area,
                        "segmentation": vertices}
            # add to new annotations
            annotations.append(annotation_starter | obj_dict)

    return annotations, images
