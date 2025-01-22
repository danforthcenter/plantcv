import cv2
from plantcv.plantcv import outputs
from plantcv.plantcv.morphology import segment_ends


def test_segment_ends(morphology_test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    leaf_obj = morphology_test_data.load_segments(morphology_test_data.segments_file, "leaves")
    skeleton = cv2.imread(morphology_test_data.skel_img, -1)
    segment_ends(skel_img=skeleton, leaf_objects=leaf_obj, mask=skeleton)
    assert len(outputs.observations['default']['segment_branch_points']['value']) == 4


def test_segment_ends_no_mask(morphology_test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    leaf_obj = morphology_test_data.load_segments(morphology_test_data.segments_file, "leaves")
    skeleton = cv2.imread(morphology_test_data.skel_img, -1)
    segment_ends(skel_img=skeleton, leaf_objects=leaf_obj, mask=None)
    assert len(outputs.observations['default']['segment_branch_points']['value']) == 4