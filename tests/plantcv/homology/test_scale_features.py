import pytest
import numpy as np
from plantcv.plantcv.homology import scale_features

# Corners of the synthetic plant: stem top, left leaf tip, right leaf tip, and stem base
PLANT_POINTS = np.array([[[58, 30]], [[30, 40]], [[89, 64]], [[61, 89]]])


@pytest.mark.parametrize("pos", ["NA", 50])
def test_scale_features(pos, synthetic_mask):
    """Test for PlantCV."""
    points_rescaled, _, _ = scale_features(mask=synthetic_mask, points=PLANT_POINTS, line_position=pos)
    # One rescaled point per input point
    assert len(points_rescaled) == 4


def test_scale_features_bad_input():
    """Test for PlantCV."""
    mask = np.array([])
    result = scale_features(mask=mask, points=PLANT_POINTS, line_position=50)
    assert np.array_equal(np.unique(result), np.array(["NA"]))
