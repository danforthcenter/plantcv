import pytest
import os
import cv2
import numpy as np

from plantcv.plantcv.visualize.time_lapse_video import time_lapse_video

@pytest.mark.parametrize("display",[False,True])
def test_plantcv_visualize_time_lapse_video_passes(display, tmpdir):
    """Test for PlantCV."""
    # Generate 3 test images and saved in tmpdir
    list_im = []
    for i in range(3):
        temp_img = np.random.rand(3,3)
        min_, max_ = np.nanmin(temp_img), np.nanmax(temp_img)
        temp_img = np.interp(temp_img, (min_, max_), (0, 255)).astype('uint8')
        img_i_path = os.path.join(tmpdir, f"img{i}.png")
        cv2.imwrite(img_i_path, temp_img)
        list_im.append(img_i_path)

    # list_im = [os.path.join(tmpdir, img) for img in os.listdir(tmpdir) if img.endswith('.png')]

    vid_name = os.path.join(tmpdir, 'test_time_lapse_video.mp4')
    _ = time_lapse_video(img_list=list_im, out_filename=vid_name, fps=29.97, display=display)
    assert os.path.exists(vid_name)

@pytest.mark.parametrize("list_im_f",
                         [([]),    # empty list
                         (['./this_img_does_not_exist.png'])])  # non existent image
def test_plantcv_visualize_time_lapse_video_errors(list_im_f, tmpdir):
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _ = time_lapse_video(img_list=list_im_f, fps=29.97)


# not all images have the same size (essential to generate a video)
def test_plantcv_visualize_time_lapse_video_different_img_sizes_warns(tmpdir, capsys):
    """Test for PlantCV."""
    # Generate 3 test images of different size and save in tmpdir
    list_im = []
    for i in range(2):
        temp_img = np.random.rand(i+2, 3)
        min_, max_ = np.nanmin(temp_img), np.nanmax(temp_img)
        temp_img = np.interp(temp_img, (min_, max_), (0, 255)).astype('uint8')
        img_i_path = os.path.join(tmpdir, f"img{i}.png")
        cv2.imwrite(img_i_path, temp_img)
        list_im.append(img_i_path)

    vid_name = os.path.join(tmpdir, 'test_time_lapse_video.mp4')
    _ = time_lapse_video(img_list=list_im, out_filename=vid_name, fps=29.97, display=True)
    _, err = capsys.readouterr()

    assert "Warning" in err and os.path.exists(vid_name)
