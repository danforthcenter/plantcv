# Read dataset of images

import os
import re


def read_dataset(source_path, pattern='', sort=True):
    """
    Read a dataset of images as a list of paths.
    Inputs:
    source_path  = Path to the directory containing the images
    pattern      = Optional, return only filenames containing the pattern
    sort         = True by default, sorts the paths alphabetically
    Returns:
    dataset = List of paths to the images in the source path
    :param source_path: str
    :param pattern: str
    :param sort: bool
    :return dataset: list
    """
    if not os.path.exists(source_path):
        raise IOError(f"Directory does not exist: {source_path}")

    img_path_list = []
    img_extensions = ['.png', '.jpg', '.jpeg', '.tif', '.tiff', '.gif']

    for root, _, files in os.walk(source_path):
        for file in files:
            # Look for images that contain [pattern] in the name
            if re.search(pattern, file):
                # Check file type so that only images get selected
                _, ext = os.path.splitext(file)
                if ext.lower() in img_extensions:
                    img_path_list.append(os.path.join(root, file))

    if sort is True:
        img_path_list = sorted(img_path_list)

    return img_path_list
