import os
import sys
import json
from copy import deepcopy
import tempfile


# Build job list
###########################################
def job_builder(meta, config):
    """Build a list of image processing jobs.

    Inputs:
    meta:         Dictionary of processed image metadata.
    config:       plantcv.parallel.WorkflowConfig object.

    Returns:
    jobs:         List of image processing commands.

    :param meta: dict
    :param config: plantcv.parallel.WorkflowConfig
    :return job_stack: list
    """

    # Overall job stack. List of list of jobs
    jobs = []

    # Get the list of images
    # images = list(meta.keys())
    images = []
    for img in list(meta.keys()):
        # # If a date range was requested, check whether the image is within range
        # if args.dates:
        #     # Convert image datetime to unix time
        #     timestamp = dt_parser(meta[img]['timestamp'])
        #     time_delta = timestamp - datetime.datetime(1970, 1, 1)
        #     unix_time = (time_delta.days * 24 * 3600) + time_delta.seconds
        #     if unix_time < args.start_date or unix_time > args.end_date:
        #         continue
        if config.coprocess is not None:
            if meta[img]['imgtype'] != config.coprocess:
                images.append(img)
        else:
            images.append(img)

    # Log the number of jobs to be run
    n_jobs = len(images)
    print(f"Job list will include {n_jobs} images", file=sys.stderr)

    # For each image
    for img in images:
        # Create JSON templates for each image
        img_meta = {"metadata": deepcopy(config.metadata_terms), "observations": {}}
        coimg_meta = {"metadata": deepcopy(config.metadata_terms), "observations": {}}

        # If there is an image co-processed with the image
        if (config.coprocess is not None) and ('coimg' in meta[img]):
            # Create an output file to store the co-image processing results and populate with metadata
            coimg = meta[meta[img]['coimg']]
            coout = open(os.path.join(config.tmp_dir, meta[img]["coimg"] + ".txt"), 'w')
            # Store metadata in JSON
            coimg_meta["metadata"]["image"] = {
                "label": "image file",
                "datatype": "<class 'str'>",
                "value": coimg['path']
            }
            # Valid metadata
            for m in list(config.metadata_terms.keys()):
                coimg_meta["metadata"][m]["value"] = coimg[m]
            json.dump(coimg_meta, coout)
            coout.close()

        # Create an output file to store the image processing results and populate with metadata
        outfile = open(os.path.join(config.tmp_dir, img + ".txt"), 'w')
        # Store metadata in JSON
        img_meta["metadata"]["image"] = {
                "label": "image file",
                "datatype": "<class 'str'>",
                "value": meta[img]['path']
            }
        # Valid metadata
        for m in list(config.metadata_terms.keys()):
            img_meta["metadata"][m]["value"] = meta[img][m]
        json.dump(img_meta, outfile)
        outfile.close()

        # Build job
        job_parts = ["python", config.workflow, "--image", meta[img]['path'],
                     "--outdir", config.img_outdir, "--result",
                     os.path.join(config.tmp_dir, img) + ".txt"]
        # Add job to list
        if config.coprocess is not None and ('coimg' in meta[img]):
            job_parts = job_parts + ["--coresult", os.path.join(config.tmp_dir, meta[img]['coimg']) + ".txt"]
        if config.writeimg:
            job_parts.append("--writeimg")
        if config.other_args:
            job_parts = job_parts + config.other_args
        jobs.append(job_parts)

    return jobs
###########################################
