import pytest
import numpy as np
from plantcv.plantcv.morphology.segment_combine import segment_combine
from tests import synthetic


def test_segment_combine():
    """Test for PlantCV."""
    skel = synthetic.skeleton()
    leaves, stem = synthetic.skeleton_segments()
    edges = stem + leaves
    # Test with list of IDs input
    _, new_objects = segment_combine(segment_list=[0, 1], objects=edges, mask=skel)
    assert len(new_objects) + 1 == len(edges)
    # The other segments keep their order, and the combined segment is appended last
    assert all(np.array_equal(a, b) for a, b in zip(new_objects[:-1], edges[2:]))
    assert np.array_equal(new_objects[-1], np.vstack([edges[1], edges[0]]))


def test_segment_combine_bad_input():
    """Test for PlantCV."""
    skel = synthetic.skeleton()
    leaves, stem = synthetic.skeleton_segments()
    with pytest.raises(RuntimeError):
        _ = segment_combine(segment_list=[0.5, 1.5], objects=stem + leaves, mask=skel)
