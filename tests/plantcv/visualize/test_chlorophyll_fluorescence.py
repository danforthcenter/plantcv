import pytest
from plantcv.plantcv.visualize import chlorophyll_fluorescence
from plantcv.plantcv import PSII_data
from altair.vegalite.v5.api import LayerChart
from tests import synthetic


def test_chlorophyll_fluorescence():
    """Test for PlantCV."""
    da = synthetic.psii_dataarray('ojip_dark')
    mask = synthetic.psii_mask()
    chart = chlorophyll_fluorescence(ps_da=da, labeled_mask=mask)
    assert isinstance(chart, LayerChart)


def test_chlorophyll_fluorescence_bad_var():
    """Test for PlantCV."""
    da = synthetic.psii_dataarray('ojip_dark')
    da.name = 'bad'
    mask = synthetic.psii_mask()
    with pytest.raises(RuntimeError):
        _ = chlorophyll_fluorescence(ps_da=da, labeled_mask=mask)


def test_chlorophyll_fluorescence_invalid_array():
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _ = chlorophyll_fluorescence(ps_da='string', labeled_mask=synthetic.psii_mask())


def test_reassign_frame_labels_invalid_class():
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _ = chlorophyll_fluorescence(ps_da=PSII_data(), labeled_mask=synthetic.psii_mask())
