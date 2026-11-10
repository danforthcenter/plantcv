import pytest
from plantcv.plantcv import outputs
from plantcv.plantcv.analyze import bound_vertical as analyze_bound_vertical


# Foreground spans columns 10:90: a line past the image edge (200) gives the full 80 px width, a line
# crossing the left leaf (40) gives columns 10-39 (30 px), and a line at the left edge (1) gives 0
@pytest.mark.parametrize('pos,exp', [[40, 30], [200, 80], [1, 0]])
def test_bound_vertical(pos, exp, synthetic_rgb, synthetic_mask):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    _ = analyze_bound_vertical(img=synthetic_rgb, labeled_mask=synthetic_mask, n_labels=1, line_position=pos)
    assert outputs.observations['default_1']['width_left_reference']['value'] == exp
    assert outputs.observations['default_1']['area_left_reference']['label'] == "pixels"
    assert outputs.observations['default_1']['area_right_reference']['label'] == "pixels"


def test_bound_vertical_grayscale_image(synthetic_gray, synthetic_mask):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    _ = analyze_bound_vertical(img=synthetic_gray, labeled_mask=synthetic_mask, n_labels=1, line_position=60)
    # Line crosses the stem: columns 10-59 (50 px) are left of it
    assert outputs.observations['default_1']['width_left_reference']['value'] == 50
