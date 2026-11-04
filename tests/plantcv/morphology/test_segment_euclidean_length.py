import pytest
import numpy as np
from plantcv.plantcv import outputs
from plantcv.plantcv.morphology.segment_euclidean_length import segment_euclidean_length
from tests import synthetic


def test_segment_euclidean_length():
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    leaves, _ = synthetic.skeleton_segments()
    _ = segment_euclidean_length(segmented_img=synthetic.skeleton(), objects=leaves)
    # Distance between segment ends: (31, 70)-(58, 70); (62, 58)-(80, 68); (40, 25)-(58, 43); (62, 43)-(80, 25)
    assert outputs.observations['default']['segment_eu_length']['value'] == pytest.approx(
        [27, np.sqrt(18 ** 2 + 10 ** 2), 18 * np.sqrt(2), 18 * np.sqrt(2)])


def test_segment_euclidean_length_bad_input():
    """Test for PlantCV."""
    skel = np.zeros((10, 10), dtype=np.uint8)
    edges = [np.array([[[5, 3]], [[4, 4]], [[3, 5]], [[4, 6]], [[5, 7]], [[6, 6]], [[7, 5]], [[6, 4]]], dtype=np.int32)]
    with pytest.raises(RuntimeError):
        _ = segment_euclidean_length(segmented_img=skel, objects=edges)
