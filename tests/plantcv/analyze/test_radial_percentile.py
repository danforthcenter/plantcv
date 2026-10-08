"""Tests for pcv.analyze.radial_percentile"""
import cv2
import numpy as np
from plantcv.plantcv.analyze.radial import radial_percentile
from plantcv.plantcv import outputs


def _binary_seed_mask(test_data):
    """Read the seed mask (JPEG) and convert it to a clean 0/255 binary mask."""
    mask = cv2.imread(test_data.rgb_seed_mask, -1)
    return np.where(mask > 127, 255, 0).astype(np.uint8)


def test_radial_rgb(test_data):
    """Test for PlantCV."""
    outputs.clear()
    img = cv2.imread(test_data.rgb_seed)
    mask = _binary_seed_mask(test_data)
    avgs = radial_percentile(img=img, labeled_mask=mask)
    assert len(avgs) == 1 and len(avgs[0]) == 3
    assert outputs.observations["default_1"]["red_50%_avg"]["value"] == avgs[0][0]


def test_radial_gray(test_data):
    """Test for PlantCV."""
    outputs.clear()
    img = cv2.imread(test_data.rgb_seed, 0)
    mask = _binary_seed_mask(test_data)
    avgs = radial_percentile(img=img, labeled_mask=mask, percentile=40)
    assert isinstance(avgs[0], float)
    assert outputs.observations["default_1"]["gray_40%_avg"]["value"] == avgs[0]


def test_radial_excludes_background():
    """Background pixels inside the cutoff radius must not bias the average."""
    outputs.clear()
    img = np.zeros((50, 50), dtype=np.uint8)
    labeled_mask = np.zeros((50, 50), dtype=np.int32)
    # Ring-like object: an "L" shape whose center of mass region includes background pixels
    img[5:45, 5:15] = 100
    img[35:45, 5:45] = 100
    labeled_mask[5:45, 5:15] = 1
    labeled_mask[35:45, 5:45] = 1
    avgs = radial_percentile(img=img, labeled_mask=labeled_mask, percentile=90)
    assert avgs[0] == 100


def test_radial_multi_object():
    """Test for PlantCV."""
    outputs.clear()
    img = np.zeros((50, 100, 3), dtype=np.uint8)
    labeled_mask = np.zeros((50, 100), dtype=np.int32)
    # Object 1: pure blue (BGR), object 2: pure red (BGR)
    img[10:40, 10:40] = (255, 0, 0)
    img[10:40, 60:90] = (0, 0, 255)
    labeled_mask[10:40, 10:40] = 1
    labeled_mask[10:40, 60:90] = 2
    avgs = radial_percentile(img=img, labeled_mask=labeled_mask, n_labels=2, label=["a", "b"])
    # Outputs are ordered R, G, B
    assert avgs == [[0.0, 0.0, 255.0], [255.0, 0.0, 0.0]]
    assert outputs.observations["b_2"]["red_50%_avg"]["value"] == 255.0


def test_radial_empty_object():
    """A label that is not present returns NaN and records no observations."""
    outputs.clear()
    img = np.full((50, 50), 100, dtype=np.uint8)
    labeled_mask = np.zeros((50, 50), dtype=np.int32)
    labeled_mask[10:40, 10:40] = 1
    avgs = radial_percentile(img=img, labeled_mask=labeled_mask, n_labels=2)
    assert avgs[0] == 100
    assert np.isnan(avgs[1])
    assert "default_2" not in outputs.observations


def test_radial_empty_rgb():
    """Test for PlantCV."""
    outputs.clear()
    img = np.zeros((50, 50, 3), dtype=np.uint8)
    labeled_mask = np.zeros((50, 50), dtype=np.uint8)
    avgs = radial_percentile(img=img, labeled_mask=labeled_mask)
    assert np.all(np.isnan(avgs[0]))


def test_radial_no_pixels_within_cutoff():
    """A percentile of 0 leaves no pixels within the cutoff."""
    outputs.clear()
    img = np.full((50, 50), 100, dtype=np.uint8)
    labeled_mask = np.zeros((50, 50), dtype=np.int32)
    labeled_mask[10:40, 10:40] = 1
    avgs = radial_percentile(img=img, labeled_mask=labeled_mask, percentile=0)
    assert np.isnan(avgs[0])
