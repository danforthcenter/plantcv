import cv2
import numpy as np
import pytest
from plantcv.plantcv import outputs
from plantcv.plantcv.morphology.analyze_stem import analyze_stem
from tests import synthetic


def test_analyze_stem():
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # A 45 degree stem of 21 pixels from (60, 89) up and to the right to (80, 69)
    stem_img = np.zeros(synthetic.PLANT_SHAPE, dtype=np.uint8)
    cv2.line(stem_img, (60, 89), (80, 69), 255, 1)
    stem_obj, _ = synthetic.find_contours(stem_img)
    _ = analyze_stem(rgb_img=cv2.cvtColor(stem_img, cv2.COLOR_GRAY2BGR), stem_objects=stem_obj)
    # y decreases by 1 for each step in x, so the slope is 1
    assert outputs.observations['default']['stem_angle']['value'] == pytest.approx(1)
    assert outputs.observations['default']['stem_height']['value'] == 21
    # The contour runs out and back over 20 diagonal steps, less the closing step: (40 - 1) * sqrt(2) / 2
    assert outputs.observations['default']['stem_length']['value'] == pytest.approx(19.5 * np.sqrt(2))


def test_analyze_stem_bad_angle():
    """Test for PlantCV."""
    outputs.clear()
    skel = cv2.cvtColor(synthetic.skeleton(), cv2.COLOR_GRAY2BGR)
    # The vertical synthetic stem, from its bottom tip to its top branch point
    stem_obj = [[[[60, 89]], [[60, 45]]]]
    _ = analyze_stem(rgb_img=skel, stem_objects=stem_obj)
    # A vertical stem has a near-infinite slope, too large to plot
    assert outputs.observations['default']['stem_angle']['value'] == 22877334.0  # recorded value
