import pytest
import cv2
from plantcv.plantcv.morphology import segment_combine


def test_segment_combine(morphology_test_data):
    """Test for PlantCV."""
    skel = cv2.imread(morphology_test_data.skel_img, -1)
    edges = morphology_test_data.load_segments(morphology_test_data.segments_file, "edges")
    # Test with list of IDs input
    _, new_objects = segment_combine(segment_list=[0, 1], objects=edges, mask=skel)
    assert len(new_objects) + 1 == len(edges)



def test_segment_combine_bad_input(morphology_test_data):
    """Test for PlantCV."""
    skel = cv2.imread(morphology_test_data.skel_img, -1)
    edges = morphology_test_data.load_segments(morphology_test_data.segments_file, "edges")
    with pytest.raises(RuntimeError):
        _ = segment_combine(segment_list=[0.5, 1.5], objects=edges, mask=skel)
