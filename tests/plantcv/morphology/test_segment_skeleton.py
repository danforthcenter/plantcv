import numpy as np
from plantcv.plantcv.morphology.segment_skeleton import segment_skeleton
from tests import synthetic


def _same_segments(segments, expected):
    """Check that two lists of contours hold the same contours in any order."""
    return len(segments) == len(expected) and all(any(np.array_equal(a, b) for b in segments) for a in expected)


def test_segment_skeleton():
    """Test for PlantCV."""
    skeleton = synthetic.skeleton()
    leaves, stem = synthetic.skeleton_segments()
    _, segment_objects = segment_skeleton(skel_img=skeleton, mask=skeleton)
    # 4 leaf segments and 3 stem segments between the branch points
    assert _same_segments(segment_objects, leaves + stem)


def test_segment_skeleton_no_mask():
    """Test for PlantCV."""
    leaves, stem = synthetic.skeleton_segments()
    _, segment_objects = segment_skeleton(skel_img=synthetic.skeleton())
    assert _same_segments(segment_objects, leaves + stem)
