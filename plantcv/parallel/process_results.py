import os
import mimetypes
import json
from plantcv.plantcv import fatal_error


# Process results. Parse individual image output files.
###########################################
def process_results(config):
    """Get results from individual files and combine into final JSON file.

    Parameters
    ----------
    config : plantcv.parallel.WorkflowConfig
        Workflow configuration object.

    Returns
    -------
    None
    """
    # process results from the checkpoint inside tmp_dir
    job_dir = config.tmp_dir
    # name outputs from config
    json_file = config.json
    # Data dictionary
    data = {"variables": {}, "entities": []}
    if os.path.exists(json_file):
        with open(json_file, 'r') as datafile:
            try:
                data = json.load(datafile)
                if "variables" not in data or "entities" not in data:
                    fatal_error("Invalid JSON file")
            except json.decoder.JSONDecodeError:
                fatal_error("Invalid JSON file")

    # Walk through the image processing job directory and process data from each file
    for (dirpath, _, filenames) in os.walk(job_dir):
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
        json.dump(data, datafile, indent=4)
