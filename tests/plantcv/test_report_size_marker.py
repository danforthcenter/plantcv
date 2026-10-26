import pytest
import numpy as np
from plantcv.plantcv import report_size_marker_area, outputs, Objects
from tests import synthetic


def _marker_roi():
    """Square ROI at columns 1:30 and rows 61:90, left of the plant (29 x 29 = 841 px)."""
    roi_contour = [np.array([[[1, 61]], [[1, 89]], [[29, 89]], [[29, 61]]], dtype=np.int32)]
    roi_hierarchy = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    return Objects(contours=[roi_contour], hierarchy=[roi_hierarchy])


# detect: red marker disk of radius 12 has 441 px (as in the two-plant mask); define: 29 x 29 ROI
@pytest.mark.parametrize("marker,exp", [["detect", 441], ["define", 841]])
def test_report_size_marker(marker, exp, synthetic_rgb):
    """Test for PlantCV."""
    # Clear outputs
    outputs.clear()
    # Draw a red marker disk of radius 12 centered at (row 75, column 15) inside the ROI
    marker_mask = synthetic.disk_mask(synthetic.PLANT_SHAPE, [(75, 15)], 12)
    synthetic_rgb[marker_mask > 0] = (0, 0, 255)
    _ = report_size_marker_area(img=synthetic_rgb, roi=_marker_roi(), marker=marker,
                                objcolor='light', thresh_channel='s', thresh=120)
    assert int(outputs.metadata["marker_area"]["value"][0]) == exp


def test_report_size_marker_grayscale_input(synthetic_gray):
    """Test for PlantCV."""
    # Clear outputs
    outputs.clear()
    _ = report_size_marker_area(img=synthetic_gray, roi=_marker_roi(), marker='define',
                                objcolor='light', thresh_channel='s', thresh=120)
    # 29 x 29 ROI
    assert int(outputs.metadata["marker_area"]["value"][0]) == 841


@pytest.mark.parametrize("marker,channel", [
    ["none", "s"],  # Invalid marker
    ["detect", None]  # Invalid channel
    ])
def test_report_size_marker_bad_inputs(marker, channel, synthetic_rgb):
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _ = report_size_marker_area(img=synthetic_rgb, roi=_marker_roi(), marker=marker,
                                    objcolor='light', thresh_channel=channel, thresh=120)


def test_report_size_marker_no_detection(synthetic_gray):
    """Test for PlantCV."""
    # Clear outputs
    outputs.clear()
    # ROI contour
    roi_contour = [np.array([[[1, 1]], [[1, 2]], [[2, 2]], [[2, 1]]], dtype=np.int32)]
    roi_hierarchy = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi = Objects(contours=[roi_contour], hierarchy=[roi_hierarchy])
    _ = report_size_marker_area(img=synthetic_gray, roi=roi, marker='define',
                                objcolor='light', thresh_channel='s', thresh=120)
    assert outputs.metadata["marker_area"]["value"][0] == 'none'
