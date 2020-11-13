import pytest
import cv2
import numpy as np
from plantcv.plantcv import acute_vertex, params, outputs


@pytest.mark.parametrize("debug", ["print", "plot", None])
def test_plantcv_acute_vertex(test_data, tmpdir, debug):
    # Test cache directory
    tmp_dir = tmpdir.mkdir("sub")
    # Set the output directory
    params.debug_outdir = str(tmp_dir)
    params.debug = debug
    # Read in test data
    img = cv2.imread(test_data["setaria_small_vis"])
    obj_contour = test_data["setaria_small_mask_contours"]
    acute = acute_vertex(obj=obj_contour, win=5, thresh=15, sep=5, img=img)
    outputs.clear()
    assert all([i == j] for i, j in zip(np.shape(acute), np.shape(test_data["acute_vertex_result"])))


@pytest.mark.parametrize("obj,win,thresh,sep", [([], 5, 15, 5), ([], 0.01, 0.01, 1)])
def test_plantcv_acute_vertex_small_contours(test_data, obj, win, thresh, sep):
    # Read in test data
    img = cv2.imread(test_data["setaria_small_vis"])
    acute = acute_vertex(obj=obj, win=win, thresh=thresh, sep=sep, img=img)
    outputs.clear()
    assert all([i == j] for i, j in zip(np.shape(acute), np.shape(test_data["acute_vertex_result"])))


def test_plantcv_acute_vertex_bad_obj(test_data):
    img = cv2.imread(test_data["setaria_small_vis"])
    obj_contour = np.array([])
    result = acute_vertex(obj=obj_contour, win=5, thresh=15, sep=5, img=img)
    outputs.clear()
    assert all([i == j] for i, j in zip(result, [0, ("NA", "NA")]))
