import cv2
import numpy as np
from plantcv.plantcv import outputs
from plantcv.plantcv.morphology import segment_ends


def test_segment_ends(morphology_test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    leaf_obj = morphology_test_data.load_segments(morphology_test_data.segments_file, "leaves")
    skeleton = cv2.imread(morphology_test_data.skel_img, -1)
    _, _, tips = segment_ends(skel_img=skeleton, leaf_objects=leaf_obj, mask=skeleton)
    assert len(tips) == 4


def test_segment_ends_no_mask(morphology_test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    leaf_obj = morphology_test_data.load_segments(morphology_test_data.segments_file, "leaves")
    skeleton = cv2.imread(morphology_test_data.skel_img, -1)
    _, _, tips = segment_ends(skel_img=skeleton, leaf_objects=leaf_obj, mask=None)
    assert len(tips) == 4
    
    
def test_segment_ends_unsortable(morphology_test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    obj = np.load(morphology_test_data.disconnected_segment_file)
    leaf_object = obj["data1"]
    skeleton = cv2.imread(morphology_test_data.disconnected_skel_img, -1)
    sorted_objs, _, tip_list = segment_ends(skel_img=skeleton, leaf_objects=[leaf_object], mask=None)
    assert len(tip_list) == 2 and len(sorted_objs) == 0
