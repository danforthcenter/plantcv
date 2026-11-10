import numpy as np
import os
import pytest
from plantcv.plantcv.transform import checkerboard_calib, calibrate_camera
from plantcv.plantcv.transform.color_correction import save_matrix
from tests import synthetic


@pytest.mark.parametrize("subdir", ["", "outputs"])
def test_checkerboard_calibration(subdir, tmp_path):
    """Test for PlantCV."""
    # checkerboard_calib creates the output directory if it does not exist
    cache_dir = os.path.join(tmp_path, "cache", subdir)
    os.makedirs(os.path.join(tmp_path, "cache"))
    checkerboard_dir = synthetic.write_checkerboards(tmp_path / "boards")
    col_corners, row_corners = synthetic.CHECKERBOARD_CORNERS
    mtx, dist = checkerboard_calib(checkerboard_dir, col_corners=col_corners, row_corners=row_corners,
                                   out_dir=cache_dir)
    # The views were rendered with focal length 300 px and principal point (160, 120): recorded estimates
    # 299.7 and 299.8 px, and (159.8, 120.0)
    camera = np.array(synthetic.CHECKERBOARD_CAMERA)
    assert mtx[0, 0] == pytest.approx(camera[0, 0], rel=0.01)
    assert mtx[1, 1] == pytest.approx(camera[1, 1], rel=0.01)
    assert mtx[0, 2] == pytest.approx(camera[0, 2], abs=1)
    assert mtx[1, 2] == pytest.approx(camera[1, 2], abs=1)
    assert np.shape(dist) == (1, 5)
    assert np.array_equal(np.load(os.path.join(cache_dir, "mtx.npz"))["arr_0"], mtx)
    assert np.array_equal(np.load(os.path.join(cache_dir, "dist.npz"))["arr_0"], dist)


@pytest.mark.parametrize("k1", [0, -0.2])
def test_calibrate_camera(k1, tmp_path):
    """Test for PlantCV."""
    img = synthetic.random_image((*synthetic.CHECKERBOARD_SHAPE, 3))
    mtx = str(tmp_path / "mtx.npz")
    dist = str(tmp_path / "dist.npz")
    save_matrix(np.array(synthetic.CHECKERBOARD_CAMERA), mtx)
    save_matrix(np.array([[k1, 0, 0, 0, 0]], dtype=np.float64), dist)
    corrected_img = calibrate_camera(img, mtx, dist)
    if k1 == 0:
        # Without distortion the image does not change
        assert np.array_equal(corrected_img, img)
    else:
        assert np.sum(img) != np.sum(corrected_img)
