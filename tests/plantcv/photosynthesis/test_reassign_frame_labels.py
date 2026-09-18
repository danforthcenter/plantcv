import pytest
import numpy as np
from plantcv.plantcv import PSII_data
from plantcv.plantcv.photosynthesis import reassign_frame_labels


@pytest.mark.parametrize("prot,frame", [["ojip_dark", "Fm"], ["ojip_light", "Fmp"]])
def test_reassign_frame_labels(prot, frame, test_data):
    """Test for PlantCV."""
    da = reassign_frame_labels(ps_da=test_data.photosynthesis.psii_cropreporter(prot),
                               mask=test_data.photosynthesis.create_ps_mask())
    assert int(da.sel(frame_label=frame).frame_num) == 2


@pytest.mark.parametrize("prot,tmask", [
    # test mask shape
    ["ojip_dark", np.ones((2, 2))],
    # test mask is binary
    ["ojip_light", np.random.random((10, 10))]])
def test_reassign_frame_labels_fatalerror(prot, tmask, test_data):
    """Test for PlantCV."""
    da = test_data.photosynthesis.psii_cropreporter(prot)
    with pytest.raises(RuntimeError):
        _ = reassign_frame_labels(ps_da=da, mask=tmask)


def test_reassign_frame_labels_invalid_array(test_data):
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _ = reassign_frame_labels(ps_da='string', mask=test_data.photosynthesis.create_ps_mask())


def test_reassign_frame_labels_invalid_name(test_data):
    """Test for PlantCV."""
    da = test_data.psii_cropreporter('ojip_dark').rename('test')
    with pytest.raises(RuntimeError):
        _ = reassign_frame_labels(ps_da=da, mask=test_data.photosynthesis.create_ps_mask())


def test_reassign_frame_labels_invalid_class(test_data):
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _ = reassign_frame_labels(ps_da=PSII_data(), mask=test_data.photosynthesis.create_ps_mask())
