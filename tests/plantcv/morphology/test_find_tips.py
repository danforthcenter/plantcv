from plantcv.plantcv import outputs
from plantcv.plantcv.morphology.find_tips import find_tips
from tests import synthetic


def test_find_tips():
    """Test for PlantCV."""
    outputs.clear()
    _ = find_tips(skel_img=synthetic.skeleton(), mask=synthetic.skeleton_mask())
    assert sorted(outputs.observations["default"]["tips"]["value"]) == sorted(synthetic.SKELETON_TIPS)


def test_find_tips_no_mask():
    """Test for PlantCV."""
    outputs.clear()
    _ = find_tips(skel_img=synthetic.skeleton())
    assert sorted(outputs.observations["default"]["tips"]["value"]) == sorted(synthetic.SKELETON_TIPS)
