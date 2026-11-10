"""Tests for pcv.plot_image."""
import pytest
import altair as alt
import pandas as pd
from matplotlib import pyplot as plt
from plantcv.plantcv import PSII_data
from plantcv.plantcv import plot_image
from tests import synthetic


def test_plot_image_rgb(synthetic_rgb):
    """Test for PlantCV."""
    plot_image(img=synthetic_rgb)
    assert True


@pytest.mark.parametrize("cmap", [None, "viridis"])
def test_plot_image_gray(cmap, synthetic_gray):
    """Test for PlantCV."""
    plot_image(img=synthetic_gray, cmap=cmap)


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


def test_plantcv_plot_image_dataarray():
    """Test for PlantCV."""
    plot_image(synthetic.psii_dataarray('ojip_dark').squeeze('measurement', drop=True), col='frame_label')
    # Assert that the image was plotted without error
    assert True


def test_plantcv_plot_image_altair():
    """Test for PlantCV."""
    data = pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [5, 4, 3, 2, 1]
    })

    # Create Altair chart
    chart = alt.Chart(data).mark_point().encode(
        x='x',
        y='y'
    )
    plot_image(chart)
    # Assert that the image was plotted without error
    assert True
