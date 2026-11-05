import numpy as np
from plantcv.plantcv.masks2labels import masks2labels
from tests import synthetic


def test_masks2labels():
    """Test for PlantCV."""
    stem, left_leaf, right_leaf, small_object = synthetic.region_masks()
    # An empty mask gets no label, so the labels stay consecutive
    empty = np.zeros_like(stem)
    labeled_mask, _, num_label = masks2labels([stem, empty, left_leaf, right_leaf, small_object])
    # 4 non-empty masks, labeled 1-4 in list order
    expected = np.zeros(synthetic.PLANT_SHAPE, dtype=np.int32)
    for value, mask in enumerate([stem, left_leaf, right_leaf, small_object], start=1):
        expected[mask > 0] = value
    assert num_label == 4
    assert np.array_equal(labeled_mask, expected)
