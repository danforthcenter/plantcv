from altair.vegalite.v5.api import Chart
from plantcv.plantcv.qc.quick_color_check import quick_color_check


def test_quick_color_check(qc_test_data):
    """Test for PlantCV."""
    # Load target image
    target_matrix = qc_test_data.load_npz(qc_test_data.target_matrix_file)
    source_matrix = qc_test_data.load_npz(qc_test_data.source1_matrix_file)
    chart = quick_color_check(target_matrix, source_matrix, num_chips=22)
    assert isinstance(chart, Chart)
