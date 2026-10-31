import pytest
import numpy as np
from plantcv.plantcv import PSII_data
from plantcv.plantcv.photosynthesis import reassign_frame_labels
from tests import synthetic


@pytest.mark.parametrize("prot,frame", [["ojip_dark", "Fm"], ["ojip_light", "Fmp"]])
def test_reassign_frame_labels(prot, frame):
    """Test for PlantCV."""
    da = reassign_frame_labels(ps_da=synthetic.psii_dataarray(prot),
                               mask=synthetic.psii_mask())
    assert int(da.sel(frame_label=frame).frame_num) == 2


@pytest.mark.parametrize("prot,tmask", [
    # test mask shape
    ["ojip_dark", np.ones((2, 2))],
    # test mask is binary
    ["ojip_light", np.random.random((10, 10))]])
def test_reassign_frame_labels_fatalerror(prot, tmask):
    """Test for PlantCV."""
    da = synthetic.psii_dataarray(prot)
    with pytest.raises(RuntimeError):
        _ = reassign_frame_labels(ps_da=da, mask=tmask)


def test_reassign_frame_labels_invalid_array():
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _ = reassign_frame_labels(ps_da='string', mask=synthetic.psii_mask())


def test_reassign_frame_labels_invalid_name():
    """Test for PlantCV."""
    da = synthetic.psii_dataarray('ojip_dark').rename('test')
    with pytest.raises(RuntimeError):
        _ = reassign_frame_labels(ps_da=da, mask=synthetic.psii_mask())


def test_reassign_frame_labels_invalid_class():
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _ = reassign_frame_labels(ps_da=PSII_data(), mask=synthetic.psii_mask())
