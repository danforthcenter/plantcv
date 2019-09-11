# Read in a hyperspectral data cube as an array and parse metadata from the header file

from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image
from plantcv.plantcv import Outputs
import numpy as np
import os


def read_data(scandir, imgname):

    raw = np.fromfile(os.path.join(scandir, imgname), np.float32, -1)
    bil_rcb = raw.reshape(1704, 978, 1600).transpose((0, 2, 1))
    return bil_rcb