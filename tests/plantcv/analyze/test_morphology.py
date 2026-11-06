import os
import cv2
import numpy as np
import pytest
from plantcv.plantcv import outputs, params
from plantcv.plantcv.analyze.morphology import morphology as analyze_morphology
from plantcv.plantcv.morphology.morph_class import morph
from plantcv.plantcv.morphology.segment_euclidean_length import _segment_euclidean_length
from plantcv.plantcv.morphology.segment_insertion_angle import _segment_insertion_angle
from plantcv.plantcv.morphology.segment_tangent_angle import _segment_tangent_angle
from plantcv.plantcv.morphology.segment_width import _segment_width
from tests import synthetic


def _make_morph(skeleton=None, leaves=None, stem=None, mask=None):
    """Make a morph object with a given skeleton, leaf segments and stem segments.

    Parameters
    ----------
    skeleton : numpy.ndarray, optional
        Skeleton image (default synthetic.skeleton()).
    leaves : list, optional
        Leaf segment contours (default the synthetic leaf segments).
    stem : list, optional
        Stem segment contours (default the synthetic stem segments).
    mask : numpy.ndarray, optional
        Binary mask (default synthetic.skeleton_mask()).

    Returns
    -------
    plantcv.plantcv.morphology.morph
        Morph object holding the given skeleton and segments.
    """
    syn_leaves, syn_stem = synthetic.skeleton_segments()
    mask = synthetic.skeleton_mask() if mask is None else mask
    morpho = morph(mask)
    morpho.pruned_skeleton = synthetic.skeleton() if skeleton is None else skeleton
    morpho.leaves = syn_leaves if leaves is None else list(leaves)
    morpho.stem = syn_stem if stem is None else list(stem)
    return morpho


@pytest.fixture(autouse=True)
def reset_outputs():
    """Clear outputs and the saved color scale before and after each test."""
    outputs.clear()
    params.saved_color_scale = None
    yield
    outputs.clear()
    params.saved_color_scale = None


EXPECTED_VARIABLES = {"segment_path_length", "segment_insertion_angle", "segment_area", "mean_segment_width",
                      "segment_width_std", "segment_width_max", "segment_eu_length", "segment_angle",
                      "stem_height", "stem_angle", "stem_length", "segment_curvature", "segment_tangent_angle"}


def test_analyze_morphology():
    """Test for PlantCV."""
    morpho = _make_morph()
    filled = analyze_morphology(morpho, size=3, label="default")
    obs = outputs.observations["default"]
    assert EXPECTED_VARIABLES.issubset(obs.keys())
    # The public function records the same values as the helpers it calls
    assert obs["segment_tangent_angle"]["value"] == pytest.approx([180, 90, 180, 180])
    assert obs["segment_insertion_angle"]["value"] == pytest.approx([90, 90, 45, 45], abs=1e-4)
    # Every per-segment trait has one value per leaf segment
    for var in ("segment_path_length", "segment_eu_length", "segment_angle", "segment_curvature",
                "segment_tangent_angle", "segment_insertion_angle", "segment_area", "mean_segment_width"):
        assert len(obs[var]["value"]) == len(morpho.leaves), var
    assert filled.shape == morpho.mask.shape


def test_analyze_morphology_stems():
    """Test for PlantCV."""
    analyze_morphology(_make_morph(), size=3, stems=True, label="default")
    obs = outputs.observations["default"]
    assert obs["leaf_area"]["value"] == [81, 83, 98, 101]
    assert obs["stem_area"]["value"] == 153
    # Width is measured for each leaf and the combined stem
    assert len(obs["mean_segment_width"]["value"]) == 5


def test_analyze_morphology_default_label(monkeypatch):
    """Test for PlantCV."""
    monkeypatch.setattr(params, "sample_label", "plant")
    analyze_morphology(_make_morph(), size=3)
    assert list(outputs.observations.keys()) == ["plant"]
    assert EXPECTED_VARIABLES.issubset(outputs.observations["plant"].keys())


def test_analyze_morphology_debug(monkeypatch, tmpdir):
    """Test for PlantCV."""
    cache = tmpdir.mkdir("cache")
    monkeypatch.setattr(params, "debug_outdir", str(cache))
    monkeypatch.setattr(params, "debug", "print")
    monkeypatch.setattr(params, "device", 0)
    analyze_morphology(_make_morph(), size=3, label="default")
    assert os.path.exists(os.path.join(str(cache), "1_analyze_morphology.png"))


def test_analyze_morphology_from_mask():
    """Test for PlantCV."""
    # End to end: skeletonize, prune and segment a real mask, then analyze it
    morpho = morph(synthetic.plant_mask(small_object=False))
    morpho.prune(size=5)
    analyze_morphology(morpho, size=3, label="default")
    obs = outputs.observations["default"]
    assert len(obs["segment_path_length"]["value"]) == len(morpho.leaves)
    assert obs["stem_height"]["value"] > 0


def test_segment_euclidean_length_bad_input():
    """Test for PlantCV."""
    # A closed diamond has no tips, so it cannot be measured end to end
    skel = np.zeros((10, 10), dtype=np.uint8)
    edges = [np.array([[[5, 3]], [[4, 4]], [[3, 5]], [[4, 6]], [[5, 7]], [[6, 6]], [[7, 5]], [[6, 4]]],
                      dtype=np.int32)]
    with pytest.raises(RuntimeError):
        _segment_euclidean_length(_make_morph(skeleton=skel, leaves=edges, mask=skel), label="default")


@pytest.mark.parametrize("size,expected", [
    # The vertical stem meets the horizontal leaves at 90 degrees and the diagonal leaves at 45 degrees
    [3, [90, 90, 45, 45]],
    # The 28-pixel leaves are pruned away completely (see test_segment_tangent_angle)
    [100, ["NA", "NA", 45, 45]]])
def test_segment_insertion_angle(size, expected):
    """Test for PlantCV."""
    _segment_insertion_angle(_make_morph(), size=size, label="default")
    obs = outputs.observations["default"]["segment_insertion_angle"]
    # The stem fit is vertical to float32 precision, so angles are within 1e-4 degrees
    assert obs["value"] == pytest.approx(expected, abs=1e-4)


def test_segment_insertion_angle_bad_stem():
    """Test for PlantCV."""
    leaves, _ = synthetic.skeleton_segments()
    # A stem piece in the far corner, too far from the lower left leaf to be merged with it
    stem_obj = [leaves[0], np.array([[[0, 0]], [[1, 1]], [[2, 2]], [[3, 3]], [[4, 4]]], dtype=np.int32)]
    with pytest.raises(RuntimeError):
        _segment_insertion_angle(_make_morph(stem=stem_obj), size=10, label="default")


def test_segment_insertion_angle_disjoint_stem():
    """Test for PlantCV."""
    # Two stem pieces with a 3-pixel gap are dilated until they merge into a single stem
    stem_img = np.zeros(synthetic.PLANT_SHAPE, dtype=np.uint8)
    cv2.line(stem_img, (60, 89), (60, 72), 255, 1)
    cv2.line(stem_img, (60, 68), (60, 47), 255, 1)
    stem_obj, _ = synthetic.find_contours(stem_img)
    _segment_insertion_angle(_make_morph(stem=stem_obj), size=3, label="default")
    assert outputs.observations["default"]["segment_insertion_angle"]["value"] == pytest.approx(
        [90, 90, 45, 45], abs=1e-4)


@pytest.mark.parametrize("stem_end,leaf_start,leaf_end", [
    # A perfectly vertical stem fits with vx ~ 0
    [((250, 50), (250, 450)), (251, 149), (330, 70)],
    # A slanted stem
    [((100, 100), (400, 400)), (151, 149), (220, 80)]])
def test_segment_insertion_angle_single_leaf(stem_end, leaf_start, leaf_end):
    """Regression test for PlantCV."""
    stem_img = np.zeros((500, 500), dtype=np.uint8)
    cv2.line(stem_img, stem_end[0], stem_end[1], 255, 1)
    leaf_img = np.zeros((500, 500), dtype=np.uint8)
    cv2.line(leaf_img, leaf_start, leaf_end, 255, 1)
    skel = stem_img | leaf_img
    stem_obj, _ = synthetic.find_contours(stem_img)
    leaf_obj, _ = synthetic.find_contours(leaf_img)
    _segment_insertion_angle(_make_morph(skeleton=skel, leaves=leaf_obj, stem=stem_obj, mask=skel),
                             size=20, label="default")
    angles = outputs.observations["default"]["segment_insertion_angle"]["value"]
    assert len(angles) == 1
    assert isinstance(angles[0], float)


def test_segment_width():
    """Test for PlantCV."""
    # Label 1 is a 7-pixel-tall bar (rows 40:47) with its midline (row 43) as the skeleton,
    # away from the bar ends. Label 2 is a single pixel off the skeleton.
    labeled_mask = np.zeros((100, 100), dtype=np.int32)
    labeled_mask[40:47, 10:90] = 1
    labeled_mask[80, 80] = 2
    skeleton = np.zeros((100, 100), dtype=np.uint8)
    skeleton[43, 30:70] = 255
    morpho = _make_morph(skeleton=skeleton, mask=(labeled_mask > 0).astype(np.uint8) * 255)
    _segment_width(morpho, labeled_mask=labeled_mask, n_labels=2, label="default")
    obs = outputs.observations["default"]
    # The dilated midline covers rows 42 and 43 equally, at distances 3 and 4 from the background:
    # mean width 2 * 3.5 = 7, the bar height
    assert obs["mean_segment_width"]["value"] == [7, 0]
    assert obs["segment_width_max"]["value"] == [8, 0]
    assert obs["segment_width_std"]["value"] == [0.5, "NA"]
    assert obs["mean_segment_width"]["label"] == [1, 2]


@pytest.mark.parametrize("size,expected", [
    # Straight leaves have parallel ends (180 degrees). The right leaf's ends are horizontal and vertical.
    [3, [180, 90, 180, 180]],
    # The 28-pixel leaves are pruned away completely. A 19-pixel leaf keeps its middle pixel, which has
    # no neighbor left to make it a tip, so both of its ends remain.
    [100, ["NA", "NA", 180, 180]]])
def test_segment_tangent_angle(size, expected):
    """Test for PlantCV."""
    _segment_tangent_angle(_make_morph(), size=size, label="default")
    assert outputs.observations["default"]["segment_tangent_angle"]["value"] == pytest.approx(expected)
