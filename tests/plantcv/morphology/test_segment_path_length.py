import numpy as np
import pytest
from plantcv.plantcv import outputs
from plantcv.plantcv.morphology.segment_path_length import segment_path_length
from tests import synthetic


def test_segment_path_length():
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    leaves, _ = synthetic.skeleton_segments()
    _ = segment_path_length(segmented_img=synthetic.skeleton(), objects=leaves)
    # A segment contour runs out and back along the segment, less its closing step, and is halved:
    # polyline length - first step / 2. Lower left: 27 - 0.5. Right: 17 + sqrt(2) + 9 - 0.5.
    # Upper leaves: 18 * sqrt(2) - sqrt(2) / 2.
    assert outputs.observations['default']['segment_path_length']['value'] == pytest.approx(
        [26.5, 25.5 + np.sqrt(2), 17.5 * np.sqrt(2), 17.5 * np.sqrt(2)])
