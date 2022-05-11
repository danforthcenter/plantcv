import os
import matplotlib
from plantcv.plantcv.annotate import ImageRegistrator

def test_plantcv_transform_img_registration_gray(transform_test_data):
    # generate fake testing images
    img_ref = transform_test_data.create_test_img((12, 10))
    img_tar = transform_test_data.create_test_img((12, 10))
    img_registrator = ImageRegistrator(img_ref, img_tar)
    assert len(img_registrator.events) == 0


def test_plantcv_transform_img_registration(transform_test_data, tmpdir):
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("sub")
    # generate fake testing images
    img_ref = transform_test_data.create_test_img((12, 10, 3))
    img_tar = transform_test_data.create_test_img((12, 10, 3))
    img_registrator = ImageRegistrator(img_ref, img_tar)


    # create mock events: left click
    for pt in [(0, 0), (1, 0), (0, 3), (4, 4), (3,2)]:
        # left click, left axis
        e1 = matplotlib.backend_bases.MouseEvent(name="button_press_event", canvas=img_registrator.fig.canvas,
                                                 x=0, y=0, button=1)
        e1.inaxes = img_registrator.axes[0]
        e1.inaxes._subplotspec = matplotlib.gridspec.SubplotSpec(matplotlib.gridspec.GridSpec(1,2,img_registrator.fig), 0)
        e1.xdata, e1.ydata = pt
        img_registrator.onclick(e1)
        # left click, right axis
        e2 = matplotlib.backend_bases.MouseEvent(name="button_press_event", canvas=img_registrator.fig.canvas,
                                                 x=0, y=0, button=1)
        e2.inaxes = img_registrator.axes[0]
        e2.inaxes._subplotspec = matplotlib.gridspec.SubplotSpec(matplotlib.gridspec.GridSpec(1,2,img_registrator.fig), 1)
        e2.xdata, e2.ydata = pt
        img_registrator.onclick(e2)
    # right click, left axis
    e1_ = matplotlib.backend_bases.MouseEvent(name="button_press_event", canvas=img_registrator.fig.canvas,
                                             x=0, y=0, button=3)
    e1_.inaxes = img_registrator.axes[0]
    e1_.inaxes._subplotspec = matplotlib.gridspec.SubplotSpec(matplotlib.gridspec.GridSpec(1, 2, img_registrator.fig), 0)
    e1_.xdata, e1_.ydata = 3, 2
    img_registrator.onclick(e1_)
    # right click, right axis
    e2_ = matplotlib.backend_bases.MouseEvent(name="button_press_event", canvas=img_registrator.fig.canvas,
                                             x=0, y=0, button=3)
    e2_.inaxes = img_registrator.axes[0]
    e2_.inaxes._subplotspec = matplotlib.gridspec.SubplotSpec(matplotlib.gridspec.GridSpec(1, 2, img_registrator.fig), 1)
    e2_.xdata, e2_.ydata = 3, 2
    img_registrator.onclick(e2_)
    img_registrator.regist()
    img_registrator.display_coords()
    img_registrator.save_model(model_file=os.path.join(cache_dir, "model"))

    assert img_registrator.model is not None and len(img_registrator.points[0]) == 4 and len(img_registrator.points[1]) == 4 and os.path.isfile(os.path.join(cache_dir, "model.pkl"))
    assert img_registrator.model is not None \
           and len(img_registrator.points[0]) == 4 \
           and len(img_registrator.points[1]) == 4 \
           and os.path.isfile(os.path.join(cache_dir, "model.pkl"))
