import pytest
import cv2
from plantcv.plantcv import outputs
from plantcv.plantcv.morphology import segment_tangent_angle


@pytest.mark.parametrize("size", [3, 100])
def test_segment_tangent_angle(size, morphology_test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    skel = cv2.imread(morphology_test_data.skel_img, -1)
    leaf_obj = morphology_test_data.load_segments(morphology_test_data.segments_file, "leaves")
    _ = segment_tangent_angle(segmented_img=skel, objects=leaf_obj, size=size)
    assert len(outputs.observations['default']['segment_tangent_angle']['value']) == 4
