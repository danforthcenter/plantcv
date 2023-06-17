import cv2
from plantcv.plantcv._helpers import _iterate_analysis


def test_iterate_analysis(test_data):
    """Test for PlantCV."""
    mask = cv2.imread(test_data.small_bin_img, -1)
    img = _iterate_analysis(img=mask, labeled_mask=mask, n_labels=1, label="test", function=analysis_test_func)
    assert img.shape == mask.shape


def analysis_test_func(img, mask, label):
    """Test analysis function."""
    if mask is not None and label is not None:
        return img
