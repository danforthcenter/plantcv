import pytest
import numpy as np
from plantcv.plantcv import outputs
from plantcv.plantcv.analyze import color as analyze_color


@pytest.mark.parametrize("colorspace", ["all", "lab", "hsv", "rgb"])
def test_color(colorspace, synthetic_rgb, synthetic_mask):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    _ = analyze_color(rgb_img=synthetic_rgb, labeled_mask=synthetic_mask, n_labels=1, colorspaces=colorspace)
    # Foreground BGR (0, 128, 0) is OpenCV hue 60, reported in degrees as 60 * 2
    assert outputs.observations['default_1']['hue_median']['value'] == 120.0


def test_color_multiple_objects(synthetic_rgb, synthetic_mask):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Split the plant into two labeled objects
    labeled_mask = np.zeros(synthetic_mask.shape, dtype=np.int32)
    labeled_mask[:, :60][synthetic_mask[:, :60] > 0] = 1
    labeled_mask[:, 60:][synthetic_mask[:, 60:] > 0] = 2
    _ = analyze_color(rgb_img=synthetic_rgb, labeled_mask=labeled_mask, n_labels=2, colorspaces="all",
                      label=["a", "b"])
    assert list(outputs.observations.keys()) == ["a_1", "b_2"]
    for sample in ("a_1", "b_2"):
        assert sum(outputs.observations[sample]['blue_frequencies']['value']) == pytest.approx(100)


def test_color_bad_imgtype(synthetic_mask):
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _ = analyze_color(rgb_img=synthetic_mask, labeled_mask=synthetic_mask, n_labels=1)


def test_color_bad_hist_type(synthetic_rgb, synthetic_mask):
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _ = analyze_color(rgb_img=synthetic_rgb, labeled_mask=synthetic_mask, n_labels=1, colorspaces='bgr')
