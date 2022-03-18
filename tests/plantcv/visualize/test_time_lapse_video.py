import pytest
import os
import cv2
import numpy as np

from plantcv.plantcv.visualize.time_lapse_video import time_lapse_video

@pytest.mark.parametrize("display",[["on"],["off"]])
def test_plantcv_visualize_time_lapse_video_passes(display, tmpdir):

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
    _, _ = time_lapse_video(img_list=list_im, out_filename=vid_name, fps=29.97, display=display)
    assert os.path.exists(vid_name)

@pytest.mark.parametrize("list_im_f",
                         [([]),    # empty list
                         (['./this_img_does_not_exist.png'])])  # non existent image
def test_plantcv_visualize_time_lapse_video_errors(list_im_f, tmpdir):
    # Generate 3 test images and saved in cache_dir
    # for i in range(3):
    #     temp_img = np.random.rand(3, 3)
    #     min_, max_ = np.nanmin(temp_img), np.nanmax(temp_img)
    #     temp_img = np.interp(temp_img, (min_, max_), (0, 255)).astype('uint8')
    #     cv2.imwrite(os.path.join(tmpdir, f"img{i}.png"), temp_img)
    with pytest.raises(RuntimeError):
        _, _ = time_lapse_video(img_list=list_im_f, fps=29.97)

# the correct directory of images as well as a list of files are provided, however the
# list is incorrect (contains correct part, but also contains incorrect part)
def test_plantcv_visualize_time_lapse_video_incorrect_list_warns(tmpdir, capsys):
    # Generate 3 test images and saved in tmpdir
    for i in range(3):
        temp_img = np.random.rand(3, 3)
        min_, max_ = np.nanmin(temp_img), np.nanmax(temp_img)
        temp_img = np.interp(temp_img, (min_, max_), (0, 255)).astype('uint8')
        cv2.imwrite(os.path.join(tmpdir, f"img{i}.png"), temp_img)
    list_img = [img for img in os.listdir(tmpdir) if img.endswith('.png')]
    list_img.append('junk.png')
    pcv.visualize.time_lapse_video(img_directory=tmpdir, img_list=list_img, fps=29.97,
                                   name_video='time_lapse_video', out_filename=tmpdir)
    out, err = capsys.readouterr()
    assert "Warning" in err and os.path.exists(os.path.join(tmpdir, 'time_lapse_video.mp4'))

# not all images have the same size (essential to generate a video)
def test_plantcv_visualize_time_lapse_video_different_img_sizes_warns(tmpdir, capsys):
    # Generate 3 test images and saved in tmpdir
    for i in range(2):
        temp_img = np.random.rand(3, 3)
        min_, max_ = np.nanmin(temp_img), np.nanmax(temp_img)
        temp_img = np.interp(temp_img, (min_, max_), (0, 255)).astype('uint8')
        cv2.imwrite(os.path.join(tmpdir, f"img{i}.png"), temp_img)
    temp_img = np.random.rand(2, 3)
    min_, max_ = np.nanmin(temp_img), np.nanmax(temp_img)
    temp_img = np.interp(temp_img, (min_, max_), (0, 255)).astype('uint8')
    cv2.imwrite(os.path.join(tmpdir, "img2.png"), temp_img)

    pcv.visualize.time_lapse_video(img_directory=tmpdir, fps=29.97, name_video='time_lapse_video',
                                   out_filename=tmpdir, display='off')
    out, err = capsys.readouterr()
    assert "Warning" in err and os.path.exists(os.path.join(tmpdir, 'time_lapse_video.mp4'))
