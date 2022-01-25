import pytest
import cv2
import numpy as np
from plantcv.plantcv import outputs
from plantcv.plantcv.morphology import segment_insertion_angle


@pytest.mark.parametrize("size", [3, 100])
def test_segment_insertion_angle(size, morphology_test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    skel = cv2.imread(morphology_test_data.skel_img, -1)
    leaf_obj = morphology_test_data.load_segments(morphology_test_data.segments_file, "leaves")
    stem_obj = morphology_test_data.load_segments(morphology_test_data.segments_file, "stem")
    _ = segment_insertion_angle(skel_img=skel, segmented_img=skel, leaf_objects=leaf_obj, stem_objects=stem_obj, size=size)
    assert len(outputs.observations['default']['segment_insertion_angle']['value']) == 4


def test_segment_insertion_angle_bad_stem(morphology_test_data):
    """Test for PlantCV."""
    skel = cv2.imread(morphology_test_data.skel_img, -1)
    leaf_obj = morphology_test_data.load_segments(morphology_test_data.segments_file, "leaves")
    stem_obj = [leaf_obj[0], np.array([[[0, 0]], [[1, 1]], [[2, 2]], [[3, 3]], [[4, 4]]], dtype=np.int32)]
    with pytest.raises(RuntimeError):
        _ = segment_insertion_angle(skel_img=skel, segmented_img=skel, leaf_objects=leaf_obj, stem_objects=stem_obj, size=10)


def test_segment_insertion_angle_overflow():
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Don't prune, would usually give overflow error without extra if statement in segment_angle
    skel = np.zeros((10, 10), dtype=np.uint8)
    leaf_obj = [np.array([[[1, 1]], [[1, 2]], [[1, 3]], [[1, 4]], [[1, 5]], [[1, 6]], [[1, 7]], [[2, 7]], [[3, 7]], [[4, 7]],
                          [[5, 7]], [[6, 7]], [[5, 7]], [[4, 7]], [[3, 7]], [[2, 7]], [[1, 6]], [[1, 5]], [[1, 4]], [[1, 3]],
                          [[1, 2]]], dtype=np.int32)]
    stem_obj = [np.array([[[8, 9]]], dtype=np.int32), np.array([[[8, 0]], [[8, 1]], [[8, 2]], [[8, 3]], [[8, 4]], [[8, 5]],
                                                                [[8, 4]], [[8, 3]], [[8, 2]], [[8, 1]]], dtype=np.int32)]
    with pytest.raises(IndexError):
        _ = segment_insertion_angle(skel_img=skel, segmented_img=skel, leaf_objects=leaf_obj, stem_objects=stem_obj, size=3)
