from plantcv.plantcv import outputs
from plantcv.plantcv.morphology.check_cycles import check_cycles
from tests import synthetic


def test_check_cycles():
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    _ = check_cycles(synthetic.skeleton(cycle=True))
    # The square outline encloses one cycle
    assert outputs.observations['default']['num_cycles']['value'] == 1


def test_check_cycles_none():
    """Test for PlantCV."""
    outputs.clear()
    _ = check_cycles(synthetic.skeleton())
    # The plant skeleton is a tree
    assert outputs.observations['default']['num_cycles']['value'] == 0
