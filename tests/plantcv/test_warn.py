from plantcv.plantcv import warn


def test_warn():
    """Test for PlantCV."""
    val = warn("This is a warning message.")
    assert val is None
