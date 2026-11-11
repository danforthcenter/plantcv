"""Tests for Morph class"""
import os
import pytest
import numpy as np
from tests import synthetic
from plantcv.plantcv._globals import params
from plantcv.plantcv.morphology.morph_class import Morph


def test_morph_init():
    """Test for PlantCV."""
    mask = synthetic.plant_mask(small_object=False)
    morpho = Morph(mask)
    assert isinstance(morpho, Morph)
    assert isinstance(morpho.stem, list) and len(morpho.stem) == 2
    assert isinstance(morpho.leaves, list) and len(morpho.leaves) == 3
    assert isinstance(morpho.skeleton, np.ndarray)
    assert np.count_nonzero(morpho.skeleton) == 106
    assert len(morpho.branch_points) == 2
    assert len(morpho.leaf_tips) == 4  # tips does not distinguish leaves vs stem segments


def test_morph_prune(monkeypatch, tmpdir):
    """Test for PlantCV."""
    cache = tmpdir.mkdir("cache")
    monkeypatch.setattr(params, "debug_outdir", cache)
    monkeypatch.setattr(params, "debug", "print")
    monkeypatch.setattr(params, "device", 0)
    mask = synthetic.plant_mask(small_object=False)
    morpho = Morph(mask)
    morpho.prune(size=30)
    assert np.count_nonzero(morpho._skeleton) == 106
    assert np.count_nonzero(morpho.skeleton) == 89
    # test that repruning starts from the same _skeleton
    morpho.prune(size=30)
    assert np.count_nonzero(morpho._skeleton) == 106
    assert np.count_nonzero(morpho.skeleton) == 89
    # test that repruning with reprune on starts from pruned skeleton
    morpho.prune(size=60, reprune=True)
    assert np.count_nonzero(morpho.skeleton) == 65
    assert os.path.exists(os.path.join(cache, "1_pruned_debug.png"))


def test_morph_cycles(monkeypatch, tmpdir):
    """Test for PlantCV."""
    cache = tmpdir.mkdir("cache")
    monkeypatch.setattr(params, "debug_outdir", cache)
    monkeypatch.setattr(params, "debug", "print")
    monkeypatch.setattr(params, "device", 0)
    cycling_skeleton = synthetic.skeleton(cycle=True).astype(np.uint8)
    morpho = Morph(cycling_skeleton)
    n_cycles = morpho.cycles
    assert n_cycles == 1
    assert os.path.exists(os.path.join(cache, "1_cycles.png"))
    params.saved_color_scale = None


def test_morph_cycles_no_debug(monkeypatch):
    """Check cyclic and acyclic skeletons without debugging."""
    monkeypatch.setattr(params, "debug", None)
    monkeypatch.setattr(params, "saved_color_scale", None)
    assert Morph(synthetic.skeleton(cycle=True)).cycles == 1
    assert Morph(synthetic.skeleton()).cycles == 0


def test_morph_combine_leaves(monkeypatch, tmpdir):
    """Test for PlantCV."""
    cache = tmpdir.mkdir("cache")
    monkeypatch.setattr(params, "debug_outdir", cache)
    monkeypatch.setattr(params, "debug", "print")
    monkeypatch.setattr(params, "device", 0)
    morpho = Morph(synthetic.plant_mask(small_object=False))
    combined = np.concatenate([morpho.leaves[1], morpho.leaves[0]], axis=0)
    morpho.combine_segments(leaves=[0, 1])
    assert len(morpho.leaves) == 2 and len(morpho.stem) == 2
    assert np.array_equal(morpho.leaves[-1], combined)
    assert os.path.exists(os.path.join(cache, "1_combined_segment_ids.png"))


def test_morph_combine_stems():
    """Test for PlantCV."""
    morpho = Morph(synthetic.plant_mask(small_object=False))
    exp_leaves = len(morpho.leaves)
    morpho.combine_segments(stems=[0, 1])
    assert len(morpho.leaves) == exp_leaves and len(morpho.stem) == 1


def test_morph_combine_mixed():
    """Test for PlantCV."""
    morpho = Morph(synthetic.plant_mask(small_object=False))
    morpho.combine_segments(leaves=[2], stems=[1], combined_type="stem")
    assert len(morpho.leaves) == 2 and len(morpho.stem) == 2


@pytest.mark.parametrize("kwargs", [
    {"leaves": [0, 9]},                                     # out of range
    {"leaves": [0, -1]},                                    # negative
    {"leaves": [0, 0]},                                     # duplicate
    {"leaves": [0]},                                        # only one segment
    {"leaves": ["0", "1"]},                                 # not ints
])
def test_morph_combine_bad_input(kwargs):
    """Test for PlantCV."""
    morpho = Morph(synthetic.plant_mask(small_object=False))
    with pytest.raises(RuntimeError):
        morpho.combine_segments(**kwargs)
