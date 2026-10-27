import pytest
from plantcv.plantcv._helpers import _iterate_analysis


def test_iterate_analysis(synthetic_mask):
    """Test for PlantCV."""
    mask = synthetic_mask
    img = _iterate_analysis(img=mask, labeled_mask=mask, n_labels=1, label="test", function=analysis_test_func)
    assert img.shape == mask.shape


def test_iterate_analysis_wrong_num_labels(synthetic_mask):
    """Test for PlantCV."""
    mask = synthetic_mask
    with pytest.raises(RuntimeError):
        _ = _iterate_analysis(img=mask, labeled_mask=mask, n_labels=1, label=["test", "test"], function=analysis_test_func)


def analysis_test_func(**kwargs):
    """Test analysis function."""
    return kwargs["img"]
