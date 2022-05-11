import pytest
from plantcv.plantcv import fatal_error


def test_fatal_error():
    """Test for PlantCV."""
    # Verify that the fatal_error function raises a RuntimeError
    with pytest.raises(RuntimeError):
        fatal_error("Test error")
