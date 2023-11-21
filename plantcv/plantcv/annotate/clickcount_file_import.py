# ClickCount File Import

import json
from plantcv.plantcv.annotate.classes import ClickCount


def clickcount_file_import(img, filename):
    """
    Function to import ClickCount coordinate file to ClickCount object
    
    Inputs:
    img = img file to initialize ClickCount class
    filename = filename of stored coordinates and classes

    :param img: ndarray
    :param filename = ndarray
    :return counter: plantcv.plantcv.classes.ClickCount
    """
    # img - img file to initialize ClickCount class
    # coor_file - file of coordinates and classes
    coords = open(filename, "r")
    coords = json.load(coords)

    keys = list(coords.keys())

    counter = ClickCount(img, figsize=(8, 6))

    for key in keys:
        keycoor = coords[key]
        keycoor = list(map(lambda sub: (sub[1], sub[0]), keycoor))
        counter.import_coords(keycoor, label=key)

    return counter
