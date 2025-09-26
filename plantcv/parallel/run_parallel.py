import os
import sys
import time
import datetime
import tempfile
import shutil
from plantcv.parallel.parsers import metadata_parser
from plantcv.parallel.job_builder import job_builder
from plantcv.parallel.multiprocess import create_dask_cluster
from plantcv.parallel.multiprocess import multiprocess
from plantcv.parallel.process_results import process_results
import plantcv.utils


def run_parallel(config):
    """Run a parallel workflow
    Parameters
    ----------
    Config = plantcv.parallel.workflowconfig object

    Returns
    -------
    None
    """
    # Job start time
    start_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    print("Starting run " + start_time + '\n', file=sys.stderr)

    # Create temporary directory for job
    if config.tmp_dir is not None:
        os.makedirs(config.tmp_dir, exist_ok=True)
    config.tmp_dir = tempfile.mkdtemp(prefix=start_time + '_', dir=config.tmp_dir)

    # Create img_outdir
    os.makedirs(config.img_outdir, exist_ok=True)

    # Remove JSON results file if append=False
    if not config.append and os.path.exists(config.json):
        os.remove(config.json)

    # Read image metadata
    ###########################################
    parser_start_time = time.time()
    print("Reading image metadata...", file=sys.stderr)
    meta, _ = metadata_parser(config=config)
    parser_clock_time = time.time() - parser_start_time
    print(f"Reading image metadata took {parser_clock_time} seconds.", file=sys.stderr)
    ###########################################

    # Process images
    ###########################################
    # Job builder start time
    job_builder_start_time = time.time()
    print("Building job list... ", file=sys.stderr)
    jobs = job_builder(meta=meta, config=config)
    job_builder_clock_time = time.time() - job_builder_start_time
    print(f"Building job list took {job_builder_clock_time} seconds.", file=sys.stderr)

    # Parallel image processing time
    multi_start_time = time.time()
    print("Processing images... ", file=sys.stderr)
    cluster_client = create_dask_cluster(cluster=config.cluster, cluster_config=config.cluster_config)
    multiprocess(jobs=jobs, client=cluster_client)
    multi_clock_time = time.time() - multi_start_time
    print(f"Processing images took {multi_clock_time} seconds.", file=sys.stderr)
    ###########################################

    # Compile image analysis results
    ###########################################
    # Process results start time
    process_results_start_time = time.time()
    print("Processing results... ", file=sys.stderr)
    process_results(job_dir=config.tmp_dir, json_file=config.json)
    process_results_clock_time = time.time() - process_results_start_time
    print(f"Processing results took {process_results_clock_time} seconds.", file=sys.stderr)
    ###########################################

    # Convert json results to csv files
    ###########################################
    # Convert results start time
    convert_results_start_time = time.time()
    print("Converting json to csv... ", file=sys.stderr)
    plantcv.utils.json2csv(config.json, config.json)
    convert_results_clock_time = time.time() - convert_results_start_time
    print(f"Processing results took {convert_results_clock_time} seconds.", file=sys.stderr)
    ###########################################

    # Cleanup
    if config.cleanup is True:
        shutil.rmtree(config.tmp_dir)
