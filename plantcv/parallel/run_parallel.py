import os
import re
import sys
import time
import datetime
import tempfile
import shutil
from plantcv.plantcv.process_results import process_results
from plantcv.plantcv.json2csv import json2csv
from plantcv.parallel.parsers import metadata_parser
from plantcv.parallel.job_builder import job_builder
from plantcv.parallel.multiprocess import create_dask_cluster
from plantcv.parallel.multiprocess import multiprocess
from plantcv.parallel.message import parallel_print


def run_parallel(config):
    """Run a parallel workflow
    Parameters
    ----------
    Config = plantcv.parallel.workflowconfig object

    Returns
    -------
    None
    """
    verbose = config.verbose
    # Job start time
    start_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    print("Starting run " + start_time + '\n', file=sys.stderr)
    config = _check_for_conda(config)
    # Create temporary directory for job
    if config.tmp_dir is not None:
        os.makedirs(os.path.join(config.tmp_dir, "_PCV_PARALLEL_CHECKPOINT_"), exist_ok=True)

    config.chkpt_start_dir = config.tmp_dir
    config.tmp_dir = tempfile.mkdtemp(prefix=start_time + '_',
                                      dir=os.path.join(config.tmp_dir, "_PCV_PARALLEL_CHECKPOINT_"))
    # if a logs directory is specified then add the tmpdir inside it.
    if config.cluster_config["log_directory"] is not None:
        config.cluster_config["log_directory"] = os.path.join(
            config.cluster_config["log_directory"], os.path.basename(config.tmp_dir)
        )
        os.makedirs(config.cluster_config["log_directory"], exist_ok=True)
    # Create img_outdir
    os.makedirs(config.img_outdir, exist_ok=True)

    # Remove JSON results file if append=False
    if not config.append and os.path.exists(config.results):
        os.remove(config.results)

    # Read image metadata
    ###########################################
    parser_start_time = time.time()
    print("Reading image metadata...", file=sys.stderr)
    meta, _ = metadata_parser(config=config)
    parser_clock_time = time.time() - parser_start_time
    parallel_print(f"Reading image metadata took {parser_clock_time} seconds.", file=sys.stderr, verbose=verbose)
    ###########################################

    # Process images
    ###########################################
    # Job builder start time
    job_builder_start_time = time.time()
    print("Building job list... ", file=sys.stderr)
    jobs = job_builder(meta=meta, config=config)
    job_builder_clock_time = time.time() - job_builder_start_time
    parallel_print(f"Building job list took {job_builder_clock_time} seconds.", file=sys.stderr, verbose=verbose)

    # Parallel image processing time
    multi_start_time = time.time()
    print("Processing images... ", file=sys.stderr)
    cluster_client = create_dask_cluster(cluster=config.cluster, cluster_config=config.cluster_config)
    multiprocess(jobs=jobs, client=cluster_client)
    multi_clock_time = time.time() - multi_start_time
    parallel_print(f"Processing images took {multi_clock_time} seconds.", file=sys.stderr, verbose=verbose)
    ###########################################

    # Compile image analysis results
    ###########################################
    # Process results start time
    process_results_start_time = time.time()
    print("Processing results... ", file=sys.stderr)
    process_results(config, outformat="json")
    process_results_clock_time = time.time() - process_results_start_time
    parallel_print(f"Processing results took {process_results_clock_time} seconds.", file=sys.stderr, verbose=verbose)
    ###########################################

    # Convert json results to csv files
    ###########################################
    # Convert results start time
    convert_results_start_time = time.time()
    print("Converting json to csv... ", file=sys.stderr)
    json2csv(config.results, os.path.splitext(config.results)[0])
    convert_results_clock_time = time.time() - convert_results_start_time
    parallel_print(f"Processing results took {convert_results_clock_time} seconds.", file=sys.stderr, verbose=verbose)
    ###########################################

    # Cleanup
    if config.cleanup is True:
        shutil.rmtree(config.tmp_dir)


def _check_for_conda(config):
    """Checks a running python process for a conda env, adding that env to cluster configuration

    Parameters
    ----------
    config = plantcv.parallel.WorkflowConfig object

    Returns
    -------
    config = plantcv.parallel.WorkflowConfig object
    """
    running_in_conda = re.search("conda|mamba|miniforge", sys.executable) is not None
    # if workflow is executed from a conda environment then activate that conda environment on workers
    if "job_script_prologue" not in config.cluster_config.keys() and running_in_conda:
        # find where the conda installation is, replace python with activate
        activation_path = re.sub("python.?$", "activate", sys.executable)
        commands = ["source " + activation_path]
        # if there is an env in the executable path after the conda/mamba/miniforge
        # then find that env and add a commmand to activate it
        if re.search("env(s)?", re.sub(".*(conda|mamba|miniforge)", "", sys.executable)) is not None:
            ex_list = re.sub(".*(conda|mamba|miniforge)", "", sys.executable).split(os.sep)
            # get name of env that was active to run plantcv
            env_index = [i for i, element in enumerate(ex_list) if re.search("^env(s)?$", element)][0]
            env_name = ex_list[env_index+1]
            commands.append("conda activate" + env_name)
        # if changing config always print a message
        print("Setting job_script_prologue to fetch active environment:\n",
              "source " + activation_path, "\nconda activate " + env_name,
              file = sys.stderr)
        # write job prologue to activate the env
        config.cluster_config["job_script_prologue"] = commands

    return config
