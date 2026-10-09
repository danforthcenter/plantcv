"""Tests for the open_url function."""
import numpy as np
import imageio.v3 as iio
import pytest
from plantcv.plantcv.io import open_url


def test_open_url(monkeypatch):
    """PlantCV Test"""
    url = ("https://datasci.danforthcenter.org/test.jpg")
    monkeypatch.setattr(iio, "imread", lambda *args, **kwargs: np.zeros((2464, 3280, 3)).astype(np.float32))
    rgb_img = open_url(url=url)
    assert rgb_img.shape == (2464, 3280, 3)


def test_open_url_unsupported(monkeypatch):
    """PlantCV Test"""
    url = "https://datasci.danforthcenter.org/test.gif"
    monkeypatch.setattr(iio, "imread", lambda *args, **kwargs: np.zeros((2464)).astype(np.float32))
    with pytest.raises(RuntimeError):
        _ = open_url(url=url)
