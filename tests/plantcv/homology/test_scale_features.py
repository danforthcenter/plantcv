import pytest
import cv2
import numpy as np
from plantcv.plantcv.homology import scale_features


@pytest.mark.parametrize("pos", ["NA", 50])
def test_scale_features(pos, test_data):
    """Test for PlantCV."""
    # Read in test data
    mask = cv2.imread(test_data.small_bin_img, -1)
    points_rescaled, _, _ = scale_features(mask=mask, points=test_data.acute_results, line_position=pos)
    assert len(points_rescaled) == 23


def test_scale_features_bad_input(test_data):
    """Test for PlantCV."""
    mask = np.array([])
    result = scale_features(mask=mask, points=test_data.acute_results, line_position=50)
    assert np.array_equal(np.unique(result), np.array(["NA"]))
