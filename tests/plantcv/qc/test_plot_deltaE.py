import os
import cv2
import numpy as np
from plantcv.plantcv._globals import outputs
from plantcv.plantcv.qc import plot_deltaE
import altair.vegalite.v5.api as alt


def test_plot_deltaE_macbeth():
    """Test for PlantCV"""
    de_mat = np.array(
        [[11.64761218, 78.27646683, 25.84812195, 0],
         [9.13727445, 53.453794, 46.75456717, 1.69993386],
         [10.24720418, 25.34728848, 58.35893906, 40.86886883],
         [35.7394108, 13.90053859, 57.72055646, 69.18880135],
         [72.58465134, 20.24932197, 20.4335013, 55.23924463],
         [73.52994424, 39.50763664, 29.62213005, 47.82905849]]
    )
    p = plot_deltaE(de_mat)
    assert isinstance(p, alt.LayerChart)


def test_plot_deltaE_astro():
    """Test for PlantCV"""
    de_mat = np.array(
        [[11.64761218, 25.84812195, 0],
         [9.13727445, 46.75456717, 1.69993386],
         [10.24720418, 58.35893906, 40.86886883],
         [72.58465134, 20.4335013, 55.23924463],
         [73.52994424, 29.62213005, 47.82905849]]
    )
    p = plot_deltaE(de_mat)
    assert isinstance(p, alt.LayerChart)


def test_plot_deltaE_file_list(qc_test_data):
    """Test for PlantCV"""
    outputs.clear()
    path = qc_test_data.cc_img
    p = plot_deltaE([path])
    assert isinstance(p, alt.LayerChart)


def test_plot_deltaE_astro_list(qc_test_data):
    """Test for PlantCV"""
    outputs.clear()
    path = qc_test_data.astrocard_img
    p = plot_deltaE([path], color_chip_size="astro")
    assert isinstance(p, alt.LayerChart)


def test_plot_deltaE_filepath(qc_test_data, tmpdir):
    """Test for PlantCV"""
    img = cv2.imread(qc_test_data.cc_img)
    cache_dir = tmpdir.mkdir("cache")
    # create a random image and write it to the temp directory
    path_to_img = os.path.join(cache_dir, 'tmp_img.png')
    cv2.imwrite(path_to_img, img)
    p = plot_deltaE(str(cache_dir))
    assert isinstance(p, alt.LayerChart)
    
