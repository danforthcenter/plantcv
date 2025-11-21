import cv2
from plantcv.plantcv import outputs
from plantcv.plantcv.morphology import segment_curvature


def test_segment_curvature(morphology_test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    skeleton = cv2.imread(morphology_test_data.skel_img, -1)
    _ = segment_curvature(segmented_img=skeleton,
                          objects=morphology_test_data.load_segments(morphology_test_data.segments_file, "leaves"))
    assert len(outputs.observations['default']['segment_curvature']['value']) == 4
