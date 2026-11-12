import numpy as np
from altair import Chart
from plantcv.plantcv.qc.quick_color_check import quick_color_check
from plantcv.plantcv.transform.standard_matrices import std_color_matrix
from tests import synthetic


def test_quick_color_check():
    """Test for PlantCV."""
    target_matrix = std_color_matrix(pos=3)
    source_matrix = synthetic.color_cast_matrix(target_matrix)
    chart = quick_color_check(source_matrix, target_matrix, num_chips=10)
    assert isinstance(chart, Chart)


def test_quick_color_check_no_num_chips():
    """Test for PlantCV."""
    target_matrix = std_color_matrix(pos=3)
    source_matrix = synthetic.color_cast_matrix(target_matrix)
    chart = quick_color_check(source_matrix, target_matrix)
    assert isinstance(chart, Chart)


def test_quick_color_check_no_target():
    """Test for PlantCV."""
    # 24 chips: the target is the standard ColorChecker
    source_matrix = synthetic.color_cast_matrix(std_color_matrix(pos=3))
    chart = quick_color_check(source_matrix)
    assert isinstance(chart, Chart)


def test_quick_color_check_no_target_astro():
    """Test for PlantCV."""
    # Load target image
    mat = np.random.randint(0, 255, (15, 3))
    index = np.arange(mat.shape[0])
    source_matrix = np.c_[index, mat]
    chart = quick_color_check(source_matrix)
    assert isinstance(chart, Chart)
