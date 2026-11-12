import numpy as np
from plantcv.plantcv.morphology.skeletonize import skeletonize
from tests import synthetic


def test_skeletonize():
    """Test for PlantCV."""
    # Each disk thins to its center pixel
    expected = np.zeros(synthetic.TWO_PLANTS_SHAPE, dtype=np.uint8)
    for y, x in synthetic.TWO_PLANTS_CENTERS:
        expected[y, x] = 255
    assert np.array_equal(skeletonize(mask=synthetic.two_plants_mask()), expected)


def test_skeletonize_thin():
    """Test for PlantCV."""
    # A 1-pixel-wide skeleton is already thin
    skeleton = synthetic.skeleton()
    assert np.array_equal(skeletonize(mask=skeleton), skeleton)
