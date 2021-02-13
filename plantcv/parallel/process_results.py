import os
import mimetypes
import json
from plantcv.plantcv import fatal_error


# Process results. Parse individual image output files.
###########################################
def process_results(job_dir, json_file):
    """Get results from individual files and combine into final JSON file.

    Args:
        job_dir:              Intermediate file output directory.
        json_file:            Json data table filehandle object.

    :param job_dir: str
    :param json_file: obj
    """

    if os.path.exists(json_file):
        with open(json_file, 'r') as datafile:
            try:
                data = json.load(datafile)
                if "variables" not in data or "entities" not in data:
                    fatal_error("Invalid JSON file")
            except:
                fatal_error("Invalid JSON file")
    else:
        # Data dictionary
        data = {"variables": {}, "entities": []}

    # Walk through the image processing job directory and process data from each file
    for (dirpath, dirnames, filenames) in os.walk(job_dir):
        for filename in filenames:
            # Make sure file is a text or json file
            if 'text/plain' in mimetypes.guess_type(filename) or 'application/json' in mimetypes.guess_type(filename):
                # Open results file
                with open(os.path.join(dirpath, filename)) as results:
                    obs = json.load(results)
                    data["entities"].append(obs)
                    # Keep track of all metadata variables stored
                    for var in obs["metadata"]:
                        data["variables"][var] = {"category": "metadata", "datatype": "<class 'str'>"}
                    # Keep track of all observations variables stored
                    for sample in obs["observations"]:
                        for othervars in obs["observations"][sample]:
                            data["variables"][othervars] = {"category": "observations",
                                                            "datatype": obs["observations"][sample][othervars]["datatype"]}

    # Write out json file with info from all images
    with open(json_file, 'w') as datafile:
        json.dump(data, datafile)
