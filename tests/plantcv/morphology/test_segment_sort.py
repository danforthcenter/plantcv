import os
import numpy as np
from plantcv.plantcv._globals import params
from plantcv.plantcv.morphology.segment_sort import segment_sort
from tests import synthetic


def test_segment_sort(monkeypatch, tmpdir):
    """Test for PlantCV."""
    cache = tmpdir.mkdir("cache")
    monkeypatch.setattr(params, "debug_outdir", cache)
    monkeypatch.setattr(params, "device", 0)
    monkeypatch.setattr(params, "debug", "print")
    skeleton = synthetic.skeleton()
    leaves, stem = synthetic.skeleton_segments()
    leaf_obj, stem_obj = segment_sort(skel_img=skeleton, objects=stem + leaves, mask=skeleton)
    # The first (bottom) stem segment is always stem; of the others only the leaves hold a tip
    assert len(leaf_obj) == 4 and len(stem_obj) == 3
    assert all(np.array_equal(a, b) for a, b in zip(leaf_obj, leaves))
    assert os.path.exists(os.path.join(cache, "0_sorted_segments.png"))


def test_segment_sort_no_mask():
    """Test for PlantCV."""
    skeleton = synthetic.skeleton()
    leaves, stem = synthetic.skeleton_segments()
    leaf_obj, stem_obj = segment_sort(skel_img=skeleton, objects=stem + leaves)
    assert len(leaf_obj) == 4 and len(stem_obj) == 3
    assert all(np.array_equal(a, b) for a, b in zip(leaf_obj, leaves))
