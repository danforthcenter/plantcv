import numpy as np
import pytest
from plantcv.plantcv import outputs
from plantcv.plantcv.morphology import segment_curvature
from tests import synthetic


def test_segment_curvature():
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    leaves, _ = synthetic.skeleton_segments()
    _ = segment_curvature(segmented_img=synthetic.skeleton(), objects=leaves)
    # Path length (see test_segment_path_length) over euclidean length (see test_segment_euclidean_length)
    assert outputs.observations['default']['segment_curvature']['value'] == pytest.approx(
        [26.5 / 27, (25.5 + np.sqrt(2)) / np.sqrt(424), 17.5 / 18, 17.5 / 18])
