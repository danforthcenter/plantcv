import pytest
from plantcv.plantcv.visualize import chlorophyll_fluorescence
from plantcv.plantcv import PSII_data
from altair.vegalite.v5.api import LayerChart


def test_chlorophyll_fluorescence(test_data):
    """Test for PlantCV."""
    da = test_data.psii_cropreporter('ojip_dark')
    mask = test_data.create_ps_mask()
    chart = chlorophyll_fluorescence(ps_da=da, labeled_mask=mask)
    assert isinstance(chart, LayerChart)


def test_chlorophyll_fluorescence_bad_var(test_data):
    """Test for PlantCV."""
    da = test_data.psii_cropreporter('ojip_dark')
    da.name = 'bad'
    mask = test_data.create_ps_mask()
    with pytest.raises(RuntimeError):
        _ = chlorophyll_fluorescence(ps_da=da, labeled_mask=mask)


def test_chlorophyll_fluorescence_invalid_array(test_data):
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _ = chlorophyll_fluorescence(ps_da='string', labeled_mask=test_data.create_ps_mask())


def test_reassign_frame_labels_invalid_class(test_data):
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _ = chlorophyll_fluorescence(ps_da=PSII_data(), labeled_mask=test_data.create_ps_mask())
