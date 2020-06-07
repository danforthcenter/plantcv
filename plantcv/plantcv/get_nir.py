# Find NIR image

import os
import re
import numpy as np


def get_nir(path, filename):
    """Find a corresponding NIR image from the same snapshot as the VIS image.

    Inputs:
    path     = path to vis image
    filename = vis image file name

    Returns:
    nirpath  = NIR image filename and path

    :param path: str
    :param filename: str
    :return nirpath: str
    """

    visname = filename.split("_")
    allfiles = np.array(os.listdir(path))
    nirfiles = []

    cam = visname[1].upper()

    if cam == "SV":
        angle = visname[2]

    for n in allfiles:
        if re.search("NIR", n) is not None:
            nirfiles.append(n)

    if cam == "TV":
        for n in nirfiles:
            if re.search("TV", n) is not None:
                nirpath = os.path.join(str(path), str(n))

    if cam == "SV":
        for n in nirfiles:
            if re.search("SV", n) is not None:
                nsplit = n.split("_")
                exangle = '\\b' + str(angle) + '\\b'
                if re.search(exangle, nsplit[2]) is not None:
                    nirpath = os.path.join(str(path), str(n))

    return nirpath
