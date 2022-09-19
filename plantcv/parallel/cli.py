#!/usr/bin/env python
import os
import sys
import argparse
import time
import datetime
import plantcv.parallel
import tempfile
import shutil


# Parse command-line arguments
###########################################
def options():
    """Parse command line options.

    Args:

    Returns:
        argparse object.
    Raises:
        IOError: if dir does not exist.
        IOError: if workflow does not exist.
        IOError: if the metadata file SnapshotInfo.csv does not exist in dir when flat is False.
        ValueError: if adaptor is not phenofront or dbimportexport.
        ValueError: if a metadata field is not supported.
    """
    parser = argparse.ArgumentParser(description='Parallel imaging processing with PlantCV.')
    config_grp = parser.add_argument_group("CONFIG")
    config_grp.add_argument("--template", required=False, help="Create a template configuration file.")
    run_grp = parser.add_argument_group("RUN")
    run_grp.add_argument("--config", required=False,
                         help="Input configuration file (created using the --template option).")
    args = parser.parse_args()

    # Create a config
    config = plantcv.parallel.WorkflowConfig()

    # Create a template configuration file if requested
    if args.template:
        config.save_config(config_file=args.template)
        sys.exit()

    # Import a configuration if provided
    if args.config:
        config.import_config(config_file=args.config)

    if not config.validate_config():
        raise ValueError("Invalid configuration file. Check errors above.")
    return config
###########################################


# Run the main program
###########################################
def main():
    """Main program.

    Args:

    Returns:

    Raises:

    """
    # Get options
    config = options()

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
    meta = plantcv.parallel.metadata_parser(config=config)
    parser_clock_time = time.time() - parser_start_time
    print(f"Reading image metadata took {parser_clock_time} seconds.", file=sys.stderr)
    ###########################################

    # Process images
    ###########################################
    # Job builder start time
    job_builder_start_time = time.time()
    print("Building job list... ", file=sys.stderr)
    jobs = plantcv.parallel.job_builder(meta=meta, config=config)
    job_builder_clock_time = time.time() - job_builder_start_time
    print(f"Building job list took {job_builder_clock_time} seconds.", file=sys.stderr)

    # Parallel image processing time
    multi_start_time = time.time()
    print("Processing images... ", file=sys.stderr)
    cluster_client = plantcv.parallel.create_dask_cluster(cluster=config.cluster, cluster_config=config.cluster_config)
    plantcv.parallel.multiprocess(jobs=jobs, client=cluster_client)
    multi_clock_time = time.time() - multi_start_time
    print(f"Processing images took {multi_clock_time} seconds.", file=sys.stderr)
    ###########################################

    # Compile image analysis results
    ###########################################
    # Process results start time
    process_results_start_time = time.time()
    print("Processing results... ", file=sys.stderr)
    plantcv.parallel.process_results(job_dir=config.tmp_dir, json_file=config.json)
    process_results_clock_time = time.time() - process_results_start_time
    print(f"Processing results took {process_results_clock_time} seconds.", file=sys.stderr)
    ###########################################

    # Cleanup
    if config.cleanup is True:
        shutil.rmtree(config.tmp_dir)
###########################################
