# Tests for pcv.analyze.distribution
import pytest
import numpy as np
from plantcv.plantcv import outputs
from plantcv.plantcv.analyze import distribution as analyze_distribution
from tests import synthetic


def test_distribution():
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    mask = synthetic.plant_mask(small_object=False)

    _ = analyze_distribution(labeled_mask=mask, n_labels=1, direction="across", bin_size=10, hist_range="relative")
    # Plant cropped to columns 30:90 gives 10 px bins starting at 0, 10, ..., 50 with counts
    # 100, 100, 200, 200, 100, 100: (0 + 1000 + 4000 + 6000 + 4000 + 5000) / 800 = 25
    assert outputs.observations['default_1']['x_distribution_mean']['value'] == 25.0


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
