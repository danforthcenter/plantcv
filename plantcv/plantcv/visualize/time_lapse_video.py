# Create time-lapse videos with input directory of images

import os
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import fatal_error
from plantcv.plantcv.transform import resize
# import warnings
from plantcv.plantcv import warn


def time_lapse_video(list_img, size_frame=None, fps=29.97, out_filename='./time_lapse_video.mp4', display='on'):
    """ Generate time-lapse video given a folder of images
    Inputs:
    img_directory  = the directory of folder of images to make the time-lapse video.
    list_img       = the desired list of images in img_directory to create the video.
            If None is passed, all images would be included by default.
    auto_sort      = whether to automatically sort the list of images.
                    Sometimes if the user provided the list of images, they don't want it to be alphabetically sorted
    suffix_img     = common suffix of all image files, can be more than extension
    size_frame     = the desired size of every frame.
            In a video, every frame should have the same size.
            The assumption is that all images given should have same size. However, in some cases, the sizes of images are
            slightly differ from each other.
            If the frame size is given, if an image is larger than the given size, the image would be cropped automatically;
            if an image is smaller than the given size, the image would be zero-padded automatically
            If the frame size is not given, the largest size of all images would be used as the frame size.
    fps            = (frames per second) frame rate.
            Commonly used values: 23.98, 24, 25, 29.97, 30, 50, 59.94, 60
    name_video     = desired saving name for the generated video
    path_video     = the desired saving path of output video. If not given, the video would be saved
            in the same directory of the images.
    display        = indicator of whether to display current status (by displaying saving directory and saving name)
            while running this function
    Outputs:
    list_img       = the list of images used to generate the video
    size_frame     = the frame size of the generated video

    :param img_directory: string
    :param list_img: list
    :param auto_sort: boolean
    :param suffix_img: string
    :param size_frame: tuple
    :param fps: float
    :param name_video: string
    :param path_video: string
    :param display: boolean
    :return list_img: list
    :return size_frame: tuple
    """

    debug = params.debug
    params.debug = None

    if len(list_img) <= 0:
        fatal_error("Image list is empty")

    imgs = []
    list_r = []
    list_c = []
    for file in list_img:
        img = cv2.imread(file)
        if img is None:
            fatal_error(f"Unable to read {file}")
        list_r.append(img.shape[0])
        list_c.append(img.shape[1])
        imgs.append(img)
    max_c, max_r = np.max(list_c), np.max(list_r)

    # If the frame size is not provided, use the largest size of the images as the frame size
    size_frame = size_frame or (max_c, max_r)

    if not (len(np.unique(list_r)) == 1 and len(np.unique(list_c)) == 1):
        warn("The sizes of images are not the same, an image resizing (cropping or zero-padding) will be done "
             f"to make all images the same size ({size_frame[0]}x{size_frame[1]}) before creating the video! ")

    out_path, out_ext = os.path.splitext(out_filename)
    if out_ext !=  '.mp4':
        out_filename =  out_path + '.mp4'

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Be sure to use lower case
    out = cv2.VideoWriter(out_filename, fourcc, fps, size_frame)

    for img in imgs:
        out.write(resize(img, size_frame, interpolation=None))
    out.release()
    cv2.destroyAllWindows()
    if display == 'on':
        print(f'Path to generated video: \n{out_filename}')

    return list_img, size_frame
