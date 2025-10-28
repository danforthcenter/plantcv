from plantcv.plantcv import params, deprecation_warning


def test_deprecation_warning():
    """Test for PlantCV."""
    # Verify that the fatal_error function raises a RuntimeError
    params.verbose = 2
    deprecation_warning("This is just a test, and it's just a warning")
    assert True
