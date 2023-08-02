import pytest
import cv2
from plotnine import ggplot
from plantcv.plantcv.visualize import obj_size_ecdf


@pytest.mark.parametrize("title", ["Include Title", None])
def test_obj_size_ecdf(title, visualize_test_data):
    """Test for PlantCV."""
    mask = cv2.imread(visualize_test_data.small_bin_img, -1)
    fig_ecdf = obj_size_ecdf(mask=mask, title=title)
    assert isinstance(fig_ecdf, ggplot)
