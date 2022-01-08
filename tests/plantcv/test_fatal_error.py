import pytest
from plantcv.plantcv import fatal_error


def test_plantcv_fatal_error():
    # Verify that the fatal_error function raises a RuntimeError
    with pytest.raises(RuntimeError):
        fatal_error("Test error")
