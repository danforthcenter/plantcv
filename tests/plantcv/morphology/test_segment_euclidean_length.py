import pytest
import cv2
import numpy as np
from plantcv.plantcv import outputs
from plantcv.plantcv.morphology import segment_euclidean_length


def test_segment_euclidean_length(morphology_test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    skeleton = cv2.imread(morphology_test_data.skel_img, -1)
    _ = segment_euclidean_length(segmented_img=skeleton,
                                 objects=morphology_test_data.load_segments(morphology_test_data.segments_file, "leaves"))
    assert len(outputs.observations['default']['segment_eu_length']['value']) == 4


def test_segment_euclidean_length_bad_input():
    """Test for PlantCV."""
    skel = np.zeros((10, 10), dtype=np.uint8)
    edges = [np.array([[[5, 3]], [[4, 4]], [[3, 5]], [[4, 6]], [[5, 7]], [[6, 6]], [[7, 5]], [[6, 4]]], dtype=np.int32)]
    with pytest.raises(RuntimeError):
        _ = segment_euclidean_length(segmented_img=skel, objects=edges)
