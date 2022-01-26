import cv2
from plantcv.plantcv.morphology import segment_sort


def test_segment_sort(morphology_test_data):
    """Test for PlantCV."""
    skeleton = cv2.imread(morphology_test_data.skel_img, -1)
    leaf_obj, _ = segment_sort(skel_img=skeleton,
                               objects=morphology_test_data.load_segments(morphology_test_data.segments_file, "edges"),
                               mask=skeleton)
    assert len(leaf_obj) == 4


def test_segment_sort_no_mask(morphology_test_data):
    """Test for PlantCV."""
    skeleton = cv2.imread(morphology_test_data.skel_img, -1)
    leaf_obj, _ = segment_sort(skel_img=skeleton,
                               objects=morphology_test_data.load_segments(morphology_test_data.segments_file, "edges"))
    assert len(leaf_obj) == 4
