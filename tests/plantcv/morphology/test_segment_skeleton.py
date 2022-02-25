import cv2
from plantcv.plantcv.morphology import segment_skeleton


def test_segment_skeleton(morphology_test_data):
    """Test for PlantCV."""
    mask = cv2.imread(morphology_test_data.skel_img, -1)
    skeleton = cv2.imread(morphology_test_data.skel_img, -1)
    _, segment_objects = segment_skeleton(skel_img=skeleton, mask=mask)
    assert len(segment_objects) == 7


def test_segment_skeleton_no_mask(morphology_test_data):
    """Test for PlantCV."""
    skeleton = cv2.imread(morphology_test_data.skel_img, -1)
    _, segment_objects = segment_skeleton(skel_img=skeleton)
    assert len(segment_objects) == 7
