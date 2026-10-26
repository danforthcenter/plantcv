import pytest
import cv2
import numpy as np
from plantcv.plantcv import Objects
from plantcv.plantcv.roi import (
    from_binary_image,
    rectangle,
    circle,
    ellipse,
    auto_grid,
    multi,
    multi_rect,
    auto_wells,
    custom,
    filter
)
from tests import synthetic


def test_from_binary_image(synthetic_rgb):
    """Test for PlantCV."""
    # Create a binary image
    bin_img = np.zeros(np.shape(synthetic_rgb)[0:2], dtype=np.uint8)
    cv2.rectangle(bin_img, (55, 55), (10, 10), 255, -1)
    roi = from_binary_image(bin_img=bin_img, img=synthetic_rgb)
    # Assert the contours and hierarchy lists contain only the ROI
    # The 46 x 46 px square has 4 * 45 = 180 boundary points
    assert np.shape(roi.contours[0]) == (1, 180, 1, 2)


def test_from_binary_image_grayscale_input(synthetic_gray):
    """Test for PlantCV."""
    # Create a binary image
    bin_img = np.zeros(np.shape(synthetic_gray)[0:2], dtype=np.uint8)
    cv2.rectangle(bin_img, (55, 55), (10, 10), 255, -1)
    roi = from_binary_image(bin_img=bin_img, img=synthetic_gray)
    # Assert the contours and hierarchy lists contain only the ROI
    # The 46 x 46 px square has 4 * 45 = 180 boundary points
    assert np.shape(roi.contours[0]) == (1, 180, 1, 2)


def test_from_binary_image_bad_binary_input():
    """Test for PlantCV."""
    # Random RGB image (the synthetic plant RGB image has only the values 0 and 128)
    rgb_img = synthetic.random_image((100, 120, 3))
    # Binary input is required but an RGB input is provided
    with pytest.raises(RuntimeError):
        _ = from_binary_image(bin_img=rgb_img, img=rgb_img)


def test_rectangle(synthetic_rgb):
    """Test for PlantCV."""
    roi = rectangle(x=10, y=10, h=50, w=50, img=synthetic_rgb)
    # Assert the contours and hierarchy lists contain only the ROI
    assert np.shape(roi.contours[0]) == (1, 4, 1, 2)


def test_rectangle_grayscale_input(synthetic_gray):
    """Test for PlantCV."""
    roi = rectangle(x=10, y=10, h=50, w=50, img=synthetic_gray)
    # Assert the contours and hierarchy lists contain only the ROI
    assert np.shape(roi.contours[0]) == (1, 4, 1, 2)


def test_rectangle_out_of_frame(synthetic_rgb):
    """Test for PlantCV."""
    # The resulting rectangle needs to be within the dimensions of the image
    with pytest.raises(RuntimeError):
        _ = rectangle(x=10, y=10, h=150, w=900, img=synthetic_rgb)


def test_circle(synthetic_rgb):
    """Test for PlantCV."""
    roi = circle(x=60, y=50, r=40, img=synthetic_rgb)
    # Assert the contours and hierarchy lists contain only the ROI
    # recorded value: number of boundary points of the radius 40 circle
    assert np.shape(roi.contours[0]) == (1, 224, 1, 2)


def test_circle_grayscale_input(synthetic_gray):
    """Test for PlantCV."""
    roi = circle(x=60, y=50, r=40, img=synthetic_gray)
    # Assert the contours and hierarchy lists contain only the ROI
    # recorded value: number of boundary points of the radius 40 circle
    assert np.shape(roi.contours[0]) == (1, 224, 1, 2)


def test_circle_out_of_frame(synthetic_rgb):
    """Test for PlantCV."""
    # The resulting rectangle needs to be within the dimensions of the image
    # (the circle extends past the left and bottom edges)
    with pytest.raises(RuntimeError):
        _ = circle(x=20, y=80, r=30, img=synthetic_rgb)


def test_ellipse(synthetic_rgb):
    """Test for PlantCV."""
    roi = ellipse(x=60, y=50, r1=40, r2=25, angle=0, img=synthetic_rgb)
    # Assert the contours and hierarchy lists contain only the ROI
    # recorded value: number of boundary points of the 40 x 25 radius ellipse
    assert np.shape(roi.contours[0]) == (1, 190, 1, 2)


def test_ellipse_grayscale_input(synthetic_gray):
    """Test for PlantCV."""
    roi = ellipse(x=60, y=50, r1=40, r2=25, angle=0, img=synthetic_gray)
    # Assert the contours and hierarchy lists contain only the ROI
    # recorded value: number of boundary points of the 40 x 25 radius ellipse
    assert np.shape(roi.contours[0]) == (1, 190, 1, 2)


def test_ellipse_out_of_frame(synthetic_rgb):
    """Test for PlantCV."""
    # The resulting rectangle needs to be within the dimensions of the image
    # (the ellipse extends past the left and bottom edges)
    with pytest.raises(RuntimeError):
        _ = ellipse(x=20, y=80, r1=30, r2=20, angle=0, img=synthetic_rgb)


def grid_mask():
    """Binary mask of four radius-10 disks in a 2 x 2 grid, centered at rows 35 and 65 and columns 40 and 80."""
    return synthetic.disk_mask(synthetic.PLANT_SHAPE, [(35, 40), (35, 80), (65, 40), (65, 80)], 10)


def test_auto_grid():
    """Test for PlantCV."""
    mask = grid_mask()
    rois = auto_grid(mask=mask, nrows=1, ncols=2)
    # Assert the contours has 2 ROIs
    assert len(rois.contours) == 2


def test_auto_grid_bad_input_img():
    """Test for PlantCV."""
    # Random RGB image (the synthetic plant RGB image has only the values 0 and 128)
    rgb_img = synthetic.random_image((100, 120, 3))
    # The user must input a binary mask to mask, not an rgb or grayscale
    with pytest.raises(RuntimeError):
        _ = auto_grid(rgb_img, nrows=1, ncols=2)


def test_auto_grid_one_column():
    """Test for PlantCV."""
    mask = grid_mask()
    rois = auto_grid(mask=mask, nrows=2, ncols=1)
    # Assert the contours has 2 ROIs
    assert len(rois.contours) == 2


def test_auto_grid_overlap(capsys):
    """Test for PlantCV."""
    mask = grid_mask()
    # Check for the overlapping ROI warning: radius-20 ROIs 30 px apart overlap but fit in the image
    _ = auto_grid(mask=mask, nrows=2, ncols=1, radius=20)
    cap = capsys.readouterr()
    assert cap.err == ("Warning: Two or more of the user defined regions of interest overlap! "
                       "If you only see one ROI then they may overlap exactly.\n")


def test_auto_grid_shrink_radius(capsys):
    """Test for PlantCV."""
    mask = grid_mask()
    # Radius-50 ROIs extend past the image edges, so the radius shrinks to fit
    rois = auto_grid(mask=mask, nrows=2, ncols=2, radius=50)
    cap = capsys.readouterr()
    assert cap.err == ("Warning: Shrinking radius to make ROIs fit in the image\n"
                       "Warning: Two or more of the user defined regions of interest overlap! "
                       "If you only see one ROI then they may overlap exactly.\n")
    assert len(rois.contours) == 4


def test_auto_grid_multiple_cols_rows():
    """Test for PlantCV."""
    mask = grid_mask()
    rois = auto_grid(mask=mask, nrows=2, ncols=2)
    # Assert the contours has 4 ROIs
    assert len(rois.contours) == 4


def test_multi(synthetic_rgb):
    """Test for PlantCV."""
    rois = multi(synthetic_rgb, coord=(10, 10), radius=10, spacing=(10, 10), nrows=2, ncols=2)
    # Assert the contours has 4 ROIs
    assert len(rois.hierarchy) == 4


def test_multi_rect(synthetic_rgb):
    """Test for PlantCV."""
    rois = multi_rect(synthetic_rgb, coord=(10, 10), h=20, w=20,
                      spacing=(10, 10), nrows=2, ncols=2)
    # Assert the contours has 4 ROIs
    assert len(rois.hierarchy) == 4


def test_auto_wells(test_data):
    """Test for PlantCV."""
    img = cv2.imread(test_data.hough_circle, -1)
    rois = auto_wells(img, 20, 50, 30, 40, 50, 4, 6, -10)
    assert len(rois.hierarchy) == 24


def test_auto_wells_in_region(test_data):
    """Test for PlantCV."""
    img = cv2.imread(test_data.hough_circle, -1)
    roi_cont = [np.array([[[50, 50]], [[50, 499]], [[399, 499]], [[399, 50]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    rect = Objects(contours=[roi_cont], hierarchy=[roi_str])
    rois = auto_wells(img, 20, 50, 30, 40, 50, 4, 6, -10, roi=rect)
    assert len(rois.hierarchy) == 12


def test_multi_rect_input_coords(synthetic_rgb):
    """Test for PlantCV."""
    rois = multi_rect(synthetic_rgb, coord=[(25, 60), (80, 40)], h=20, w=20)
    # Assert the contours has 2 ROIs
    assert len(rois.hierarchy) == 2


def test_multi_input_coords(synthetic_rgb):
    """Test for PlantCV."""
    rois = multi(synthetic_rgb, coord=[(25, 60), (80, 40)], radius=20)
    # Assert the contours has 2 ROIs
    assert len(rois.hierarchy) == 2


def test_multi_bad_input(synthetic_rgb):
    """Test for PlantCV."""
    # The user must input a list of custom coordinates OR inputs to make a grid. Not both
    with pytest.raises(RuntimeError):
        _ = multi(synthetic_rgb, coord=[(25, 60), (80, 40)], radius=20, spacing=(10, 10), nrows=3, ncols=6)


def test_multi_rect_bad_input(synthetic_rgb):
    """Test for PlantCV."""
    # The user must input a list of custom coordinates OR inputs to make a grid. Not both
    with pytest.raises(RuntimeError):
        _ = multi_rect(synthetic_rgb, coord=[(25, 60), (80, 40)],
                       h=10, w=10, spacing=(10, 10), nrows=3, ncols=6)


def test_multi_bad_input_no_radius(synthetic_rgb):
    """Test for PlantCV."""
    # The user must input a radius if using a list of custom coordinates
    with pytest.raises(RuntimeError):
        _ = multi(synthetic_rgb, coord=[(25, 60), (80, 40)])


def test_multi_bad_input_oob(synthetic_rgb):
    """Test for PlantCV."""
    # nputs to make a grid make ROIs that go off the screen
    with pytest.raises(RuntimeError):
        _ = multi(synthetic_rgb, coord=(25000, 12000), radius=2, spacing=(1, 1), nrows=3, ncols=6)


def test_multi_bad_input_oob_list(synthetic_rgb):
    """Test for PlantCV."""
    # All vertices in the list of centers must draw roi's that are inside the image
    with pytest.raises(RuntimeError):
        _ = multi(synthetic_rgb, coord=[(25000, 25000), (25000, 12000), (12000, 12000)], radius=20)


def test_roi_custom(synthetic_rgb):
    """Test for PlantCV."""
    roi = custom(img=synthetic_rgb, vertices=[[60, 1], [95, 50], [65, 55], [60, 62], [40, 45]])
    assert np.shape(roi.contours[0]) == (1, 5, 2)


def test_custom_bad_input(synthetic_rgb):
    """Test for PlantCV."""
    # ROI goes out of bounds
    with pytest.raises(RuntimeError):
        _ = custom(img=synthetic_rgb, vertices=[[226, -1], [3130, 1848], [2404, 2029], [2205, 2298], [1617, 1761]])


# ROI rows 35:55 and columns 20:70 contains the left leaf (280 px) and stem rows 35:55 (20 x 4 = 80 px)
# but only part of the plant, and not the small object
PARTIAL_ROI = [np.array([[[20, 35]], [[20, 54]], [[69, 54]], [[69, 35]]], dtype=np.int32)]


@pytest.mark.parametrize("mode,exp", [["largest", 800], ["cutto", 360], ["partial", 800], ["within", 0]])
def test_filter(mode, exp, synthetic_mask):
    """Test for PlantCV."""
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi_Obj = Objects(contours=[PARTIAL_ROI], hierarchy=[roi_str])
    # cutto keeps 280 + 80 = 360 px; largest and partial keep the whole 800 px plant
    filtered_mask = filter(mask=synthetic_mask, roi=roi_Obj, roi_type=mode)
    area = cv2.countNonZero(filtered_mask)
    # Assert that the contours were filtered as expected
    assert area == exp


def test_within_filter(synthetic_mask):
    """Test for PlantCV."""
    # ROI rows and columns 25:95 encloses the whole plant but not the small object
    roi = [np.array([[[25, 25]], [[25, 94]], [[94, 94]], [[94, 25]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi_Obj = Objects(contours=[roi], hierarchy=[roi_str])
    filtered_mask = filter(mask=synthetic_mask, roi=roi_Obj, roi_type="within")
    area = cv2.countNonZero(filtered_mask)
    # Assert that the contours were filtered as expected
    # Only the 800 px plant is within the ROI
    assert area == 800


def test_filter_multi(synthetic_mask):
    """Test for PlantCV."""
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    # make a multi-ROI by repeating the same roi twice
    roi_Obj = Objects(contours=[PARTIAL_ROI, PARTIAL_ROI], hierarchy=[roi_str, roi_str])
    filtered_mask = filter(mask=synthetic_mask, roi=roi_Obj, roi_type="partial")
    area = cv2.countNonZero(filtered_mask)
    # Assert that the contours were filtered as expected
    # The 800 px plant overlaps the ROI
    assert area == 800


def test_filter_bad_input(synthetic_mask):
    """Test for PlantCV."""
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi_Obj = Objects(contours=[PARTIAL_ROI], hierarchy=[roi_str])
    with pytest.raises(RuntimeError):
        _ = filter(mask=synthetic_mask, roi=roi_Obj, roi_type="cut")


def test_filter_grayscale_input(synthetic_gray):
    """Test for PlantCV."""
    mask = np.zeros(np.shape(synthetic_gray)[:2], dtype=np.uint8)
    cnt, cnt_str = synthetic.find_contours(synthetic.plant_mask())
    cv2.drawContours(mask, cnt, -1, (255), -1, lineType=8, hierarchy=cnt_str)
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi_Obj = Objects(contours=[PARTIAL_ROI], hierarchy=[roi_str])
    filtered_mask = filter(mask=mask, roi=roi_Obj, roi_type="partial")
    area = cv2.countNonZero(filtered_mask)
    # Assert that the contours were filtered as expected
    # The 800 px plant overlaps the ROI
    assert area == 800


def test_filter_no_overlap(synthetic_mask):
    """Test for PlantCV."""
    # ROI rows 0:25 and columns 95:120 does not overlap the plant or the small object
    roi = [np.array([[[95, 0]], [[95, 24]], [[119, 24]], [[119, 0]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi_Obj = Objects(contours=[roi], hierarchy=[roi_str])
    filtered_mask = filter(mask=synthetic_mask, roi=roi_Obj, roi_type="partial")
    area = cv2.countNonZero(filtered_mask)
    # Assert that the contours were filtered as expected
    assert area == 0


def test_filter_nested():
    """Test for PlantCV."""
    # Create test data
    img = np.zeros((100, 100), dtype=np.uint8)
    mask = np.zeros(np.shape(img)[:2], dtype=np.uint8)
    cnt = [np.array([[[25, 25]], [[25, 49]], [[49, 49]], [[49, 25]]], dtype=np.int32),
           np.array([[[34, 35]], [[35, 34]], [[39, 34]], [[40, 35]], [[40, 39]], [[39, 40]], [[35, 40]], [[34, 39]]],
                    dtype=np.int32)]
    cnt_str = np.array([[[-1, -1,  1, -1], [-1, -1, -1,  0]]], dtype=np.int32)
    cv2.drawContours(mask, cnt, -1, (255), -1, lineType=8, hierarchy=cnt_str)
    area_pre = cv2.countNonZero(mask)
    # Add small 2x2 square that should get filtered out
    mask = cv2.rectangle(mask, (5, 5), (7, 7), 255, -1)
    area_total = cv2.countNonZero(mask)

    roi = [np.array([[[0, 0]], [[0, 99]], [[99, 99]], [[99, 0]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi_Obj = Objects(contours=[roi], hierarchy=[roi_str])
    filtered_mask = filter(mask=mask, roi=roi_Obj, roi_type="largest")
    filtered_area = cv2.countNonZero(filtered_mask)
    assert area_pre == filtered_area
    assert area_total > filtered_area
