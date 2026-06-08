import numpy as np
from altair.vegalite.v5.api import Chart
from plantcv.plantcv.qc.quick_color_check import quick_color_check


def test_quick_color_check(qc_test_data):
    """Test for PlantCV."""
    # Load target image
    target_matrix = qc_test_data.load_npz(qc_test_data.target_matrix_file)
    source_matrix = qc_test_data.load_npz(qc_test_data.source1_matrix_file)
    chart = quick_color_check(source_matrix, target_matrix, num_chips=10)
    assert isinstance(chart, Chart)


def test_quick_color_check_no_num_chips(qc_test_data):
    """Test for PlantCV."""
    # Load target image
    target_matrix = qc_test_data.load_npz(qc_test_data.target_matrix_file)
    source_matrix = qc_test_data.load_npz(qc_test_data.source1_matrix_file)
    chart = quick_color_check(source_matrix, target_matrix)
    assert isinstance(chart, Chart)


def test_quick_color_check_no_target(qc_test_data):
    """Test for PlantCV."""
    # Load target image
    source_matrix = qc_test_data.load_npz(qc_test_data.source1_matrix_file)
    chart = quick_color_check(source_matrix)
    assert isinstance(chart, Chart)


def test_quick_color_check_no_target_astro(qc_test_data):
    """Test for PlantCV."""
    # Load target image
    mat = np.random.randint(0, 255, (15, 3))
    index = np.arange(mat.shape[0])
    source_matrix = np.c_[index, mat]
    chart = quick_color_check(source_matrix)
    assert isinstance(chart, Chart)
