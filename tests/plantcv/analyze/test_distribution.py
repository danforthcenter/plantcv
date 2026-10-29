# Tests for pcv.analyze.distribution
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
