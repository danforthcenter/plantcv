import cv2
import matplotlib
from plantcv.plantcv import Points


def test_points_interactive(annotate_test_data):
    """Test for PlantCV."""
    # Read in a test grayscale image
    img = cv2.imread(annotate_test_data.small_rgb_img)

    # initialize interactive tool
    drawer_rgb = Points(img, figsize=(12, 6))

    # simulate mouse clicks
    # event 1, left click to add point
    e1 = matplotlib.backend_bases.MouseEvent(name="button_press_event", canvas=drawer_rgb.fig.canvas,
                                             x=0, y=0, button=1)
    point1 = (200, 200)
    e1.xdata, e1.ydata = point1
    drawer_rgb.onclick(e1)

    # event 2, left click to add point
    e2 = matplotlib.backend_bases.MouseEvent(name="button_press_event", canvas=drawer_rgb.fig.canvas,
                                             x=0, y=0, button=1)
    e2.xdata, e2.ydata = (300, 200)
    drawer_rgb.onclick(e2)

    # event 3, left click to add point
    e3 = matplotlib.backend_bases.MouseEvent(name="button_press_event", canvas=drawer_rgb.fig.canvas,
                                             x=0, y=0, button=1)
    e3.xdata, e3.ydata = (50, 50)
    drawer_rgb.onclick(e3)

    # event 4, right click to remove point with exact coordinates
    e4 = matplotlib.backend_bases.MouseEvent(name="button_press_event", canvas=drawer_rgb.fig.canvas,
                                             x=0, y=0, button=3)
    e4.xdata, e4.ydata = (50, 50)
    drawer_rgb.onclick(e4)

    # event 5, right click to remove point with coordinates close but not equal
    e5 = matplotlib.backend_bases.MouseEvent(name="button_press_event", canvas=drawer_rgb.fig.canvas,
                                             x=0, y=0, button=3)
    e5.xdata, e5.ydata = (301, 200)
    drawer_rgb.onclick(e5)

    assert drawer_rgb.points[0] == point1
