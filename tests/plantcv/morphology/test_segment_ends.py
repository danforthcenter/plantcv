import cv2
import pytest
from plantcv.plantcv import outputs
from plantcv.plantcv.morphology import segment_ends


def test_segment_ends(morphology_test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    leaf_obj = morphology_test_data.load_segments(morphology_test_data.segments_file, "leaves")
    skeleton = cv2.imread(morphology_test_data.skel_img, -1)
    _, _, _, tips = segment_ends(skel_img=skeleton, leaf_objects=leaf_obj, mask=skeleton)
    assert len(tips) == 4


def test_segment_ends_no_mask(morphology_test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    leaf_obj = morphology_test_data.load_segments(morphology_test_data.segments_file, "leaves")
    skeleton = cv2.imread(morphology_test_data.skel_img, -1)
    _, _, _, tips = segment_ends(skel_img=skeleton, leaf_objects=leaf_obj, mask=None)
    assert len(tips) == 4
    
    
def test_segment_ends_unsortable(morphology_test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    leaf_objects=morphology_test_data.load_segments(morphology_test_data.segments_file, "edges")
    skeleton = cv2.imread(morphology_test_data.skel_img, -1)
    with pytest.raises(IndexError):
        _ = segment_ends(skel_img=skeleton, leaf_objects=leaf_objects, mask=None)
