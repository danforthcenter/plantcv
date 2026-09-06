import pytest
import numpy as np
from plantcv.plantcv.get_kernel import get_kernel, _format_kernel


def test_get_kernel_cross():
    """Test for PlantCV."""
    kernel = get_kernel(size=(3, 3), shape="cross")
    assert (kernel == np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])).all()


def test_get_kernel_rectangle():
    """Test for PlantCV."""
    kernel = get_kernel(size=(3, 3), shape="rectangle")
    assert (kernel == np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])).all()


def test_get_kernel_ellipse():
    """Test for PlantCV."""
    kernel = get_kernel(size=(3, 3), shape="ellipse")
    assert (kernel == np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])).all()


def test_get_kernel_bad_input_size():
    """Test for PlantCV."""
    with pytest.raises(ValueError):
        _ = get_kernel(size=(1, 1), shape="ellipse")


def test_get_kernel_bad_input_shape():
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _ = get_kernel(size=(3, 1), shape="square")


@pytest.mark.parametrize("k, to", [[3, int],
                                   [(3, 3), int],
                                   [np.ones((3, 3)), int],
                                   [3, tuple],
                                   [(3, 3), tuple],
                                   [np.ones((3, 3)), tuple],
                                   [3, np.ndarray],
                                   [(3, 3), np.ndarray],
                                   [np.ones((3, 3)), np.ndarray]
                                   ])
def test_format_kernel(k, to):
    """Test for PlantCV."""
    kern = _format_kernel(k, to)
    assert isinstance(kern, to)
