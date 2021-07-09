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
    config_grp = parser.add_argument_group('CONFIG')
    config_grp.add_argument("--config", required=False,
                            help="Input configuration file (exported from WorkflowConfig)."
                                 "If provided all other arguments are ignored.")
    cmdline_grp = parser.add_argument_group("COMMAND-LINE")
    cmdline_grp.add_argument("-d", "--dir", help='Input directory containing images or snapshots.',
                             required="--config" not in sys.argv)
    cmdline_grp.add_argument("-a", "--adaptor",
                             help='Image metadata reader adaptor. PhenoFront metadata is stored in a CSV file and the '
                                  'image file name. For the filename option, all metadata is stored in the image file '
                                  'name. Current adaptors: phenofront, filename', default="phenofront")
    cmdline_grp.add_argument("-p", "--workflow", help='Workflow script file.', required="--config" not in sys.argv)
    cmdline_grp.add_argument("-j", "--json", help='Output database file name.', required="--config" not in sys.argv)
    cmdline_grp.add_argument("-f", "--meta",
                             help='Image filename metadata structure. Comma-separated list of valid metadata terms. '
                                  'Valid metadata fields are: ' +
                                  ', '.join(map(str, list(vars(plantcv.parallel.WorkflowConfig()).keys()))),
                             required="--config" not in sys.argv)
    cmdline_grp.add_argument("-i", "--outdir", help='Output directory for images. Not required by all workflows.',
                             default=".")
    cmdline_grp.add_argument("-T", "--cpu", help='Number of CPU processes to use.', default=1, type=int)
    cmdline_grp.add_argument("-c", "--create",
                             help='will overwrite an existing database'
                                  'Warning: activating this option will delete an existing database!',
                             default=False, action="store_true")
    cmdline_grp.add_argument("-D", "--dates",
                             help='Date range. Format: YYYY-MM-DD-hh-mm-ss_YYYY-MM-DD-hh-mm-ss. If the second date '
                                  'is excluded then the current date is assumed.',
                             required=False)
    cmdline_grp.add_argument("-t", "--type", help='Image format type (extension).', default="png")
    cmdline_grp.add_argument("-l", "--delimiter", help='Image file name metadata delimiter character.Alternatively,'
                                                       'a regular expression for parsing filename metadata.',
                             default='_')
    cmdline_grp.add_argument("-M", "--match",
                             help='Restrict analysis to images with metadata matching input criteria. Input a '
                                  'metadata:value comma-separated list. This is an exact match search. '
                                  'E.g. imgtype:VIS,camera:SV,zoom:z500',
                             required=False)
    cmdline_grp.add_argument("-C", "--coprocess",
                             help='Coprocess the specified imgtype with the imgtype specified in --match '
                                  '(e.g. coprocess NIR images with VIS).',
                             default=None)
    cmdline_grp.add_argument("-s", "--timestampformat",
                             help='a date format code compatible with strptime C library, '
                                  'e.g. "%%Y-%%m-%%d %%H_%%M_%%S", except "%%" symbols must be escaped on Windows with '
                                  '"%%" e.g. "%%%%Y-%%%%m-%%%%d %%%%H_%%%%M_%%%%S"'
                                  'default format code is "%%Y-%%m-%%d %%H:%%M:%%S.%%f"',
                             required=False, default='%Y-%m-%d %H:%M:%S.%f')
    cmdline_grp.add_argument("-w", "--writeimg", help='Include analysis images in output.', default=False,
                             action="store_true")
    cmdline_grp.add_argument("-o", "--other_args", help='Other arguments to pass to the workflow script.',
                             required=False)
    cmdline_grp.add_argument("-z", "--cleanup", help='Remove temporary working directory', default=False)
    args = parser.parse_args()

    # Create a config
    config = plantcv.parallel.WorkflowConfig()

    # Import a configuration if provided
    if args.config:
        config.import_config(config_file=args.config)
    else:
        if args.dates:
            dates = args.dates.split('_')
            if len(dates) == 1:
                # End is current time
                dates.append(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
            start = map(int, dates[0].split('-'))
            end = map(int, dates[1].split('-'))
            # Use the parsed input datetimes to create datetime strings that match the input timestampformat
            args.start_date = datetime.datetime(*start).strftime(args.timestampformat)
            args.end_date = datetime.datetime(*end).strftime(args.timestampformat)
        else:
            args.start_date = datetime.datetime(1970, 1, 1, 0, 0, 1).strftime(args.timestampformat)
            args.end_date = datetime.datetime.now().strftime(args.timestampformat)

        # Metadata restrictions
        args.imgtype = {}
        if args.match is not None:
            pairs = args.match.split(',')
            for pair in pairs:
                key, value = pair.split(':')
                if key not in args.imgtype:
                    args.imgtype[key] = []
                args.imgtype[key].append(value)

        # Populate config object
        config.input_dir = args.dir
        config.json = args.json
        config.filename_metadata = args.meta.split(",")
        config.workflow = args.workflow
        config.img_outdir = args.outdir
        config.start_date = args.start_date
        config.end_date = args.end_date
        config.imgformat = args.type
        config.delimiter = args.delimiter
        config.metadata_filters = args.imgtype
        config.timestampformat = args.timestampformat
        config.writeimg = args.writeimg
        if args.other_args:
            config.other_args = args.other_args.split(" ")
        config.coprocess = args.coprocess
        config.cleanup = args.cleanup
        config.append = not args.create
        config.cluster = "LocalCluster"
        config.cluster_config = {"n_workers": args.cpu, "cores": 1, "memory": "1GB", "disk": "1GB"}

    if not config.validate_config():
        raise ValueError("Invalid configuration file. Check errors above.")
    return config


###########################################

# Main
###########################################
def main():
    """Main program.

    Args:

    Returns:

    Raises:

    """

    # Job start time
    start_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    print("Starting run " + start_time + '\n', file=sys.stderr)

    # Get options
    config = options()

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


if __name__ == '__main__':
    __spec__ = None
    main()
