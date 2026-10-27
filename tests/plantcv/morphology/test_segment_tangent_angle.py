import pytest
from plantcv.plantcv import outputs
from plantcv.plantcv.morphology.segment_tangent_angle import segment_tangent_angle
from tests import synthetic


@pytest.mark.parametrize("size,expected", [
    # Straight leaves have parallel ends (180 degrees). The right leaf's ends are horizontal and vertical.
    [3, [180, 90, 180, 180]],
    # The 28-pixel leaves are pruned away completely. A 19-pixel leaf keeps its middle pixel, which has
    # no neighbor left to make it a tip, so both of its ends remain.
    [100, ["NA", "NA", 180, 180]]])
def test_segment_tangent_angle(size, expected):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    leaves, _ = synthetic.skeleton_segments()
    _ = segment_tangent_angle(segmented_img=synthetic.skeleton(), objects=leaves, size=size)
    assert outputs.observations['default']['segment_tangent_angle']['value'] == pytest.approx(expected)
