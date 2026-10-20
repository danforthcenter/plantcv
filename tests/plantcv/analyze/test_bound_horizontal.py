import pytest
import cv2
import numpy as np
from plantcv.plantcv import outputs
from plantcv.plantcv.analyze import bound_horizontal as analyze_bound_horizontal
from plantcv.plantcv.analyze.bound_horizontal import _boundary_img_annotation


@pytest.mark.parametrize('pos,exp', [[200, 58], [-1, 0], [100, 0], [150, 11]])
def test_analyze_bound_horizontal(pos, exp, test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    mask = cv2.imread(test_data.small_bin_img, -1)
    _ = analyze_bound_horizontal(img=img, labeled_mask=mask, simplify=True,
                                 n_labels=1, line_position=pos)
    assert outputs.observations["default_1"]["height_above_reference"]["value"] == exp
    assert outputs.observations["default_1"]["area_above_reference"]["label"] == "pixels"
    assert outputs.observations["default_1"]["area_below_reference"]["label"] == "pixels"


def test_analyze_bound_horizontal_grayscale_image(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_gray_img, -1)
    mask = cv2.imread(test_data.small_bin_img, -1)
    boundary_img = analyze_bound_horizontal(img=img, labeled_mask=mask, simplify=False,
                                            n_labels=1, line_position=200)
    assert len(boundary_img.shape) == 2


def test_analyze_bound_horizontal_simplify_labels(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    mask = cv2.imread(test_data.small_bin_img, -1)
    labeled = analyze_bound_horizontal(img=img, labeled_mask=mask, simplify=True,
                                       n_labels=1, line_position=150, label="prefix")
    # Simplified output is 1 above the line and 2 below
    assert np.array_equal(np.unique(labeled), [0, 1, 2])
    assert np.count_nonzero(labeled) == np.count_nonzero(mask)
    assert "prefix_1" in outputs.observations


@pytest.mark.parametrize("axis", [0, 1])
def test_boundary_img_annotation_simplify_colors(axis):
    """Test for PlantCV."""
    # Two objects on either side of the line plus one straddling it
    mask = np.zeros((50, 100), dtype=np.int32)
    mask[5:15, 5:20] = 1
    mask[35:45, 60:80] = 2
    mask[20:30, 40:60] = 3
    img = np.zeros((50, 100, 3), dtype=np.uint8)
    out_img, out_mask = _boundary_img_annotation(img, mask, [25, 50][axis], axis, simplify=True)
    colors = {tuple(c) for c in out_img.reshape(-1, 3)}
    # Both sides of the boundary are painted
    assert (255, 0, 255) in colors
    assert (0, 255, 0) in colors
    assert np.array_equal(np.unique(out_mask), [0, 1, 2])
