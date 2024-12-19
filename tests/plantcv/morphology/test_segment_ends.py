import cv2
from plantcv.plantcv import outputs
from plantcv.plantcv.morphology import segment_ends


def test_segment_ends(morphology_test_data):
    """Test for PlantCV."""
    leaf_obj = morphology_test_data.load_segments(morphology_test_data.segments_file, "leaves")
    skeleton = cv2.imread(morphology_test_data.skel_img, -1)
    segment_ends(segmented_img=skeleton, objects=leaf_obj)
    assert len(outputs.observations['default']['segment_branch_points']['value']) == 4
