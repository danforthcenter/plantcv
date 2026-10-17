import pytest
from plantcv.plantcv import params
from plantcv.plantcv._helpers import _area_unit


@pytest.mark.parametrize("unit,expected", [["pixels", "pixels"], ["px", "px"], ["Pixel", "Pixel"],
                                           ["mm", "mm2"], ["cm", "cm2"]])
def test_area_unit(unit, expected, monkeypatch):
    """Test for PlantCV."""
    monkeypatch.setattr(params, "unit", unit)
    assert _area_unit() == expected


def test_area_unit_override(monkeypatch):
    """Test for PlantCV."""
    monkeypatch.setattr(params, "unit", "mm")
    monkeypatch.setattr(params, "area_unit", "mm^2")
    assert _area_unit() == "mm^2"
