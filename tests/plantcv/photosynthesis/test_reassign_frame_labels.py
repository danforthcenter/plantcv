import pytest
import numpy as np
from plantcv.plantcv import PSII_data
from plantcv.plantcv.photosynthesis import reassign_frame_labels


@pytest.mark.parametrize("prot,frame", [["darkadapted", "Fm"], ["lightadapted", "Fmp"]])
def test_reassign_frame_labels(prot, frame, photosynthesis_test_data):
    """Test for PlantCV."""
    da, _, _ = reassign_frame_labels(ps_da=photosynthesis_test_data.psii_cropreporter(prot),
                                     mask=photosynthesis_test_data.create_ps_mask())
    assert int(da.sel(frame_label=frame).frame_num) == 2


@pytest.mark.parametrize("prot,tmask", [
    # test mask shape
    ["darkadapted", np.ones((2, 2))],
    # test mask is binary
    ["lightadapted", np.random.random((10, 10))]])
def test_reassign_frame_labels_fatalerror(prot, tmask, photosynthesis_test_data):
    """Test for PlantCV."""
    da = photosynthesis_test_data.psii_cropreporter(prot)
    with pytest.raises(RuntimeError):
        _, _ = reassign_frame_labels(ps_da=da, mask=tmask)


def test_reassign_frame_labels_invalid_array(photosynthesis_test_data):
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _, _ = reassign_frame_labels(ps_da='string', mask=photosynthesis_test_data.create_ps_mask())


def test_reassign_frame_labels_invalid_name(photosynthesis_test_data):
    """Test for PlantCV."""
    da = photosynthesis_test_data.psii_cropreporter('darkadapted').rename('test')
    with pytest.raises(RuntimeError):
        _, _ = reassign_frame_labels(ps_da=da, mask=photosynthesis_test_data.create_ps_mask())


def test_reassign_frame_labels_invalid_class(photosynthesis_test_data):
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _, _ = reassign_frame_labels(ps_da=PSII_data(), mask=photosynthesis_test_data.create_ps_mask())
