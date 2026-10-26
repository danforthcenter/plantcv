import numpy as np
from plantcv.plantcv._helpers import _object_composition
from tests import synthetic


def test_object_composition(synthetic_mask):
    """Test for PlantCV."""
    cnt, cnt_str = synthetic.find_contours(synthetic_mask)
    contours = _object_composition(contours=cnt, hierarchy=cnt_str)
    # The plant and small object are both outer contours, so both are stacked
    expected = np.vstack(cnt)
    assert np.array_equal(expected, contours)


def test_object_composition_nested():
    """Test for PlantCV."""
    # Create test data
    cnt = [np.array([[[25, 25]], [[25, 49]], [[49, 49]], [[49, 25]]], dtype=np.int32),
           np.array([[[34, 35]], [[35, 34]], [[39, 34]], [[40, 35]], [[40, 39]], [[39, 40]], [[35, 40]], [[34, 39]]],
                    dtype=np.int32)]
    cnt_str = np.array([[[-1, -1,  1, -1], [-1, -1, -1,  0]]], dtype=np.int32)
    contours = _object_composition(contours=cnt, hierarchy=cnt_str)
    assert contours is not None
