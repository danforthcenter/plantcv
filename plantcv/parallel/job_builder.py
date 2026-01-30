import os
import sys
import json
from copy import deepcopy
import uuid


# Build job list
###########################################
def job_builder(meta, config):
    """Build a list of image processing jobs.

    Parameters
    ----------
    meta:         pandas.core.frame.Dataframe
                     Dataframe of image metadata
    config:       plantcv.parallel.WorkflowConfig object.
                     Workflow configuration

    Returns
    -------
    jobs:         list, iimage processing commands.
    """
    # Overall job stack. List of list of jobs
    jobs = []
    # make pandas groupby object
    meta = meta.groupby(by=config.groupby)

    # Log the number of jobs to be run
    n_jobs = len(meta)
    print(f"Task list includes {n_jobs} workflows", file=sys.stderr)

    # Each grouping has a tuple of grouped metadata values and a dataframe of image metadata
    for _, grp_df in meta:
        # Create a JSON template for each group
        img_meta = {"metadata": deepcopy(config.metadata_terms), "observations": {}}

        # Store metadata in JSON
        img_meta["metadata"]["filepath"] = {
                "label": "image files",
                "datatype": "<class 'str'>",
                "value": grp_df["filepath"].values.tolist()
            }

        # Valid metadata
        for m in list(config.metadata_terms.keys()):
            img_meta["metadata"][m]["value"] = grp_df[m].values.tolist()

        # Create random unique output file to store the image processing results and populate with metadata
        outfile = os.path.join(config.tmp_dir, f"{uuid.uuid4()}.json")
        with open(outfile, "w") as fp:
            json.dump(img_meta, fp, indent=4)

        # Generate image names if set to auto
        if config.group_name == "auto":
            names = []
            for i in range(0, len(grp_df)):
                names.append(f"image{i + 1}")
        else:
            names = list(grp_df[config.group_name])

        # Build job
        job_parts = ["python", config.workflow, "--outdir", config.img_outdir, "--result", outfile,
                     "--checkpoint", str(config.checkpoint), "--tmpfile", outfile,
                     "--names", ",".join(map(str, names))]
        # Add other arguments
        for key, value in config.other_args.items():
            job_parts.append(f"--{key}")
            job_parts.append(value)
        if config.writeimg:
            job_parts.append("--writeimg")
        for fname in grp_df["filepath"].values.tolist():
            job_parts.append(fname)
        jobs.append(job_parts)

    return jobs
###########################################
