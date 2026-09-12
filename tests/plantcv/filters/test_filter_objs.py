import cv2
import numpy as np
import pytest
from plantcv.plantcv import params
from plantcv.plantcv import Objects
from plantcv.plantcv.filters import obj_props
from plantcv.plantcv import create_labels
from plantcv.plantcv._helpers import _rect_filter, _rect_replace
from skimage.measure import label, regionprops


def test_filter_objs_upper_na(filters_test_data):
    """Test for PlantCV."""
    params.debug = "plot"
    # Read in test data
    mask = cv2.imread(filters_test_data.barley_example)
    filtered_mask = obj_props(bin_img=mask)
    _, nobjs = create_labels(mask=filtered_mask)
    params.debug = None
    assert nobjs == 20


def test_filter_objs_lower_thresh(filters_test_data):
    """Test for PlantCV."""
    # Read in test data
    mask = cv2.imread(filters_test_data.barley_example)
    filtered_mask = obj_props(bin_img=mask, cut_side="lower", thresh=0.6, regprop="solidity")
    _, nobjs = create_labels(mask=filtered_mask)
    assert nobjs == 11


def test_filter_objs_in_thresh(filters_test_data):
    """Test for PlantCV."""
    # Read in test data
    mask = cv2.imread(filters_test_data.barley_example)
    filtered_mask = obj_props(bin_img=mask, cut_side="in", thresh=(0.1, 0.6), regprop="solidity")
    _, nobjs = create_labels(mask=filtered_mask)
    assert nobjs == 11


def test_filter_objs_out_thresh(filters_test_data):
    """Test for PlantCV."""
    # Read in test data
    mask = cv2.imread(filters_test_data.barley_example)
    filtered_mask = obj_props(bin_img=mask, cut_side="out", thresh=(0.6, 0.8), regprop="solidity")
    _, nobjs = create_labels(mask=filtered_mask)
    assert nobjs == 16


def test_filter_objs_lower_thresh_roi(filters_test_data):
    """Test for PlantCV."""
    # Read in test data
    mask = cv2.imread(filters_test_data.barley_example)
    roi_con = [np.array([[[10, 25]], [[10, 2500]], [[2500, 2500]], [[2500, 25]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi = Objects(contours=[roi_con], hierarchy=[roi_str])
    filtered_mask = obj_props(bin_img=mask, cut_side="lower", thresh=0.6, regprop="solidity", roi=roi)
    _, nobjs = create_labels(mask=filtered_mask)
    assert nobjs == 11


def test_bad_params(filters_test_data):
    """PlantCV Test"""
    mask = cv2.imread(filters_test_data.barley_example)
    with pytest.raises(RuntimeError):
        _ = obj_props(bin_img=mask, cut_side="middle")


def test_bad_thresh_lower(filters_test_data):
    """PlantCV Test"""
    mask = cv2.imread(filters_test_data.barley_example)
    with pytest.raises(RuntimeError):
        _ = obj_props(bin_img=mask, cut_side="lower", thresh=(1, 2))


def test_bad_thresh_in(filters_test_data):
    """PlantCV Test"""
    mask = cv2.imread(filters_test_data.barley_example)
    with pytest.raises(RuntimeError):
        _ = obj_props(bin_img=mask, cut_side="in", thresh=1)


def test_bad_property(filters_test_data):
    """PlantCV Test"""
    mask = cv2.imread(filters_test_data.barley_example)
    with pytest.raises(RuntimeError):
        _ = obj_props(bin_img=mask, regprop="bbox")


def test_empty_mask():
    """PlantCV Test"""
    mask = np.zeros((100, 100))
    fmask = obj_props(bin_img=mask, regprop="solidity")
    assert np.sum(fmask) == 0


def _reference_obj_props(bin_img, cut_side="upper", thresh=0, regprop="area", roi=None):
    """Pre-vectorization implementation of obj_props, kept as an equivalence reference.

    This is the original object-at-a-time algorithm: it rebuilt the output with a full-array
    np.where per object. obj_props now paints every object in a single pass, which is the same
    result for far less work (O(pixels + objects) instead of O(objects x pixels)). This copy
    exists so the tests below can prove those two are identical rather than assume it.
    """
    sub_bin_img = _rect_filter(bin_img, roi=roi)
    if np.count_nonzero(sub_bin_img) != 0:
        labeled_img = label(sub_bin_img)
        obj_measures = regionprops(labeled_img)
        sub_filtered_mask = np.zeros(labeled_img.shape, dtype=np.uint8)
        for obj in obj_measures:
            val = getattr(obj, regprop)
            if cut_side == "upper":
                gray_val = 255 if val > thresh else 0
            elif cut_side == "lower":
                gray_val = 255 if val < thresh else 0
            elif cut_side == "in":
                gray_val = 255 if min(thresh) < val < max(thresh) else 0
            else:
                gray_val = 255 if val < min(thresh) or val > max(thresh) else 0
            sub_filtered_mask += np.where(labeled_img == obj.label, gray_val, 0).astype(np.uint8)
    else:
        sub_filtered_mask = np.copy(sub_bin_img)
    return _rect_replace(bin_img, sub_filtered_mask, roi)


# Every scalar property obj_props accepts, paired with a threshold that splits the barley
# objects into a non-trivial mix of kept and dropped.
EQUIVALENCE_PROPS = [
    ("area", 5000),
    ("area_bbox", 8000),
    ("area_convex", 6000),
    ("area_filled", 5000),
    ("axis_major_length", 100),
    ("axis_minor_length", 40),
    ("eccentricity", 0.9),
    ("equivalent_diameter_area", 80),
    ("euler_number", 0),
    ("extent", 0.5),
    ("feret_diameter_max", 120),
    ("orientation", 0),
    ("perimeter", 400),
    ("perimeter_crofton", 400),
    ("solidity", 0.6),
]


@pytest.mark.parametrize("regprop,thresh", EQUIVALENCE_PROPS)
@pytest.mark.parametrize("cut_side", ["upper", "lower"])
def test_filter_objs_matches_reference(filters_test_data, regprop, thresh, cut_side):
    """Vectorized obj_props is byte-identical to the object-at-a-time original."""
    mask = cv2.imread(filters_test_data.barley_example, cv2.IMREAD_GRAYSCALE)
    observed = obj_props(bin_img=mask, cut_side=cut_side, thresh=thresh, regprop=regprop)
    expected = _reference_obj_props(bin_img=mask, cut_side=cut_side, thresh=thresh, regprop=regprop)
    assert np.array_equal(observed, expected)
    assert observed.dtype == expected.dtype


@pytest.mark.parametrize("cut_side,thresh", [("in", (0.1, 0.6)), ("out", (0.6, 0.8))])
def test_filter_objs_matches_reference_tuple_thresh(filters_test_data, cut_side, thresh):
    """The 'in' and 'out' cut sides are byte-identical to the original too."""
    mask = cv2.imread(filters_test_data.barley_example, cv2.IMREAD_GRAYSCALE)
    observed = obj_props(bin_img=mask, cut_side=cut_side, thresh=thresh, regprop="solidity")
    expected = _reference_obj_props(bin_img=mask, cut_side=cut_side, thresh=thresh, regprop="solidity")
    assert np.array_equal(observed, expected)


def test_filter_objs_matches_reference_multichannel(filters_test_data):
    """A 3-channel mask, the shape cv2.imread hands back by default, still matches."""
    mask = cv2.imread(filters_test_data.barley_example)
    observed = obj_props(bin_img=mask, cut_side="lower", thresh=0.6, regprop="solidity")
    expected = _reference_obj_props(bin_img=mask, cut_side="lower", thresh=0.6, regprop="solidity")
    assert np.array_equal(observed, expected)
    assert observed.dtype == expected.dtype


def test_filter_objs_matches_reference_roi(filters_test_data):
    """With an ROI, the untouched region outside the rectangle is preserved identically."""
    mask = cv2.imread(filters_test_data.barley_example, cv2.IMREAD_GRAYSCALE)
    roi_con = [np.array([[[10, 25]], [[10, 2500]], [[2500, 2500]], [[2500, 25]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi = Objects(contours=[roi_con], hierarchy=[roi_str])
    observed = obj_props(bin_img=mask, cut_side="lower", thresh=0.6, regprop="solidity", roi=roi)
    expected = _reference_obj_props(bin_img=mask, cut_side="lower", thresh=0.6, regprop="solidity", roi=roi)
    assert np.array_equal(observed, expected)
    assert observed.dtype == expected.dtype


def test_filter_objs_matches_reference_empty(filters_test_data):
    """The empty-mask short circuit returns the same array, and the same dtype, as before."""
    mask = np.zeros((100, 100))
    observed = obj_props(bin_img=mask, regprop="solidity")
    expected = _reference_obj_props(bin_img=mask, regprop="solidity")
    assert np.array_equal(observed, expected)
    assert observed.dtype == expected.dtype


def test_filter_objs_matches_reference_all_kept_and_all_dropped(filters_test_data):
    """Thresholds that keep everything, and that keep nothing, both still match."""
    mask = cv2.imread(filters_test_data.barley_example, cv2.IMREAD_GRAYSCALE)
    for thresh in (0, 10 ** 9):
        observed = obj_props(bin_img=mask, cut_side="upper", thresh=thresh, regprop="area")
        expected = _reference_obj_props(bin_img=mask, cut_side="upper", thresh=thresh, regprop="area")
        assert np.array_equal(observed, expected)


def test_filter_objs_matches_reference_many_objects():
    """A speckled mask, the case the vectorized rebuild exists for, still matches exactly."""
    rng = np.random.default_rng(42)
    mask = np.zeros((300, 300), dtype=np.uint8)
    mask[rng.random((300, 300)) > 0.7] = 255
    observed = obj_props(bin_img=mask, cut_side="upper", thresh=2, regprop="area")
    expected = _reference_obj_props(bin_img=mask, cut_side="upper", thresh=2, regprop="area")
    assert np.array_equal(observed, expected)


def test_filter_objs_debug_plot_output(filters_test_data, capsys):
    """params.debug == 'plot' still prints the same three lines, formatted the same way."""
    mask = cv2.imread(filters_test_data.barley_example, cv2.IMREAD_GRAYSCALE)
    params.debug = "plot"
    _ = obj_props(bin_img=mask, regprop="area")
    observed = capsys.readouterr().out
    params.debug = None
    values = [obj.area for obj in regionprops(label(mask))]
    assert observed == (f"Min value = {min(values)}\n"
                        f"Max value = {max(values)}\n"
                        f"Mean value = {sum(values)/len(values)}\n")


def test_filter_objs_device_increment(filters_test_data):
    """The step counter still advances by the same amount per call."""
    mask = cv2.imread(filters_test_data.barley_example, cv2.IMREAD_GRAYSCALE)
    params.device = 0
    _ = obj_props(bin_img=mask, regprop="area")
    assert params.device == 2
