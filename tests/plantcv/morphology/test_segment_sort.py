import numpy as np
from plantcv.plantcv.morphology.segment_sort import segment_sort
from tests import synthetic


def test_segment_sort():
    """Test for PlantCV."""
    skeleton = synthetic.skeleton()
    leaves, stem = synthetic.skeleton_segments()
    leaf_obj, stem_obj = segment_sort(skel_img=skeleton, objects=stem + leaves, mask=skeleton)
    # The first (bottom) stem segment is always stem; of the others only the leaves hold a tip
    assert len(leaf_obj) == 4 and len(stem_obj) == 3
    assert all(np.array_equal(a, b) for a, b in zip(leaf_obj, leaves))


def test_segment_sort_no_mask():
    """Test for PlantCV."""
    skeleton = synthetic.skeleton()
    leaves, stem = synthetic.skeleton_segments()
    leaf_obj, stem_obj = segment_sort(skel_img=skeleton, objects=stem + leaves)
    assert len(leaf_obj) == 4 and len(stem_obj) == 3
    assert all(np.array_equal(a, b) for a, b in zip(leaf_obj, leaves))
