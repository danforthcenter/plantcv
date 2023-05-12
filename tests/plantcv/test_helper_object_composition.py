import numpy as np
from plantcv.plantcv._helpers import _object_composition


def test_object_composition(test_data):
    """Test for PlantCV."""
    # Read in test data
    cnt, cnt_str = test_data.load_contours(test_data.small_contours_file)
    contours = _object_composition(contours=cnt, hierarchy=cnt_str)
    expected = test_data.load_composed_contours(test_data.small_composed_contours_file)
    assert np.all(expected) == np.all(contours)


def test_object_composition_nested():
    """Test for PlantCV."""
    # Create test data
    cnt = [np.array([[[25, 25]], [[25, 49]], [[49, 49]], [[49, 25]]], dtype=np.int32),
           np.array([[[34, 35]], [[35, 34]], [[39, 34]], [[40, 35]], [[40, 39]], [[39, 40]], [[35, 40]], [[34, 39]]],
                    dtype=np.int32)]
    cnt_str = np.array([[[-1, -1,  1, -1], [-1, -1, -1,  0]]], dtype=np.int32)
    contours = _object_composition(contours=cnt, hierarchy=cnt_str)
    assert contours is not None
