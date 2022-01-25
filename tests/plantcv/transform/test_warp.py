import pytest
import numpy as np
from plantcv.plantcv.transform import warp, warp_align


def test_warp_default(transform_test_data):
    """Test for PlantCV."""
    img = transform_test_data.create_test_img((12, 10, 3))
    refimg = transform_test_data.create_test_img((12, 10, 3))
    pts = [(0, 0), (1, 0), (0, 3), (4, 4)]
    refpts = [(0, 0), (1, 0), (0, 3), (4, 4)]
    _, mat = warp(img, refimg, pts, refpts, method="default")
    assert mat.shape == (3, 3)


def test_warp_lmeds(transform_test_data):
    """Test for PlantCV."""
    img = transform_test_data.create_test_img((10, 10, 3))
    refimg = transform_test_data.create_test_img((11, 11))
    pts = [(0, 0), (1, 0), (0, 3), (4, 4)]
    refpts = [(0, 0), (1, 0), (0, 3), (4, 4)]
    _, mat = warp(img, refimg, pts, refpts, method="lmeds")
    assert mat.shape == (3, 3)


def test_warp_rho(transform_test_data):
    """Test for PlantCV."""
    img = transform_test_data.create_test_img_bin((10, 10))
    refimg = transform_test_data.create_test_img((11, 11))
    pts = [(0, 0), (1, 0), (0, 3), (4, 4)]
    refpts = [(0, 0), (1, 0), (0, 3), (4, 4)]
    _, mat = warp(img, refimg, pts, refpts, method="rho")
    assert mat.shape == (3, 3)


def test_warp_ransac(transform_test_data):
    """Test for PlantCV."""
    img = transform_test_data.create_test_img((100, 150))
    refimg = transform_test_data.create_test_img((10, 15))
    pts = [(0, 0), (149, 0), (99, 149), (0, 99), (3, 3)]
    refpts = [(0, 0), (0, 14), (9, 14), (0, 9), (3, 3)]
    _, mat = warp(img, refimg, pts, refpts, method="ransac")
    assert mat.shape == (3, 3)


@pytest.mark.parametrize("pts, refpts", [
    [[(0, 0)], [(0, 0), (0, 1)]],  # different # of points provided for img and refimg
    [[(0, 0)], [(0, 0)]],  # not enough pairs of points provided
    [[(0, 0), (0, 14), (9, 14), (0, 9), (3, 3)],
     [(0, 0), (149, 0), (99, 149), (0, 99), (3, 3)]]  # homography not able to be calculated (cannot converge)
])
def test_warp_err(pts, refpts, transform_test_data):
    """Test for PlantCV."""
    img = transform_test_data.create_test_img((10, 15))
    refimg = transform_test_data.create_test_img((100, 150))
    method = "rho"
    with pytest.raises(RuntimeError):
        warp(img, refimg, pts, refpts, method=method)


def test_warp_align(transform_test_data):
    """Test for PlantCV."""
    img = transform_test_data.create_test_img((10, 10, 3))
    refimg = transform_test_data.create_test_img((11, 11))
    mat = np.array([[1.00000000e+00,  1.04238500e-15, -7.69185075e-16],
                    [1.44375646e-16,  1.00000000e+00,  0.00000000e+00],
                    [-5.41315251e-16,  1.78930521e-15,  1.00000000e+00]])
    warp_img = warp_align(img=img, mat=mat, refimg=refimg)
    assert warp_img.shape == (11, 11, 3)
