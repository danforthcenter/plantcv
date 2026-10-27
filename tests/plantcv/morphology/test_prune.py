import numpy as np
from plantcv.plantcv.morphology.prune import prune
from tests import synthetic


def test_prune():
    """Test for PlantCV."""
    skeleton = synthetic.skeleton()
    pruned_img, _, _ = prune(skel_img=skeleton, size=1, mask=skeleton)
    # No leaf segment is 1 pixel or shorter, so pruning only removes the 5 tip pixels
    expected = skeleton.copy()
    for x, y in synthetic.SKELETON_TIPS:
        expected[y, x] = 0
    assert np.array_equal(pruned_img, expected)


def test_prune_no_mask():
    """Test for PlantCV."""
    skeleton = synthetic.skeleton()
    pruned_img, _, _ = prune(skel_img=skeleton, size=100)
    # Every leaf segment is removed, then one more pixel is pruned from each remaining end,
    # leaving the stem without its bottom tip: x = 60, y = 45..88
    expected = np.zeros_like(skeleton)
    expected[45:89, 60] = 255
    assert np.array_equal(pruned_img, expected)


def test_prune_size0():
    """Test for PlantCV."""
    skeleton = synthetic.skeleton()
    pruned_img, _, _ = prune(skel_img=skeleton, size=0)
    assert np.array_equal(pruned_img, skeleton)
