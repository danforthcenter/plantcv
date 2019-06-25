# Read Array Data As An 8-bit Image

import os
import pandas as pd
import numpy as np
from plantcv.plantcv import fatal_error
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import params


def read_array_asimg(array,sep=','):
    """This function reads in data as as an array and then converts it to a scaled image (0-255)

    Inputs:
    array        = path to csv or txt file
    sep          = separator, default=','
    
    Returns:
    arrayvalues      = array of values (unscaled)
    scaledarrayimg   = three channel image scaled from 0 to 255
    path             = path to array file
    array_name       = name of array file

    :param arrayvalues: numpy array
    :param scaledarrayimg: numpy array
    :return path: str
    :return path: array_name
    """
    params.device += 1
    
    inputarray=pd.read_csv(array, sep=sep,header=None)
    arrayvalues=inputarray.values

    if inputarray is None:
        fatal_error("Failed to open " + array)

    path, array_name = os.path.split(array)
    
    scaled=np.interp(arrayvalues, (arrayvalues.min(), arrayvalues.max()), (0, 255))
    scaledimg=np.stack((scaled,scaled,scaled), axis=-1)
    scaledarrayimg=(scaledimg).astype('uint8')
    
    if params.debug == "print":
        print_image(scaledarrayimg,os.path.join(params.debug_outdir, "scaled_array.png"))

    elif params.debug == "plot":
        plot_image(scaledarrayimg)

    return arrayvalues,scaledarrayimg,path,array_name