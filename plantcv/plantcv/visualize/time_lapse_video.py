# Create time-lapse videos with input directory of images

import os
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import fatal_error
from plantcv.plantcv.transform import resize
# import warnings
from plantcv.plantcv import warn


def time_lapse_video(img_list, out_filename='./time_lapse_video.mp4', fps=29.97, display='on'):
    """ Generate time-lapse video given a list of paths to the images

    Inputs:
    img_list       = the desired list of images in img_directory to create the video.
            If None is passed, all images would be included by default.
    fps            = (frames per second) frame rate.
            Commonly used values: 23.98, 24, 25, 29.97, 30, 50, 59.94, 60
    out_filename   = name of file to save the generated video to
    display        = if True, displays the path to the generated video

    Outputs:
    img_list       = the list of images used to generate the video
    frame_size     = the frame size of the generated video

    :param img_list: list
    :param fps: float
    :param out_filename: string
    :param display: boolean
    :return img_list: list
    :return frame_size: tuple
    """

    debug = params.debug
    params.debug = None

    if len(img_list) <= 0:
        fatal_error("Image list is empty")

    imgs = []
    list_r = []
    list_c = []
    for file in img_list:
        img = cv2.imread(file)
        if img is None:
            fatal_error(f"Unable to read {file}")
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

    out_path, out_ext = os.path.splitext(out_filename)
    if out_ext !=  '.mp4':
        out_filename =  out_path + '.mp4'

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Be sure to use lower case
    out = cv2.VideoWriter(out_filename, fourcc, fps, frame_size)

    for img in imgs:
        out.write(resize(img, frame_size, interpolation=None))
    out.release()
    cv2.destroyAllWindows()
    if display == 'on':
        print(f'Path to generated video: \n{out_filename}')

    return img_list, frame_size
