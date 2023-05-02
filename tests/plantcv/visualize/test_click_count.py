import os
import numpy as np
import matplotlib
from plantcv.plantcv.transform import rescale
from plantcv.plantcv.visualize import ClickCount


def test_plantcv_visualize_click_count(tmpdir):
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("cache")
    # generate fake testing image
    temp = rescale(np.random.rand(5, 5))
    img = np.stack((temp,)*3, axis=-1)
    counter = ClickCount(img, figsize=(12, 6))
    assert len(counter.count) == 0

    # import coordinates
    counter.import_coords([(0, 0)], label="total")
    counter.import_coords([(0, 1)], label="c1")
    counter.import_coords([(0, 2)], label="total")
    assert len(counter.count) == 2

    # save coordinates
    coord_file = os.path.join(cache_dir, 'coord.json')
    counter.save_coords(coord_file)
    assert os.path.exists(coord_file)

    # view different classes
    counter.view()
    counter.view(label="c1", color="r", view_all=True)
    counter.view(label="c2", color="r", view_all=True)
    counter.view(label="c2", color="k", view_all=True)
    assert len(counter.points) == 3

    # create mock events
    # left click
    e1 = matplotlib.backend_bases.MouseEvent(name="button_press_event", canvas=counter.fig.canvas, x=0, y=0, button=1)
    e1.xdata = 0
    e1.ydata = 0

    # right click
    e1_ = matplotlib.backend_bases.MouseEvent(name="button_press_event", canvas=counter.fig.canvas, x=0, y=0, button=3)
    e1_.xdata = 0
    e1_.ydata = 0

    # left click
    e2 = matplotlib.backend_bases.MouseEvent(name="button_press_event", canvas=counter.fig.canvas, x=0, y=0, button=1)
    e2.xdata = 1
    e2.ydata = 1

    # right click
    e2_ = matplotlib.backend_bases.MouseEvent(name="button_press_event", canvas=counter.fig.canvas, x=0, y=0, button=3)
    e2_.xdata = 1.2
    e2_.ydata = 1.2

    counter.onclick(e1)
    counter.onclick(e1_)
    counter.onclick(e2)
    counter.onclick(e2_)
    assert len(counter.events) == 4
