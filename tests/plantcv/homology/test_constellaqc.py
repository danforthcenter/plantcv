import pytest
from plantcv.plantcv import params
from plantcv.plantcv.homology import constellaqc


@pytest.mark.parametrize("debug", ["plot", None])
def test_plantcv_homology_constellaqc(debug, homology_test_data):
    """Test for PlantCV."""
    # Set debug
    params.debug = debug
    plms = homology_test_data.read_df(homology_test_data.plms_landmarks)
    annotations = homology_test_data.read_df(homology_test_data.plms_annotated)
    constellaqc(denovo_groups=plms, annotated_groups=annotations)
    assert True
