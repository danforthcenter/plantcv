import cv2
import pytest
from plantcv.plantcv._helpers import _logical_operation


def test_logical_operation_bad_type(test_data):
    """Test for PlantCV."""
    mask = cv2.imread(test_data.small_bin_img, -1)
    with pytest.raises(RuntimeError):
        _ = _logical_operation(bin_img1=mask, bin_img2=mask, operation="invalid")
