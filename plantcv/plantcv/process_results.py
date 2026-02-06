import os
import mimetypes
import json
from plantcv.plantcv.fatal_error import fatal_error
from plantcv.plantcv.json2csv import json2csv


# Process results. Parse individual image output files.
###########################################
def process_results(input_dir=".", filename="results", outformat="csv"):
    """Get results from individual files and combine into final JSON file.

    Parameters
    ----------
    input_dir : str or plantcv.parallel.WorkflowConfig
        Path to directory of results or Workflow configuration object, defaults to ".".
    filename: str
        Filename for combined output.
    outformat: str
        type of output file to write, options are "csv" and "json". Defaults to "csv"

    Returns
    -------
    None
    """
    job_dir, json_file = _handle_config_process_results(input_dir, filename)
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
        for fn in filenames:
            # Make sure file is a text or json file
            if 'text/plain' in mimetypes.guess_type(fn) or 'application/json' in mimetypes.guess_type(fn):
                # Open results file
                with open(os.path.join(dirpath, fn)) as results:
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
    # if outmode is csv then convert json to csv and delete json file
    if outformat.lower() == "csv":
        csv_prefix = os.path.splitext(json_file)[0]
        json2csv(json_file, csv_prefix)
        os.remove(json_file)


def _handle_config_process_results(input_dir, filename):
    """Handle parallel configuration objects when processing PlantCV results

    Parameters
    ----------
    config : plantcv.parallel.WorkflowConfig
        Workflow configuration object.

    Returns
    -------
    None
    """
    # if input_dir is not a str then it is a workflowconfig
    if not isinstance(input_dir, str):
        config = input_dir
        if "chkpt_start_dir" not in config.__dict__:
            config.chkpt_start_dir = config.tmp_dir
            # process results from the checkpoint inside start point for tmp dirs
        input_dir = os.path.join(config.chkpt_start_dir, "_PCV_PARALLEL_CHECKPOINT_")
        # name outputs from config
        filename = config.results
    return input_dir, filename
