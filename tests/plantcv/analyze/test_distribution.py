# Tests for pcv.analyze.distribution
import cv2
import numpy as np
import pytest
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


def test_distribution_bin_size_larger_than_relative_extent():
    """A bin_size larger than the object extent raises a clear error instead of IndexError."""
    mask = np.zeros((100, 120), np.uint8)
    mask[40:60, 40:80] = 255

    with pytest.raises(RuntimeError, match="bin_size"):
        analyze_distribution(labeled_mask=mask, n_labels=1, direction="across", hist_range="relative")


def test_distribution_bin_size_larger_than_absolute_extent():
    """A bin_size larger than the image extent raises a clear error instead of IndexError."""
    mask = np.zeros((50, 120), np.uint8)
    mask[10:40, 40:80] = 255

    with pytest.raises(RuntimeError, match="bin_size"):
        analyze_distribution(labeled_mask=mask, n_labels=1, bin_size=100, direction="down",
                             hist_range="absolute")
