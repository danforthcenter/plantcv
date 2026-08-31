import pytest
import cv2
import numpy as np
from plantcv.plantcv import outputs
from plantcv.plantcv.morphology.segment_insertion_angle import segment_insertion_angle


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


def test_segment_insertion_angle_vertical_stem():
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # A perfectly vertical stem fits with vx ~ 0; extrapolating the stem line to the
    # image edges then overflows the 32-bit coordinates cv2.line accepts
    from plantcv.plantcv._helpers import _cv2_findcontours
    stem_img = np.zeros((500, 500), dtype=np.uint8)
    cv2.line(stem_img, (250, 50), (250, 450), 255, 1)
    leaf_img = np.zeros((500, 500), dtype=np.uint8)
    cv2.line(leaf_img, (251, 149), (330, 70), 255, 1)
    skel = stem_img | leaf_img
    stem_obj, _ = _cv2_findcontours(bin_img=stem_img)
    leaf_obj, _ = _cv2_findcontours(bin_img=leaf_img)
    labeled_img = segment_insertion_angle(skel_img=skel, segmented_img=skel, leaf_objects=leaf_obj,
                                          stem_objects=stem_obj, size=20)
    angles = outputs.observations['default']['segment_insertion_angle']['value']
    assert len(angles) == 1
    assert abs(angles[0] - 45) < 5
    # The stem line is still drawn, as a vertical line
    assert (labeled_img[:, 250] == 150).any()


def test_segment_insertion_angle_slanted_stem(morphology_test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # A slanted stem keeps the extrapolated stem line, drawn to the image edges
    from plantcv.plantcv._helpers import _cv2_findcontours
    stem_img = np.zeros((500, 500), dtype=np.uint8)
    cv2.line(stem_img, (100, 100), (400, 400), 255, 1)
    leaf_img = np.zeros((500, 500), dtype=np.uint8)
    cv2.line(leaf_img, (151, 149), (220, 80), 255, 1)
    skel = stem_img | leaf_img
    stem_obj, _ = _cv2_findcontours(bin_img=stem_img)
    leaf_obj, _ = _cv2_findcontours(bin_img=leaf_img)
    labeled_img = segment_insertion_angle(skel_img=skel, segmented_img=skel, leaf_objects=leaf_obj,
                                          stem_objects=stem_obj, size=20)
    assert len(outputs.observations['default']['segment_insertion_angle']['value']) == 1
    # The stem line is extrapolated beyond the stem segment itself
    assert (labeled_img[440:500, 440:500] == 150).any()
    assert not (labeled_img[:, 250] == 150).all()
