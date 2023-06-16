import pytest
import numpy as np
from plantcv.plantcv import outputs
from plantcv.plantcv.homology import landmark_reference_pt_dist


@pytest.mark.parametrize("points,centroid,bline", [
    [[(10, 1000)], (10, 10), (10, 10)],
    [[], (0, 0), (0, 0)],
    [[(0.0139, 0.2569), (0.2361, 0.2917), (0.3542, 0.3819), (0.3542, 0.4167), (0.375, 0.4236), (0.7431, 0.3681),
      (0.8958, 0.3542), (0.9931, 0.3125), (0.1667, 0.5139), (0.4583, 0.8889), (0.4931, 0.5903), (0.3889, 0.5694),
      (0.4792, 0.4306), (0.2083, 0.5417), (0.3194, 0.5278), (0.3889, 0.375), (0.3681, 0.3472), (0.2361, 0.0139),
      (0.5417, 0.2292), (0.7708, 0.3472), (0.6458, 0.3472), (0.6389, 0.5208), (0.6458, 0.625)], (0.4685, 0.4945),
     (0.4685, 0.2569)]
])
def test_landmark_reference_pt_dist(points, centroid, bline):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    landmark_reference_pt_dist(points_r=points, centroid_r=centroid, bline_r=bline)
    assert len(outputs.observations['default'].keys()) == 8


def test_landmark_reference_pt_dist_bad_centroid():
    """Test for PlantCV."""
    result = landmark_reference_pt_dist(points_r=[], centroid_r=('a', 'b'), bline_r=(0, 0))
    assert np.array_equal(np.unique(result), np.array(["NA"]))
