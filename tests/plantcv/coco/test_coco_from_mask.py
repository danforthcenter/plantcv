import pytest
import numpy as np
from plantcv.plantcv.classes import COCO
from plantcv.plantcv.coco.coco_from_mask import (_coco_annotation_from_mask, _mask_to_polygons,
                                                  _mask_to_rle)


def test_mask_to_rle_starts_with_foreground():
    """Test for PlantCV."""
    mask = np.zeros((3, 3), dtype=np.uint8)
    mask[0, 0] = 255
    # column-major runs always start with background, so a leading 0 run is added
    assert _mask_to_rle(mask) == {"counts": [0, 1, 8], "size": [3, 3]}


def test_mask_to_rle_starts_with_background():
    """Test for PlantCV."""
    mask = np.zeros((3, 3), dtype=np.uint8)
    mask[1, 0] = 255
    assert _mask_to_rle(mask) == {"counts": [1, 1, 7], "size": [3, 3]}


def test_coco_iscrowd_rle():
    """Test for PlantCV."""
    mask = np.zeros((10, 20), dtype=np.uint8)
    mask[0:4, 0:5] = 255
    coco = COCO(mask, iscrowd=1)
    seg = coco.annotations[0]["segmentation"]
    assert seg["size"] == [10, 20]
    assert seg["counts"][0] == 0
    assert sum(seg["counts"]) == 200
    assert sum(seg["counts"][1::2]) == coco.annotations[0]["area"] == 20



def test_coco_duplicate_image_id():
    """Test for PlantCV."""
    mask = np.zeros((20, 20), dtype=np.uint8)
    mask[5:10, 5:10] = 255
    coco = COCO(mask, image_id=5)
    with pytest.raises(ValueError):
        coco.add_record(source=mask, image_id=5)


def test_coco_annotation_labeled_mask():
    """Test for PlantCV."""
    # two touching objects that connected component labeling would merge
    mask = np.zeros((30, 30), dtype=np.int32)
    mask[5:15, 5:15] = 1
    mask[5:15, 15:25] = 2
    annotations, image = _coco_annotation_from_mask(COCO(), mask)
    assert image["width"] == 30 and image["height"] == 30
    assert [a["bbox"] for a in annotations] == [[5, 5, 10, 10], [15, 5, 10, 10]]
    assert [a["area"] for a in annotations] == [100, 100]
    assert [a["id"] for a in annotations] == [1, 2]


def test_coco_annotation_nested_mask():
    """Test for PlantCV."""
    mask = np.zeros((120, 120), dtype=np.uint8)
    mask[60:110, 20:80] = 255
    mask[75:95, 35:65] = 0
    coco = COCO(mask)
    assert coco.annotations[0]["area"] == 2400
