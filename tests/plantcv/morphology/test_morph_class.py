"""Tests for Morph class"""
import os
import numpy as np
from tests import synthetic
from plantcv.plantcv._globals import params
from plantcv.plantcv.morphology.morph_class import morph


def test_morph_init():
    """Test for PlantCV."""
    mask = synthetic.plant_mask(small_object=False)
    morpho = morph(mask)
    assert isinstance(morpho, morph)
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
    morpho = morph(mask)
    morpho.prune(size=30)
    assert np.count_nonzero(morpho._skeleton) == 106
    assert np.count_nonzero(morpho.skeleton) == 89
    morpho.prune(size=60, reprune=True)
    assert np.count_nonzero(morpho.skeleton) == 65
    assert os.path.exists(os.path.join(cache, "3_pruned_debug.png"))


def test_morph_cycles(monkeypatch, tmpdir):
    """Test for PlantCV."""
    cache = tmpdir.mkdir("cache")
    monkeypatch.setattr(params, "debug_outdir", cache)
    monkeypatch.setattr(params, "debug", "print")
    monkeypatch.setattr(params, "device", 0)
    cycling_skeleton = synthetic.skeleton(cycle=True)
    mask = np.zeros(cycling_skeleton.shape[:2], dtype=np.uint8)
    morpho = morph(mask)
    morpho.skeleton = cycling_skeleton
    n_cycles = morpho.cycles
    assert n_cycles == 1
    assert os.path.exists(os.path.join(cache, "1_cycles.png"))
