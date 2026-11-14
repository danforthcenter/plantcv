"""Tests for Morph class"""
import os
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
    assert os.path.exists(os.path.join(cache, "3_pruned_debug.png"))


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
