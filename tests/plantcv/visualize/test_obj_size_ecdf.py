"""Tests for pcv.visualize.obj_size_ecdf."""
import cv2
from altair.vegalite.v5.api import Chart
from plantcv.plantcv.visualize import obj_size_ecdf


def test_obj_size_ecdf(visualize_test_data):
    """Test for PlantCV."""
    mask = cv2.imread(visualize_test_data.small_bin_img, -1)
    fig_ecdf = obj_size_ecdf(mask=mask)
    assert isinstance(fig_ecdf, Chart)
