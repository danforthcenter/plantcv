import os
import pytest
import numpy as np
from plantcv.plantcv.classes import COCO, Objects, Point


def _square_mask():
    """Helper for tests."""
    mask = np.zeros((100, 100), dtype=np.uint8)
    mask[30:70, 30:70] = 1
    return mask


def test_init_coco():
    """Test for PlantCV."""
    coco = COCO()
    assert isinstance(coco, COCO)


def test_init_complex_coco():
    """Test for PlantCV."""
    mask = np.zeros((100, 100), dtype=np.uint8)
    mask[30:70, 30:70] = 1
    coco = COCO(source=mask, description="description", datetime="datetime",
                id=1, name="my_license", url="my_license.com",
                image_id=200, filename="my_file.png", iscrowd=1)
    assert isinstance(coco, COCO)


def test_coco_add_record():
    """Test for PlantCV."""
    mask = np.zeros((100, 100), dtype=np.uint8)
    mask[30:70, 30:70] = 1
    mask2 = np.zeros((150, 150), dtype=np.uint8)
    mask2[30:70, 30:70] = 1
    coco = COCO(mask)
    coco.add_record(source=mask2)
    assert isinstance(coco, COCO)
    assert len(coco.annotations) == 2


def test_coco_clear():
    """Test for PlantCV."""
    mask = np.zeros((100, 100), dtype=np.uint8)
    mask[30:70, 30:70] = 1
    coco = COCO(source=mask)
    coco_imgs = coco.images
    coco.clear()
    # check that adding data worked
    assert len(coco_imgs) == 1
    # check that removing data cleared all lists
    assert coco.info == {}
    for attr in ["licenses", "images", "annotations", "categories"]:
        assert getattr(coco, attr) == []
        # touch the setters
        setattr(coco, attr, [1])
        assert getattr(coco, attr) == [1]


def test_coco_str_repr():
    """Test for PlantCV."""
    coco = COCO()
    assert "plantcv.plantcv.COCO" in str(coco)
    assert "plantcv.plantcv.COCO" in coco.__repr__()


def test_coco_save_and_load(tmpdir):
    """Test for PlantCV."""
    coco = COCO(description="testing")
    assert coco.info["description"] == "testing"
    cache_dir = tmpdir.mkdir("cache")
    outpath = os.path.join(cache_dir, "coco.json")
    # check saving as write
    coco.save(outpath, coco_suffix=False)
    assert os.path.exists(outpath)
    # check loading
    coco_new = COCO()
    coco_new.load(outpath)
    assert coco_new.info["description"] == "testing"
    # check saving with append
    coco_new.save(outpath, mode="a", coco_suffix=False)
    assert os.path.exists(outpath)


def test_coco_updating_list_fields():
    """Test for PlantCV."""
    coco = COCO(description="testing", id=1, name="Open")
    assert coco.licenses[0]["name"] == "Open"
    coco.add_record(info = {"datetime": "now"}, rights={"id": 1, "name": "Open Access"})
    assert coco.licenses[0]["name"] == "Open Access"
    coco.add_record(rights={"id": 2, "name": "Open"})
    assert coco.licenses[1]["name"] == "Open"


def test_coco_append_category_conflict(tmpdir):
    """Test for PlantCV."""
    outpath = os.path.join(tmpdir.mkdir("cache"), "coco.json")
    # existing file has category 1 = "plant"
    COCO(source=_square_mask()).save(outpath, mode="w")
    # new data uses category 1 = "weed"
    coco = COCO()
    coco.add_record(source=_square_mask(), category={"id": 1, "name": "weed"})
    with pytest.raises(ValueError):
        coco.save(outpath, mode="a")


def test_coco_add_record_default_category():
    """Test for PlantCV."""
    coco = COCO()
    coco.add_record(source=_square_mask())
    assert coco.categories == [{"id": 1, "name": "plant"}]
    assert coco.annotations[0]["category_id"] == 1


def test_coco_add_record_undefined_category():
    """Test for PlantCV."""
    coco = COCO()
    with pytest.raises(ValueError):
        coco.add_record(source=_square_mask(), category_id=2)


def test_coco_add_record_default_category_with_existing():
    """Test for PlantCV."""
    # categories exist but none is id 1, so the default category_id is undefined
    coco = COCO(source=_square_mask(), category_id=2)
    with pytest.raises(ValueError):
        coco.add_record(source=_square_mask())


def test_coco_roi_source():
    """Test for PlantCV."""
    roi = [np.array([[[150, 150]], [[150, 174]], [[249, 174]], [[249, 150]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi_Obj = Objects(contours=[roi], hierarchy=[roi_str])
    coco = COCO(source=roi_Obj, shape=(250, 250))
    assert len(coco.annotations) == 1


def test_coco_roi_source_no_shape():
    """Test for PlantCV."""
    roi = [np.array([[[150, 150]], [[150, 174]], [[249, 174]], [[249, 150]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi_Obj = Objects(contours=[roi], hierarchy=[roi_str])
    with pytest.raises(RuntimeError):
        _ = COCO(source=roi_Obj)


def test_coco_add_record_bad_input_type():
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _ = COCO(source={})


def test_coco_format_points():
    """Test for PlantCV."""
    img = np.random.randint(0, 256, (10, 10, 3), dtype=np.uint8)
    mask = np.zeros((12, 12), dtype=np.uint8)
    mask[10, 10] = 1
    p = Point(img)
    p.markers = [(10, 10)]
    coco = COCO(mask, points = p)
    assert coco.annotations[0]["keypoints"] == [10, 10, 2]


def test_coco_format_points_tuple():
    """Test for PlantCV."""
    img = np.random.randint(0, 256, (10, 10, 3), dtype=np.uint8)
    mask = np.zeros((12, 12), dtype=np.uint8)
    mask[10, 10] = 1
    p = (10, 10)
    coco = COCO(mask, points = p)
    assert coco.annotations[0]["keypoints"] == [10, 10, 2]


def test_coco_bad_points():
    """Test for PlantCV."""
    img = np.random.randint(0, 256, (10, 10, 3), dtype=np.uint8)
    mask = np.zeros((12, 12), dtype=np.uint8)
    mask[10, 10] = 1
    p = (10, 10, 10, 10)
    with pytest.raises(RuntimeError):
        _ = COCO(mask, points = p)


def test_coco_one_point_many_objects_error():
    """Test for PlantCV."""
    img = np.random.randint(0, 256, (10, 10, 3), dtype=np.uint8)
    mask = np.zeros((12, 12), dtype=np.uint8)
    mask[8:10, 8:10] = 1
    mask[3:6, 3:6] = 1
    p = Point(img)
    p.markers = [(10, 10)]
    with pytest.raises(RuntimeError):
        _ = COCO(mask, points = p)
