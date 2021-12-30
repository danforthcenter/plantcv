import pytest
import cv2
from matplotlib import pyplot as plt
import pandas as pd
from plotnine import ggplot
from plantcv.plantcv import plot_image


def test_plot_rgb(test_data):
    img = cv2.imread(test_data.small_rgb_img)
    plot_image(img=img)
    assert True


@pytest.mark.parametrize("cmap", [None, "viridis"])
def test_plot_gray(cmap, test_data):
    gray_img = cv2.imread(test_data.small_gray_img, -1)
    plot_image(img=gray_img, cmap=cmap)


def test_plot_matplotlib():
    fig = plt.figure()
    with pytest.raises(RuntimeError):
        plot_image(fig)


def test_plot_plotnine():
    dataset = pd.DataFrame({'x': [1, 2, 3, 4], 'y': [1, 2, 3, 4]})
    img = ggplot(data=dataset)
    plot_image(img=img)
    # Assert that the image was plotted without error
    assert True
