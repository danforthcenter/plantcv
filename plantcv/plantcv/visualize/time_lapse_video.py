# Create time-lapse videos with input directory of images

import os
import imageio.v3 as iio
import numpy as np
from plantcv.plantcv._globals import params
from plantcv.plantcv.transform.resize import resize
from plantcv.plantcv.io.read_dataset import read_dataset
from plantcv.plantcv.warn import warn


def time_lapse_video(source, out_filename='./time_lapse_video.mp4', fps=29.97):
    """Generate time-lapse video given a list of paths to the images

    Parameters:
    -----------
    source         = string or list,
        Path to a folder of images to use or list of paths to the images to create the video
    out_filename   = string,
        name of file to save the generated video to
    fps            = float,
        frame rate (frames per second)

    Returns:
    --------
    frame_size     = tuple,
        the frame size of the generated video
    """
    params.debug = None
    img_list = source
    if isinstance(source, str):
        img_list = read_dataset(source, sort=True)

    imgs = []
    list_r = []
    list_c = []
    for file in img_list:
        img = iio.imread(file)
        list_r.append(img.shape[0])
        list_c.append(img.shape[1])
        imgs.append(img)
    max_c, max_r = np.max(list_c), np.max(list_r)

    # use the largest size of the images as the frame size
    # frame_size = frame_size or (max_c, max_r)
    frame_size = (max_c, max_r)

    if not (len(np.unique(list_r)) == 1 and len(np.unique(list_c)) == 1):
        warn("The sizes of images are not the same, an image resizing (cropping or zero-padding) will be done "
             f"to make all images the same size ({frame_size[0]}x{frame_size[1]}) before creating the video! ")

    out_path, _ = os.path.splitext(out_filename)
    out_filename = out_path + '.mp4'

    frames = [resize(img, frame_size, interpolation=None) for img in imgs]
    iio.imwrite(out_filename, frames, plugin="FFMPEG", fps=fps, codec="libx264")

    return frame_size
