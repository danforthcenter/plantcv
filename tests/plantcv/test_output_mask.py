import os
from plantcv.plantcv import output_mask


def test_output_mask(synthetic_gray, synthetic_mask, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("cache")
    *results, = output_mask(img=synthetic_gray, mask=synthetic_mask, filename='test.png', outdir=cache_dir,
                            mask_only=False)
    imgpath = results[0]
    maskpath = results[1]
    assert all([os.path.exists(imgpath) is True, os.path.exists(maskpath) is True])
