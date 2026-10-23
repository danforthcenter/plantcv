import os
import re
import json
import mimetypes
from plantcv.plantcv.classes import COCO


def process_coco_results(filename, source=".", pattern="_pcv_coco.json", mode="w"):
    """Combine COCO records into a single json file

    Parameters
    ----------
    filename : str,
        Name of file to save.
    source : str or list,
        str is taken as a filepath to search for results that match the pattern in
        list is taken as a list of filepaths
    pattern : str
        Pattern used to match filenames using re.search.
        Defaults to '_pcv_coco.json'. `None` or '.' will use all json files.

    Returns:
    --------
    None
    """
    output = COCO()
    if pattern is None:
        pattern = "."
    filelist = source
    if isinstance(source, str):
        filelist = []
        for (dirpath, _, filenames) in os.walk(source):
            for fn in filenames:
                if ('text/plain' in mimetypes.guess_type(fn) or
                    'application/json' in mimetypes.guess_type(fn)) and re.search(pattern, fn):
                    filelist.append(os.path.join(dirpath, fn))

    for fn in filelist:
        fn_coco = COCO()
        fn_coco.load(fn)
        output._append(fn_coco)

    output.save(filename, mode=mode, coco_suffix=False)
