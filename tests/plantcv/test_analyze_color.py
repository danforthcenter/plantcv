import pytest
import cv2
from plantcv.plantcv import analyze_color, outputs


@pytest.mark.parametrize("colorspace", ["all", "lab", "hsv", "rgb"])
def test_analyze_color(colorspace, test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    mask = cv2.imread(test_data.small_bin_img, -1)
    _ = analyze_color(rgb_img=img, mask=mask, colorspaces=colorspace)
    assert outputs.observations['default']['hue_median']['value'] == 80.0


def test_analyze_color_bad_imgtype(test_data):
    """Test for PlantCV."""
    img_binary = cv2.imread(test_data.small_bin_img, -1)
    mask = cv2.imread(test_data.small_bin_img, -1)
    with pytest.raises(RuntimeError):
        _ = analyze_color(rgb_img=img_binary, mask=mask, hist_plot_type=None)


def test_analyze_color_bad_hist_type(test_data):
    """Test for PlantCV."""
    img = cv2.imread(test_data.small_rgb_img)
    mask = cv2.imread(test_data.small_bin_img, -1)
    with pytest.raises(RuntimeError):
        # TODO: change hist_plot_type to colorspaces after deprecation
        _ = analyze_color(rgb_img=img, mask=mask, hist_plot_type='bgr')
