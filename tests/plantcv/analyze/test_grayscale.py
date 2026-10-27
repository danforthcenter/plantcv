import numpy as np
from plantcv.plantcv import outputs
from plantcv.plantcv.analyze import grayscale as analyze_grayscale


def test_grayscale(synthetic_gray, synthetic_mask):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    _ = analyze_grayscale(gray_img=synthetic_gray, labeled_mask=synthetic_mask, n_labels=1, bins=256)
    # 800 of 816 masked pixels are plant (200); the other 16 are the small object (120)
    assert int(outputs.observations['default_1']['gray_median']['value']) == 200


def test_grayscale_16bit(synthetic_gray, synthetic_mask):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    _ = analyze_grayscale(gray_img=np.uint16(synthetic_gray), labeled_mask=synthetic_mask, n_labels=1, bins=256)
    # 800 of 816 masked pixels are plant (200); the other 16 are the small object (120)
    assert int(outputs.observations['default_1']['gray_median']['value']) == 200


def test_grayscale_multiple_objects(synthetic_gray, synthetic_mask):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Split the foreground through the stem into two labeled objects (label 3 is absent)
    labeled_mask = np.zeros(synthetic_mask.shape, dtype=np.int32)
    labeled_mask[:, :60][synthetic_mask[:, :60] > 0] = 1
    labeled_mask[:, 60:][synthetic_mask[:, 60:] > 0] = 2
    _ = analyze_grayscale(gray_img=synthetic_gray, labeled_mask=labeled_mask, n_labels=3, bins=256,
                          label=["a", "b", "c"])
    assert list(outputs.observations.keys()) == ["a_1", "b_2"]
    for i, sample in enumerate(("a_1", "b_2"), start=1):
        assert sum(outputs.observations[sample]['gray_frequencies']['value']) == np.count_nonzero(labeled_mask == i)
