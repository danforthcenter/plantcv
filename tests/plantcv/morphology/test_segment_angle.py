import cv2
import numpy as np
from plantcv.plantcv import outputs
from plantcv.plantcv.morphology import segment_angle


def test_segment_angle(morphology_test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    skeleton = cv2.imread(morphology_test_data.skel_img, -1)
    _ = segment_angle(segmented_img=skeleton,
                      objects=morphology_test_data.load_segments(morphology_test_data.segments_file, "leaves"))
    assert len(outputs.observations['default']['segment_angle']['value']) == 4


def test_segment_angle_overflow():
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Don't prune, would usually give overflow error without extra if statement in segment_angle
    skeleton = np.zeros((10, 10), dtype=np.uint8)
    edges = [np.array([[[5, 3]], [[5, 4]], [[5, 5]], [[5, 6]], [[5, 7]], [[5, 6]], [[5, 5]], [[5, 4]]], dtype=np.int32)]
    _ = segment_angle(segmented_img=skeleton, objects=edges)
    assert len(outputs.observations['default']['segment_angle']['value']) == 1
