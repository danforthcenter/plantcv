import cv2
import numpy as np
from plantcv.plantcv import outputs
from plantcv.plantcv.morphology.segment_ends import segment_ends
from tests import synthetic

# Leaf tips, and the leaf segment ends next to the branch points (see tests/synthetic.py)
LEAF_TIPS = [(31, 70), (80, 68), (40, 25), (80, 25)]
LEAF_INNER_ENDS = [(58, 70), (62, 58), (58, 43), (62, 43)]


def _check_sorted(sorted_objs, leaves):
    """Check that leaves are sorted by the y-coordinate of their inner end, bottom first."""
    assert np.array_equal(sorted_objs[0], leaves[0]) and np.array_equal(sorted_objs[1], leaves[1])
    # The upper leaves share the inner end y-coordinate 43
    assert all(any(np.array_equal(a, b) for b in sorted_objs[2:]) for a in leaves[2:])


def test_segment_ends():
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    leaves, _ = synthetic.skeleton_segments()
    skeleton = synthetic.skeleton()
    sorted_objs, inner, tips = segment_ends(skel_img=skeleton, leaf_objects=leaves, mask=skeleton)
    assert sorted(tips) == sorted(LEAF_TIPS)
    assert sorted(inner) == sorted(LEAF_INNER_ENDS)
    _check_sorted(sorted_objs, leaves)


def test_segment_ends_no_mask():
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    leaves, _ = synthetic.skeleton_segments()
    sorted_objs, inner, tips = segment_ends(skel_img=synthetic.skeleton(), leaf_objects=leaves, mask=None)
    assert sorted(tips) == sorted(LEAF_TIPS)
    assert sorted(inner) == sorted(LEAF_INNER_ENDS)
    _check_sorted(sorted_objs, leaves)


def test_segment_ends_unsortable():
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # A leaf disconnected from the rest of the skeleton has a tip at both ends and no branch point
    skeleton = np.zeros(synthetic.PLANT_SHAPE, dtype=np.uint8)
    cv2.line(skeleton, (30, 80), (70, 40), 255, 1)
    leaf_object, _ = synthetic.find_contours(skeleton)
    sorted_objs, inner, tip_list = segment_ends(skel_img=skeleton, leaf_objects=list(leaf_object), mask=None)
    assert sorted(tip_list) == [(30, 80), (70, 40)]
    assert inner == [] and sorted_objs == []
