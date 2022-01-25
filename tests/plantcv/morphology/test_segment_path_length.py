import cv2
from plantcv.plantcv import outputs
from plantcv.plantcv.morphology import segment_path_length


def test_segment_path_length(morphology_test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    skel = cv2.imread(morphology_test_data.skel_img, -1)
    _ = segment_path_length(segmented_img=skel,
                            objects=morphology_test_data.load_segments(morphology_test_data.segments_file, "leaves"))
    assert len(outputs.observations['default']['segment_path_length']['value']) == 4
