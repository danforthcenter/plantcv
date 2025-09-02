from plantcv.plantcv import warn


def test_warn():
    """Test for PlantCV."""
    warn("This is a warning message.")
    assert True
