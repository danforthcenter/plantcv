"""ClickCount File Import"""
import json
from plantcv.plantcv.annotate.classes import ClickCount


def clickcount_file_import(img, coord_file):
    """function to import ClickCount Coor file to ClickCount object"""

    coords = open( coord_file, "r")
    coords = json.load(coords)

    keys = list(coords.keys())
    
    counter = ClickCount(img, figsize=(8, 6))
    
    for key in keys:
        keycoor = coords[key]
        keycoor = list(map(lambda sub: (sub[1], sub[0]), keycoor))
        counter.import_coords(keycoor, label=key)
        
    return counter

