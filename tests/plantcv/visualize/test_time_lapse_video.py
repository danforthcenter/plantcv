import os
import cv2
import numpy as np
from plantcv.plantcv.visualize.time_lapse_video import time_lapse_video


def test_plantcv_visualize_time_lapse_video_list_input(tmpdir):
    """Test for PlantCV."""
    # Generate 3 test images and saved in tmpdir
    list_im = []
    for i in range(3):
        temp_img = np.random.rand(3, 3)
        min_, max_ = np.nanmin(temp_img), np.nanmax(temp_img)
        temp_img = np.interp(temp_img, (min_, max_), (0, 255)).astype('uint8')
        img_i_path = os.path.join(tmpdir, f"img{i}.png")
        cv2.imwrite(img_i_path, temp_img)
        list_im.append(img_i_path)

    vid_name = os.path.join(tmpdir, 'test_time_lapse_video.mp4')
    _ = time_lapse_video(source=list_im, out_filename=vid_name, fps=29.97)
    assert os.path.exists(vid_name) and os.path.getsize(vid_name) > 100


def test_plantcv_visualize_time_lapse_video_str_input(tmpdir):
    """Test for PlantCV."""
    # Generate 3 test images and saved in tmpdir
    for i in range(3):
        temp_img = np.random.rand(3, 3)
        min_, max_ = np.nanmin(temp_img), np.nanmax(temp_img)
        temp_img = np.interp(temp_img, (min_, max_), (0, 255)).astype('uint8')
        img_i_path = os.path.join(tmpdir, f"img{i}.png")
        cv2.imwrite(img_i_path, temp_img)

    vid_name = os.path.join(tmpdir, 'test_time_lapse_video.mp4')
    _ = time_lapse_video(source=str(tmpdir), out_filename=vid_name, fps=29.97)
    assert os.path.exists(vid_name) and os.path.getsize(vid_name) > 100


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
    _ = time_lapse_video(source=list_im, out_filename=vid_name, fps=29.97)
    _, err = capsys.readouterr()

    assert "Warning" in err and os.path.exists(vid_name)
