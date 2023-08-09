"""Tests for pcv.plot_image."""
import pytest
import cv2
from matplotlib import pyplot as plt
from plantcv.plantcv import PSII_data
from plantcv.plantcv import plot_image


def test_plot_image_rgb(test_data):
    """Test for PlantCV."""
    img = cv2.imread(test_data.small_rgb_img)
    plot_image(img=img)
    assert True


@pytest.mark.parametrize("cmap", [None, "viridis"])
def test_plot_image_gray(cmap, test_data):
    """Test for PlantCV."""
    gray_img = cv2.imread(test_data.small_gray_img, -1)
    plot_image(img=gray_img, cmap=cmap)


def test_plot_image_matplotlib():
    """Test for PlantCV."""
    fig = plt.figure()
    with pytest.raises(RuntimeError):
        plot_image(fig)


def test_plot_image_bad_type():
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        plot_image(img=[])


def test_plot_image_psiidata():
    """Test for PlantCV."""
    psii = PSII_data()
    with pytest.raises(RuntimeError):
        plot_image(psii)


def test_plantcv_plot_image_dataarray(test_data):
    """Test for PlantCV."""
    plot_image(test_data.psii_cropreporter('ojip_dark').squeeze('measurement', drop=True), col='frame_label')
    # Assert that the image was plotted without error
    assert True
