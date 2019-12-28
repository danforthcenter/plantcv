#!/usr/bin/env python
import os
import sys
import argparse
import time
import datetime
import plantcv.parallel as pcvp


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
    # Job start time
    start_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    print("Starting run " + start_time + '\n', file=sys.stderr)

    parser = argparse.ArgumentParser(description='Parallel imaging processing with PlantCV.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-d", "--dir", help='Input directory containing images or snapshots.', required=True)
    parser.add_argument("-p", "--workflow", help='Workflow script file.', required=True)
    parser.add_argument("-j", "--json", help='Output database file name.', required=True)
    parser.add_argument("-f", "--meta",
                        help='Image filename metadata structure. Comma-separated list of valid metadata terms. '
                             'Valid metadata fields are listed in the documentation.', required=True)
    parser.add_argument("-i", "--outdir", help='Output directory for images. Not required by all workflows.',
                        default=".")
    parser.add_argument("-T", "--cpu", help='Number of CPU processes to use.', default=1, type=int)
    parser.add_argument("-c", "--create",
                        help='will overwrite an existing database'
                             'Warning: activating this option will delete an existing database!',
                        default=False, action="store_true")
    parser.add_argument("-D", "--dates",
                        help='Date range. Format: YYYY-MM-DD-hh-mm-ss_YYYY-MM-DD-hh-mm-ss. If the second date '
                             'is excluded then the current date is assumed.',
                        required=False)
    parser.add_argument("-t", "--type", help='Image format type (extension).', default="png")
    parser.add_argument("-l", "--delimiter", help='Image file name metadata delimiter character.' 
                                                  'Alternatively, a regular expression for parsing filename metadata.',
                        default='_')
    parser.add_argument("-M", "--match",
                        help='Restrict analysis to images with metadata matching input criteria. Input a '
                             'metadata:value comma-separated list. This is an exact match search. '
                             'E.g. imgtype:VIS,camera:SV,zoom:z500',
                        required=False)
    parser.add_argument("-C", "--coprocess",
                        help='Coprocess the specified imgtype with the imgtype specified in --match '
                             '(e.g. coprocess NIR images with VIS).',
                        default=None)
    parser.add_argument("-s", "--timestampformat", 
                        help='a date format code compatible with strptime C library, '
                             'e.g. "%%Y-%%m-%%d %%H_%%M_%%S", except "%%" symbols must be escaped on Windows with "%%" '
                             'e.g. "%%%%Y-%%%%m-%%%%d %%%%H_%%%%M_%%%%S"'
                             'default format code is "%%Y-%%m-%%d %%H:%%M:%%S.%%f"',
                        required=False,
                        default='%Y-%m-%d %H:%M:%S.%f')
    parser.add_argument("-w", "--writeimg", help='Include analysis images in output.', default=False,
                        action="store_true")
    parser.add_argument("-o", "--other_args", help='Other arguments to pass to the workflow script.', required=False)
    args = parser.parse_args()

    if args.dates:
        dates = args.dates.split('_')
        if len(dates) == 1:
            # End is current time
            dates.append(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
        start = map(int, dates[0].split('-'))
        end = map(int, dates[1].split('-'))
        # Convert start and end dates to Unix time
        start_td = datetime.datetime(*start) - datetime.datetime(1970, 1, 1)
        end_td = datetime.datetime(*end) - datetime.datetime(1970, 1, 1)
        args.start_date = (start_td.days * 24 * 3600) + start_td.seconds
        args.end_date = (end_td.days * 24 * 3600) + end_td.seconds
    else:
        args.start_date = 1
        args.end_date = None

    args.start_time = start_time

    # Recreate JSON file if flag is on
    if os.path.exists(args.json) and args.create:
        os.remove(args.json)

    # Metadata restrictions
    args.imgtype = {}
    if args.match is not None:
        pairs = args.match.split(',')
        for pair in pairs:
            key, value = pair.split(':')
            args.imgtype[key] = value
    else:
        args.imgtype = None

    config = pcvp.Config(input_dir=args.dir, json=args.json, filename_metadata=args.meta.split(","),
                         output_dir=args.outdir, processes=args.cpu, start_date=args.start_date, end_date=args.end_date,
                         imgformat=args.type, delimiter=args.delimiter, metadata_filters=args.imgtype,
                         timestampformat=args.timestampformat, writeimg=args.writeimg, other_args=args.other_args)

    if not os.path.exists(args.workflow):
        raise IOError("File does not exist: {0}".format(args.workflow))

    return config, args.workflow


###########################################

# Main
###########################################
def main():
    """Main program.

    Args:

    Returns:

    Raises:

    """

    # Get options
    config, workflow = options()

    # Read image file names
    ###########################################
    jobcount, meta = pcvp.metadata_parser(data_dir=config.input_dir, meta_fields=config.metadata_structure, valid_meta=config.metadata_terms,
                                          meta_filters=config.metadata_filters, date_format=config.timestampformat, start_date=config.start_date, end_date=config.end_date,
                                          delimiter=config.delimiter, file_type=config.imgformat, coprocess=config.coprocess)
    ###########################################

    # Process images
    ###########################################
    # Job builder start time
    job_builder_start_time = time.time()
    print("Building job list... ", file=sys.stderr)
    jobs = pcvp.job_builder(meta=meta, valid_meta=config.metadata_terms, workflow=workflow, job_dir=config.tmp_dir,
                            out_dir=config.output_dir, coprocess=config.coprocess, other_args=config.other_args,
                            writeimg=config.writeimg)
    # Job builder clock time
    job_builder_clock_time = time.time() - job_builder_start_time
    print("took " + str(job_builder_clock_time) + '\n', file=sys.stderr)

    # Parallel image processing time
    multi_start_time = time.time()
    print("Processing images... ", file=sys.stderr)

    pcvp.multiprocess(jobs, config.processes)

    # Parallel clock time
    multi_clock_time = time.time() - multi_start_time
    print("took " + str(multi_clock_time) + '\n', file=sys.stderr)
    ###########################################

    # Compile image analysis results
    ###########################################
    # Process results start time
    process_results_start_time = time.time()
    print("Processing results... ", file=sys.stderr)
    pcvp.process_results(job_dir=config.tmp_dir, json_file=config.json)
    # Process results clock time
    process_results_clock_time = time.time() - process_results_start_time
    print("took " + str(process_results_clock_time) + '\n', file=sys.stderr)
    ###########################################

###########################################


if __name__ == '__main__':
    __spec__ = None
    main()
