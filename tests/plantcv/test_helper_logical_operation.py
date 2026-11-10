import pytest
from plantcv.plantcv._helpers import _logical_operation


def test_logical_operation_bad_type(synthetic_mask):
    """Test for PlantCV."""
    mask = synthetic_mask
    with pytest.raises(RuntimeError):
        _ = _logical_operation(bin_img1=mask, bin_img2=mask, operation="invalid")
