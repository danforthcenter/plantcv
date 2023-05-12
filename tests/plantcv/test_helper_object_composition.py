import numpy as np
from plantcv.plantcv._helpers import _object_composition


def test_object_composition(test_data):
    """Test for PlantCV."""
    # Read in test data
    cnt, cnt_str = test_data.load_contours(test_data.small_contours_file)
    contours = _object_composition(contours=cnt, hierarchy=cnt_str)
    expected = test_data.load_composed_contours(test_data.small_composed_contours_file)
    assert np.all(expected) == np.all(contours)

