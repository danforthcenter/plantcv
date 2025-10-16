import cv2
import numpy as np
from plantcv.plantcv import outputs
from plantcv.plantcv.morphology import segment_width


def test_segment_width(morphology_test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    leaf_obj = morphology_test_data.load_segments(morphology_test_data.segments_file, "leaves")
    skeleton = cv2.imread(morphology_test_data.skel_img, -1)
    _ = segment_width(img=skeleton, labeled_mask=leaf_obj)
    assert outputs.observations['leaves_1']['segment_width']['value'] == 2

