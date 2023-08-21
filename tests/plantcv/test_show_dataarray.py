import pytest
from plantcv.plantcv._show_dataarray import _show_dataarray


def test_show_dataarray(test_data):
    """Test for PlantCV."""
    _show_dataarray(test_data.psii_cropreporter('ojip_dark').squeeze('measurement', drop=True), col='frame_label')
    # Assert that the image was plotted without error
    assert True


def test_show_dataarray_bad_kwarg(test_data):
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _show_dataarray(test_data.psii_cropreporter('ojip_dark').squeeze('measurement', drop=True), col=None)


def test_show_dataarray_missing_dim(test_data):
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _show_dataarray(test_data.psii_cropreporter('ojip_dark').squeeze('measurement', drop=True)[0, :, :],
                        col="frame_label")


def test_show_dataarray_too_many_dims(test_data):
    """Test for PlantCV."""
    # pcolormesh() fails with ValueError if ndim != 2 in addition to row and/or col
    with pytest.raises(ValueError):
        _show_dataarray(img=test_data.psii_cropreporter('ojip_dark'), col_wrap=4, row='frame_label')


def test_show_dataarray_too_few_dims(test_data):
    """Test for PlantCV."""
    # pcolormesh() fails with ValueError if ndim != 2 in addition to row and/or col
    with pytest.raises(ValueError):
        _show_dataarray(img=test_data.psii_cropreporter('ojip_dark')[:, :, 0, 0], col_wrap=4, row='frame_label')
