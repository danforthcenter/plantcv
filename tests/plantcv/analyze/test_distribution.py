# Tests for pcv.analyze.distribution
import cv2
from plantcv.plantcv import outputs
from plantcv.plantcv.analyze import distribution as analyze_distribution


def test_distribution(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Read in test data
    mask = cv2.imread(test_data.small_bin_fill, -1)

    _ = analyze_distribution(labeled_mask=mask, n_labels=1, direction="across", hist_range="relative")
    print(outputs.observations)
    assert int(outputs.observations['default_1']['x_distribution_mean']['value']) == 130
