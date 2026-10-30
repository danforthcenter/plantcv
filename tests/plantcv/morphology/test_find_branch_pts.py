from plantcv.plantcv import outputs
from plantcv.plantcv.morphology.find_branch_pts import find_branch_pts
from tests import synthetic


def test_find_branch_pts():
    """Test for PlantCV."""
    outputs.clear()
    _ = find_branch_pts(skel_img=synthetic.skeleton(), mask=synthetic.skeleton_mask())
    assert sorted(outputs.observations["default"]["branch_pts"]["value"]) == sorted(synthetic.SKELETON_BRANCH_PTS)


def test_find_branch_pts_no_mask():
    """Test for PlantCV."""
    outputs.clear()
    _ = find_branch_pts(skel_img=synthetic.skeleton())
    assert sorted(outputs.observations["default"]["branch_pts"]["value"]) == sorted(synthetic.SKELETON_BRANCH_PTS)
