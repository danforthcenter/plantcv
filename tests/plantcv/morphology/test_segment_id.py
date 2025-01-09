import cv2
from plantcv.plantcv.morphology import segment_id


def test_segment_id(morphology_test_data):
    """Test for PlantCV."""
    skel = cv2.imread(morphology_test_data.skel_img, -1)
    leaf_obj = morphology_test_data.load_segments(morphology_test_data.segments_file, "leaves")
    _, labeled_img = segment_id(skel_img=skel, objects=leaf_obj, mask=skel)
    assert skel.shape == labeled_img.shape[:2]


def test_segment_id_no_mask(morphology_test_data):
    """Test for PlantCV."""
    skel = cv2.imread(morphology_test_data.skel_img, -1)
    leaf_obj = morphology_test_data.load_segments(morphology_test_data.segments_file, "leaves")
    _, labeled_img = segment_id(skel_img=skel, objects=leaf_obj)
    assert skel.shape == labeled_img.shape[:2]
