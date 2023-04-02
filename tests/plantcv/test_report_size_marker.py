import pytest
import cv2
import numpy as np
from plantcv.plantcv import report_size_marker_area, outputs, Objects


@pytest.mark.parametrize("marker,exp", [["detect", 1257], ["define", 2601]])
def test_report_size_marker(marker, exp, test_data):
    """Test for PlantCV."""
    # Clear outputs
    outputs.clear()
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    # Draw a marker
    img = cv2.circle(img, (50, 100), 20, (0, 0, 255), thickness=-1)
    # ROI contour
    roi_contour = [np.array([[[25, 75]], [[25, 125]], [[75, 125]], [[75, 75]]], dtype=np.int32)]
    roi_hierarchy = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi = Objects(contours=[roi_contour], hierarchy=[roi_hierarchy])
    _ = report_size_marker_area(img=img, roi=roi, marker=marker,
                                objcolor='light', thresh_channel='s', thresh=120)
    assert int(outputs.observations["default"]["marker_area"]["value"]) == exp


def test_report_size_marker_grayscale_input(test_data):
    """Test for PlantCV."""
    # Clear outputs
    outputs.clear()
    # Read in test data
    img = cv2.imread(test_data.small_gray_img, -1)
    # ROI contour
    roi_contour = [np.array([[[25, 75]], [[25, 125]], [[75, 125]], [[75, 75]]], dtype=np.int32)]
    roi_hierarchy = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi = Objects(contours=[roi_contour], hierarchy=[roi_hierarchy])
    _ = report_size_marker_area(img=img, roi=roi, marker='define',
                                objcolor='light', thresh_channel='s', thresh=120)
    assert int(outputs.observations["default"]["marker_area"]["value"]) == 2601


@pytest.mark.parametrize("marker,channel", [
    ["none", "s"],  # Invalid marker
    ["detect", None]  # Invalid channel
    ])
def test_report_size_marker_bad_inputs(marker, channel, test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    # ROI contour
    roi_contour = [np.array([[[25, 75]], [[25, 125]], [[75, 125]], [[75, 75]]], dtype=np.int32)]
    roi_hierarchy = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi = Objects(contours=[roi_contour], hierarchy=[roi_hierarchy])
    with pytest.raises(RuntimeError):
        _ = report_size_marker_area(img=img, roi=roi, marker=marker,
                                    objcolor='light', thresh_channel=channel, thresh=120)
