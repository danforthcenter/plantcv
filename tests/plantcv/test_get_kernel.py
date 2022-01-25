import pytest
import numpy as np
from plantcv.plantcv import get_kernel


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
