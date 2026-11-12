import numpy as np
import pytest
from plantcv.plantcv import outputs
from plantcv.plantcv.morphology.segment_angle import segment_angle
from tests import synthetic


def test_segment_angle():
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    leaves, _ = synthetic.skeleton_segments()
    _ = segment_angle(segmented_img=synthetic.skeleton(), objects=leaves)
    angles = outputs.observations['default']['segment_angle']['value']
    # Lower left leaf is horizontal. Upper left leaf: y decreases with x, slope -1, -45 degrees.
    # Upper right leaf: y increases with x, slope 1, 45 degrees.
    assert angles[0] == 0
    assert angles[1] == pytest.approx(-19.65889359)  # recorded value: the bent right leaf
    assert angles[2:] == pytest.approx([-45, 45])


def test_segment_angle_overflow():
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Don't prune, would usually give overflow error without extra if statement in segment_angle
    skeleton = np.zeros((10, 10), dtype=np.uint8)
    edges = [np.array([[[5, 3]], [[5, 4]], [[5, 5]], [[5, 6]], [[5, 7]], [[5, 6]], [[5, 5]], [[5, 4]]], dtype=np.int32)]
    _ = segment_angle(segmented_img=skeleton, objects=edges)
    assert len(outputs.observations['default']['segment_angle']['value']) == 1
