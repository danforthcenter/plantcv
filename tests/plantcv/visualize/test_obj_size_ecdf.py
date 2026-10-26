"""Tests for pcv.visualize.obj_size_ecdf."""
from altair.vegalite.v5.api import Chart
from plantcv.plantcv.visualize import obj_size_ecdf


def test_obj_size_ecdf(synthetic_mask):
    """Test for PlantCV."""
    mask = synthetic_mask
    fig_ecdf = obj_size_ecdf(mask=mask)
    assert isinstance(fig_ecdf, Chart)
